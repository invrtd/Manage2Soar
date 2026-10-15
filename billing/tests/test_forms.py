from datetime import date, datetime
from datetime import timezone as dt_timezone

import pytest
from django.utils import timezone

from billing.forms import ManualEntryForm, OpeningBalanceOverrideForm

# 03:00 UTC on Jan 1 is still the evening of Dec 31 in Los Angeles, so the
# server (UTC) date runs a day ahead of the club-local date.
SERVER_NOW = datetime(2020, 1, 1, 3, 0, tzinfo=dt_timezone.utc)
CLUB_TODAY = date(2019, 12, 31)


@pytest.fixture
def club_evening(enable_billing_app, monkeypatch):
    enable_billing_app.club_timezone = "America/Los_Angeles"
    enable_billing_app.save(update_fields=["club_timezone"])
    monkeypatch.setattr(timezone, "now", lambda: SERVER_NOW)


@pytest.mark.parametrize("form_class", [ManualEntryForm, OpeningBalanceOverrideForm])
def test_effective_date_defaults_to_club_local_date(club_evening, form_class):
    form = form_class()

    initial = form.get_initial_for_field(
        form.fields["effective_date"], "effective_date"
    )

    assert SERVER_NOW.date() != CLUB_TODAY
    assert initial == CLUB_TODAY
