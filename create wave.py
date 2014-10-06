wave_vals = {
	'name': object.x_name,
	'x_date': object.x_date,
	'x_vehicle_id': object.x_vehicle_id.id,
	'user_id': object.x_user_id.id,
	'picking_ids': [(4,picking_id) for picking_id in context['picking_ids']],
	'state': 'in_progress'
}
wave_id = pool['stock.picking.wave'].create(cr, uid, wave_vals, context=context)
# action_id = pool['ir_model_data'].get_object_reference(cr, uid, 'stock_picking_wave', 'action_picking_wave')
action_id = 456
action_dict = pool['ir.actions.act_window'].read(cr, uid, [action_id], context=context, load='_classic_write')[0]
action_dict.pop('views')
action_dict.update({
	'res_id': wave_id,
	'view_type': 'form',
	'view_mode': 'form,tree'

	})
#raise Warning(action_dict)




# action =  {
# 	'type': 'ir.actions.act_window',
# 	'name': 'Picking Wave',
# 	'res_model': 'stock.picking.wave',
# 	'res_id': wave_id,
# 	'view_mode': 'form',
#    zoo