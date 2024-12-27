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

# Web log

```bash
cat nohup.out | ansi2html > test.html
```

# Nginx

```bash
sudo apt update
sudo apt install -y colorized-logs 
sudo docker pull nginx:latest
mkdir -p /home/share/nginx
sudo docker run -it -d -p 8080:80 --name web -v /home/share/nginx:/usr/share/nginx/html nginx:latest
cat nohup.out | ansi2html > /home/share/nginx/check_log.html
```