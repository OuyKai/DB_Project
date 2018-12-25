import socket
import _thread
import config
from manager import manager

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((config.ip_address, config.ip_port))
    s.listen(config.listen_limit)
    print('======================start=======================')
    print('                  服务器正在运行...')
    print('=======================end========================')
    while True:
        sock, address = s.accept()
        try:
            _thread.start_new_thread(manager, (sock, address))
        except:
            print('连接异常终止: source: %s' % address + ' --- destination: %s' % config.ip_address)
