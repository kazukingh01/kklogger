import glob, argparse
import smtplib, argparse, glob
from email.mime.text import MIMEText
from email.utils import formatdate
# local package
from kklogger import set_logger
from kklogger.util.com import strfind


def create_message(from_addr, to_addr, bcc_addrs, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From']    = from_addr
    msg['To']      = to_addr
    msg['Bcc']     = bcc_addrs
    msg['Date']    = formatdate()
    return msg

def send(from_addr, to_addrs, password, msg):
    smtpobj = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
    smtpobj.login(from_addr, password)
    smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
    smtpobj.close()


parser = argparse.ArgumentParser(
    description="This command is easy way to mail a log file to gmail address.",
    epilog=r"""
    [kklogmail --fr aaa@aaa.ccc --to bbb@bbb.ccc --path ~/log/aaaa.`date "+%Y%m%d"`.log --sub check_daily --tail 500 --kwd error --mail]
    """
)
parser.add_argument("--fr",   type=str, help="email address form XXX. ex) --fr XXX@gmail.com", required=True)
parser.add_argument("--to",   type=str, help="email address to   YYY. ex) --to YYY@gmail.com", required=True)
parser.add_argument("--pwd",  type=str, help="password. ex) --password ZZZZ")
parser.add_argument("--sub",  type=str, help=r"subject. If you want to use space, escape it. ex) --error\ log\ xxxx.log")
parser.add_argument("--path", type=str, help=r"Targe files path. It's searched via glob.glob(**). ex) --path ../logfiles/\*.log", required=True)
parser.add_argument("--tail", type=int, help="search for final n-line. ex) --tail 20", default=20)
parser.add_argument("--kwd",  type=str, help="If you want to make a trriger to mail, type a keyword which include in tail of logs. ex) --kwd error")
parser.add_argument("--mail", action='store_true', help="If you want send email, set this option. ex) --mail", default=False)
args = parser.parse_args()
assert strfind(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", args.fr)
assert strfind(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", args.to)
assert args.pwd is None or isinstance(args.pwd, str)
assert args.sub is None or isinstance(args.sub, str)
FROM_ADDRESS = args.fr
TO_ADDRESS   = args.to
MY_PASSWORD  = args.pwd
BCC          = ''
SUBJECT      = args.sub
LOGGER = set_logger(__name__)


def logmail():
    LOGGER.info(f"{args}")
    msgs = []
    for file in glob.glob(args.path):
        with open(file, mode="r") as f: body = f.readlines()
        body = f"{file}\n\n" + "".join(body[-args.tail:])
        if args.kwd is not None:
            if body.lower().find(args.str.lower()) >= 0:
                msgs.append(body)
        else:
            msgs.append(body)
    if len(msgs) > 0:
        msgs = "\n\n==========\n\n".join(msgs)
        msgs = create_message(FROM_ADDRESS, TO_ADDRESS, BCC, SUBJECT, msgs)
        LOGGER.info(f"Below text will be sent.\n\nfrom: {FROM_ADDRESS}\nto: {TO_ADDRESS}\nsub: {SUBJECT}\nbody: \n{msgs}\n")
        if args.mail:
            send(FROM_ADDRESS, TO_ADDRESS, MY_PASSWORD, msgs)
    else:
        LOGGER.info("Nothing to be sent.")
