select 
	t.forder_id,
	t.fsku_code,
	t.fbatch_package_num,
	t.Fsku_total_amount,
	tt.Fsku_total_amount,
	t.freal_cost_amount,
	tt.freal_cost_amount,
	t.fdelivery_status,
	tt.fdelivery_status,
	t.ftransport_status,
	tt.ftransport_status,
	t.fship_num,
	tt.fship_num,
	t.fsku_price,
	tt.fsku_price,
	t.Fcost_price,
	tt.Fcost_price
from (
	select 
			os.forder_id,
			os.fsku_code,
			os.fbatch_id,
			os.fbatch_package_id,
			os.fbatch_package_num,
			if(co.fdelivery_status = 0 or co.fdelivery_status is null, 0, 1) fdelivery_status,
			co.ftransport_status,
			co.fship_num,
			co.fsku_price fcost_price,
			if(co.fdelivery_status = 0 or co.fdelivery_status is null, 0, if(os.folder_impairment_price > 0, os.folder_impairment_price, co.fsku_price)) fsku_price,
			ifnull(os.fsku_amount, 0) + ifnull(os.ffreight_amount, 0) - IF(op.fchannel_order_type is null or op.fchannel_order_type = 0 , ifnull(os.fdiscount_amount, 0 ), 0) AS 'Fsku_total_amount',
			ifnull(if(co.fdelivery_status = 0 or co.fdelivery_status is null, 0, if(os.folder_impairment_price > 0, os.folder_impairment_price, co.fsku_price) * co.fship_num),0) freal_cost_amount
	from league.t_bbc_order_sku os	
	left join league.t_bbc_order o on o.forder_id = os.forder_id
	left join league.t_bbc_order_payment op on o.forder_payment_id = op.forder_payment_id	
	left join (
		select 
				co.forder_id,
				os.fsupplier_order_id,
				os.fbatch_id,
				os.fsku_code,
				os.fbatch_package_id,
				os.fbatch_package_num,					
				os.fship_num,				
				os.fsku_price,
-- 				if(fpackage_total_cost is not null , fpackage_total_cost, fsku_price) fsku_price,
				if(fdelivery_time is null, 0, 1) fdelivery_status,
				sto.ftransport_status
			from league.t_bbc_supplier_order_sku os
			left join league.t_bbc_supplier_order co on co.fsupplier_order_id = os.fsupplier_order_id
-- 			LEFT JOIN (
-- 				select 
-- 					bor.fsupplier_sku_batch_id,
-- 					bor.fbatch_package,
-- 					fpackage_total_cost
-- 				from league.t_bbc_sku_batch_old_record bor
-- 				INNER JOIN (
-- 					select max(fcreate_time) fcreate_time, fsupplier_sku_batch_id,fbatch_package
-- 					from league.t_bbc_sku_batch_old_record
-- 					group by fsupplier_sku_batch_id,fbatch_package
-- 				) r on r.fcreate_time = bor.fcreate_time and  r.fsupplier_sku_batch_id = bor.fsupplier_sku_batch_id and r.fbatch_package = bor.fbatch_package
-- 			) bor on bor.fsupplier_sku_batch_id = os.fbatch_id and  bor.fbatch_package = os.fbatch_package_num
			left join (
				select 
					fsupplier_order_id,
					max(fstaus) ftransport_status,
					max(fdelivery_time) fdelivery_time
				from 	league.t_bbc_supplier_transport_order
				where fstaus >= 2
				GROUP BY fsupplier_order_id
			) sto on sto.fsupplier_order_id = co.fsupplier_order_id
			where co.fstatus not in(4,5)
	) co on co.forder_id = o.forder_id and co.fsku_code = os.fsku_code and co.fbatch_package_num = os.fbatch_package_num		
	left join league.t_bbc_user u on op.fuid = u.fuid
	left join league.t_bbc_channel ca on ca.fchannel_id = op.fchannel_id		
	where  (u.funame not in ('18575598014','YW123456','xingyunlianmeng') or ca.fchannel_account not in ('18575598014','YW123456','xingyunlianmeng')) and op.fpay_time >= '2020-11-01 00:00:00' and fpay_time <= '2020-11-15 23:59:59' 
) t
left join (	
	select						
			so.forder_id,
			so.forder_payment_id,
			so.finternational_code finternational_code,
			so.fsku_code,   
			so.fbatch_id,
			so.fbatch_package_num,
			so.fpay_time,  					
			ifnull(co.fdelivery_status, 0) fdelivery_status,
			co.ftransport_status,
			co.fship_num,
			so.fsku_num fsku_num ,
			so.forder_total_amount Fsku_total_amount,
			co.fpurchase_sku_price Fcost_price,
			if(co.fdelivery_status is null or co.fdelivery_status= 0, 0, if(so.folder_impairment_price > 0, so.folder_impairment_price, co.fpurchase_sku_price)) fsku_price,
			ifnull(if(co.fdelivery_status is null or co.fdelivery_status= 0, 0, if(so.folder_impairment_price > 0, so.folder_impairment_price, co.fpurchase_sku_price) *  co.fship_num), 0) freal_cost_amount
		from t_dws_bbc_fourth_sell_order so
		left join (
			select
				sum(co.fship_num) fship_num,
				co.fpurchase_sku_price fpurchase_sku_price,
				co.fpurchase_freight_amount fpurchase_freight_amount,
				if(max(spo.fdelivery_time) is null, 0, 1) fdelivery_status,
				max(spo.ftransport_status) ftransport_status,
				co.fcooperation_type,			
				co.fsupplier_sku_id,
				co.forder_id forder_id,
				co.fsku_code,
				max(co.fsupplier_id) fsupplier_id,
				co.fbatch_package_num,
				co.fbatch_id
			from t_dws_bbc_fourth_cost_order co						
			left join (
						select
							forder_id,
							fbatch_id,
							fsku_code,
							fbatch_package_num,
							ftransport_status,
							fdelivery_time
						from t_dwd_bbc_transport_order
						where ftransport_status >= 2
						group by forder_id,fbatch_id,fsku_code,fbatch_package_num
				) spo on co.fbatch_id = spo.fbatch_id and  co.forder_id = spo.forder_id and co.fsku_code=spo.fsku_code and co.fbatch_package_num = spo.fbatch_package_num
				where co.fstatus != 4
				group  by co.forder_id, co.fsku_code, co.fbatch_package_num, co.fbatch_id
		) co on co.forder_id=so.forder_id and co.fsku_code = so.fsku_code and co.fbatch_package_num =so.fbatch_package_num 
		where so.funame not in ('18575598014','YW123456','xingyunlianmeng')  and  so.fpay_time >= '2020-11-01 00:00:00' and so.fpay_time <= '2020-11-15 23:59:59' 
)tt on t.forder_id = tt.forder_id and t.fsku_code = tt.fsku_code and t.fbatch_package_num = tt.fbatch_package_num 
where tt.forder_id is null or t.freal_cost_amount <> tt.freal_cost_amount;
		
		
		