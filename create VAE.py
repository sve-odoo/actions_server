vae_obj = self.pool.get('x_vae.fiche')
lot_obj = self.pool.get('stock.production.lot')
if object.type == 'in':
    if object.product_id.x_vae:
        vae_id = vae_obj.create(cr, uid, {
            'x_name': object.prodlot_id.name,
            'x_product_id': object.product_id.id,
            'x_date_achat': object.date})
        object.prodlot_id.write({'x_vae_id':vae_id})
if object.type == 'out':
    if object.product_id.x_vae:
        order_obj = self.pool.get('sale.order')
        order_ids = order_obj.search(cr, uid, [('name', '=', object.origin)], context=context)
        order = order_obj.browse(cr, uid, order_ids)[0]
        vae_ids = vae_obj.search(cr, uid, [
            ('x_name', '=', object.prodlot_id.name),
            ('x_product_id', '=', object.product_id.id)], context=context)
        vae_obj.write(cr, uid, vae_ids, {
            'x_state': 'vendu',
            'x_customer_id': object.partner_id.id,
            'x_origin': object.origin or '',
            'x_vendeur_id': order.user_id.id,
            'x_vente_date': order.date_confirm}, context=context)