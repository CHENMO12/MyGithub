from ftplib import FTP


def ftp_down(HOST, romatepath, filename, localpath):
    user = "caihuizi"
    password = "Caihuizi123"
    ftp = FTP(HOST)  # 连接远程服务器IP地址
    ftp.encoding = 'utf-8'  # 解决中文乱码问题
    ftp.login(user, password)
    # print (ftp.getwelcome())#显示ftp服务器欢迎信息
    ftp.cwd(romatepath)  # 选择操作目录
    bufsize = 1024
    file_handler = open(localpath, 'wb').write  # 以写模式在本地打开文件
    ftp.retrbinary('RETR %s' % filename, file_handler, bufsize)
    ftp.quit()
    print("ftp down OK")


ftp_down("172.16.12.45", "/商铺产品/JK/V4R6/trunk/V4R6B15-04/", "sql", "")

# ('caihuizi', 'Caihuizi123')
