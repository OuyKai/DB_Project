import threading

mutex = threading.Lock()

Dictionary = {
    'request': '0000', # 顾客请求manager
    'order': '0001', # 顾客点单
    'checkout': '0010', # 结账
    'employ': '0011',
    'cook': '0100',
    'serve': '0101', # 发工资
    'login': '0111', # 登录
    'fire': '1000', # 解雇
    'working': '1001', # 工作
    'wait': '1010',
    'show': '1011',
    'eof': '1100',
    'yes': '1101',
    'no': '1110',
    'quit': '1111', # 退出
}

ip_address = '172.18.34.38'
ip_port = 10086
db_port = 3306
db_name = 'MY_RESTAURANT'
root_name = 'guest'
root_password = '123456'
customer_name = 'cost'
customer_password = '123456'

listen_limit = 10
table = [0] * listen_limit

waiter_salary = []
cooker_salary = []

sign_up = "sign_up"
enter = "enter_restaurant"
order = "order_food"
change = "change_order_state"
fire = "dismiss_worker"
record = "record_worker"
food = "change_food_state"
checkout = "gain_money"
set_state = "set_worker_state"

cook_food_list = []
serve_dish_list = []
finish_food = [[]] * listen_limit

waiter_list = []
cooker_list = []

food_menu = []
customer_cur = ""