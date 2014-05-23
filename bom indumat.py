bom_obj = self.pool.get("mrp.bom")

# Update the Website availability of the current product
avail = object.product_id.qty_available+object.product_id.outgoing_qty
object.product_id.write({'x_availability':avail})

# Find bom lines where this product is the component
bom_line_ids = bom_obj.search(cr,uid,[('product_id','=',object.product_id.id),('bom_id','!=',False)],context=context)
# Find parent boms of all these lines
boms = bom_obj.browse(cr,uid,bom_obj.search(cr,uid,[('bom_lines','in',bom_line_ids)],context=context),context=context)

# Update the Website availability of the parent products
for b in boms:
    avail = []
    for l in b.bom_lines:
        avail.append(int(l.product_id.x_availability/l.product_qty))
    b.product_id.write({'x_availability':min(avail)})