select 
	sum(Fsku_total_amount) '销售GMV',
	sum(fcost_amount) '采购GMV',
	sum(fcost_real_amount) '已发货采购GMV',
	sum(Fsku_total_amount - ifnull(faftersale_user_amount, 0) - ifnull(fuser_aftersale_work_amonut,0) ) '实际GMV',
	sum(fcost_real_amount - ifnull(faftersale_supplier_amount, 0) - ifnull(fsupplier_work_amount, 0) - ifnull(fsupplier_aftersale_work_amount, 0)) '实际成本',
	sum(faftersale_user_amount) '售后退客户金额',	
	sum(faftersale_supplier_amount) '售后供应商退我司金额',	
	sum(fsupplier_aftersale_work_amount) '售后供应商调整金额',	
	sum(fuser_aftersale_work_amonut) '售后工单用户调整金额',	
	sum(fuser_recharge_amount) '用户充值金额',
	sum(fsupplier_work_amount) '供应商调整金额'	
from (
	select 
		o.forder_payment_id,
		o.forder_id,
		o.fsku_amount,
		ifnull(so.Fsku_total_amount, 0) Fsku_total_amount,
		so.fdiscount_amount,
		if(co.fdelivery_status = 0, 0, if(so.folder_impairment_price > 0, so.folder_impairment_price * co.fship_num, co.fcost_amount)) fcost_amount,
		co.fcost_real_amount,
		if(co.forder_id is null, 0, oa.faftersale_user_amount) faftersale_user_amount,
		if(co.forder_id is null, 0, oa.faftersale_supplier_amount) faftersale_supplier_amount,
		oa.fsupplier_aftersale_work_amount,
		oa.fuser_aftersale_work_amonut,
		uk.fuser_recharge_amount,
		sk.fsupplier_work_amount,		
		if(co.forder_id is not null, 1, 0) co_id
	from t_bbc_order o
	left join ( -- 销售
		select 
			os.forder_id,
			sum(IF(op.fchannel_order_type is null or op.fchannel_order_type = 0 , ifnull(os.fdiscount_amount, 0 ),0)) fdiscount_amount,
			sum(ifnull(os.fsku_amount, 0) + ifnull(os.ffreight_amount, 0) - IF(op.fchannel_order_type is null or op.fchannel_order_type = 0 , ifnull(os.fdiscount_amount, 0 ), 0)) AS 'Fsku_total_amount'
		from t_bbc_order_sku os
		left join t_bbc_order o on o.forder_id = os.forder_id
		left join t_bbc_order_payment op on o.forder_payment_id = op.forder_payment_id
		GROUP BY os.forder_id
	) so on so.forder_id = o.forder_id
	left join ( -- 采购
		select 
			forder_id,
			sum(fcost_amount) fcost_amount,
			sum(fship_num) fship_num,
			max(if(fdelivery_time is null, 0, 1)) fdelivery_status,
			sum(if(fdelivery_time is null, 0, fcost_amount)) fcost_real_amount
		from (
			select 
				co.forder_id,
				co.fsupplier_order_id,
				sku.fship_num,
				(sku.fcost_amount + co.freal_freight_amount) fcost_amount,
				co.fcreate_time,
				sto.fdelivery_time
			from t_bbc_supplier_order co
			left join (
				select 
					fsupplier_order_id,
					sum(fship_num) fship_num,
					sum(fship_num * if(fpackage_total_cost is not null , fpackage_total_cost, fsku_price)) fcost_amount
				from t_bbc_supplier_order_sku os
				LEFT JOIN (
					select 
						bor.fsupplier_sku_batch_id,
						bor.fbatch_package,
						fpackage_total_cost
					from league.t_bbc_sku_batch_old_record bor
					INNER JOIN (
						select max(fcreate_time) fcreate_time, fsupplier_sku_batch_id,fbatch_package
						from league.t_bbc_sku_batch_old_record
						group by fsupplier_sku_batch_id,fbatch_package
					) r on r.fcreate_time = bor.fcreate_time and  r.fsupplier_sku_batch_id = bor.fsupplier_sku_batch_id and r.fbatch_package = bor.fbatch_package
        ) bor on bor.fsupplier_sku_batch_id = os.fbatch_id and  bor.fbatch_package = os.fbatch_package_num
				group by fsupplier_order_id
			) sku on sku.fsupplier_order_id = co.fsupplier_order_id
			left join (
				select 
					fsupplier_order_id,max(fdelivery_time) fdelivery_time
				from 	t_bbc_supplier_transport_order
				where fstaus >= 2
				GROUP BY fsupplier_order_id
			) sto on sto.fsupplier_order_id = co.fsupplier_order_id
			where co.fstatus not in (4,5)
		) t
		GROUP BY forder_id
	) co on co.forder_id = o.forder_id
	left join ( --  售后,售后工单		
		select 
			oa.forder_id,
			sum(faftersale_total_amount) faftersale_user_amount,
			sum(fsupplier_drawback_amount) faftersale_supplier_amount,		
			sum(uk.fuser_aftersale_work_amonut) fuser_aftersale_work_amonut,
			sum(sk.fsupplier_aftersale_work_amount) fsupplier_aftersale_work_amount			
		from t_bbc_order_aftersale oa
		left join t_bbc_order_aftersale_adjust oaa on oa.forder_aftersale_id = oaa.forder_aftersale_id
		left join (
			select 
				forder_aftersale_id,(fapply_amount) fuser_aftersale_work_amonut
			from t_bbc_user_work
			where fstatus = 2 
			GROUP BY forder_aftersale_id
		) uk on uk.forder_aftersale_id = oa.forder_aftersale_id
		left join (
			select 
				forder_aftersale_id,(fapply_amount) fsupplier_aftersale_work_amount
			from t_bbc_supplier_work
			where fstatus = 2
			GROUP BY forder_aftersale_id
		) sk  on sk.forder_aftersale_id = oa.forder_aftersale_id
		-- where oa.fcheck_time > '1970-01-01 00:00:00'
		where oa.faftersale_status = 8
		group by oa.forder_id
	) oa on oa.forder_id = o.forder_id
	left join (
		select forder_id, sum(fapply_amount) fuser_recharge_amount
		from 	t_bbc_user_work 
		where fstatus = 2  and fwork_type = 2
		group by forder_id
	) uk on uk.forder_id = o.forder_id
	left join (
		select  
			forder_id,
			sum(if(fapply_type = 2, - fapply_amount, fapply_amount)) fsupplier_work_amount
		from  t_bbc_supplier_work
		where fstatus = 2 and fwork_type = 2
		GROUP BY forder_id
	) sk on sk.forder_id = o.forder_id
	left join league.t_bbc_order_payment op on o.forder_payment_id = op.forder_payment_id
	left join t_bbc_user u on op.fuid = u.fuid
	left join t_bbc_channel_account ca on ca.fchannel_id = op.fchannel_id
	where op.fpay_time >= '2020-10-01 00:00:00' and fpay_time <= '2020-10-31 23:59:59'  and (u.funame not in ('18575598014','YW123456','xingyunlianmeng') or ca.fchannel_account_id not in ('18575598014','YW123456','xingyunlianmeng'))
) t
-- group by forder_id
-- order by forder_id;



