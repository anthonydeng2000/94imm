# -*- coding: utf-8 -*-
import sys

sys.path.append('../')
import pymysql, time, os, random, shutil, platform
from config import mysql_config,site_path

dbhost = {
    "host": mysql_config['HOST'],
    "dbname": mysql_config['NAME'],
    "user": mysql_config['USER'],
    "password": mysql_config['PASSWORD']
}


def do_post(file_dir, sleep_time="0", num=1):
    '''
    :param file_dir: 字都搜索此目录下载二级目录，二级目录名为发布的图集名，二级目录下文件自动移动到static/images下
    :param sleep_time: 发布间隔，默认为0
    :return:
    '''
    db = pymysql.connect(dbhost.get("host"), dbhost.get("user"), dbhost.get("password"), dbhost.get("dbname"))
    cursor = db.cursor()
    for index, files in enumerate(os.walk(file_dir)):
        if index > num:
            break
        else:
            tagidlist = []
            sysstr = platform.system()
            if sysstr == "Windows":
                title = files[0].split("\\")[-1]
                os_path = file_dir.split("\\")[-1]
            elif sysstr == "Linux":
                title = files[0].split("/")[-1]
                os_path = file_dir.split("/")[-1]
            if title != os_path:
                if 'cos' in title or "COS" in title or 'Cos' in title:
                    type_id = 6
                    tags = ['cosplay', '萝莉', '美腿', '少女']
                elif "袜" in title or "丝" in title or "制服" in title:
                    type_id = 2
                    tags = ['丝袜诱惑', '美腿', '制服美女', '大尺度']
                elif "青春" in title or "清纯" in title:
                    type_id = 3
                    tags = ['清纯', '可人', '少女']
                elif "萝莉" in title:
                    type_id = 4
                    tags = ['娇躯', '萝莉', '粉嫩']
                else:
                    type_id = 1
                    tags = ['性感', '美胸', '诱惑']
                isExists = cursor.execute("SELECT * FROM images_page WHERE title =" + "'" + title + "'" + " limit 1;")
                if isExists != 0:
                    print("已存在：" + title)
                else:
                    for tag in tags:
                        sqltag = "SELECT * FROM images_tag WHERE tag =" + "'" + tag + "'" + " limit 1;"
                        isExiststag = cursor.execute(sqltag)
                        if isExiststag != 1:
                            cursor.execute("INSERT INTO images_tag (tag) VALUES (%s)", tag)
                        cursor.execute("SELECT id FROM images_tag WHERE tag =" + "'" + tag + "'")
                        for id in cursor.fetchall():
                            tagidlist.append(id[0])
                    p = (title, str(tagidlist), time.strftime('%Y-%m-%d', time.localtime(time.time())), type_id, "1")
                    cursor.execute(
                        "INSERT INTO images_page (title,tagid,sendtime,typeid,firstimg) VALUES (%s,%s,%s,%s,%s)",
                        p)
                    pageid = cursor.lastrowid
                    data_sj = time.localtime(int(time.time()))
                    time_str = time.strftime("%Y%m%d", data_sj)
                    rpath = time_str + "/" + "".join(random.sample('abcdefghijklmnopqrstuvwxyz', 7))
                    count = 1
                    for name in files[2]:
                        path = files[0] + "/" + name
                        rename = str(count) + "." + name.split(".")[-1]
                        path_isExists = os.path.exists(site_path+"static/images/" + rpath)
                        if not path_isExists:
                            os.makedirs(site_path+"static/images/" + rpath)
                        try:
                            shutil.move(path, site_path+"static/images/" + rpath + "/" + rename)
                            imgp = "/static/images/" + rpath + "/" + rename
                            if count == 1:
                                cursor.execute(
                                    "UPDATE images_page SET firstimg = %s WHERE id=%s", (imgp, pageid))
                            cursor.execute("INSERT INTO images_image (pageid,imageurl) VALUES (%s,%s)", (pageid, imgp))

                        except Exception as e:
                            print(e)
                            break
                        count += 1
                    try:
                        os.removedirs(files[0])
                    except:
                        print("目录不为空，无法删除")
                print("发布完成：" + title)
            time.sleep(int(sleep_time))


if __name__ == "__main__":
    path = site_path+'post'
    num = int(sys.argv[1])
    do_post(path, "0",num)
