# coding=utf-8
"""
FTP常用操作
"""
import sys
from ftplib import FTP
import os

def getbinary(ftp, filename, outfile=None):
    if outfile is None:
       outfile = sys.stdout
    ftp.retrbinary("RETR " + filename, outfile.write)

host = "10.132.203.206"
username = "zonghs"
password = "zonghs123"
port = 21

ftp = FTP()
ftp.connect(host=host, port=port)  # 连接ftp
ftp.login(username, password)  # 登录ftp
print(ftp.getwelcome())
getbinary(ftp, "welcome.msg")