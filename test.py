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

customer_cur.callproc(config.enter, (number_of_table, number_of_order))
data = customer_cur.fetchall()
print(data)
print(number_of_order, number_of_table)
