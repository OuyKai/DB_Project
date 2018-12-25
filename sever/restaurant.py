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
        try:
            con = pymysql.connect(
                host=config.ip_address,
                port=config.ip_port,
                user=username,
                password=password,
                db=config.db_name
            )
            self.cur = con.cursor()
        except pymysql.Error as e:
            sock.send(config.Dictionary['no'].encode())
            print("Error %d: %s"%(e.args[0],e.args[1]))
        sock.send(config.Dictionary['yes'].encode())
        return

    def Sign_up(self, sock, para):
        data = para.strip.split()
        username = data[0]
        password = data[1]
        flag = False
        try:
            self.cur.callproc(config.sign_up, (username, password, flag))
        except pymysql.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
        if flag == True:
            sock.send(config.Dictionary['yes'].encode())
        else:
            sock.send(config.Dictionary['no'].encode())
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
