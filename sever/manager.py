import restaurant
import config
import time

def get_command(sock):
    command = sock.recv(4).decode()
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
            restaurant.Login(sock, para, temp)
        elif command == config.Dictionary['employ']:
            restaurant.Sign_up(sock, para, temp)
        elif command == config.Dictionary['order']:
            restaurant.Order(sock, para, temp)
        elif command == config.Dictionary['checkout']:
            restaurant.checkout(sock, para, temp)
        elif command == config.Dictionary['payoff']:
            restaurant.Payoff(sock, para, temp)
        elif command == config.Dictionary['quit']:
            return
        else: print("Error command : " + str(command))

def manager(sock, address):
    temp = restaurant.Restaurant()
    try:
        print('连接建立: source address %s:%s' % address)
        role = sock.recv(1024).decode()
        if role == "customer":
            if 0 not in config.table:
                print("No seat, Please wait")
            while True:
                time.sleep(1)
                if 0 in config.table:
                    break
            temp.number = config.table.index(0)

            config.mutex.acquire()
            config.table[temp.number] = 1
            config.mutex.release()

            sock.send(temp.number)
            print("There is a free seat >>> " + str(temp.number))
        elif role == "waiter":
            config.mutex.acquire()
            config.waiter_list.append(0)
            config.mutex.release()
        elif role == "cooker":
            config.mutex.acquire()
            config.cooker_list.append(0)
            config.mutex.release()
        manager_work(sock, temp)
    except:
        print('连接终止: source: %s:%s' % address)
        print('==================================================')
    if temp.number != -1:
        config.mutex.acquire()
        config.table[temp.number] = 1
        config.mutex.release()
    return