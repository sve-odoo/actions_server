#Let's say you want to create a new button on the partner's list view for inviting partner to an event when the event is
#confirmed. you can create a automated action that would trigger the following server action:

reg_obj = self.pool['event.registration']
partner_obj = self.pool['res.partner']
sa_obj = self.pool['ir.actions.server']
event_name = "Invite partner to: " + object.name
mycode = """reg_obj = self.pool['event.registration']
event_obj = self.pool['event.event']
for partner_id in context['active_ids']:
	partner_item = self.browse(cr,uid,partner_id,context=context)
	res = {
	'event_id': """ +str(object.id)+""",
	'partner_id' : partner_item.id,
	'name': partner_item.name,
	'phone':partner_item.phone,
	'email':partner_item.email,
	'x_date_event': event_obj.browse(cr,uid,"""+str(object.id)+""").date_end
	}
	reg_id = reg_obj.create(cr,uid,res,context=context)"""

sa_res = {
    'name': event_name,
    'model_id': int(self.pool.get('ir.model').search(cr,uid,[('model','=','res.partner')])[0]),
    'state': 'code',
    'code': mycode
}
serv_action_id = sa_obj.create(cr,uid,sa_res,context=context)
sa_obj.browse(cr,uid,serv_action_id,context=context).create_action()

#in fact, it's a server action that creates another server action that is made for adding contacts to the event you just confirmed.
#at the end of the action, you'll see it's adding the freshly created server action to the "more" menu of the res.partner
