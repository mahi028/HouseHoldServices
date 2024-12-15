from application.modules.commit import commitdb, adddb, rollbackdb
from application.modals import  ServicePro
from flask import jsonify, request, current_app, abort
from flask_restful import Resource, marshal_with, fields
from flask_jwt_extended import current_user
from application.modules.RBAC import  pro_required
from application.form import  CreateServiceProForm
from werkzeug.utils import secure_filename
from uuid import uuid4
import os
from application import cache

pro_feilds = {
    "id": fields.Integer,
    "desc" : fields.String,
    "serv_id": fields.Integer,
    "experience" : fields.Integer,
    "service_area_pin_code" : fields.Integer,
    "status": fields.String,
    "rating": fields.Integer,
}

class ServiceProApi(Resource):   
    @pro_required
    @cache.memoize(20)
    @marshal_with(pro_feilds)
    def get(self):
        pro = ServicePro.query.get(current_user.id)

        if pro:
            return pro
        abort(404, description="ProfessionalNotFound")
         
    @pro_required
    def post(self):
        if ServicePro.query.get(current_user.id):
            abort(409, description="PrefessionalAlreadyExists")

        form = CreateServiceProForm()
        # print(form.desc)
                                
        if form.validate_on_submit():
            doc_file = request.files.get('id_document')

            if not doc_file:
                abort(400, description="Image not Provided")

            doc_path = None
            new_doc_name = None
            if doc_file != None:
            # Create unique name for image
                unique_name = str(uuid4())
                doc_ext = doc_file.filename.split('.')[1] #image extension

                #validate doc extension
                # if not doc_ext in ['pdf', 'txt']:
                #     abort(400, description="WrongFileFormat")

                new_doc_name = unique_name+'.'+doc_ext
                doc_file.filename = new_doc_name
                doc_filename = secure_filename(doc_file.filename)
                
                upload_folder = current_app.config['UPLOAD_FOLDER']
                doc_path = os.path.join(upload_folder, doc_filename)
                
            try:
                doc_file.save(doc_path)

                new_service_pro = ServicePro(
                                    id = current_user.id,
                                    desc = form.desc.data,
                                    serv_id = form.serv_id.data, 
                                    experience = form.experience.data,
                                    service_area_pin_code = form.service_area_pin_code.data,
                                    id_document_url = "http://localhost:5000/static/upload/" + new_doc_name,
                                    )
                
                adddb(new_service_pro)
                commitdb()

            except Exception as err:
                print(err)
                rollbackdb()
                abort(500, description="SomethingWentWrong")

            else:
                print("helloo")
                return jsonify({"msg":"Success"})#chnage it to json
        abort(400, description="FormDidnotValidate")
    