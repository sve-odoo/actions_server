#Three separate server actions


#Sur le SO
bom_obj = self.pool.get("mrp.bom")
sol_obj = self.pool.get("sale.order.line")

so_total_cost = 0.0
so_total_price = 0.0

for l in object.order_line:
    if l.property_ids:
        prop_ids = []
        for i in l.property_ids:
            prop_ids.append(i.id)
        bom_ids = bom_obj.search(cr,uid,[('property_ids', 'in', [prop_ids[0]]), ('product_id', '=', l.product_id.id)], context=context)
        if bom_ids:
            bom_browse = bom_obj.browse(cr,uid,bom_ids[0],context=context)
            object.write({'order_line':[(1,l.id,{'purchase_price':bom_browse.x_total_cost,'x_bom_id':bom_browse.id})]})
    purchase_price = sol_obj.read(cr, uid, [l.id], ['purchase_price'], context=context)
    so_total_cost += purchase_price[0]['purchase_price'] * l.product_uom_qty 
    so_total_price += l.price_subtotal

computed_margin = (1-(so_total_cost/so_total_price))*100
object.write({'x_margin':computed_margin})






#Sur la bom
total_cost=0.0
for line in object.bom_lines:
    total_cost = total_cost + line.product_id.standard_price*line.product_qty
total_cost = total_cost / object.product_qty
object.write({'x_total_cost':total_cost})






# sur l'article
bom_obj = self.pool.get("mrp.bom")
#Find all bom lines regarding this product
bom_ids = bom_obj.search(cr, uid, [('product_id', '=', object.id),('bom_id','!=',False)], context=context)
bom_browseobjects = bom_obj.browse(cr, uid, bom_ids, context=context)

# for all those bom lines, update the unit cost
for bom in bom_browseobjects:
    total_cost=0.0
    for line in bom.bom_id.bom_lines:
        total_cost = total_cost + line.product_id.standard_price*line.product_qty
    total_cost = total_cost / bom.bom_id.product_qty
    bom.bom_id.write({'x_total_cost':total_cost})