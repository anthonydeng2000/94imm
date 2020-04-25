import pymysql, random, requests, threading, os

dbhost={
        "host":"127.0.0.1",
        "dbname":"www_94imm_com",
        "user":"www_94imm_com",
        "password":"TpRJnRh3nd2MJshf"
    }
db = pymysql.connect(dbhost.get("host"), dbhost.get("user"), dbhost.get("password"), dbhost.get("dbname"))
cursor = db.cursor()

rlock = threading.RLock()

pic_list=[]
def get_id():
    id_list = []
    cursor.execute('select * from images_page')
    ls = cursor.fetchall()
    for pic in ls:
        fpic = "/".join(pic[4].split("/")[0:-1])
        if pic[6][0:24] == "http://www.nvshenge.com/":
            continue
        if not os.path.exists("/root/94imm" + pic[4]):
            id_list.append({"id": pic[0], "path": fpic})
        else:
            if os.path.getsize("/root/94imm" + pic[4]) == 0:
                id_list.append({"id": pic[0], "path": fpic})
        # id_list.append({"id": pic[0], "path": fpic})
    return id_list


def get_ls():
    global pic_list
    cursor.execute('select * from images_image')
    for sql in cursor.fetchall():
        loc_pic="/root/94imm"+sql[2]
        origin_url=sql[-1]
        if os.path.exists(loc_pic):
            if os.path.getsize(loc_pic)<=1024:
                pic_list.append({"url": origin_url, "path": loc_pic})
            else:
                pass
        else:
            pic_list.append({"url": origin_url, "path": loc_pic})
    return pic_list

def get_img():
    global pic_list
    while True:
        rlock.acquire()
        if len (pic_list)==0:
            rlock.release()
            break
        else:
            data=pic_list.pop()
            url=data["url"]
            path=data["path"]
            rlock.release()
            page=requests.get(url)
            if page.status_code !=200:
                cursor.fetchall('delete from images_image where origin_url =%s'%(data[url]))
            else:
                content = page.content
                dir_path = "/".join(path.split("/")[0:-1])
                print(dir_path)
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                with open(path,"wb") as w:
                    w.write(content)
            print(url)

# def test():
#     cursor.execute('select * from images_image where pageid=%s'%(57387))
#     ps=cursor.fetchall()
#     print(ps)

if __name__ == "__main__":
    # get_ls()
    # id_list=get_id()

    #print(id_list)
    get_ls()
    for i in range(10):
        it=threading.Thread(target=get_img)
        it.start()
        it.join()
    # get_ls(id_list)
