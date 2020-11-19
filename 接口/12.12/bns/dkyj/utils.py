# -*-coding: utf-8 -*-
#@Time     : 2019/11/18 19:29
#@Author   : zhongqingqing
#@FileName : utils.py

import sys, datetime
sys.path.append("..")
import os

from base.helper import MysqlHelper
import config
import jpype


# 从数据库中获取账号密码 -- iot平台
def get_md5Password_from_mysql_in_iot(user_phone):
    db_conn = MysqlHelper(host=config.get_db_host,username=config.get_db_username,password=config.get_db_password)
    cmd = "select password from iot_auth.user where phone=\"{}\";".format(user_phone)
    password_by_md5 = db_conn.query_sql(cmd)
    if not password_by_md5:
        exit("无法从数据库查询到数据。sql：{}".format(cmd))
    return [x[0] for x in password_by_md5].pop()

# 从数据库中获取账号密码 -- mall平台
def get_md5Password_from_mysql_in_mall(user_phone):
    db_conn = MysqlHelper(host=config.get_db_host, username=config.get_db_username, password=config.get_db_password)
    cmd = "select password from auth.user where phone=\"{}\";".format(user_phone)
    password_by_md5 = db_conn.query_sql(cmd)
    return [x[0] for x in password_by_md5].pop()

# 从数据库中获取设备的publicKey
def get_publicKey_from_mysql(equipmentno):
    db_conn = MysqlHelper(host=config.get_db_host,username=config.get_db_username,password=config.get_db_password)
    cmd = 'select a.device_code,b.public_key from device.device_base as a left join device.device_cert b on a.id =b.device_base_id where a.device_code = "{}"'.format(equipmentno)
    publicKey = db_conn.query_sql(cmd)
    if not publicKey:
        raise Exception("无法从数据库查询到数据。sql：{}".format(cmd))
    return str([x[1] for x in publicKey if x[0] == equipmentno][0])

class RSA(object):
    __species = None
    __first_init = True

    def __new__(cls, *args, **kwargs):
        if cls.__species == None:
            cls.__species = object.__new__(cls)
        return cls.__species

    def __init__(self):
        if self.__first_init:
            jar_path = os.path.dirname(__file__) + os.sep + '..' + os.sep + '..' + os.sep + "testdata" + os.sep + 'jarfile_dir' + os.sep + 'rsa.jar'
            jvm_arg = "-Djava.class.path=%s" % jar_path
            if not jpype.isJVMStarted():
                jpype.startJVM(jpype.get_default_jvm_path(), "-ea", jvm_arg)
            if not jpype.isThreadAttachedToJVM():
                jpype.attachThreadToJVM()
            import time
            time.sleep(0.5)
            JDClass = jpype.JClass("dj.RSATool")
            self.jd = JDClass()

    def rsa_pubkey_encrypt(self,publicKey,content):
        return self.jd.pubKeyEncrypt(publicKey,content)

    def rsa_pubkey_decrypt(self,publicKey,encodeString):
        return self.jd.pubKeyDecrypt(publicKey,encodeString)

    def rsa_private_encrypt(self,privateKey,content):
        return self.jd.priKeyEncrypt(privateKey,content)

    def rsa_private_decrypt(self,privateKey,encodeString):
        return self.jd.priKeyDecrypt(privateKey,encodeString)



if __name__ == '__main__':
    res = get_md5Password_from_mysql_in_iot("13255970108")
    print(res)
