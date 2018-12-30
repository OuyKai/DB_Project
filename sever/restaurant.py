import config
import pymysql
import time

class Restaurant():
    def __init__(self):
        self.role = ""
        self.name = ""
        self.start_time = 0
        self.number_of_table = -1
        self.number_of_order = -1
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
            self.start_time = time.time()
            sock.send(config.Dictionary['yes'].encode())
        except pymysql.Error as e:
            sock.send(config.Dictionary['no'].encode())
            print("Error %d: %s"%(e.args[0],e.args[1]))
        return

    def Enter(self):
        config.mutex.acquire()
        config.customer_cur.callproc(config.enter, (self.number_of_table, self.number_of_order))
        config.mutex.release()
        if self.number_of_table == -1:
            return False
        else:
            return True

    def Employ(self, sock, para):
        username = para[0]
        password = para[1]
        role = para[2]
        flag = False
        try:
            self.cur.callproc(config.sign_up, (username, password, role, flag))
        except pymysql.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
        if flag == True:
            sock.send(config.Dictionary['yes'].encode())
        else:
            sock.send(config.Dictionary['no'].encode())
        return

    def Show(self, sock):
        record_list = self.cur.callproc(config.show, ())
        len_of_record_list = len(record_list)
        sock.send(str(len_of_record_list).encode())
        for record in record_list:
            sock.send(record.encode())
        return

    def Order(self, sock, para):
        '''
        调用order函数
        :param sock:
        :param para:
        :return:
        '''
        money = 0
        for food in para:
            self.cur.callproc(config.order, (self.number_of_order, food, money))
            if money == -1:
                sock.send(config.Dictionary['no'].encode())
                return
            self.cost += money
        config.mutex.acquire()
        for food in para:
            config.cook_food_list.append((self.number_of_table, food, self.number_of_order))
        config.mutex.release()
        sock.send(config.Dictionary['yes'].encode())
        sock.send(str(self.cost).encode())
        print(str(self.number_of_table) + " 完成点餐，点餐如下 >> "
              + str(para) + " 共计 " + str(self.cost) + " 元")
        return

    def Wait(self, sock):
        while True:
            time.sleep(1)
            config.mutex.acquire()
            if len(config.finish_food[self.number_of_table]) != 0:
                food = config.finish_food[self.number_of_table][0]
                sock.send(food.encode())
                del config.finish_food[self.number_of_table][0]
                flag = sock.recv(1024).decode()
                if flag == config.Dictionary['yes']:
                    self.cur.callproc(config.change, (self.number_of_order))
                    config.mutex.release()
                    print(str(self.number_of_table) + " 号桌已完成," + str(self.number_of_order) + " 号订单完成")
                    return
            config.mutex.release()

    def Checkout(self, sock):
        '''
        数据库加钱
        :param sock:
        :return:
        '''
        self.cur.callproc(config.checkout, (self.number_of_table, self.number_of_order, self.cost))
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
                order = config.cook_food_list[0][2]
                sock.send((food + config.Dictionary['eof']).encode())
                self.cur.callproc(config.set_state, (self.name, True, -1, order))
                config.cook_food_list = config.cook_food_list[1:]
                config.mutex.release()

                self.cur.callproc(config.set_state, (self.name, False, -1, order))
                flag = sock.recv(1024).decode()
                if flag == config.Dictionary['yes']:
                    config.mutex.acquire()
                    self.cur.callproc(config.record, (food, order, self.name))
                    print("-* " + str(table) + " 号桌 : " + food + " 已被 " + self.name + " 完成 *-")
                    config.serve_dish_list.append((table, food, order))
                    config.mutex.release()
                    continue
                else:
                    config.mutex.acquire()
                    config.cook_food_list.append((table, food, order))
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
                order = config.cook_food_list[0][2]
                sock.send((food + config.Dictionary['eof']).encode())
                self.cur.callproc(config.set_state, (self.name, True, table, -1))
                config.serve_dish_list = config.serve_dish_list[1:]
                config.mutex.release()

                self.cur.callproc(config.set_state, (self.name, False, table, -1))
                flag = sock.recv(1024).decode()
                if flag == config.Dictionary['yes']:
                    config.mutex.acquire()
                    self.cur.callproc(config.record, (food, order, self.name))
                    print("-* " + str(table) + " 号桌 : " + food + " 已被 " + self.name + " 上菜 *-")
                    config.finish_food[table].append(food)
                    config.mutex.release()
                    continue
                else:
                    config.mutex.acquire()
                    config.serve_dish_list.append((table, food, order))
                    config.mutex.release()
                    print("Waiter down ! Error !")
            else:
                config.mutex.release()
            time.sleep(1)
        return

    def Fire(self, sock, para):
        username = para
        self.cur.callproc(config.fire, (username))
        print(username + " 已解雇")
        sock.send(config.Dictionary['yes'].encode())
        config.mutex.acquire()
        for cooker in config.cooker_list:
            if cooker.name == username:
                config.cooker_list.remove(cooker)
                break
        config.mutex.release()
        return

