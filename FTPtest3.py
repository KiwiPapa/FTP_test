import sys
import ftplib
import os
from ftplib import FTP

ftp = FTP("10.132.203.206")
ftp.login("zonghs", "zonghs123")


def downloadFiles(path, destination):
    # path & destination are str of the form "/dir/folder/something/"
    # path should be the abs path to the root FOLDER of the file tree to download
    try:
        ftp.cwd(path)
        # clone path to destination
        os.chdir(destination)
        os.mkdir(destination[0:len(destination)] + path)
        print(destination[0:len(destination)] + path + "built")
    except OSError:
        # folder already exists at destination
        pass
    except ftplib.error_perm:
        # invalid entry (ensure input form: "/dir/folder/something/")
        print("error: could not change to " + path)
        sys.exit("ending session")

    # list children:
    filelist = ftp.nlst()

    for file in filelist:
        try:
            # this will check if file is folder:
            ftp.cwd(path + file + "/")
            # if so, explore it:
            downloadFiles(path + file + "/", destination)
        except ftplib.error_perm:
            # not a folder with accessible content
            # download & return
            os.chdir(destination[0:len(destination) - 1] + path)
            # possibly need a permission exception catch:
            ftp.retrbinary("RETR " + file, open(os.path.join(destination, file), "wb").write)
            print(file + " downloaded")
    return


source = "/app/zonghs/"
dest = "/IN"
downloadFiles(source, dest)
