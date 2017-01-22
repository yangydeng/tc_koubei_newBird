drop procedure if exists count_user_pay;

delimiter //
create procedure count_user_pay(in _day int(10),in out_day int(10))
begin
	
	
	declare year_and_month varchar(10) default '2016-10-';
    
    declare time_start varchar(10) default ' 00:00:00';
    declare time_end varchar(10) default ' 23:59:59';
    
    loop_label: loop

    
    
    select shop_id,count(user_id) as count_pay from user_pay where time_stamp>= concat(year_and_month,_day,time_start) 
    and time_stamp<=concat(year_and_month,_day,time_end) group by shop_id order by shop_id;
    
    set _day = _day+1;
    if _day> out_day then
    leave loop_label;
    end if;
    
    end loop;
    
    end//
    delimiter ;
call count_user_pay(1,30);



