task_obj=self.pool.get("project.task")
if object.product_id.x_project_id and object.prodlot_id:
    values = {'project_id':object.product_id.x_project_id.id}
    if task_obj.search(cr,uid,[('name','=',object.prodlot_id.name),('project_id','=',object.product_id.x_project_id.id)],context=context) == []:
        if object.product_qty == 1:
            values['name'] = object.prodlot_id.name
            if object.picking_id.origin:
                values['x_origin'] = object.picking_id.origin           
            values['x_picking_id'] = object.picking_id.id
            if object.picking_id.x_use_date:
                values['x_use_date'] = object.picking_id.x_use_date
            if object.picking_id.x_pack_date:
                values['x_pack_date'] = object.picking_id.x_pack_date
            if object.product_id.default_code:
                values['x_sap_code'] = object.product_id.default_code
            if object.product_id.x_product_code:
                values['x_product_code'] = object.product_id.x_product_code
            values['x_location_id'] = object.location_dest_id.id
        else:
            values['name'] = "Erreur"
            values['description'] = "Un mouvement de stock ne peut créer qu'une seule tâche."
    else:
        values['name'] = "Erreur"
        values['description'] = "Une tâche existe déjà pour ce numéro de série pour cet article."
    task_id = task_obj.create(cr,uid,values,context=context)
    object.write({'x_task_id':task_id})