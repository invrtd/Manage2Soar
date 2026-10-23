const test = require('node:test');
const assert = require('node:assert/strict');
const { parseIGC, flightTimes } = require('../igc-flight-times.js');

function fix(seconds, longitudeThousandths, valid = 'A', altitude = 100) {
    const clock = `${String(Math.floor(seconds / 3600)).padStart(2, '0')}${String(Math.floor(seconds / 60) % 60).padStart(2, '0')}${String(seconds % 60).padStart(2, '0')}`;
    return `B${clock}0000000N000${String(longitudeThousandths).padStart(5, '0')}E${valid}${String(altitude).padStart(5, '0')}${String(altitude).padStart(5, '0')}`;
}

function track(start = 10 * 3600, offset = 0) {
    return [
        fix(start, offset), fix(start + 5, offset), fix(start + 10, offset),
        fix(start + 15, offset + 27), fix(start + 20, offset + 54),
        fix(start + 25, offset + 81), fix(start + 30, offset + 108),
        fix(start + 35, offset + 108), fix(start + 40, offset + 108),
        fix(start + 45, offset + 108), fix(start + 50, offset + 108),
    ];
}

function igc(lines, date = '010726') {
    return `AXCS123\nHFDTE${date}\n${lines.join('\n')}\n`;
}

test('detects sustained movement, ignores pre/post-flight fixes and converts UTC to club time', () => {
    const result = flightTimes(igc(track(10 * 3600 + 59 * 60 + 40)), 'America/New_York', '2026-07-01');
    assert.deepEqual(result, { launchTime: '06:59', landingTime: '07:00' });
});

test('rejects two complete flights instead of silently choosing one', () => {
    const lines = [...track(), ...track(11 * 3600, 108)];
    assert.throws(() => flightTimes(igc(lines), 'UTC', '2026-07-01'), /multiple flights/);
});

test('rejects missing landing and GPS gaps during flight', () => {
    assert.throws(() => flightTimes(igc(track().slice(0, 7)), 'UTC', '2026-07-01'), /Landing is not recorded/);
    const lines = [...track().slice(0, 7), fix(10 * 3600 + 110, 108)];
    assert.throws(() => flightTimes(igc(lines), 'UTC', '2026-07-01'), /gap during flight/);
});

test('rejects a file already moving before the first ground fixes', () => {
    assert.throws(() => flightTimes(igc(track().slice(2)), 'UTC', '2026-07-01'), /Takeoff is not recorded/);
});

test('validates date and GPS fixes', () => {
    assert.throws(() => parseIGC(igc(track(), '320726')), /date is invalid/);
    assert.throws(() => parseIGC(igc(track().map(line => line.slice(0, 24) + 'V' + line.slice(25)))), /too few valid/);
    assert.throws(() => flightTimes(igc(track()), 'UTC', '2026-07-02'), /outside this logsheet date/);
});

test('tracks UTC midnight rollover', () => {
    const lines = [fix(86395, 0), fix(86399, 0), fix(0, 0), fix(5, 0)];
    const fixes = parseIGC(igc(lines));
    assert.equal((fixes[3].time - fixes[2].time) / 1000, 5);
});

test('supports older IGC flight dates', () => {
    assert.equal(new Date(parseIGC(igc(track(), '010799'))[0].time).getUTCFullYear(), 1999);
});
