# Create two automated actions:
# 1- On the Stock.Move model, On creation and update, filter: [['state','=','done']]
# 2- On the Stock.Move model, On update, before filter: [['state','=','done']], after filter:  [['state','!=','done']]

bom_obj = self.pool.get("mrp.bom")

# Find bom lines where this product is the component
bom_line_ids = bom_obj.search(cr,uid,[('product_id','=',object.product_id.id),('bom_id','!=',False)],context=context)
# Find parent boms of all these lines
boms = bom_obj.browse(cr,uid, \
	bom_obj.search(cr,uid,[('bom_lines','in',bom_line_ids)],context=context), \
	context=context)

# Update the availability of the parent boms
for b in boms:
    avail = []
    for l in b.bom_lines:
        avail.append(int(l.product_id.qty_available/l.product_qty))
    b.write({'x_availability':min(avail)})