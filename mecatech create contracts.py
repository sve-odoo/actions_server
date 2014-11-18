partner_obj = pool['res.partner']
contract_obj = pool['account.analytic.account']
invoice_line_obj = pool['account.analytic.invoice.line']
prod_obj = pool['product.product']
partners = partner_obj.browse(cr,uid,context['active_ids'],context=context)
for p in partners:
    categ_ids = [c.id for c in p.category_id]
    if 2 in categ_ids: #entr 1-20
        prod_id = 3
    elif 3 in categ_ids: #entr 21-100
        prod_id = 5
    elif 4 in categ_ids: #entr 101 - 250
        prod_id = 6
    elif 5 in categ_ids: #entr 251-500
        prod_id = 7
    elif 6 in categ_ids: #entr 501-1000
        prod_id = 8
    elif 7 in categ_ids: #entr >1000
        prod_id = 9
    elif 10 in categ_ids or 8 in categ_ids: #academie
        prod_id = 10
    elif not p.category_id or 12 in categ_ids: #autre
        prod_id = 14    
    elif 13 in categ_ids: #cc
        prod_id = 12
    prod = prod_obj.browse(cr,uid,prod_id,context=context)
    line_vals = {
        'product_id': prod.id,
       # 'uom_id': prod.uom_id.id,
        }
    line_vals.update(invoice_line_obj.product_id_change(cr,uid,[],prod.id, False, 1, False, p.id, False, 1, 1)['value'],context=context)
    vals = {
        'partner_id': p.id,
        'name': p.name + u' - Adhésion ' + prod.name,
        'recurring_rule_type':'yearly',
        'recurring_invoices': True,
        'code': p.name,
        'type':'contract',
        'recurring_interval':1,
        'recurring_next_date': (datetime.date.today() + dateutil.relativedelta.relativedelta(years=0)).strftime("%Y-%m-%d"),
        'recurring_invoice_line_ids': [(0,0,line_vals)]
        }
    contract_obj.create(cr,uid,vals,context=context)