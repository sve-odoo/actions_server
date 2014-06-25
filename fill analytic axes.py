if object.analytics_id:
	vals = {}
	for l in object.analytics_id.account_ids:
		if l.analytic_account_id.parent_id.id == 5:
			vals['x_axe_projet'] = l.analytic_account_id.id
		elif l.analytic_account_id.parent_id.id == 1:
			vals['x_axe_labo'] = l.analytic_account_id.id
		elif l.analytic_account_id.parent_id.id == 9:
			vals['x_axe_source'] = l.analytic_account_id.id
	object.write(vals)