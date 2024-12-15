from application import db
from application.modules.commit import commitdb, adddb, rollbackdb
from application.modals import ServicePro, Feedback, Service, ServiceRequest
from flask import jsonify,  abort, send_file
from flask_restful import Resource, marshal_with, fields, marshal
from flask_jwt_extended import current_user, jwt_required
from application.modules.RBAC import admin_required, cust_required, pro_required
from application.form import ServiceRqstForm, CloseServiceForm, FeedbackForm
from application.modules import tasks
from application import cache
from celery.result import AsyncResult
from sqlalchemy import func, desc

service_fields = {
    'serv_id': fields.Integer, 
    'name': fields.String,
    'desc': fields.String,
    'base_price': fields.Integer,
    'min_time': fields.Integer,
    'image_url': fields.String,
}

rqst_fields = {
    'rqst_id': fields.Integer,
    'cust_id': fields.Integer,
    'customer.user.name': fields.String,
    'service.name': fields.String,
    'serv_pro_id': fields.String,
    'service_pro.user.name': fields.String,
    'service_msg': fields.String,
    'status': fields.String,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'completed_at': fields.DateTime,
    'total_cost': fields.String,
}

feedback_fields = {
    "rqst_id": fields.Integer,
    "serv_pro_id": fields.Integer,
    "cust_id": fields.Integer,
    "cust.user.name": fields.String,
    "feedback_by": fields.String,
    "feedback_id": fields.String,
    "feedback_rating": fields.Integer,
    "feedback_comment": fields.String
}

class Services(Resource):
    # @cache.cached(100, 'get_services')
    @marshal_with(service_fields)
    def get(self):
        services = Service.query.all()
        return services

class GetService(Resource):
    @cache.memoize(20)
    @marshal_with(service_fields)
    def get(self, serv_id):
        service = Service.query.get(serv_id)
        return service
    
class CreateServiceRequest(Resource):
    @jwt_required()
    @marshal_with(rqst_fields)
    def get(self):
        
        match current_user.role:
            case 1:
                service_requests = ServiceRequest.query.all()

            case 2:
                service_requests = ServiceRequest.query.filter_by(serv_pro_id = current_user.id).all()

            case 3:
                service_requests = ServiceRequest.query.filter_by(cust_id= current_user.id).all()

        return service_requests


    @cust_required
    def post(self, serv_pro_id):
        serv_pro = ServicePro.query.get(serv_pro_id)
            
        if not serv_pro:
            abort(404, descrption="ProfessionalNotFound")

        if serv_pro.status != 'Approved' or serv_pro.user.flag_status:
            abort(401, desription="Professional Either Not Approved or is flagged")

        form = ServiceRqstForm()
        if form.validate_on_submit():
            new_rqst = ServiceRequest(cust_id = current_user.id, 
                                    serv_pro_id = serv_pro.id,
                                    serv_id = serv_pro.serv_id,
                                    service_msg = form.service_msg.data,
                                    )
            try:
                adddb(new_rqst)
                commitdb()
            except Exception as err:
                print(err)
                rollbackdb()
                abort(500)
            else:
                return jsonify({"msg":"Success"})
        print(form.errors)
        abort(400, description="FormError")

    def patch(self, rqst_id, action):
        rqst = ServiceRequest.query.get(rqst_id)

        if not rqst:
            abort(404, description="Request Not Found")
            
        rqst.changeStatus(action)
        return jsonify({'msg':"Success"})

class CompleteRequest(Resource):
    @pro_required
    def post(self, rqst_id):
        rqst = ServiceRequest.query.get(rqst_id)
        if not rqst:
            abort(404, description="Request Not Found")

        form = CloseServiceForm()
        if form.validate_on_submit():
            rqst.changeStatus('complete', ext_cost = int(form.ext_cost.data))
            return jsonify({'msg':"Success"})

        print(form.errors)
        abort(400, description="Invalid or missing Params")

class FeedbackApi(Resource):
    @marshal_with(feedback_fields)
    def get(self, serv_pro_id):
        feedbacks = Feedback.query.filter_by(serv_pro_id = serv_pro_id).all()
        return feedbacks

    @jwt_required()
    def post(self, rqst_id):
        rqst = ServiceRequest.query.get(rqst_id)

        if not rqst:
            abort(404, description="Request Not Found")
        if rqst.status == "Completed" or rqst.status == "Cancelled":

            form = FeedbackForm()
            if form.validate_on_submit():
                if int(form.feedbackRating.data) >= 1 and int(form.feedbackRating.data) <= 5:
                    try:
                        feedback = Feedback(rqst_id = rqst_id, serv_pro_id = rqst.serv_pro_id, cust_id = rqst.cust_id, feedback_by = current_user.role, feedback_comment = form.feedback.data, feedback_rating = int(form.feedbackRating.data))
                        adddb(feedback)
                        commitdb()

                        avg_rating = (
                                    db.session.query(func.avg(Feedback.feedback_rating))
                                    .filter(Feedback.feedback_by == 3)
                                    .scalar()  # Returns a single scalar value (the average rating)
                                )
                        
                        feedback.service_pro.rating = avg_rating if avg_rating else feedback.feedback_rating
                        commitdb()
                        
                    except Exception as err:
                        rollbackdb()
                        print(err)
                        abort(500)


                    return jsonify({'msg':"Success"})
                
            print(form.error)
            abort(400, description="Invalid or missing Params")
        abort(409, description="ServiceNOtComplete")


class ServiceReport(Resource):
    @admin_required
    def get(self, task_id):
        res = AsyncResult(task_id)

        if res.ready():
            print('complete')
            return send_file(res.result, as_attachment=True)
        
        abort(421, description="TaskPending")
    
    
    @admin_required
    def post(self):
        service_requests = ServiceRequest.query.all()
        if not service_requests:
            abort(404, description="No Service Request")
        task = tasks.makeServiceReport.delay()
        return  jsonify({"msg":"Success", 'task_id':task.id})
    