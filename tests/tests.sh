#!/bin/bash
set -euo pipefail

if [ -d "venv" ]; then
    rm -rf venv
fi

python -m venv venv
source venv/bin/activate

commit_hash=$(git log -1 --format=%H)
echo "Latest commit hash: $commit_hash"
pip install "git+https://github.com/kazukingh01/kklogger.git@$commit_hash"

python test.py
kklogrm --path ./test.YYYY-MM-DD\*.log --fr 20250101 --to 20250301 --rm

last_line=$(tail -n 1 test.log)
last_char="${last_line: -1}"

if [ "$last_char" = "2" ]; then
    echo "!!!!! OK !!!!!"
else
    echo "!!!!! NG !!!!!"
    exit 1
fi

rm -rf venv
rm test.log