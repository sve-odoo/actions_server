field_obj = pool['ir.model.fields']
data_obj = pool['ir.model.data']
prod_obj = pool['product.product']
module_obj = pool['ir.module.module']

vals_list = [{
            'name': 'x_manufacturer',
            'field_description': 'Manufacturer Product Name',
            'ttype': 'many2one',
            'state': 'manual',
            'model_id': data_obj._get_id(cr, uid, 'product', 'model_product_template'),
            'relation': 'res.partner'
		},
		{
            'name': 'x_manufacturer_pname',
            'field_description': 'Manufacturer Product Name',
            'ttype': 'char',
            'state': 'manual',
            'model_id': data_obj._get_id(cr, uid, 'product', 'model_product_template')
		},
		{
            'name': 'x_manufacturer_pref',
            'field_description': 'Manufacturer Product Code',
            'ttype': 'char',
            'state': 'manual',
            'model_id': data_obj._get_id(cr, uid, 'product', 'model_product_template')
		},
	]


for vals in vals_list:
	field_obj.create(cr, uid, vals, context=context)

domain = ['|', '|', ('manufacturer', '!=', False), ('manufacturer_pname', '!=', False), ('manufacturer_pref', '!=', False)]
prod_ids = prod_obj.search(cr, uid, domain, context=context)
products = prod_obj.browse(cr, uid, prod_ids, context=context)
for product in products:
	vals = {
		'x_manufacturer': product.manufacturer.id,
		'x_manufacturer_pname': product.manufacturer_pname,
		'x_manufacturer_pref': product.manufacturer_pref,
		}
	product.write(vals)

prod_manuf_module_id = data_obj._get_id(cr, uid, 'base', 'module_product_manufacturer')
8/0
module_obj.module_uninstall(cr, uid, [prod_manuf_module_id], context=context)