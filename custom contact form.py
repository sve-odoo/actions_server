#When customizing the contact form, this server action can be used to actually fill fields in the crm.lead
#This server action should be called by an "on creation" automated action on the "crm.lead" model

#You can just customize the name of the contact form field (label) and the crm.lead field to fill (field_to_fill)

label = 'street'
field_to_fill = 'street'

if object.description:
	descr = object.description
	label_start = descr.find(label+':')
	if label_start != -1:
		content_start = label_start + len(label) + 2
		content_end = descr.find('\n',content_start)
		if content_end == -1:
		    content = str(descr[content_start:])
		else:
		    content = str(descr[content_start:content_end])
		object.write({field_to_fill:content})