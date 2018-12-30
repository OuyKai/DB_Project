import socket
import _thread
import config
import pymysql
from manager import manager

def Update():
    con = pymysql.connect(
        host=config.ip_address,
        port=config.db_port,
        user=config.root_name,
        password=config.root_password,
        db=config.db_name
    )
    cur = con.cursor()
    cur.execute("select * from menu")
    menu = cur.fetchall()
    for food in menu:
        config.food_menu.append(list(food))
        print(config.food_menu)

    con = pymysql.connect(
        host=config.ip_address,
        port=config.db_port,
        user=config.customer_name,
        password=config.customer_password,
        db=config.db_name
    )
    config.mutex.acquire()
    config.customer_cur = con.cursor()
    config.mutex.release()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((config.ip_address, config.ip_port))
    s.listen(config.listen_limit)
    print('======================start=======================')
    print('                  服务器正在运行...')
    print('=======================end========================')

    Update()
    while True:
        sock, address = s.accept()
        try:
            _thread.start_new_thread(manager, (sock, address))
        except:
            print('连接异常终止: source: %s' % address + ' --- destination: %s' % config.ip_address)
