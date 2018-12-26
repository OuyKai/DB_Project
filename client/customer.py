from enum import Enum
import os
import config
import time

class State(Enum):
    waiting = "waiting"
    consuming = "consuming"

class Customer():
    def __init__(self):
        self.table = 0
        self.order = []
        self.cost = 0
        self.time = 0
        self.state = State.waiting
        return

    def Order(self, sock):
        '''
        after think of menu
        call restaurant.order

        :return:
        '''
        food_name = input("Please input what your want >>> ")
        self.order.append(food_name)
        while food_name != "over":
            food_name = input("Please input what your want >>> ")
            self.order.append(food_name)
        menu = ""
        for food in self.order:
            menu += (food + " ")
        sock.send(menu)
        flag = sock.recv(1024).decode()
        if flag == config.Dictionary['yes']:
            self.cost = sock.recv(1024).decode()
            self.Eat()
            return True
        return False

    def Eat(self):
        '''
        eat food

        :return:
        '''
        time.sleep(10)
        return

    def Checkout(self, sock):
        '''
        checkout

        :return:
        '''
        sock.send(config.Dictionary['checkout'])
        sock.send(str(self.cost))
        flag = sock.recv(1024).decode()
        if flag == config.Dictionary['yes']:
            return True
        return False

def customer(sock):
    os.system('cls')
    sock.send("customer".encode())
    temp = Customer()
    temp.table = sock.recv(1024).decode()

    print('Welcome to use the client(input help for help)')
    while True:
        operation = input("Please input what you want >>> ")
        if operation == 'order':
            temp.Order(sock)
        elif operation == 'checkout':
            temp.Checkout(sock)
        elif operation == 'help':
            print('order: order what food you want.')
            print('checkout: checkout when you want to leave.')
            print('back: back to last window.')
        elif operation == 'back':
            return
        else:
            print('wrong command, please input again.')
