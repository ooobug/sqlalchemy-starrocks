show databases;
show tables in test;
describe test.test_date;
select * from test.test_date;
select `year` as yr, `tag`, count(`year`) as yr_cnt from test.test_date where `month` <= month(now()) group by `year`,`tag`;
