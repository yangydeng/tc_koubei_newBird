use tc_koubei;


load data infile 'H:\\tianchi\\raw_data\\dataset\\user_view.txt'
into table user_view
fields terminated by ','
optionally enclosed by '"'
lines terminated by '\n';

