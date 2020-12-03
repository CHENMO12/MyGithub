-- bb
select sum(fsell_amount),sum(fcost_amount),sum(freal_gmv),sum(freal_profit) from t_dws_order_report where fsource_type = 1 and fpay_time >= '2020-11-01'  and fpay_time <= '2020-11-10';

select sum(fsell_amount),sum(fcost_amount),sum(freal_gmv),sum(freal_profit) from t_dws_order_report where fsource_type = 1 and fpay_time >= '2020-10-01' and fpay_time <= '2020-10-31';


select sum(fsell_amount),sum(fcost_amount),sum(freal_gmv),sum(freal_profit) from t_dws_order_detail where fsource_type = 1 and fpay_time >= '2020-10-01' and fpay_time <= '2020-10-31';


select sum(fsell_amount),sum(fcost_amount),sum(freal_gmv),sum(freal_profit) from t_dws_order_detail where fsource_type = 1 and fpay_time >= '2020-11-01';

-- bbc
select sum(fsell_amount),sum(fcost_amount),sum(freal_gmv),sum(freal_profit) from t_dws_order_report where fsource_type = 4 and fpay_time >= '2020-11-01'  and fpay_time <= '2020-11-16';

select sum(fsell_amount),sum(fcost_amount),sum(freal_gmv),sum(freal_profit) from t_dws_order_detail where fsource_type = 4 and fpay_time >= '2020-11-01' and fpay_time <= '2020-11-16';

select sum(fsell_amount),sum(fcost_amount),sum(freal_gmv),sum(freal_profit) from t_dws_order_report where fsource_type = 4 and fpay_time >= '2020-10-01' and fpay_time <= '2020-10-31';

select sum(fsell_amount),sum(fcost_amount),sum(freal_gmv),sum(freal_profit) from t_dws_order_detail where fsource_type = 4 and fpay_time >= '2020-10-01' and fpay_time <= '2020-10-31';

select sum(fsell_amount),sum(fcost_amount),sum(freal_gmv),sum(freal_profit) from t_dws_order_detail where fsource_type = 4 and fpay_time >= '2020-10-01' and fpay_time <= '2020-10-31';

-- 合计
select sum(fsell_amount),sum(fcost_amount),sum(freal_gmv),sum(freal_profit) from t_dws_order_report where  fpay_time >= '2020-11-01'  and fpay_time <= '2020-11-12';


select sum(fsell_amount),sum(fcost_amount),sum(freal_gmv),sum(freal_profit) from t_dws_order_detail where fpay_time >= '2020-11-01' and fpay_time <= '2020-11-12';


select sum(fsell_amount),sum(fcost_amount),sum(freal_gmv),sum(freal_profit) from t_dws_order_detail where  fpay_time >= '2020-10-01' and fpay_time <= '2020-10-31';


select sum(fsell_amount),sum(fcost_amount),sum(freal_gmv),sum(freal_profit) from t_dws_order_detail where fpay_time >= '2020-10-01' and fpay_time <= '2020-10-31';