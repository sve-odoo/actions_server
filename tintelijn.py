bom_obj = self.pool["mrp.bom"]
vals_list = []
for l in object.order_line:
	# Find bom lines where this product is the finished product
	if l.product_id:
		bom_ids = bom_obj.search(cr,uid,[('product_id','=',l.product_id.id),('bom_id','=',False)],context=context)
		if bom_ids:
			bom = bom_obj.browse(cr,uid,bom_ids[0],context=context)
			total_cost = 0.0
			working_hours = 0.0
			for bl in bom.bom_lines:
				if bl.product_id.type == "service":
					total_cost += bl.product_qty * bl.product_id.standard_price * object.x_difficulty_so * l.x_difficulty_sol * object.x_transport
					working_hours += bl.product_qty * object.x_difficulty_so * l.x_difficulty_sol * l.product_uom_qty
				else:
					total_cost += bl.product_qty * bl.product_id.standard_price * object.x_transport
			vals = {
				'purchase_price': total_cost, 
				'x_working_hours': working_hours, 
				'price_unit': total_cost * object.x_margin
				}
			vals_list.append((1,l.id,vals))
if vals_list:
	object.write({'order_line':vals_list})
