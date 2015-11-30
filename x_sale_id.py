sale_obj = self.pool["sale.order"]
if object.origin:
    sale_ids = sale_obj.search(cr, uid, [('name', '=', object.origin)],context=context)
    if sale_ids:
        object.write({'x_sale_id': sale_ids[0]})
