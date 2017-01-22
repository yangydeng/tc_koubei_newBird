select shop_id,count(*) as count from user_pay where time_stamp>='2016-10-30 00:00:00' and time_stamp<='2016-10-30 23:59:59' group by 
shop_id order by shop_id;