import glob, argparse, re, datetime, os, subprocess
# local package
from kklogger import set_logger
from kklogger.util.com import str_to_datetime


parser = argparse.ArgumentParser(
    description="This command is easy way to remove log files which have datetime format in file name.",
    epilog="""
    [(1) rmlog --path ./logs/pylog_YYYYMMDD.log --fr 20240101 --to 20240201]
    [(2) rmlog --path ./logs/pylog_YYYYMMDD.log --nl 10]
    """
)
parser.add_argument("--path", type=str, help="glob.globe(**) path. YYYY: year, MM: month, DD: day, X: extra number. ex) --path \*YYYYMMDD.X.log", required=True)
parser.add_argument("--fr",   type=str_to_datetime, help="target removed files from date. ex) --fr 20210101")
parser.add_argument("--to",   type=str_to_datetime, help="target removed files to   date. ex) --ut 20210101")
parser.add_argument("--nl",   type=int, help="target removed files sorted by created datetime until N files left. if '--nl 10', 10 files left. ex) --nl 10")
parser.add_argument("--rm",   action='store_true', help="If you want to remove files after you check, add this option. ex) --rm", default=False)
args = parser.parse_args()
if args.time is not None:
    assert args.time >= 1
    assert (args.fr is None) and (args.to is None)
else:
    assert (args.fr is not None) and (args.to is not None)
    assert args.fr < args.to


LOGGER = set_logger(__name__)


def rmlog(args):
    LOGGER.info(f"{args}")
    if args.time is not None:
        proc = subprocess.run(f"ls -t {args.path}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        for x in proc.stdout.strip().split("\n")[args.time:]:
            LOGGER.info(f"remove target: {x}")
            if args.rm: os.remove(x)
    else:
        path = args.path.replace("YYYY", "*").replace("MM", "*").replace("DD", "*").replace("X", "*")
        list_files = glob.glob(path)
        regex = args.path.replace(".", r"\.").replace("*", ".*"). \
                    replace("YYYY", "(?P<year>[0-9][0-9][0-9][0-9])"). \
                    replace("MM",   "(?P<month>[0-9][0-9])"). \
                    replace("DD",   "(?P<day>[0-9][0-9])"). \
                    replace("X",    "[0-9]")
        def work(x, regex):
            m = re.search(regex, x)
            if m is None:
                return False
            else:
                return datetime.datetime(int(m.group("year")), int(m.group("month")), int(m.group("day")))
        list_date = [work(x, regex) for x in list_files]
        for x, y in zip(list_files, list_date):
            if isinstance(y, bool) and y == False:
                continue
            if args.fr <= y <= args.to:
                LOGGER.info(f"remove target: {x}")
                if args.rm: os.remove(x)
