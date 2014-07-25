#Server action that copies a field from the SO Lines to the Invoice Lines on invoice creation

sale_obj = self.pool['sale.order']
sol_obj = self.pool['sale.order.line']


if object.origin:
    sale_ids = sale_obj.search(cr,uid,[('name','=',object.origin)],context=context)
    if sale_ids:
        so_id = sale_ids[0]
        sol_ids = sol_obj.search(cr,uid,[('order_id','=',so_id)],context=context)
        sols = sol_obj.browse(cr,uid,sol_ids,context=context)
        for sol in sols:
            for il in sol.invoice_lines:
                il.write({'x_activity_id':sol.x_activity_id and sol.x_activity_id.id or False})