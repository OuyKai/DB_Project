import pymysql
from sever import config

con = pymysql.connect(
    host=config.ip_address,
    port=config.db_port,
    user=config.customer_name,
    password=config.customer_password,
    db=config.db_name
)
customer_cur = con.cursor()

customer_cur.execute('call ' + config.enter + '(@a, @b);')
customer_cur.execute('select @a, @b;')
temp = customer_cur.fetchaone()
number_of_table = temp[0]
number_of_order = temp[1]
print(number_of_table, number_of_order)
