import re
from datetime import timedelta


TIMEDELTA_REGEX = (
    r'((?P<days>\d+)d)?'
    r'((?P<hours>\d+)h)?'
    r'((?P<minutes>\d+)m)?'
)

TIMEDELTA_PATTERN = re.compile(TIMEDELTA_REGEX, re.IGNORECASE)


def parse_delta(delta):
    match = TIMEDELTA_PATTERN.match(delta)
    if match:
        parts = {k: int(v) for k, v in match.groupdict().items() if v}
        return timedelta(**parts)
