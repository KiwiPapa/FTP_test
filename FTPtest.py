# coding=utf-8
from ctypes import *
import os
import sys
import ftplib


class myFtp:
    ftp = ftplib.FTP()

    def __init__(self, host, port=21):
        self.ftp.connect(host, port)

    def Login(self, user, passwd):
        self.ftp.login(user, passwd)
        print(self.ftp.welcome)

    def DownLoadFile(self, LocalFile, RemoteFile):  # 下载单个文件
        file_handler = open(LocalFile, 'wb')
        print(file_handler)
        # self.ftp.retrbinary("RETR %s" % (RemoteFile), file_handler.write)#接收服务器上文件并写入本地文件
        self.ftp.retrbinary('RETR ' + RemoteFile, file_handler.write)
        file_handler.close()
        return True

    def DownLoadFileTree(self, LocalDir, RemoteDir):  # 下载整个目录下的文件
        print("remoteDir:", RemoteDir)
        if not os.path.exists(LocalDir):
            os.makedirs(LocalDir)
        self.ftp.cwd(RemoteDir)
        RemoteNames = self.ftp.nlst()
        print("RemoteNames", RemoteNames)
        for file in RemoteNames:
            Local = os.path.join(LocalDir, file)
            print(self.ftp.nlst(file))
            if self.ftp.nlst(file)[0] != file: # 取nlst后不为本身，说明为目录(有瑕疵)
                if not os.path.exists(Local):
                    os.makedirs(Local)
                try:
                    print(self.ftp.nlst(file))
                    if self.ftp.nlst(file) == []: # 空文件夹情况
                        print('**********', file)
                        print(self.ftp.pwd())
                        # self.ftp.cwd("..")
                    else:
                        self.DownLoadFileTree(Local, file)
                except:
                    print('Not a directory')
            else:
                try:
                    self.DownLoadFile(Local, file)
                except:
                    print('Error downloading a file')
        self.ftp.cwd("..")
        return

    def close(self):
        self.ftp.quit()


if __name__ == "__main__":
    ftp = myFtp('10.132.203.206')
    ftp.Login('zonghs', 'zonghs123')
    ftp.DownLoadFileTree('./Software', '/oracle_data9/arc_data/SGI1/2016年油套管检测归档/下载测试')
    print("更新完毕。")