#Let's say you want to create a new button on the partner's list view for inviting partner to an event when the event is
#confirmed. you can create a automated action that would trigger the following server action:

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
	'email':partner.email
	}
	reg_obj.create(cr,uid,vals,context=context)
"""

sa_obj = self.pool['ir.actions.server']
if sa_obj.search(cr,uid,[('code','=',mycode)],context=context):
	raise Warning("A server action already exists for this event.")

sa_res = {
    'name': 'Invite partner to: ' + object.name,
    'model_id': self.pool['ir.model'].search(cr,uid,[('model','=','res.partner')],context=context)[0],
    'state': 'code',
    'code': mycode
}
serv_action_id = sa_obj.create(cr,uid,sa_res,context=context)
sa_obj.browse(cr,uid,serv_action_id,context=context).create_action()

#in fact, it's a server action that creates another server action that is made for adding contacts to the event you just confirmed.
#at the end of the action, you'll see it's adding the freshly created server action to the "more" menu of the res.partner
