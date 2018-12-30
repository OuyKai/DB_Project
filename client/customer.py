import os
import config
import time
import random

class Customer():
    def __init__(self):
        self.table = 0
        self.order = []
        self.food = []
        self.cost = 0
        self.time = random.randint(1, 20)
        return

    def Order(self, sock):
        '''
        after think of menu
        call restaurant.order

        :return:
        '''
        order = []
        food_name = input("Please input food name(input over to stop) >>> ")
        while food_name != "over":
            order.append(food_name)
            food_name = input("Please input food name >>> ")
        menu = ""
        for food in order:
            menu += (food + " ")
        sock.send(config.Dictionary['order'].encode())
        sock.send((menu + config.Dictionary['eof']).encode())
        flag = sock.recv(1024).decode()
        if flag == config.Dictionary['yes']:
            self.cost = sock.recv(1024).decode()
            for food in order:
                self.order.append(food)
            print(str(self.table) + " 完成点餐，点餐如下 >> "
                  + menu + " 共计 " + str(self.cost) + " 元")
            return True
        return False

    def Wait(self, sock):
        sock.send(config.Dictionary['wait'].encode())
        sock.send(config.Dictionary['eof'].encode())
        while True:
            food = sock.recv(1024).decode()
            print(food + " 已完成，请慢用")
            self.food.append(food)
            if len(self.food) != len(self.order):
                sock.send(config.Dictionary['no'].encode())
            else:
                sock.send(config.Dictionary['yes'].encode())
                return

    def Eat(self):
        '''
        eat food

        :return:
        '''
        time.sleep(self.time * len(self.order))
        return

    def Checkout(self, sock):
        '''
        checkout

        :return:
        '''
        sock.send(config.Dictionary['checkout'].encode())
        sock.send(config.Dictionary['eof'].encode())
        flag = sock.recv(1024).decode()
        if flag == config.Dictionary['yes']:
            return True
        return False

def customer(sock):
    os.system('cls')
    sock.send("customer".encode())

    len_of_food_menu = int(sock.recv(1024).decode())
    for i in range(len_of_food_menu):
        food = sock.recv(1024).decode()
        config.food_menu.append(food)

    temp = Customer()
    flag = sock.recv(1024).decode()
    if flag == config.Dictionary['no']:
        print("No seat or no employee, Please wait...")
        temp.table = int(sock.recv(1024).decode())
    else:
        temp.table = int(flag)

    print('Welcome to use the client(input help for help)')
    while True:
        operation = input("Please input what you want >>> ")
        if operation == 'order':
            if temp.Order(sock):
                print("Order successfully !")
                temp.Wait(sock)
                # temp.Eat()
            else:
                print("Failed")
        elif operation == 'checkout':
            if temp.Checkout(sock):
                print("checkout successfully !")
            else:
                print("Error")
        elif operation == 'help':
            print('order: order what food you want.')
            print('checkout: checkout when you want to leave.')
            print('back: back to last window.')
        elif operation == 'back':
            return
        else:
            print('wrong command, please input again.')
