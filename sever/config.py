import threading

mutex = threading.Lock()

Dictionary = {
    'request': '0000', # 顾客请求manager
    'order': '0001', # 顾客点单
    'checkout': '0010', # 结账
    'start': '0011',
    'cook': '0100',
    'payoff': '0101', # 发工资
    'sign_up': '0110', # 注册
    'login': '0111', # 登录
    'fire': '1000', # 解雇
    'working': '1101', # 工作
    'eof': '1100',
    'yes': '1101',
    'no': '1110',
    'quit': '1111', # 退出
}

ip_address = '127.0.0.1'
ip_port = 10086
db_name = 'MY_RESTAURANT'

listen_limit = 10
table = [0] * listen_limit

waiter_salary = []
cooker_salary = []

sign_up = "sign_up"

serve_dish_list = []
cook_food_list = []