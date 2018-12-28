import threading

mutex = threading.Lock()

Dictionary = {
    'request': '0000', # 顾客请求manager
    'order': '0001', # 顾客点单
    'checkout': '0010', # 结账
    'employ': '0011',
    'cook': '0100',
    'payoff': '0101', # 发工资
    'sign_up': '0110', # 注册
    'login': '0111', # 登录
    'fire': '1000', # 解雇
    'working': '1001', # 工作
    'wait': '1010',
    'eof': '1100',
    'yes': '1101',
    'no': '1110',
    'quit': '1111', # 退出
}

ip_address = '172.18.34.38'
ip_port = 10086
db_port = 3306
db_name = 'MY_RESTAURANT'

listen_limit = 10
table = [0] * listen_limit

waiter_salary = []
cooker_salary = []

sign_up = "sign_up"

cook_food_list = []
serve_dish_list = []
finish_food = [[]] * listen_limit

waiter_list = []
cooker_list = []