bom_obj = self.pool['mrp.bom']

# Update the Website availability of the current product
avail = object.product_id.virtual_available - object.product_id.incoming_qty
object.product_id.write({'x_availability': avail})
object.product_id.product_tmpl_id.write({'x_availability': avail})

# Find boms where this product is the component
bom_ids = bom_obj.search(cr, uid, [('bom_line_ids.product_id', 'in', [object.product_id.id])], context=context)
boms = bom_obj.browse(cr, uid, bom_ids, context=context)

# Update the Website availability of the parent templates' variants
for b in boms:
    tmpl_avail = []
    # Find all variants linked to this BoM 
    for variant in b.product_id and [b.product_id] or b.product_tmpl_id.product_variant_ids:
        avail = []
        for l in b.bom_line_ids:
            if set([al.id for al in l.attribute_value_ids]).issubset(set([vl.id for vl in variant.attribute_value_ids])):
                avail.append(int(l.product_id.x_availability / l.product_qty))
        tmpl_avail.append(min(avail))
        variant.write({'x_availability': tmpl_avail[-1]})
    b.product_tmpl_id.write({'x_availability': max(tmpl_avail)})