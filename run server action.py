if object.x_ronde_id:
    # I explicitely trigger this SA because the "action" key in context prevents an automated action to trigger another one.
    sa_obj = pool['ir.actions.server']
    sa_obj.run(cr, uid, 526, context=dict(context, active_id=object.x_ronde_id.id, active_model='x_ronde'))
