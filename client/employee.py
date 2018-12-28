from enum import Enum
import config
import os
import random
import time

def get_command(sock):
    command = sock.recv(1024).decode()
    print("接收指令为 >> " + str(command))
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
    print("接收参数为 >> " + str(para))
    return para

class Job(Enum):
    boss = "boss"
    waiter = "waiter"
    cooker = "cooker"

class Employee():
    def __init__(self, job):
        self.job = job
        self.time = random.randint(1, 20)
        return

    def Login(self, sock, username, password):
        sock.send(config.Dictionary['login'].encode())
        sock.send((username + ' ' + password + config.Dictionary['eof']).encode())
        flag = sock.recv(1024).decode()
        if flag == config.Dictionary['yes']:
            print("Login successfully !")
            return True
        else:
            print("Login failed !")
            return False


    def Employ(self, sock):
        username = input("Please input username >>> ")
        password = input("Please input password >>> ")
        sock.send(config.Dictionary['sign_up'].encode())
        sock.send((username + ' ' + password + config.Dictionary['eof']).encode())
        flag = sock.recv(1024).decode()
        if flag == config.Dictionary['yes']:
            print("Employ successfully !")
            return True
        else:
            print("Employ failed !")
            return False


    def Fire(self, sock):
        username = input("Please input the username you want to fire >>> ")
        sock.send(config.Dictionary['sign_up'].encode())
        sock.send((username + config.Dictionary['eof']).encode())
        flag = sock.recv(1024).decode()
        if flag == config.Dictionary['yes']:
            print("Fire successfully !")
            return True
        else:
            print("Fire failed !")
            return False

    def Cook(self, sock, para):
        '''
        cooker cooking

        :return:
        '''
        time.sleep(self.time)
        print("cook finish")
        print(para)
        sock.send(config.Dictionary['yes'].encode())
        return

    def Serve(self, sock, para):
        time.sleep(self.time)
        print("sever dish")
        print(para)
        sock.send(config.Dictionary['yes'].encode())
        return

    def Payoff(self, sock):
        return


def boss(sock):
    os.system('cls')
    sock.send("boss".encode())
    temp = Employee(Job.boss)

    print("Please login first(input back to return)")
    while True:
        username = input("username(or back) >>> ")
        if username == "back":
            return
        password = input("password >>> ")
        if temp.Login(sock, username, password):
            print('Welcome to use the client(input help for help)')
            while True:
                operation = input("Please input what you want >>> ")
                if operation == 'payoff':
                    temp.Payoff(sock)
                elif operation == 'employ':
                    temp.Employ(sock)
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
    sock.send(config.Dictionary['working'].encode())
    sock.send(config.Dictionary['eof'].encode())
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

    print("Please login first(input back to return)")
    while True:
        username = input("username(or back) >>> ")
        if username == "back":
            return
        password = input("password >>> ")
        if temp.Login(sock, username, password):
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
    sock.send(config.Dictionary['working'].encode())
    sock.send(config.Dictionary['eof'].encode())
    while True:
        command = get_command(sock)
        para = get_para(sock)
        if command == config.Dictionary['serve']:
            waiter.serve(para)
            sock.send(config.Dictionary['yes'].encode())
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

    print("Please login first(input back to return)")
    while True:
        username = input("username(or back) >>> ")
        if username == "back":
            return
        password = input("password >>> ")
        if temp.Login(sock, username, password):
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
