bom_obj = self.pool["mrp.bom"]
vals_list = []
total_working_hours = 0.0
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
			total_working_hours += working_hours
			vals_sol = {
				'purchase_price': total_cost, 
				'x_working_hours': working_hours, 
				'price_unit': total_cost * object.x_margin
				}
			vals_list.append((1,l.id,vals_sol))
		# If margin has to be applied on non-bom products lines
		# vals_list.append((1,l.id,{'price_unit': total_cost * object.x_margin}}))
vals_so = {}
if total_working_hours:
	vals_so.update({'x_working_hours_so':total_working_hours})

if vals_list:
	vals_so.update({'order_line':vals_list})

if vals_so:
	object.write(vals_so)
