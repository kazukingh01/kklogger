import re, datetime


__all__ = [
    "strfind",
    "str_to_datetime",
]


def strfind(pattern: str, string: str, flags=0) -> bool:
    if len(re.findall(pattern, string, flags=flags)) > 0:
        return True
    else:
        return False

def str_to_datetime(string: str, tzinfo: datetime.timezone=datetime.timezone.utc) -> datetime.datetime:
    if   strfind(r"^[0-9]+$", string) and len(string) == 8:
        return datetime.datetime(int(string[0:4]), int(string[4:6]), int(string[6:8]), tzinfo=tzinfo)
    elif strfind(r"^[0-9][0-9][0-9][0-9]/([0-9]|[0-9][0-9])/([0-9]|[0-9][0-9])$", string):
        strwk = string.split("/")
        return datetime.datetime(int(strwk[0]), int(strwk[1]), int(strwk[2]), tzinfo=tzinfo)
    elif strfind(r"^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$", string):
        strwk = string.split("-")
        return datetime.datetime(int(strwk[0]), int(strwk[1]), int(strwk[2]), tzinfo=tzinfo)
    elif strfind(r"^[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]$", string):
        strwk = string.split("-")
        return datetime.datetime(int(strwk[2]), int(strwk[1]), int(strwk[0]), tzinfo=tzinfo)
    elif strfind(r"^[0-9]+$", string) and len(string) == 14:
        return datetime.datetime(int(string[0:4]), int(string[4:6]), int(string[6:8]), int(string[8:10]), int(string[10:12]), int(string[12:14]), tzinfo=tzinfo)
    else:
        raise ValueError(f"{string} is not converted to datetime.")
