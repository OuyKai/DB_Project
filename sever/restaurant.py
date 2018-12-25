import config
import pymysql

class Restaurant():
    def __init__(self):
        self.limit_of_table = 0
        self.open_time = 0
        self.close_time = 0
        self.number = -1
        return

    def Login(self, sock, para):
        data = para.strip().split()
        username = data[0]
        password = data[1]
        self.con = pymysql.connect(
            host = config.ip_address,
            port = config.ip_port,
            user = username,
            password = password,
            db = config.db_name
        )
        sock.send(config.Dictionary['yes'].encode())
        return

    def Sign_up(self, sock, para):
        data = para.strip.split()
        username = data[0]
        password = data[1]

        sock.send(config.Dictionary['yes'].encode())
        return

    def Reception(self, sock, para):
        '''
        请求waiter sleep
        :return:
        '''
        number_of_table = int(para)
        sock.send(config.Dictionary['yes'].encode())
        return

    def Order(self, sock, para):
        sock.send(config.Dictionary['yes'].encode())
        return

    def checkout(self, sock, para):
        sock.send(config.Dictionary['yes'].encode())
        return


    def Employ(self, sock, para):
        sock.send(config.Dictionary['yes'].encode())
        return

    def Unemploy(self, sock, para):
        sock.send(config.Dictionary['yes'].encode())
        return

    def Payoff(self, sock, para):
        sock.send(config.Dictionary['yes'].encode())
        return
