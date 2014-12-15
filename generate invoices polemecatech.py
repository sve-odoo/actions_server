partner_obj = self.pool['res.partner']
invoice_obj = self.pool['account.invoice']
invoice_line_obj = self.pool['account.invoice.line']
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
    elif 10 in categ_ids: #academie
    	prod_id = 10
    # elif 3 in categ_ids: #accord
    # 	prod_id = 11
    # elif 3 in categ_ids: #adisif
    # 	prod_id = 13
    elif 12 in categ_ids: #autre
    	prod_id = 14	
    elif 13 in categ_ids: #cc
    	prod_id = 12
    line_vals = {}
    vals = {}
    vals.update(invoice_obj.onchange_partner_id('out_invoice',p.id,'','','',1)['value'])

    line_vals = {'product_id':prod_id}
    line_vals.update(invoice_line_obj.product_id_change(prod_id, False, 1, False, 'out_invoice', p.id, 1, 0.0, False, context, 1)['value'])

    vals.update({
    	'partner_id': p.id,
    	'invoice_line': [(0,0,line_vals)]
    	})

	invoice_obj.create(cr,uid,vals,context=context)