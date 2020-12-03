select
		forder_id,
	 sum(销售金额) '销售GMV',
	 sum(采购金额) '已发货采购GMV',
	 if(fdelivery_status = 0, 0 , sum(实际gmv)) '实际GMV',
	 if(fdelivery_status = 0, 0 , sum(采购金额) - sum(成本调整金额)) '实际成本',
	 if(fdelivery_status = 0, 0 , sum(实际gmv) - sum(采购金额) + sum(成本调整金额)) '毛利',
	 sum(售后订单退客户金额) '售后退客户金额',
	 sum(售后订单供应商退我司金额金额) '售后供应商退我司金额',
	 sum(售后工单用户调整金额) '售后工单用户调整金额',
	 sum(售后工单供应商调整金额) '售后工单供应商调整金额',
	 sum(供应商调整金额) '供应商调整金额'
	from (
		select 
			so.forder_payment_id,
			so.forder_id,
			so.fbatch_id,
			so.fsku_code,
			so.fbatch_package_num,
			so.forder_total_amount '销售金额',
			co.fpurchase_sku_price,
			co.fpurchase_freight_amount,
			ifnull(if(co.fdelivery_status is null or fdelivery_status= 0, 0, if(so.folder_impairment_price > 0, so.folder_impairment_price, co.fpurchase_sku_price) *  co.fship_num + co.fpurchase_freight_amount), 0) '采购金额',
			
			if(co.fdelivery_status is null or fdelivery_status = 0, 0, so.forder_total_amount - ifnull(oa.faftersale_refund_user_amount,0) - ifnull(oa.fuser_aftersale_work_amonut, 0)) '实际gmv',			
			ifnull(oa.faftersale_refund_sup_amount,0) + ifnull(oa.fsupplier_aftersale_work_amount,0) +  ifnull(sk.fwork_sup_amount, 0) '成本调整金额',
			ifnull(oa.faftersale_refund_user_amount,0) '售后订单退客户金额',
			ifnull(oa.faftersale_refund_sup_amount,0) '售后订单供应商退我司金额金额',			
			ifnull(oa.fuser_aftersale_work_amonut,0) '售后工单用户调整金额',		
			ifnull(oa.fsupplier_aftersale_work_amount,0) '售后工单供应商调整金额',			
			ifnull(sk.fwork_sup_amount,0) '供应商调整金额',
			ifnull(co.fdelivery_status, 0) fdelivery_status,
			so.fsku_num			
		from t_dws_bbc_fourth_sell_order so
		left join ( -- 采购
			select 				
				co.forder_id,
				co.fsku_code,
				co.fbatch_package_num,
				co.fbatch_id,
				sum(co.fship_num) fship_num,	
				co.fpurchase_sku_price fpurchase_sku_price,
				co.fpurchase_freight_amount fpurchase_freight_amount,
				if(max(spo.fdelivery_time) is null, 0, 1) fdelivery_status
			from t_dws_bbc_fourth_cost_order co  			
			left join (		
				select 
					forder_id,
					fbatch_id,
					fsku_code,
					fbatch_package_num,
					fdelivery_time
				from t_dws_bbc_fourth_transport_order
				where ftransport_status >= 2
				group by forder_id,fbatch_id,fsku_code,fbatch_package_num	    
			) spo on co.fbatch_id = spo.fbatch_id and  co.forder_id = spo.forder_id and co.fsku_code=spo.fsku_code and co.fbatch_package_num = spo.fbatch_package_num
			where co.fstatus <> 4 
			group by co.forder_id, co.fsku_code,co.fbatch_package_num,co.fbatch_id,co.fship_num		
		) co on co.forder_id=so.forder_id and co.fsku_code = so.fsku_code and co.fbatch_package_num =so.fbatch_package_num and so.fbatch_id = co.fbatch_id
		left join ( --  售后，售后调整
			 select 
				forder_id,
				fbatch_id,
				fbatch_package_num,
				fsku_code,
				sum(faftersale_total_amount) faftersale_refund_user_amount,
				sum(fsupplier_drawback_amount) faftersale_refund_sup_amount,
				sum(fuser_aftersale_work_amonut) fuser_aftersale_work_amonut,
				sum(fsupplier_aftersale_work_amount) fsupplier_aftersale_work_amount
			from (
					select 
						oa.forder_id,
						sku.forder_aftersale_id,
						sku.fsku_code,
						sku.fbatch_id,
						sku.fbatch_package_num,
						CONVERT((t.faftersale_total_amount * if(sku.faftersale_num = 0, 1, sku.faftersale_num) / num), BIGINT) faftersale_total_amount,
						CONVERT((t.fsupplier_drawback_amount * if(sku.faftersale_num = 0, 1, sku.faftersale_num) / num), BIGINT) fsupplier_drawback_amount,
						CONVERT((t.fuser_aftersale_work_amonut * if(sku.faftersale_num = 0, 1, sku.faftersale_num) / num), BIGINT) fuser_aftersale_work_amonut,
						CONVERT((t.fsupplier_aftersale_work_amount * if(sku.faftersale_num = 0, 1, sku.faftersale_num) / num), BIGINT) fsupplier_aftersale_work_amount
					from league.t_bbc_order_aftersale_sku sku
					left join league.t_bbc_order_aftersale oa on oa.forder_aftersale_id = sku.forder_aftersale_id
					left join (	
						select 	
							oa.forder_id,
							oa.forder_aftersale_id,
							max(oaa.faftersale_total_amount) faftersale_total_amount,
							max(oaa.fsupplier_drawback_amount) fsupplier_drawback_amount,
							max(uk.fuser_aftersale_work_amonut) fuser_aftersale_work_amonut,
							max(sk.fsupplier_aftersale_work_amount) fsupplier_aftersale_work_amount,
							if(sum(oas.faftersale_num) = 0, count(oas.forder_aftersale_id), sum(oas.faftersale_num)) num
						from league.t_bbc_order_aftersale_adjust oaa
						left join league.t_bbc_order_aftersale oa on oa.forder_aftersale_id=oaa.forder_aftersale_id
						LEFT JOIN league.t_bbc_order_aftersale_sku oas on oas.forder_aftersale_id = oa.forder_aftersale_id
						left join (
							select 
								forder_aftersale_id,
								sum(fapply_amount) fuser_aftersale_work_amonut
							from league.t_bbc_user_work
							where fstatus = 2 
							GROUP BY forder_aftersale_id
						) uk on uk.forder_aftersale_id = oa.forder_aftersale_id
						left join (
							select 
								forder_aftersale_id,sum(fapply_amount) fsupplier_aftersale_work_amount
							from league.t_bbc_supplier_work
							where fstatus = 2
							GROUP BY forder_aftersale_id
						) sk  on sk.forder_aftersale_id = oa.forder_aftersale_id
						where oa.faftersale_status in(6,7,8)
						GROUP BY oa.forder_id,oa.forder_aftersale_id
					) t on sku.forder_aftersale_id =  t.forder_aftersale_id
			) t			
			GROUP BY forder_id,fbatch_id, fbatch_package_num, fsku_code
		) oa on oa.forder_id = so.forder_id and oa.fbatch_id= so.fbatch_id and oa.fsku_code = so.fsku_code and oa.fbatch_package_num = so.fbatch_package_num
		left join ( -- 供应商调整
			select 
					so.forder_id,
					sku.fsku_code,
					sku.fbatch_id,
					sku.fbatch_package_num,
					CONVERT(sum(t.fsupplier_work_amount * 1 / num), BIGINT) fwork_sup_amount
				from league.t_bbc_supplier_order_sku sku
				left join league.t_bbc_supplier_order so on so.fsupplier_order_id = sku.fsupplier_order_id
				inner join (
						select 	
							oaa.fsupplier_order_id,
							max(sk.fapply_amount) fsupplier_work_amount,
							count(oaa.fsupplier_sku_id) num
						from league.t_bbc_supplier_order_sku oaa
						inner join (
							select 
								fsupplier_order_id,
								sum(if(fapply_type = 2, - fapply_amount, fapply_amount)) fapply_amount
							from league.t_bbc_supplier_work	
							where fstatus = 2 and fwork_type = 2
							group by fsupplier_order_id	
						) sk on sk.fsupplier_order_id = oaa.fsupplier_order_id
						GROUP BY oaa.fsupplier_order_id
				) t on t.fsupplier_order_id = sku.fsupplier_order_id
				group by so.forder_id,sku.fsku_code,sku.fbatch_id,sku.fbatch_package_num
		) sk on sk.forder_id = so.forder_id and sk.fsku_code = so.fsku_code and sk.fbatch_id = so.fbatch_id and sk.fbatch_package_num = so.fbatch_package_num
		where so.fpay_time BETWEEN '2020-10-01 00:00:00' and '2020-10-27 23:59:59' -- and so.forder_id = 'XS6032959594543504'-- and so.funame not in ('18575598014',   'YW123456',  'xingyunlianmeng')  -- and so.forder_id = 'XS6014816036121628' and so.
	) t
-- 	group by t.forder_id
-- 	order by forder_id;