if object.type =='out_invoice':
    sol_obj = self.pool['sale.order.line']
    for ail in object.invoice_line:
        domain = [('invoice_lines','=', ail.id)]
        sol_ids = sol_obj.search(cr, uid, domain, limit=1, context=context)
        if sol_ids:
            sol = sol_obj.browse(cr, uid, sol_ids[0], context=context)
            ail.write({'x_so_name_mri' : sol.order_id.name,
                'x_so_creation_date_mri': sol.order_id.date_order})
 
elif object.type=='in_invoice':
    pol_obj = self.pool['purchase.order.line']
    for il in object.invoice_line:
        domain = [('invoice_lines','=', il.id)]
        pol_ids = pol_obj.search(cr, uid, domain, limit=1, context=context)
        if pol_ids:
            pol = pol_obj.browse(cr, uid, pol_ids[0], context=context)
            if pol.move_ids:
                il.write ({'x_in_name_mri': pol.move_ids[0].picking_id.name,
                    'x_in_date_mri': pol.move_ids[0].picking_id.date})
