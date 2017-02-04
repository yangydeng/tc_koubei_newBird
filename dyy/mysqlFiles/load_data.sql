use tc_koubei;


load data infile 'H://tc_koubei_newBird//dyy//csv//count_user_pay.csv'
into table count_user_pay
fields terminated by ','
optionally enclosed by '"'
lines terminated by '\n';



