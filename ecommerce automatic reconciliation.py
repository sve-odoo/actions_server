# put the id of your payment journal here
journal_id = 10

voucher_obj = self.pool['account.voucher']
for inv in object.sale_order_id.invoice_ids:

	self.pool['account.invoice'].signal_workflow(cr, uid, [inv.id], 'invoice_open')

	context = dict(context or {})
	context.update({
		'invoice_id': inv.id,
		'invoice_type': inv.type,
		'type': inv.type in ('out_invoice','out_refund') and 'receipt' or 'payment',
		'payment_expected_currency': inv.currency_id.id,
		'default_partner_id': self.pool['res.partner']._find_accounting_partner(inv.partner_id).id,
		'default_amount': inv.type in ('out_refund', 'in_refund') and -inv.residual or inv.residual,
		'default_reference': inv.name,
		'default_type': inv.type in ('out_invoice','out_refund') and 'receipt' or 'payment',
		'default_journal_id': journal_id
		})

	default_keys = [vdk for vdk in voucher_obj._defaults.keys()]
	vals = voucher_obj.default_get(cr, uid, default_keys, context=context)

	onchange_date_vals = voucher_obj.onchange_date(cr, uid, [], vals['date'], vals['currency_id'], 
		vals['payment_rate_currency_id'], vals['amount'], vals['company_id'], 
		context=context)['value']
	vals.update(onchange_date_vals)

	onchange_partner_vals = voucher_obj.onchange_partner_id(cr, uid, [], vals['partner_id'], 
		vals['journal_id'], vals['amount'], vals['currency_id'], 
		vals['type'], False, context=context)['value']
	vals.update(onchange_partner_vals)

	onchange_amount_vals = voucher_obj.onchange_amount(cr, uid, [], vals['amount'], vals['payment_rate'], 
		vals['partner_id'], vals['journal_id'], vals['currency_id'], vals['type'], 
		vals['date'], vals['payment_rate_currency_id'], vals['company_id'], context=context)['value']
	vals.update(onchange_amount_vals)

	onchange_journal_vals = voucher_obj.onchange_journal(cr, uid, [], vals['journal_id'], 
		vals['line_cr_ids'], False, vals['partner_id'], vals['date'], vals['amount'], 
		vals['type'], vals['company_id'], context=context)['value']
	vals.update(onchange_journal_vals)

	vals['line_cr_ids'] = [(0,0,x) for x in vals['line_cr_ids']]
	vals['line_dr_ids'] = [(0,0,x) for x in vals['line_dr_ids']]

	voucher_id = voucher_obj.create(cr, uid, vals, context=context)
	voucher_obj.button_proforma_voucher(cr, uid, [voucher_id], context=context)

