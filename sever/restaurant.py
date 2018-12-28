import config
import pymysql
import time

class Restaurant():
    def __init__(self):
        self.role = ""
        self.name = ""
        self.start_time = 0
        self.number_of_table = -1
        self.order_list = []
        self.cost = 0
        self.cook_list = []
        self.serve_list = []
        return

    def Login(self, sock, para):
        username = para[0]
        password = para[1]
        try:
            con = pymysql.connect(
                host=config.ip_address,
                port=config.db_port,
                user=username,
                password=password,
                db=config.db_name
            )
            self.cur = con.cursor()
            self.name = username
        except pymysql.Error as e:
            sock.send(config.Dictionary['no'].encode())
            print("Error %d: %s"%(e.args[0],e.args[1]))
        self.start_time = time.time()
        sock.send(config.Dictionary['yes'].encode())
        return

    def Employ(self, sock, para):
        username = para[0]
        password = para[1]
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
        print(str(para[0]) + " : " + str(para[1:]))
        self.cost = len(para)
        config.mutex.acquire()
        for food in para[1:]:
            config.cook_food_list.append((para[0], food))
        config.mutex.release()
        sock.send(config.Dictionary['yes'].encode())
        sock.send(str(self.cost).encode())
        print("Order successfully ! ")
        return

    def wait(self, sock):
        while True:
            flag = sock.recv(1024).decode()
            if flag == config.Dictionary['yes']:
                print(str(self.number_of_table) + " 号桌已完成")
                return
            time.sleep(1)
            config.mutex.acquire()
            if len(config.finish_food[self.number_of_table]) != 0:
                food = config.finish_food[self.number_of_table][0]
                sock.send(food.encode())
                del config.finish_food[self.number_of_table][0]
            config.mutex.release()

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
        while time.time() - self.start_time <= 8 * 60 * 60:
            config.mutex.acquire()
            if len(config.cook_food_list) != 0:
                sock.send(config.Dictionary['cook'].encode())
                table = config.cook_food_list[0][0]
                food = config.cook_food_list[0][1]
                sock.send(food.encode())
                config.cook_food_list = config.cook_food_list[1:]
                config.mutex.release()

                flag = sock.recv(1024).decode()
                if flag == config.Dictionary['yes']:
                    config.mutex.acquire()
                    print("-* " + str(table) + " 号桌 : " + food + " 已被 " + self.name + " 完成 *-")
                    config.serve_dish_list.append((table, food))
                    config.mutex.release()
                    continue
                else:
                    config.mutex.acquire()
                    config.cook_food_list.append((table, food))
                    config.mutex.release()
                    print("-* Cooker down ! Error ! *-")
            else:
                config.mutex.release()
            time.sleep(1)
        return

    def Serve(self, sock):
        while time.time() - self.start_time <= 8 * 60 * 60:
            config.mutex.acquire()
            if len(config.serve_dish_list) != 0:
                sock.send(config.Dictionary['serve'].encode())
                table = config.serve_dish_list[0][0]
                food = config.serve_dish_list[0][1]
                sock.send(food.encode())
                config.serve_dish_list = config.serve_dish_list[1:]
                config.mutex.release()
                flag = sock.recv(1024).decode()
                if flag == config.Dictionary['yes']:
                    print(food + " have been served by " + self.name)
                    config.mutex.acquire()
                    config.finish_food[table].append(food)
                    config.mutex.release()
                    continue
                else:
                    config.mutex.acquire()
                    config.serve_dish_list.append((table, food))
                    config.mutex.release()
                    print("Waiter down ! Error !")
            else:
                config.mutex.release()
            time.sleep(1)
        return

    def Unemploy(self, sock, para):
        username = para
        print(username + " 已解雇")
        sock.send(config.Dictionary['yes'].encode())
        return

    def Payoff(self, sock):

        sock.send(config.Dictionary['yes'].encode())
        return
