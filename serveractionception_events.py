#Let's say you want to create a new button on the partner's list view for inviting partner to an event when the event is
#confirmed. you can create a automated action that would trigger the following server action:

reg_obj = self.pool['event.registration']
partner_obj = self.pool['res.partner']
sa_obj = self.pool['ir.actions.server']
event_name = "Invite partner to: " + object.name
mycode = """
reg_obj = self.pool['event.registration']
event_obj = self.pool['event.event']
partners = self.browse(cr,uid,context['active_ids'],context=context)
for partner in partners:
	vals = {
	'event_id': """+str(object.id)+""",
	'partner_id' : partner.id,
	'name': partner.name,
	'phone':partner.phone,
	'email':partner.email,
	'x_date_event': event_obj.browse(cr,uid,"""+str(object.id)+""",context=context).date_end
	}
	reg_obj.create(cr,uid,vals,context=context)"""

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
