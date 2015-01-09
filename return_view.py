# In this example, create an object, then return the view associated with it:
new_order_id = pool['sale.order'].create(cr, uid, newordervals, context=context)

action= {
    'name': 'Sale Order',
    'view_type': 'form',
    'view_mode': 'form',
    'view_id': self.pool.get('ir.ui.view').search(cr, uid, [('name', '=', 'sale.order.form')])[0],
    'res_model': 'sale.order',
    'res_id': new_order_id,
    'type': 'ir.actions.act_window',
}
