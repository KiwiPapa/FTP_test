# coding=utf-8
from ftplib import FTP
import logging.config

# 文件服务器参数
ftp_param = {
    'host': '10.132.203.206',
    'port': 21,
    'user': 'zonghs',
    'pwd': 'zonghs123',
    'points_dir': 'comm/cust_point/',
    'desDir': '/oracle_data9/arc_data/SGI1/2016年油套管检测归档/下载测试'
}

bufsize = 1024  # 缓冲区大小

logger = logging.getLogger(__name__)

# 设置变量
ftp = FTP()

# 连接的ftp sever和端口
ftp.connect(ftp_param['host'], ftp_param['port'])

# 登录
ftp.login(ftp_param['user'], ftp_param['pwd'])

# 打印欢迎信息
logger.debug(ftp.getwelcome())

# 进入远程目录
remotepath = ftp_param['desDir']
ftp.cwd(remotepath)

filenames = ftp.nlst()
# 需要下载的文件
for filename in filenames:
    # 以写的模式在本地打开文件
    file_handle = open(filename, "wb").write

    # 接收服务器上文件并写入本地文件
    ftp.retrbinary("RETR " + filename, file_handle, bufsize)

# 退出ftp
ftp.quit()