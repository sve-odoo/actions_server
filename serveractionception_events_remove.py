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
sa_ids = sa_obj.search(cr,uid,[('code','=',mycode)],context=context)
if sa_ids:
	sa_obj.unlink(cr,uid,sa_ids,context=context)
else:
	raise Warning("No server action exists for this event.")