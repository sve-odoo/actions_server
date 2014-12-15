weight = 0.0
product_uom_obj = pool['product.uom']
for line in object.order_line:
    if not line.product_id or line.is_delivery:
        continue
    q = product_uom_obj._compute_qty(cr, uid, line.product_uom.id, line.product_uom_qty, line.product_id.uom_id.id)
    weight += (line.product_id.weight or 0.0) * q
if weight < 80:
    values = {
        'x_weight_lt_80': weight,
        'x_weight_gt_80': False,
        }
else:
    values = {
        'x_weight_lt_80': False,
        'x_weight_gt_80': weight,
    }
object.write(values)