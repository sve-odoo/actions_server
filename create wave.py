wave_vals = {
	'name': object.x_name,
	'x_date': object.x_date,
	'x_vehicle_id': object.x_vehicle_id.id,
	'user_id': object.x_user_id.id,
	'picking_ids': [(4,picking_id) for picking_id in context['picking_ids']],
	'state': 'in_progress'
}
wave_id = pool['stock.picking.wave'].create(cr, uid, wave_vals, context=context)

action_dict = pool['ir.actions.act_window'].for_xml_id(cr, uid, 'stock_picking_wave', 'action_picking_wave', context=context)
action_dict.update({
	'res_id': wave_id,
	'view_mode': 'form,tree'
	})
action_dict.pop('views')
action = action_dict