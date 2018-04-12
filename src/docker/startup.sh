#!/bin/bash

cd /opt/archer
# 切换python运行环境
source /opt/venv4archer/bin/activate
#启动ngnix
/usr/sbin/nginx

#收集所有的静态文件到STATIC_ROOT
python3 manage.py collectstatic -v0 --noinput

settings=${1:-"archer.settings"}
ip=${2:-"127.0.0.1"}
port=${3:-8000}

gunicorn -w 2 --env DJANGO_SETTINGS_MODULE=${settings} --error-logfile=/tmp/archer.err -b ${ip}:${port}  --daemon archer.wsgi:application