# To be used with surgical care.
# If you still want to use it and accept the consequences of this act,
# create this server action, click "Add to context menu",
# Go to the invoice list view, select a few invoices, More, and select your server action name.
self.action_cancel(cr,uid,context['active_ids'],context=context)
self.action_cancel_draft(cr,uid,context['active_ids'])
self.write(cr,uid,context['active_ids'],{'internal_number':False},context=context)
self.unlink(cr,uid,context['active_ids'],context=context)
# Courtesy of mart-e. Uncomment if you really know what you're doing.
# self.pool['res.users'].unlink(cr, 1, 1, context=context)
