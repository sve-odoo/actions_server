po_obj = self.pool.get('purchase.order')
po_line_obj = self.pool.get('purchase.order.line')

if not object.project_id:
    raise Warning ("Veuillez assigner un compte analytique sur le bon de commande.")

suppliers_ids = [l.product_id.seller_ids[0].name.id for l in object.order_line if l.product_id and l.product_id.seller_ids]
suppliers_ids = set(suppliers_ids)

for s in suppliers_ids:
    po_vals = {
        'partner_id': s,
        'origin':object.name,
        }
    po_vals.update(po_obj.default_get(cr,uid,['warehouse_id'],context=context))
    po_vals.update(po_obj.onchange_warehouse_id(cr,uid,[],po_vals['warehouse_id'])['value'])        
    po_vals.update(po_obj.onchange_partner_id(cr,uid,[],s)['value'])
    po_id = po_obj.create(cr,uid,po_vals,context=context)
    po = po_obj.browse(cr,uid,po_id,context=context)
    object.write({'x_purchase_ids':[(4,po_id)]})
    for l in object.order_line:
        if l.product_id and l.product_id.seller_ids and l.product_id.seller_ids[0].name.id == s:
            line_vals = {
                'name':l.name,
                'product_id':l.product_id.id,
                'x_image':l.x_image,
                'x_label':l.x_label,
                'product_qty':l.product_uom_qty,
                'account_analytic_id': object.project_id.id,
                'order_id': po.id,
                }
            line_vals.update(po_line_obj.onchange_product_id(cr, uid, [], po.pricelist_id.id, \
                line_vals['product_id'], line_vals['product_qty'], False, po.partner_id.id,\
                po.date_order, po.fiscal_position.id, context=context)['value'])
            #po_obj.write(cr,uid,po_id,{'order_line':[(0,0,line_vals)]},context=context
            po_line_id = po_line_obj.create(cr,uid,line_vals,context=context)
            l.write({'x_purchase_line_id':po_line_id})