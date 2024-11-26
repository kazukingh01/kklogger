# kklogger
My logger package

# Install

```bash
pip install git+https://github.com/kazukingh01/kklogger.git
```

# Command

You have to escape * ( to \* ).

```bash
kklogrm --path ~/main/log/\*.YYYYMMDD.log --fr 20241001 --to 20241002 # --rm
kklogrm --path ~/main/log/\*.YYYYMMDD.log --nl 10 # --rm
kklogmail --fr aaa@aaa.ccc --to bbb@bbb.ccc --path ~/log/aaaa.`date "+%Y%m%d"`.log --sub check_daily --tail 500 --kwd error # --mail
```