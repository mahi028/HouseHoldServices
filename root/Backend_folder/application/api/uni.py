from application.modals import  User, ServicePro, Customer, Service
from flask import jsonify, request, abort
from flask_restful import Resource, marshal_with, fields, marshal
from flask_jwt_extended import current_user, jwt_required
from application import cache
from sqlalchemy.orm import joinedload
professional_fields = {
    "id": fields.Integer,
    "desc" : fields.String,
    "serv_id": fields.Integer,
    "service.name": fields.String,
    "user.contact_number": fields.String,
    "user.name": fields.String,
    "experience" : fields.Integer,
    "service_area_pin_code" : fields.Integer,
    "status": fields.String,
    "rating": fields.String,
    "user.flag_status": fields.Boolean,
}

cust = {
    "pin_code":fields.Integer
}
    
class GetProfessionalDetails(Resource):
    @jwt_required()
    @cache.memoize(20)
    @marshal_with(professional_fields)
    def get(self):
        serv_id = request.args.get('serv_id') if request.args.get('serv_id') != 'null' else None
        name = request.args.get('name') if request.args.get('name') != 'null' else None
        role = current_user.role
        pin_code = None

        if role == 3:
            x = marshal(current_user.customer, cust)
            pin_code = x[0]['pin_code']

        if serv_id:
            if role == 1:
                service_pro = ServicePro.query.filter_by(serv_id= serv_id).all()
            else:
                service_pro = ServicePro.query.filter(
                                    ServicePro.serv_id == serv_id,
                                    ServicePro.service_area_pin_code == pin_code,
                                    ServicePro.status == 'Approved',
                                    User.flag_status == False
                                ).all()
                
            if service_pro:
                return service_pro
            abort(404, description="ProfessionalNotFound")

        if name:
            services = Service.query.filter(Service.name.like(f'%{name}%')).all()
            service_pros = []
            for service in services:
                if role == 1:
                    service_pro = ServicePro.query.filter_by(serv_id = service.serv_id).all()
                else:
                    service_pro = ServicePro.query.filter(
                                        ServicePro.serv_id == serv_id,
                                        ServicePro.service_area_pin_code == pin_code,
                                        ServicePro.status == 'Approved',
                                        User.flag_status == False  # Ensure the flag_status is False
                                    ).all()

                if service_pro:
                    service_pros.append(service_pro) 
            if service_pros:
                return service_pros
            abort(404, description="ProfessionalNotFound")

        service_pros = ServicePro.query.all()
        if service_pros:
            return service_pros
        abort(404, description="ProfessionalNotFound")

class Profile(Resource):
    @jwt_required()
    def get(self, id):
        user = User.query.get(id)
        role = user.role
        # if current_user.role == 1 or service_pro.status == 'Approved' or current_user.id == service_pro.id:

        match role:
            case 1:
                admin = User.query.get(id)
                if admin:
                    return jsonify({
                        "id": admin.id,
                        "user_name": admin.name,
                        "role": admin.role,
                        "email": admin.email,
                        "name": admin.name,
                        "contact_num": admin.contact_number,
                        "date_created": admin.date_created,
                        "profile_picture_path": admin.profile_picture_path,
                    })
                abort(404, 'AdminNotfound')
            case 2:
                service_pro = ServicePro.query.get(id)

                return jsonify({
                    "id": service_pro.id,
                    "service_pro_uid": service_pro.service_pro_uid,
                    "desc": service_pro.desc,
                    "serv_id": service_pro.serv_id,
                    "serv_name": service_pro.service.name,
                    "experience": service_pro.experience,
                    "service_area_pin_code": service_pro.service_area_pin_code,
                    "id_document_url": service_pro.id_document_url,
                    "status": service_pro.status,
                    "rating": service_pro.rating,
                    "user_name": service_pro.user.user_name,
                    "role": service_pro.user.role,
                    "email": service_pro.user.email,
                    "name": service_pro.user.name,
                    "contact_num": service_pro.user.contact_number,
                    "date_created": service_pro.user.date_created,
                    "profile_picture_path": service_pro.user.profile_picture_path,
                    "flag_status":service_pro.user.flag_status
                })
            
            case 3:
                cust = Customer.query.get(id)
                return jsonify({
                    "id": cust.id,
                    "cust_uid": cust.cust_uid,
                    "pin_code": cust.pin_code,
                    "address": cust.address,
                    "user_name": cust.user.name,
                    "role": cust.user.role,
                    "email": cust.user.email,
                    "name": cust.user.name,
                    "contact_num": cust.user.contact_number,
                    "date_created": cust.user.date_created,
                    "profile_picture_path": cust.user.profile_picture_path,
                    "flag_status":cust.user.flag_status
                })