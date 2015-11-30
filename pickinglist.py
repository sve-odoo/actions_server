prod_mod = pool['product.product']

# Remove any record linked to the picking list of this ronde:
line_obj = pool['x_pickinglist_line']
cell_obj = pool['x_pickinglist_cell']

frz_line_ids = line_obj.search(cr, uid, [('x_frz_ronde_id', '=', object.id)], context=context)
dry_line_ids = line_obj.search(cr, uid, [('x_dry_ronde_id', '=', object.id)], context=context)

line_obj.unlink(cr, uid, frz_line_ids + dry_line_ids, context=context)
# The cells will be deleted in cascade.

loc_obj = pool['stock.location']
stock_loc_browse = loc_obj.browse(cr, uid, 12, context=context)  #hardcode id of location "stock"

dry_weight = 0
frz_weight = 0

# The y axis is the list of products
# The x axis is the list of delivery orders
frz_qty = dict()
frz_qty['Total'] = {'Total': 0}
frz_y_axis = set()

dry_qty = dict()
dry_qty['Total'] = {'Total': 0}
dry_y_axis = set()

for picking in object.x_picking_ids:
    if picking.state == 'cancel':
        continue
    # if not picking.move_lines:
    #     raise Warning("At least one of the selected delivery orders is empty.")
    if picking.x_sequence in frz_qty or picking.x_sequence in dry_qty:
        raise Warning('Each delivery order needs to have a unique sequence within a Ronde\n'\
            'Elke levering dient een unieke ordernummer te hebben in een ronde')
    # Initiate the column for the current picking
    frz_qty[picking.x_sequence] = {'Total': 0}
    dry_qty[picking.x_sequence] = {'Total': 0}
    for line in picking.move_lines:
        if line.state == 'cancel':
            continue
        # Find whether the product is a frozen or a dry product, based on the putaway stategy
        prod_loc_id = loc_obj.get_putaway_strategy(cr, uid, stock_loc_browse, line.product_id, context=context)
        if prod_loc_id == 20:  #hardcode freezer location id
            # In the current column,
            # - if no cell exist for the current product, create one
            frz_qty[picking.x_sequence].setdefault(line.product_id.name, 0)
            # - add the current product quantity to this cell
            frz_qty[picking.x_sequence][line.product_id.name] += line.product_uom_qty
            # - add the current product quantity to the 'Total' of the cell
            frz_qty[picking.x_sequence]['Total'] += line.product_uom_qty
            # In the 'Total' column,
            # - if no cell exist for the current product, create one
            frz_qty['Total'].setdefault(line.product_id.name, 0)
            # - add the current product quantity to this cell
            frz_qty['Total'][line.product_id.name] = frz_qty['Total'][line.product_id.name] + line.product_uom_qty
            # Add the current product quantity to the complete total
            frz_qty['Total']['Total'] += line.product_uom_qty
            # Add the current product to the list of frozen products
            frz_y_axis.add(line.product_id.name)
            frz_weight += line.weight
        else:
            dry_qty[picking.x_sequence].setdefault(line.product_id.name, 0)
            dry_qty[picking.x_sequence][line.product_id.name] += line.product_uom_qty
            dry_qty[picking.x_sequence]['Total'] += line.product_uom_qty
            dry_qty['Total'].setdefault(line.product_id.name, 0)
            dry_qty['Total'][line.product_id.name] = dry_qty['Total'][line.product_id.name] + line.product_uom_qty
            dry_qty['Total']['Total'] += line.product_uom_qty
            dry_y_axis.add(line.product_id.name)
            dry_weight += line.weight

if frz_y_axis:
    frz_x_axis = frz_qty.keys()
    frz_x_axis.remove('Total')
    frz_x_axis.sort()
    frz_x_axis.append('Total')
    frz_y_axis = list(frz_y_axis)
    frz_ids = prod_mod.search(cr, uid, [('name', 'in', frz_y_axis)], order='x_pick_volgorde asc', context=context)
    frz_read_names = prod_mod.read(cr, uid, frz_ids, ['name'], context=context)
    frz_names = [item['name'] for item in frz_read_names]
    frz_y_axis = frz_names
    frz_y_axis.append('Total')

    for ycount, y in enumerate(['dummy'] + frz_y_axis):
        line_id = line_obj.create(cr, uid, {'x_frz_ronde_id': object.id}, context=context)
        for xcount, x in enumerate(['dummy'] + frz_x_axis):
            cell_values = {'x_line_id': line_id}
            if ycount == 0 and xcount == 0:  # cell (1,1)
                cell_values['x_content'] = "Products"
            elif xcount == 0:  # first column
                cell_values['x_content'] = y
            elif ycount == 0:  # title line
                cell_values['x_content'] = xcount if xcount != len(frz_x_axis) else "Total"
            elif x in frz_qty and y in frz_qty[x]:  # non-empty cells
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
    dry_ids = prod_mod.search(cr, uid, [('name', 'in', dry_y_axis)], order='x_pick_volgorde asc', context=context)
    dry_read_names = prod_mod.read(cr, uid, dry_ids, ['name'], context=context)
    dry_names = [item['name'] for item in dry_read_names]
    dry_y_axis = dry_names
    dry_y_axis.append('Total')

    for ycount, y in enumerate(['dummy'] + dry_y_axis):
        line_id = line_obj.create(cr, uid, {'x_dry_ronde_id': object.id}, context=context)
        for xcount, x in enumerate(['dummy'] + dry_x_axis):
            cell_values = {'x_line_id': line_id}
            if ycount == 0 and xcount == 0:  # cell (1,1)
                cell_values['x_content'] = "Products"
            elif xcount == 0:  # first column
                cell_values['x_content'] = y
            elif ycount == 0:  # title line
                cell_values['x_content'] = xcount if xcount != len(dry_x_axis) else "Total"
            elif x in dry_qty and y in dry_qty[x]: # non-empty cells
                cell_values['x_content'] = int(dry_qty[x][y]) if dry_qty[x][y] == int(dry_qty[x][y]) else dry_qty[x][y]
            else:  # empty cells
                cell_values['x_content'] = ""
            cell_id = cell_obj.create(cr, uid, cell_values, context=context)

object.write({
    'x_dry_weight': dry_weight,
    'x_frz_weight': frz_weight,
    })

action = {
    'type': 'ir.actions.report.xml',
    'report_name': '__custo__.report_ronde_pickinglist_document.sve',
    'datas': {
        'ids': [object.id],
        }
    # 'data': {
    #     'dry_weight': dry_weight,
    #     'frz_weight': frz_weight,
    #     }
    }
