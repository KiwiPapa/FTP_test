# coding=utf-8
import shutil
import os
import ftplib


class myFTP:
    ftp = ftplib.FTP()

    def __init__(self, host, port=21):
        self.ftp.connect(host, port)

    def Login(self, user, passwd):
        self.ftp.login(user, passwd)
        print(self.ftp.welcome)

    def Cwd(self, path):
        self.ftp.cwd(path)

    def Nlst(self):
        return self.ftp.nlst()

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
            if self.ftp.nlst(file) == []: # 空文件夹情况
                if not os.path.exists(Local):
                    os.makedirs(Local)
            else:
                if self.ftp.nlst(file)[0] != file: # 取nlst后不为本身，说明为目录(有瑕疵)
                    if not os.path.exists(Local):
                        os.makedirs(Local)
                    try:
                        self.DownLoadFileTree(Local, file)
                    except:
                        print('Error downloading a directory')
                else:
                    try:
                        self.DownLoadFile(Local, file)
                    except:
                        print('Error downloading a file')
        self.ftp.cwd("..")
        return

    def close(self):
        self.ftp.quit()

# 清理所有非空文件夹和文件
def clean_dir_of_all(path):
    list = os.listdir(path)
    if len(list) != 0:
        for i in range(0, len(list)):
            path_to_clean = os.path.join(path, list[i])
            if '.' not in list[i]:
                shutil.rmtree(path_to_clean)  # 清理文件夹，可非空
            else:
                os.remove(path_to_clean)  # 清理文件
    else:
        pass

if __name__ == "__main__":
    ftp = myFTP('10.132.203.206')
    ftp.Login('zonghs', 'zonghs123')
    local_path = './工程测井工作助手(自动更新版)'
    # local_path = r'C:\Users\YANGYI\source\repos\GC_Logging_Helper_Release'
    remote_path = '/oracle_data9/arc_data/SGI1/2016年油套管检测归档/工程测井工作助手最新版本'

    # 打开本地版本号
    try:
        with open(local_path + '/版本号.txt', "r") as f:
            license_str = f.read()
        local_license_date = int(license_str)

        # 打开服务器版本号
        ftp.Cwd(remote_path)
        filenames = ftp.Nlst()
        filename = '版本号.txt'
        LocalFile = local_path + '/temp/版本号.txt'
        RemoteFile = filename

        # 接收服务器上文件并写入本地文件
        if not os.path.exists(local_path + '/temp'):
            os.makedirs(local_path + '/temp')
        ftp.DownLoadFile(LocalFile, RemoteFile)

        with open(local_path + '/temp/版本号.txt', "r") as f:
            license_str = f.read()
        remote_license_date = int(license_str)

        if local_license_date < remote_license_date:
            clean_dir_of_all(local_path)
            ftp.DownLoadFileTree(local_path, remote_path)
            print("更新完毕。")
        elif local_license_date >= remote_license_date:
            print("本地软件版本已经是最新，无需更新。")
    except:
        ftp.DownLoadFileTree(local_path, remote_path)
        print("下载完毕。")