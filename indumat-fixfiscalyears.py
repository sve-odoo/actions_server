# indumat
# 1 - Find 2014 account.move.lines that are reconciled with OD/0001 opening entries 
# - Store exact amount in note
# 2 - Unreconcile them
# 3 - Generate opening entries
# 4 - Reconcile (1) lines with opening entries

opening_id = 18

note = self.pool['note.note'].browse(cr, uid, 15, context=context)

move_obj = self.pool['account.move']
line_obj = self.pool['account.move.line']
reconcile_obj = self.pool['account.move.reconcile']

opening_entry = move_obj.browse(cr, uid, 18, context=context)

# opening_entry_line_ids = [line.id for line in opening_entry.line_id]
# opening_entry_lines = move_obj.browse(cr, uid, opening_entry_line_ids, context=context)

reconcile_partial_ids = [line.reconcile_partial_id.id for line in opening_entry.line_id if line.reconcile_partial_id]
if reconcile_partial_ids:
	raise Warning('Some opening entry lines are partially reconciled: ', reconcile_partial_ids)

reconcile_ids = [line.reconcile_id.id for line in opening_entry.line_id if line.reconcile_id]
reconciles = reconcile_obj.browse(cr, uid, reconcile_ids, context=context)

reconcile_lines_nested = [r.line_id for r in reconciles]
reconcile_lines = [item for sublist in reconcile_lines_nested for item in sublist] # moi pas comprendre
reconcile_line_ids = [line.id for line in reconcile_lines]

domain = [('id', 'in', reconcile_line_ids), ('period_id.fiscalyear_id', '=', 2)]
objective1_line_ids = line_obj.search(cr, uid, domain, context=context)
# objective1_lines = line_obj.browse(cr, uid, objective1_line_ids, context=context)

# objective1_not_fully_reconciled_partners = [l.partner_id for l in objective1_lines if l.partner_id and not l.partner_id.credit and not l.partner_id.credit]



action_id = 227
action_dict = pool['ir.actions.act_window'].read(cr, uid, [action_id], context=context, load='_classic_write')[0]
action_dict.update({
	'view_type': 'form',
	'view_mode': 'form,tree',
	'domain': [('id', 'in', objective1_line_ids)]
	})
action = action_dict

# note.write({'memo':objective1_line_ids})
