from datetime import date

from elb_log_tools import logs


def test_emit_dates():
    d = date.today()
    dates = list(logs.emit_dates(d, 2))
    assert len(dates) == 2
