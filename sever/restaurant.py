import config
import pymysql
import time

class Restaurant():
    def __init__(self):
        self.role = ""
        self.start_time = 0
        self.number_of_table = -1
        self.order_list = []
        self.cost = 0
        self.cook_list = []
        self.serve_list = []
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
        self.start_time = time.time()
        sock.send(config.Dictionary['yes'].encode())
        return

    def Employ(self, sock, para):
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

    def Order(self, sock, para):
        '''
        调用order函数
        :param sock:
        :param para:
        :return:
        '''
        menu = para.strip.split()
        print(menu[0] + " : " + menu[1:])
        self.cost = len(menu)
        config.mutex.acquire()
        for food in menu:
            config.cook_food_list.append(food)
        config.mutex.release()
        sock.send(config.Dictionary['yes'].encode())
        sock.send(str(self.cost).encode())
        return

    def Checkout(self, sock):
        '''
        数据库加钱
        :param sock:
        :return:
        '''
        print(str(self.number_of_table) + " 号桌已结账 >> " + str(self.cost) + " 元")
        sock.send(config.Dictionary['yes'].encode())
        return

    def Cook(self, sock):
        food = ""
        while time.time() - self.start_time <= 8 * 60 * 60:
            config.mutex.acquire()
            if len(config.cook_food_list) != 0:
                sock.send(config.Dictionary['cook'].encode())
                food = config.cook_food_list[0]
                sock.send(food.encode())
                config.cook_food_list = config.cook_food_list[1:]
            config.mutex.release()
            flag = sock.recv(1024).decode()
            if flag == config.Dictionary['yes']:
                config.mutex.acquire()
                config.serve_dish_list.append(food)
                config.mutex.release()
                continue
            else:
                config.mutex.acquire()
                config.cook_food_list.append(food)
                config.mutex.release()
                print("Cooker down ! Error !")
        return

    def Serve(self, sock):
        food = ""
        while time.time() - self.start_time <= 8 * 60 * 60:
            config.mutex.acquire()
            if len(config.cook_food_list) != 0:
                sock.send(config.Dictionary['serve'].encode())
                food = config.serve_dish_list[0]
                sock.send(food.encode())
                config.serve_dish_list = config.serve_dish_list[1:]
            config.mutex.release()
            flag = sock.recv(1024).decode()
            if flag == config.Dictionary['yes']:
                print(food + " have been served !")
                continue
            else:
                config.mutex.acquire()
                config.serve_dish_list.append(food)
                config.mutex.release()
                print("Waiter down ! Error !")
        return

    def Unemploy(self, sock, para):
        username = para
        print(username + " 已解雇")
        sock.send(config.Dictionary['yes'].encode())
        return

    def Payoff(self, sock):

        sock.send(config.Dictionary['yes'].encode())
        return
