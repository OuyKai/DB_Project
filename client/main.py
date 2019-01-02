
import socket
import config
from customer import customer
from employee import boss, cooker, waiter
import os


def help():
    print('if you are boss, please input "boss".')
    print('if you are cooker, please input "cooker".')
    print('if you are waiter, please input "waiter".')
    print('if you are customer, please input "customer".')
    print('quit: close the connection and quit.')
    return


def main_cycle():
    os.system('cls')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # print(config.ip_address)
        sock.connect((config.ip_address, config.ip_port))
    except:
        print("sever is busy, please connect later")
        return
    print('Welcome to use the client(input help for help)')
    while True:
        role = input("Please input who are you >>> ")
        if role == 'boss':
            boss(sock)
        elif role == 'cooker':
            cooker(sock)
        elif role == 'waiter':
            waiter(sock)
        elif role == 'customer':
            customer(sock )
        elif role == 'help':
            help()
        elif role == 'quit':
            sock.send(b'1111')
            sock.close()
            break
        else:
            print('wrong command, please input again.')
    print('The client has been logged out.')
    return


if __name__ == "__main__":
    main_cycle()


