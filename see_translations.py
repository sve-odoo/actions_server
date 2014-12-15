domain = [('type', '=', 'view')]
context.update({
    'default_module': '__custo__',
    'default_type': 'view',
})

if object.type == "qweb":
    parent = object.inherit_id
    current = object
    while parent and current.mode != 'base':
        current = parent
        parent = parent.inherit_id
    domain += [('res_id', '=', current.id)]
    context.update({
        'default_name': 'website',
        'default_res_id': current.id,
    })
else:
    domain += [('name', '=', object.model)]
    context.update({
        'search_default_group_by_src': 1,
        'default_name': object.model,
    })

action_dict = pool['ir.actions.act_window'].for_xml_id(
    cr, uid, 'base', 'action_translation', context=context)
action_dict.update({
    'domain': domain,
    'context': context,
})
action = action_dict
