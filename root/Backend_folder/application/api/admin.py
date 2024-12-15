from application import db
from application.modules.commit import commitdb, adddb, deletedb, rollbackdb
from application.modals import  User, ServicePro, Service, ServiceRequest
from flask import jsonify, request, current_app, abort
from flask_restful import Resource, fields
from application.modules.RBAC import admin_required
from application.form import UpdateService, CreateServiceForm
from werkzeug.utils import secure_filename
from uuid import uuid4
import os
from sqlalchemy import func

user_feilds = {
    "id": fields.Integer,
    "user_name" : fields.String,
    "role": fields.Integer,
    "email" : fields.String,
    "name" : fields.String,
    "profile_picture_path" : fields.String,
}

class ApprovePro(Resource):
    @admin_required
    def post(self, id, action):
        pro = ServicePro.query.get(id)
        if not pro:
            abort(404, description="ProfessionalNotFound")    
        pro.approval_status(action)
        return jsonify({"msg":"Success"})
    
class FlagUser(Resource):
    @admin_required
    def post(self, id):
        user = User.query.get(id)
        if not user:
            abort(404, description="UserNotFound")    
        flag = user.updateFlag()
        return jsonify({"msg":"Success","flag":flag})

class CreateServices(Resource):
    @admin_required
    def post(self):
        form = CreateServiceForm()
        
        image_file = request.files.get('image')
        print(image_file)
        image_path = None
        new_image_name = None
        if image_file != None:
        # Create unique name for image
            unique_name = str(uuid4())
            image_ext = image_file.filename.split('.')[1] #image extension
            new_image_name = unique_name+'.'+image_ext
            image_file.filename = new_image_name
            image_filename = secure_filename(image_file.filename)
            
            upload_folder = current_app.config['UPLOAD_FOLDER']
            image_path = os.path.join(upload_folder, image_filename)

        if form.validate_on_submit():
            try:
                if image_file:
                    image_file.save(image_path) 
                new_service = Service(name = form.name.data,
                                    desc = form.desc.data,
                                    base_price = int(form.base_price.data),
                                    min_time = int(form.min_time.data),
                                    image_url = "http://localhost:5000/static/upload/" + new_image_name if image_file else None
                                    )
                adddb(new_service)
                commitdb()

            except Exception as err:
                rollbackdb()
                print(err)
                abort(500)
            
            else:
                return jsonify({'msg': 'success'})
        print(form.errors)
        abort(400, description="Wrong or missing parameters")
    
    @admin_required
    def patch(self, serv_id):
        service = Service.query.get(serv_id)

        if not service:
            abort(404, description="ServiceNotFound")

        form = UpdateService()

        image_file = request.files.get('image')
        image_path = None
        new_image_name = None
        old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], service.image_url.strip().split('/')[-1])

        if form.validate_on_submit():
            image_path = None
            new_image_name = None
            if image_file != None:
            # Create unique name for image
                unique_name = str(uuid4())
                image_ext = image_file.filename.split('.')[1] #image extension
                new_image_name = unique_name+'.'+image_ext
                image_file.filename = new_image_name
                image_filename = secure_filename(image_file.filename)
                
                upload_folder = current_app.config['UPLOAD_FOLDER']
                image_path = os.path.join(upload_folder, image_filename)

                service_image_name = service.image_url.strip().split('/')[-1]

            msg = service.updateServices(form, "http://localhost:5000/static/upload/" + new_image_name if image_file else None)

            image_file.save(image_path)
            if image_file and not service_image_name == "service.jpeg":
                os.remove(old_image_path)

            return jsonify(msg)
        print(form.errors)
        abort(400, description=form.errors)

    @admin_required
    def delete(self, serv_id):
        service = Service.query.get(serv_id)

        if service:
            try:
                service_image_name = service.image_url.strip().split('/')[-1]
                if not service_image_name == "service.jpeg":
                    old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], service.image_url.strip().split('/')[-1])
                    os.remove(old_image_path)

                deletedb(service)
                commitdb()
            except Exception as err:
                rollbackdb()
                print(err)
                abort(500)
            else:
                return jsonify({"msg":"Success"})
        abort(404, description="ServiceNotFound")

class Statistics(Resource):
    def get(self, stat_type):
        match stat_type:
            case 'service':
                services = Service.query.group_by(Service.name).all()
                service_names = []
                service_stats = []

                for service in services:
                    service_names.append(service.name)
                    service_stats.append(len(service.service_pro))

                return jsonify({'labels': service_names, "stats":service_stats})

            case 'service_request':
                services = Service.query.group_by(Service.name).all()
                service_names = []
                service_stats = []

                for service in services:
                    service_names.append(service.name)
                    service_stats.append(len(service.service_request))

                return jsonify({'labels': service_names, "stats":service_stats})

            case 'request':
                stats = (
                    db.session.query(ServiceRequest.status, func.count(ServiceRequest.rqst_id))
                    .group_by(ServiceRequest.status)
                    .all()
                )
                
                status_array = [status for status, _ in stats]
                count_array = [count for _, count in stats]
                
                return jsonify({"labels": status_array, "stats": count_array})
                
            case _:
                pass