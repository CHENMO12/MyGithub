SELECT
    fgoods_order_id,
    fdate,
    CONVERT (  fbuy_num , INT ) fbuy_num,
    fsku_amount  sell_amount,
   fcost_amount  cost_aomunt,
     freal_gmv  freal_gmv,
    freal_cost_amount  freal_cost_amount,
   profit  freal_profit,
    faftersale_refund_user_amount  faftersale_refund_user_amount,
    faftersale_refund_sup_amount  faftersale_refund_sup_amount,
  faftersale_work_refund_user_amount  faftersale_work_refund_user_amount,
  faftersale_work_refund_sup_amount  faftersale_work_refund_sup_amount,
     fwork_user_amount  fwork_user_amount,
    fwork_sup_amount fwork_sup_amount,
   fartificial_adjust_amount 
    FROM
    (
    SELECT
    so.fgoods_order_id,
    so.finternational_code,
    so.funame,
    so.fbrand_id,
    so.ftrade_type,
    so.ftrade_type_var,
    so.fcategory_id1,
    IFNULL(po.fservice_type,0) fservice_type,
    so.fbuy_num,
    so.fsku_amount,
    IFNULL(po.fcost_amount,0) fcost_amount,

    IF(fsupplier_order_id IS NULL,0, so.fsku_amount - ifnull( oa.faftersale_refund_user_amount, 0 ) - ifnull( oaw.fsgtk, 0 ) - ifnull( fwork_user_amount, 0 )) freal_gmv,
      ifnull( po.fcost_amount - ifnull( oa.faftersale_refund_sup_amount, 0 ) - ifnull( oaw.fsgtg, 0 ) - ifnull( fwork_sup_amount, 0 ) ,0)freal_cost_amount,
    IF(fsupplier_order_id IS NULL,0, so.fsku_amount - ifnull( oa.faftersale_refund_user_amount, 0 ) - ifnull( oaw.fsgtk, 0 ) - ifnull( fwork_user_amount, 0 ) - (IFNULL(po.fcost_amount,0) - ifnull( oa.faftersale_refund_sup_amount, 0 ) - ifnull( oaw.fsgtg, 0 ) - ifnull( fwork_sup_amount, 0 ))) profit,
    DATE_FORMAT( so.fpay_time, '%Y-%m-%d' ) fdate,
    ifnull( oa.faftersale_refund_user_amount, 0 ) faftersale_refund_user_amount,#售后退客户金额
    ifnull( oa.faftersale_refund_sup_amount, 0 ) faftersale_refund_sup_amount,#售后供应商退我司金额
    ifnull( oaw.fsgtk, 0 ) faftersale_work_refund_user_amount,#售后工单退客户金额
    ifnull( oaw.fsgtg, 0 ) faftersale_work_refund_sup_amount,#售后工单供应商退我司金额
    ifnull( fwork_user_amount, 0 ) fwork_user_amount,#客户调整金额
    ifnull( fwork_sup_amount, 0 ) fwork_sup_amount,#供应商调整金额
    ifnull( dor.fcost_adjust_amount, 0 ) fartificial_adjust_amount
    FROM
    t_dws_bbc_third_sell_order so
    LEFT JOIN t_dws_bbc_third_cost_order po ON po.fgoods_order_id = so.fgoods_order_id
    AND po.fcost_order_status != 3  and po.Fdeliver_time is not null
    AND po.fis_delete = 0
    LEFT JOIN t_dm_order_reset dor ON so.fgoods_order_id = dor.forder_id
    LEFT JOIN t_dm_order_exclude oe ON so.fgoods_order_id = oe.forder_id
    AND oe.fsource_type = 3
    LEFT JOIN (
    SELECT
    Fgoods_order_id,
    sum( IF ( Fchange_type = 2, IF ( Ftype = 1, Famount,- Famount ), 0 ) ) fwork_user_amount,
    sum( IF ( Fchange_type = 1, IF ( Ftype = 2, Famount,- Famount ), 0 ) ) fwork_sup_amount
    FROM
    t_xyb2b_work_order
    WHERE
    Fstatus = 1
    GROUP BY
    Fgoods_order_id
    ) wo ON wo.Fgoods_order_id = so.Fgoods_order_id
    LEFT JOIN (
    SELECT
    Fgoods_order_id,
    faftersale_id,
    sum( IFNULL( oa.Frefund_real_money + oa.Frefund_freight, 0 ) ) faftersale_refund_user_amount,
    sum( ifnull( oa.Frefund_sup_real_money, 0 ) ) faftersale_refund_sup_amount
    FROM
    t_xyb2b_order_aftersale oa
    WHERE
    oa.Frefund_aftersale_status = 7
    GROUP BY
    Fgoods_order_id
    ) oa ON so.Fgoods_order_id = oa.Fgoods_order_id

    LEFT JOIN (
    select
    a.fgoods_order_id,
    sum(if(oaw.Frole_type=1,if(oaw.Fsum_type=0,oaw.Fadjust_sum,-oaw.Fadjust_sum),0)) fsgtk, -- '售后工单（退客户款）',
    sum(if(oaw.Frole_type=2,if(oaw.Fsum_type=1,oaw.Fadjust_sum,-oaw.Fadjust_sum),0)) fsgtg -- '售后工单（供应商退我司）'
    from
    t_xyb2b_order_aftersale_work oaw
    left join t_xyb2b_order_aftersale a on a.Faftersale_id=oaw.Faftersale_id
    where oaw.Fcheck_status =1
    group by a.fgoods_order_id

    ) oaw on oaw.fgoods_order_id=so.fgoods_order_id

    WHERE
    DATE_FORMAT(so.fpay_time,'%Y-%m-%d') >=DATE_FORMAT( '2020-10-01','%Y-%m-%d')
   and  DATE_FORMAT(so.fpay_time,'%Y-%m-%d') <=DATE_FORMAT( '2020-10-27','%Y-%m-%d')
    AND so.forder_status > 1
    AND oe.forder_exclude_id IS NULL
    )
		order by fgoods_order_id;