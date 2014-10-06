action = {
    'name':'Create Picking Wave',
    'view_mode': 'form',
    #'view_id': view_id,
    'view_type': 'form',
    'res_model': 'x_wizard_create_wave',
    'type': 'ir.actions.act_window',
    'nodestroy': True,
    'target': 'new',
    'domain': '[]',
    'context': {'picking_ids': context['active_ids']}
}