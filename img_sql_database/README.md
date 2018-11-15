https://blog.csdn.net/weixin_40396510/article/details/79277731
主要安装配置过程参照以上的链接，几点注意：
1.我电脑上装的是8.0.2版本，建议统一成一样的，8.0附近的也可以,否则一些语句可能不兼容；
2.配置流程基本一样，但最后设置密码文中是5.7版本，文中的方法有点问题，可以参考文章下面的评论或百度一下报错信息找下解决方法；
3.启动数据库后，像我电脑后面是开机自启服务了，不知道其他电脑会不会一样自启；
4.可以安装一下MySQL Workbench 8.0 可以百度搜索下载，可以界面化地看到你的数据库和数据；
5.import MySQLdb 如果import不成功要安装一下；
6.在sql_setup.py中设置mysql的用户密码等参数，以及你建立的库和表的名称，然后运行sql_setup.py可以配置设定格式的表格
运行正常会显示：
create database flask_sql
database connected
Database version : 8.0.12 
create table ImagesDatabase
(1, 'Allen', '2018-10-19 20:00:00', 'fat', 'e:/img1')
(2, 'Mike', '2018-10-19 20:00:02', 'fat', 'e:/img2')
(3, 'John', '2018-10-19 20:00:04', 'fat', 'e:/img3')
(4, 'Amy', '2018-10-19 20:00:06', 'ventricular', 'e:/img4')
(5, 'James', '2018-10-19 20:00:08', 'brain', 'e:/img5')
database disconnected
7.其他地方程序有 #mysql setup params 的都要设置对应参数
8.可运行sql_test.py 和 image_table_test.py 测试其他功能是否正常
sql_test.py 程序运行输出：
database connected
Database version : 8.0.12 
INSERT INTO ImagesDatabase(User,Time,Type,Path) VALUES('Adams','2018-10-26 11:21:00','fat','E:/1.jpg')
insert done
database committed
database disconnected
database connected
SELECT * FROM ImagesDatabase WHERE Type = 'ventricular'
select ventricular done
read done Amy 2018-10-19 20:00:06 ventricular e:/img4
Amy 2018-10-19 20:00:06 ventricular e:/img4
SELECT * FROM ImagesDatabase WHERE User = 'Mike'
select Mike done
read done Mike 2018-10-19 20:00:02 fat e:/img2
Mike 2018-10-19 20:00:02 fat e:/img2
database disconnected

image_table_test.py 程序运行会输出数据库列表中数据，此处不具体列举