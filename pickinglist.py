# Remove any record linked to the picking list of this picking wave:
line_obj = pool['x_pickinglist_line']
cell_obj = pool['x_pickinglist_cell']

frz_line_ids = line_obj.search(cr, uid, [('x_frz_wave_id', '=', object.id)], context=context)
dry_line_ids = line_obj.search(cr, uid, [('x_dry_wave_id', '=', object.id)], context=context)
cell_ids = cell_obj.search(cr, uid, [('x_line_id', 'in', frz_line_ids + dry_line_ids)], context=context)

line_obj.unlink(cr, uid, frz_line_ids + dry_line_ids, context=context)
cell_obj.unlink(cr, uid, cell_ids, context=context)


loc_obj = pool['stock.location']
stock_loc_browse = loc_obj.browse(cr, uid, 12, context=context) #hardcode id of location "stock"

frz_qty = dict()
frz_qty['Total'] = {'Total': 0}
frz_y_axis = set()

dry_qty = dict()
dry_qty['Total'] = {'Total': 0}
dry_y_axis = set()

for picking in object.picking_ids:
    # if not picking.move_lines:
    #     raise Warning("At least one of the selected delivery orders is empty.")
    if picking.x_sequence in frz_qty or picking.x_sequence in dry_qty:
        raise Warning('Each delivery order needs to have a unique sequence within a Picking Wave\n'\
            'Elke levering dient een unieke ordernummer te hebben in een ronde')
    # Initiate the column for the current picking
    frz_qty[picking.x_sequence] = {'Total': 0}
    dry_qty[picking.x_sequence] = {'Total': 0}
    for line in picking.move_lines:
        # Find whether the product is a frozen or a dry product, based on the putaway stategy
        prod_loc_id = loc_obj.get_putaway_strategy(cr, uid, stock_loc_browse, line.product_id, context=context)
        if prod_loc_id == 20: #hardcode freezer location id
            # In the current column,
            # - if no cell exist for the current product, create one
            frz_qty[picking.x_sequence].setdefault(line.product_id.display_name, 0)
            # - add the current product quantity to this cell
            frz_qty[picking.x_sequence][line.product_id.display_name] += line.product_uom_qty
            # - add the current product quantity to the 'Total' of the cell
            frz_qty[picking.x_sequence]['Total'] += line.product_uom_qty
            # In the 'Total' column,
            # - if no cell exist for the current product, create one
            frz_qty['Total'].setdefault(line.product_id.display_name, 0)
            # - add the current product quantity to this cell
            frz_qty['Total'][line.product_id.display_name] = frz_qty['Total'][line.product_id.display_name] + line.product_uom_qty
            # Add the current product quantity to the complete total
            frz_qty['Total']['Total'] += line.product_uom_qty
            # Add the current product to the list of frozen products
            frz_y_axis.add(line.product_id.display_name)
        else:
            dry_qty[picking.x_sequence].setdefault(line.product_id.display_name, 0) 
            dry_qty[picking.x_sequence][line.product_id.display_name] += line.product_uom_qty
            dry_qty[picking.x_sequence]['Total'] += line.product_uom_qty
            dry_qty['Total'].setdefault(line.product_id.display_name, 0)
            dry_qty['Total'][line.product_id.display_name] = dry_qty['Total'][line.product_id.display_name] + line.product_uom_qty
            dry_qty['Total']['Total'] += line.product_uom_qty
            dry_y_axis.add(line.product_id.display_name)

if frz_y_axis:
    frz_x_axis = frz_qty.keys()
    frz_x_axis.remove('Total')
    frz_x_axis.sort()
    frz_x_axis.append('Total')
    frz_y_axis = list(frz_y_axis)
    frz_y_axis.append('Total')

    for ycount, y in enumerate(['dummy'] + frz_y_axis):
        line_id = line_obj.create(cr, uid, {'x_frz_wave_id': object.id}, context=context)
        for xcount, x in enumerate(['dummy'] + frz_x_axis):
            cell_values = {'x_line_id': line_id}
            if ycount == 0 and xcount == 0: # cell (1,1)
                cell_values['x_content'] = "Products"
            elif xcount == 0: # first column
                cell_values['x_content'] = y
            elif ycount == 0: # title line
                cell_values['x_content'] = x
            elif x in frz_qty and y in frz_qty[x]: # non-empty cells
                cell_values['x_content'] = int(frz_qty[x][y]) if frz_qty[x][y] == int(frz_qty[x][y]) else frz_qty[x][y]
            else: # empty cells
                cell_values['x_content'] = ""
            cell_id = cell_obj.create(cr, uid, cell_values, context=context)
     
if dry_y_axis:
    dry_x_axis = dry_qty.keys()
    dry_x_axis.remove('Total')
    dry_x_axis.sort()
    dry_x_axis.append('Total')
    dry_y_axis = list(dry_y_axis)
    dry_y_axis.append('Total')

    for ycount, y in enumerate(['dummy'] + dry_y_axis):
        line_id = line_obj.create(cr, uid, {'x_dry_wave_id': object.id}, context=context)
        for xcount, x in enumerate(['dummy'] + dry_x_axis):
            cell_values = {'x_line_id': line_id}
            if ycount == 0 and xcount == 0: # cell (1,1)
                cell_values['x_content'] = "Products"
            elif xcount == 0: # first column
                cell_values['x_content'] = y
            elif ycount == 0: # title line
                cell_values['x_content'] = x
            elif x in dry_qty and y in dry_qty[x]: # non-empty cells
                cell_values['x_content'] = int(dry_qty[x][y]) if dry_qty[x][y] == int(dry_qty[x][y]) else dry_qty[x][y]
            else: # empty cells
                cell_values['x_content'] = ""
            cell_id = cell_obj.create(cr, uid, cell_values, context=context)
