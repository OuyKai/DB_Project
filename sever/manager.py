import restaurant
import config
import time
import random

def get_command(sock):
    command = sock.recv(1024).decode()
    return command

def get_para(sock):
    msg = ''
    while True:
        data = sock.recv(1024)
        if data[-4:].decode() == config.Dictionary['eof']:
            msg += data[:-4].decode()
            break
        else:
            msg += data.decode()
    para = msg.strip().split()
    return para

def manager_work(sock, temp):
    while True:
        command = get_command(sock)
        para = get_para(sock)
        if command == config.Dictionary['login']:
            temp.Login(sock, para)
        elif command == config.Dictionary['employ']:
            temp.Sign_up(sock, para)
        elif command == config.Dictionary['order']:
            temp.Order(sock, para)
        elif command == config.Dictionary['checkout']:
            temp.checkout(sock, para)
        elif command == config.Dictionary['payoff']:
            temp.Payoff(sock, para)
        elif command == config.Dictionary['quit']:
            return
        else: print("Error command : " + str(command))

def manager(sock, address):
    temp = restaurant.Restaurant()
    try:
        print('连接建立: source address %s:%s' % address)
        role = sock.recv(1024).decode()
        if role == "customer":
            if 0 not in config.table or len(config.waiter_list) == 0 or len(config.cooker_list) == 0:
                print("No seat or no employee, Please wait")
            while True:         # 等到有桌子有人的时候才让他进来
                time.sleep(1)
                if 0 in config.table and len(config.cooker_list) != 0 and len(config.waiter_list) != 0:
                    break

            size_of_waiter = len(config.waiter_list)
            temp.number_of_waiter = random.randint(0, size_of_waiter - 1)
            temp.number_of_table = config.table.index(0)

            config.mutex.acquire()
            config.table[temp.number_of_table] = 1
            config.waiter_list[temp.number_of_waiter].table.append(temp.number_of_table)
            config.mutex.release()

            sock.send(temp.number_of_table)

            manager_work(sock, temp)

            config.mutex.acquire()
            config.table[temp.number_of_table] = 0
            config.waiter_list[temp.number_of_waiter].table.remove(temp.number_of_table)
            config.mutex.release()

        elif role == "waiter":
            config.mutex.acquire()
            config.waiter_list.append(temp)
            config.mutex.release()

            manager_work(sock, temp)

            config.mutex.acquire()
            config.waiter_list.remove(temp)
            config.mutex.release()

        elif role == "cooker":
            config.mutex.acquire()
            config.cooker_list.append(temp)
            config.mutex.release()

            manager_work(sock, temp)

            config.mutex.acquire()
            config.cooker_list.remove(temp)
            config.mutex.release()

    except:
        print('连接终止: source: %s:%s' % address)
        print('==================================================')

    sock.close()
    return