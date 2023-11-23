from datetime import timedelta
from app.utils.timedelta import parse_delta


def test_day_deltas():
    assert parse_delta('3d') == timedelta(days=3)
    assert parse_delta('37D') == timedelta(days=37)


def test_hours_deltas():
    assert parse_delta('18h') == timedelta(hours=18)
    assert parse_delta('11H') == timedelta(hours=11)


def test_minute_deltas():
    assert parse_delta('129m') == timedelta(minutes=129)
    assert parse_delta('12M') == timedelta(minutes=12)


def test_combined_deltas():
    assert parse_delta('3d5h') == timedelta(days=3, hours=5)
    assert parse_delta('13d19m') == timedelta(days=13, minutes=19)
    assert parse_delta('4h19m') == timedelta(hours=4, minutes=19)
    assert parse_delta('13d4h19m') == timedelta(days=13, hours=4, minutes=19)
