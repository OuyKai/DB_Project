import restaurant
import config
import time

def get_command(sock):
    command = sock.recv(1024).decode()
    print("接收指令为 >> " + str(command))
    return command

def get_para(sock):
    msg = ''
    while True:
        data = sock.recv(1024).decode()
        if data[-4:] == config.Dictionary['eof']:
            msg += data[:-4]
            break
        else:
            msg += data
    para = msg.strip().split()
    print("接收参数为 >> " + str(para))
    return para

def manager_work(sock, temp):
    while True:
        command = get_command(sock)
        para = get_para(sock)
        if command == config.Dictionary['login']:
            temp.Login(sock, para)
        elif command == config.Dictionary['employ']:
            temp.Employ(sock, para)
        elif command == config.Dictionary['order']:
            temp.Order(sock, para)
        elif command == config.Dictionary['wait']:
            temp.Wait(sock)
        elif command == config.Dictionary['checkout']:
            temp.Checkout(sock)
        elif command == config.Dictionary['fire']:
            temp.Fire(sock, para)
        elif command == config.Dictionary['show']:
            temp.Show(sock)
        elif command == config.Dictionary['working']:
            if temp.role == "cooker":
                config.mutex.acquire()
                config.cooker_list.append(temp)
                config.mutex.release()
                temp.Cook(sock)
            else:
                config.mutex.acquire()
                config.waiter_list.append(temp)
                config.mutex.release()
                temp.Serve(sock)
        elif command == config.Dictionary['quit']:
            return
        else: print("Error command : " + str(command))

def manager(sock, address):
    temp = restaurant.Restaurant()
    print('连接建立: source address %s:%s' % address)
    role = sock.recv(1024).decode()
    if role == "customer":
        len_of_food_menu = len(config.food_menu)
        sock.send(str(len_of_food_menu).encode())
        for food in config.food_menu:
            sock.send(food.encode())

        if 0 not in config.table or len(config.waiter_list) == 0 or len(config.cooker_list) == 0:
            print("No seat or no employee, Please wait")
            sock.send(config.Dictionary['no'].encode())
        while True:         # 等到有桌子有人的时候才让他进来
            time.sleep(1)
            if 0 in config.table and len(config.cooker_list) != 0 and len(config.waiter_list) != 0:
                if temp.Enter():
                    break

        temp.role = "customer"
        temp.start_time = time.time()

        config.mutex.acquire()
        config.table[temp.number_of_table] = 1
        config.mutex.release()

        sock.send(str(temp.number_of_table).encode())

        manager_work(sock, temp)

        config.mutex.acquire()
        config.table[temp.number_of_table] = 0
        config.mutex.release()

    elif role == "waiter":
        temp.role = "waiter"
        manager_work(sock, temp)

        config.mutex.acquire()
        if temp in config.waiter_list:
            config.waiter_list.remove(temp)
        config.mutex.release()

    elif role == "cooker":
        temp.role = "cooker"
        manager_work(sock, temp)

        config.mutex.acquire()
        if temp in config.cooker_list:
            config.cooker_list.remove(temp)
        config.mutex.release()

    else:
        temp.role = "boss"
        manager_work(sock, temp)

    sock.close()
    return
