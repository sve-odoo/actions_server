# In this example, create a "Sequence Code" in the Odoo Configuration, named "article" and a sequence linked to this code
# For example, this server action can be called by an automated action "On Creation" on the model Product.product.
object.write({'default_code': pool['ir.sequence'].next_by_code(cr, 1, 'article',context)})