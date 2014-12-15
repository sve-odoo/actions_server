picking_out_id = self.pool['ir.model.data'].get_object_reference(cr, uid, 'stock', 'picking_type_out')[1]
template_id = object.product_id.id
move_ids = self.search(cr, uid, [('picking_type_id', '=', picking_out_id), ('product_id', '=', template_id)])

planned_sales_floating_qty = 0.0
planned_sales_ground_qty = 0.0
out_by_ship = {}
for move in self.browse(cr, uid, move_ids):
    if move.x_picking_source and move.x_picking_source.state == 'assigned':
        planned_sales_floating_qty += move.product_qty
        #Compute out qty by ship in
        if out_by_ship.get(move.x_picking_source.id):
            out_by_ship[move.x_picking_source.id] += move.product_qty
        else:
            out_by_ship[move.x_picking_source.id] = move.product_qty
    else:
        planned_sales_ground_qty += move.product_qty
        

picking_in_id = self.pool['ir.model.data'].get_object_reference(cr, uid, 'stock', 'picking_type_in')[1]
move_in_ids = self.search(cr, uid, [
                                ('picking_type_id', '=', picking_in_id), 
                                ('product_id', '=', template_id), 
                                ('state', '=', 'assigned')
                             ])
ship = {}
for move in self.browse(cr, uid, move_in_ids):
    if ship.get(move.picking_id.id):
        ship[move.picking_id.id]['x_total_floating_qty'] += move.product_qty
        ship[move.picking_id.id]['x_available_floating_qty'] += move.product_qty
        
    else:
        ship[move.picking_id.id] = {
                                    'x_name' : move.picking_id.name,
                                    'x_picking' : move.picking_id.id,
                                    'x_total_floating_qty' : move.product_qty,
                                    'x_available_floating_qty' : move.product_qty - out_by_ship.get(move.picking_id.id, 0.0),
                                    'x_planned_date_available' : move.picking_id.date,
                                    'x_product_id' : object.product_id.product_tmpl_id.id
                                }
value = {
  'x_virtual_ground_qty'  : object.product_id.qty_available - planned_sales_ground_qty,
  'x_virtual_floating_qty': object.product_id.incoming_qty - planned_sales_floating_qty,
  'x_shipping_boat_ids' : [(2, boat.id) for boat in object.product_id.product_tmpl_id.x_shipping_boat_ids],
}
self.pool['product.template'].write(cr, uid, object.product_id.product_tmpl_id.id, value)
for val in ship.values():
    self.pool['x_shipping_boat'].create(cr, uid, val)