/* IGC fixes are UTC. Detect a single complete flight locally; never upload the file. */
(function () {
    'use strict';

    const TAKEOFF_SPEED = 10; // m/s: XCSoar's fallback without a glider polar
    const LANDING_SPEED = 5; // m/s: hysteresis for slow flight
    const MAX_FIX_GAP = 20; // seconds; don't infer motion across a recorder gap
    const MAX_SPEED = 120; // m/s; discard implausible GPS jumps

    function parseIGC(text) {
        const dateMatch = text.match(/^HFDTE(?:DATE:)?\s*(\d{2})(\d{2})(\d{2})/mi);
        if (!dateMatch) throw new Error('IGC flight date (HFDTE) is missing.');

        const day = Number(dateMatch[1]);
        const month = Number(dateMatch[2]);
        const shortYear = Number(dateMatch[3]);
        const year = (shortYear >= 80 ? 1900 : 2000) + shortYear;
        const initialDate = Date.UTC(year, month - 1, day);
        const date = new Date(initialDate);
        if (date.getUTCFullYear() !== year || date.getUTCMonth() !== month - 1 || date.getUTCDate() !== day) {
            throw new Error('IGC flight date is invalid.');
        }

        const fixes = [];
        let dayOffset = 0;
        let lastSeconds = -1;
        for (const line of text.split(/\r?\n/)) {
            if (!line.startsWith('B') || line.length < 35) continue;
            const record = /^B(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})(\d{3})([NS])(\d{3})(\d{2})(\d{3})([EW])([AV])([+\-]?\d{5})([+\-]?\d{5})/.exec(line);
            if (!record) continue;
            const [hour, minute, second] = record.slice(1, 4).map(Number);
            if (hour > 23 || minute > 59 || second > 59) continue;
            const seconds = hour * 3600 + minute * 60 + second;
            if (seconds < lastSeconds) {
                if (lastSeconds - seconds < 12 * 3600) throw new Error('IGC fixes are out of order.');
                dayOffset++;
            }
            lastSeconds = seconds;
            if (record[12] !== 'A') continue;

            const latitude = Number(record[4]) + (Number(record[5]) + Number(record[6]) / 1000) / 60;
            const longitude = Number(record[8]) + (Number(record[9]) + Number(record[10]) / 1000) / 60;
            if (latitude > 90 || longitude > 180) continue;
            const altitude = Number(record[14]);
            fixes.push({
                time: initialDate + dayOffset * 86400000 + seconds * 1000,
                lat: latitude * (record[7] === 'S' ? -1 : 1),
                lon: longitude * (record[11] === 'W' ? -1 : 1),
                altitude,
            });
        }
        if (fixes.length < 4) throw new Error('IGC file has too few valid GPS fixes.');
        return fixes;
    }

    function distance(a, b) {
        const toRadians = Math.PI / 180;
        const lat = (b.lat - a.lat) * toRadians;
        const lon = (b.lon - a.lon) * toRadians;
        const h = Math.sin(lat / 2) ** 2 +
            Math.cos(a.lat * toRadians) * Math.cos(b.lat * toRadians) * Math.sin(lon / 2) ** 2;
        return 12742000 * Math.asin(Math.sqrt(Math.min(1, h)));
    }

    function detectFlight(fixes) {
        const flights = [];
        let flying = false;
        let movingSince = null;
        let stationarySince = null;
        let groundedBeforeStart = false;
        let takeoff = null;
        let groundAltitude = fixes[0].altitude;

        for (let i = 1; i < fixes.length; i++) {
            const previous = fixes[i - 1];
            const current = fixes[i];
            const dt = (current.time - previous.time) / 1000;
            if (dt <= 0) continue;
            if (dt > MAX_FIX_GAP) {
                if (flying || movingSince !== null) throw new Error('GPS recording has a gap during flight.');
                stationarySince = null;
                groundedBeforeStart = false;
                continue;
            }
            const speed = distance(previous, current) / dt;
            if (speed > MAX_SPEED) throw new Error('IGC file contains an implausible GPS jump.');

            if (!flying) {
                if (speed >= TAKEOFF_SPEED) {
                    if (movingSince === null) movingSince = previous.time;
                    if (current.time - movingSince >= 10000) {
                        if (!groundedBeforeStart) throw new Error('Takeoff is not recorded clearly in this file.');
                        flying = true;
                        takeoff = movingSince;
                        movingSince = null;
                        stationarySince = null;
                    }
                } else {
                    movingSince = null;
                    if (speed < LANDING_SPEED) {
                        if (stationarySince === null) stationarySince = previous.time;
                        if (current.time - stationarySince >= 5000) groundedBeforeStart = true;
                        groundAltitude = current.altitude;
                    } else {
                        stationarySince = null;
                    }
                }
            } else if (speed < LANDING_SPEED && current.altitude < groundAltitude + 250) {
                if (stationarySince === null) stationarySince = previous.time;
                if (current.time - stationarySince >= 10000) {
                    flights.push({ takeoff, landing: stationarySince });
                    flying = false;
                    takeoff = null;
                    stationarySince = null;
                    groundedBeforeStart = true;
                    if (flights.length > 1) throw new Error('This IGC file contains multiple flights.');
                }
            } else {
                stationarySince = null;
            }
        }
        if (flying || movingSince !== null) throw new Error('Landing is not recorded clearly in this file.');
        if (flights.length !== 1) throw new Error('Could not detect a complete flight in this IGC file.');
        return flights[0];
    }

    function localParts(timestamp, timeZone) {
        const parts = new Intl.DateTimeFormat('en-GB', {
            timeZone, year: 'numeric', month: '2-digit', day: '2-digit',
            hour: '2-digit', minute: '2-digit', hourCycle: 'h23',
        }).formatToParts(new Date(timestamp));
        const values = Object.fromEntries(parts.map(part => [part.type, part.value]));
        return { date: `${values.year}-${values.month}-${values.day}`, time: `${values.hour}:${values.minute}` };
    }

    function flightTimes(text, timeZone, logDate) {
        const flight = detectFlight(parseIGC(text));
        const launch = localParts(flight.takeoff, timeZone);
        const landing = localParts(flight.landing, timeZone);
        if (launch.date !== logDate || landing.date !== logDate || landing.time < launch.time) {
            throw new Error('Detected flight falls outside this logsheet date or crosses midnight.');
        }
        return { launchTime: launch.time, landingTime: landing.time };
    }

    if (typeof module !== 'undefined' && module.exports) {
        module.exports = { parseIGC, detectFlight, flightTimes };
    }

    if (typeof document === 'undefined') return;

    document.addEventListener('change', async function (event) {
        if (event.target.id !== 'igc-flight-file') return;
        const input = event.target;
        const file = input.files && input.files[0];
        if (!file) return;
        const form = input.closest('form');
        const status = form.querySelector('#igc-flight-status');
        const launch = form.querySelector('[name="launch_time"]');
        const landing = form.querySelector('[name="landing_time"]');
        const logsheet = document.getElementById('logsheetContainer');
        status.className = 'small text-muted';
        status.textContent = 'Reading IGC file…';
        try {
            if (file.size > 5 * 1024 * 1024) throw new Error('IGC file exceeds the 5 MB limit.');
            if (!/\.igc$/i.test(file.name)) throw new Error('Please select an .igc file.');
            const text = await file.text();
            if (!input.isConnected || input.files[0] !== file) return;
            const times = flightTimes(text, logsheet.dataset.clubTimezone, logsheet.dataset.logsheetDate);
            launch.value = times.launchTime;
            landing.value = times.landingTime;
            launch.dispatchEvent(new Event('input', { bubbles: true }));
            landing.dispatchEvent(new Event('input', { bubbles: true }));
            status.className = 'small text-success';
            status.textContent = 'Flight times detected. Review them before saving.';
        } catch (error) {
            status.className = 'small text-danger';
            status.textContent = error.message || 'Could not read this IGC file.';
        }
        input.value = ''; // the file is not part of the form submission
    });
})();
