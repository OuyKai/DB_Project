
create procedure sign_up(IN username char(16), IN my_password char(16), IN this_position varchar(16), OUT is_signUp bool)

create procedure enter_restaurant(OUT my_table_id int, OUt my_order_id int)
#返回桌号和订单号，如果没有位置，均返回-1

create procedure order_food(IN my_order_id int, IN my_food_name char(16),OUT my_price int)
#输入订单号、菜名，输出为价格（-1表示不能点此菜，>=0为这个菜的价格）

create procedure check_order_state(IN my_order_id int, OUT is_finished bool)

create procedure record_worker(IN this_food_names varchar(16),IN this_table_id int, IN this_worker_name varchar(16))

create procedure change_order_state(IN my_order_id int)

create procedure dismiss_worker(IN this_worker_name varchar(16),OUT is_available bool)

create procedure show_menu()