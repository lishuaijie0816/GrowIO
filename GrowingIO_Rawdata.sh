#!/bin/sh

echo `date`" ----> 开始下载" >> /Users/weiche/data/GrowingIO/log/run.log &&

cd /Users/weiche/data/GrowingIO/script &&

/usr/local/bin/python3 GrowingIO_Rawdata.py

if [ $? -eq 0 ];then
    echo `date`" ----> 下载完成" >> /Users/weiche/data/GrowingIO/log/run.log
else
    echo `date`" ----> 下载失败" >> /Users/weiche/data/GrowingIO/log/run.err
fi
