# Add the link to the "Banque carrefour des entreprises" company page.
# Prerequisite:
#1-Create a field x_bce , string on res_partner
#2-Create a field x_lien_bcp, string on res_partners
# View suggestion:
# <data>
# <field name="website" position="after">
#     <field name="x_bce" attrs="{'invisible': [('is_company', '=', False)]}"/>
# </field>
# <notebook position="before">
#     <group>
#         <field name="x_lien_bce" widget="url" attrs="{'invisible': ['|',('is_company', '=', False),('x_bce', '=', False)]}" readonly="True" colspan="2" />
#     </group>
# </notebook>
# <data>


if object.x_bce:
    full_string = object.x_bce.replace(".", "")
    for ch in full_string:
        if ch != '0':
        	break
        full_string = full_string[1:]
    object.write({'x_lien_bce': 'http://kbopub.economie.fgov.be/kbopub/toonondernemingps.html?lang=fr&ondernemingsnummer='+full_string})
else:
    object.write({'x_lien_bce': False})