# Set the body of the message
body = u'<p>Bonjour,</p><p>Ce message pour vous signaler que votre contact <b>' + object.name +  
	u'</b> a un statut indéterminé. Pourriez-vous mettre à jour cette information dans le système ?</p>' +
	u'<p><i>Envoyé par le système OpenERP de XXXX.</i></p>'
# Set the subject of the message
subject = u'Question concernant le contact ' + object.name
# Send the message to all followers of the current object. The "1" means the the sender will be the admin. 
# Put "uid" instead if you want the message to be sent by the current user.
self.message_post(cr, 1, object.id, body=body, subject=subject, type='comment', subtype='mail.mt_comment')