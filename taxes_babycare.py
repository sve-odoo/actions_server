if not object.parent_id:
    if object.country_id and object.country_id.x_eu and object.vat and object.country_id.code != 'NL':
        values = {
            'property_account_position': 3,
            'property_product_pricelist': 3,
            }
    elif object.country_id and not object.country_id.x_eu:
        values = {
            'property_account_position': 4,
            'property_product_pricelist': 3,
            }
    else:
        values = {
            'property_account_position': 1,
            }
    object.write(values)