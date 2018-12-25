from enum import Enum
import config
import os

def get_command(sock):
    command = sock.recv(4)
    return command

def get_para(sock):
    msg = ''
    while True:
        data = sock.recv(1024)
        if data[-4:].decode() == config.Dictionary['eof']:
            msg += data[:-4]
            break
        else:
            msg += data
    para = msg.strip().split()
    return para

class Job(Enum):
    boss = "boss"
    waiter = "waiter"
    cooker = "cooker"
    reception = "reception"

class Employee():
    def __init__(self, job):
        self.job = job
        return

    def login(self, sock, username, password):
        sock.send(config.Dictionary['login'])
        sock.send(username + ' ' + password)
        flag = sock.recv(4)
        if flag == config.Dictionary['yes']:
            return True
        else:
            return False


    def sign_up(self, sock):
        username = input("Please input your username >>> ")
        password = input("Please input your password >>> ")
        sock.send(config.Dictionary['sign_up'])
        sock.send(username + ' ' + password)
        flag = sock.recv(4)
        if flag == config.Dictionary['yes']:
            return True
        else:
            return False


    def fire(self, sock):
        username = input("Please input the username you want to fire >>> ")
        sock.send(config.Dictionary['sign_up'])
        sock.send(username)
        flag = sock.recv(4)
        if flag == config.Dictionary['yes']:
            return True
        else:
            return False

    def Reception(self, sock):
        '''
        if there have any seat in restaurant
        it is called by restaurant
        :return:
        '''
        return

    def Refused(self, sock):
        '''
        if there have not any seat in restaurant
        it is called by restaurant

        :return:
        '''
        return

    def Order(self, sock):
        '''
        after customer order
        it is called by restaurant

        :return:
        '''
        return

    def Cook(self, sock):
        '''
        cooker cooking

        :return:
        '''
        return

    def Leave(self, sock):
        '''
        resignation

        :return:
        '''
        return

    def Checkout(self, sock):
        '''
        reception checkout

        :return:
        '''
        return

    def Acount(self, sock):
        return


def boss_work(sock, boss):
        return

def boss(sock):
    os.system('cls')
    sock.send("boss".encode())
    temp = Employee(Job.boss)

    print("Please login first(input back")
    while True:
        username = input("username(or back) >>> ")
        if username == "back":
            return
        password = input("password >>> ")
        if temp.login(sock, username, password):
            print('Welcome to use the client(input help for help)')
            while True:
                operation = input("Please input what you want >>> ")
                if operation == 'payoff':
                    print()
                elif operation == 'employ':
                    temp.sign_up(sock)
                elif operation == 'help':
                    print('payoff: check account of restaurant.')
                    print('back: back to last window.')
                elif operation == 'back':
                    return
                else:
                    print('wrong command, please input again.')
        else:
            print("username or password error, please input again")

def cooker_work(sock, cooker):
    sock.send(config.Dictionary['working'])
    while True:
        command = get_command(sock)
        para = get_para(sock)
        if command == config.Dictionary['cook']:
            cooker.Cook(para)
        else:
            print("error command: " + command)

def cooker(sock):
    '''
    查看面板是否有未做的订单
    完成订单

    :param s:
    :return:
    '''
    os.system('cls')
    sock.send("cooker".encode())
    temp = Employee(Job.cooker)

    print("Please login first(input back")

    while True:
        username = input("username(or back) >>> ")
        if username == "back":
            return
        password = input("password >>> ")
        if temp.login(sock, username, password):
            print('Welcome to use the client(input help for help)')
            while True:
                operation = input("Please input what you want >>> ")
                if operation == 'work':
                    cooker_work(sock, temp)
                elif operation == 'help':
                    print('work: check order and finish it.')
                    print('back: back to last window.')
                elif operation == 'back':
                    return
                else:
                    print('wrong command, please input again.')
        else:
            print("username or password error, please input again")

def waiter_work(sock, waiter):
    while True:
        command = get_command(sock)
        para = get_para(sock)
        if command == config.Dictionary['start']:
            waiter.Reception(para)
        elif command == config.Dictionary['order']:
            waiter.Order(para)
        elif command == config.Dictionary['checkout']:
            waiter.Checkout(para)
        else:
            print("error command: " + command)

def waiter(sock):
    '''
    查看面板是否有未服务的顾客
    查看面板是否有未传达的订单
    服务顾客
    传达订单

    :param s:
    :return:
    '''
    os.system('cls')
    sock.send("waiter".encode())
    temp = Employee(Job.waiter)

    print("Please login first(input back")

    while True:
        username = input("username(or back) >>> ")
        if username == "back":
            return
        password = input("password >>> ")
        if temp.login(sock, username, password):
            print('Welcome to use the client(input help for help)')
            while True:
                operation = input("Please input what you want >>> ")
                if operation == 'work':
                    waiter_work(sock, temp)
                elif operation == 'help':
                    print('work: check order and finish it.')
                    print('back: back to last window.')
                elif operation == 'back':
                    return
                else:
                    print('wrong command, please input again.')
        else:
            print("username or password error, please input again")
