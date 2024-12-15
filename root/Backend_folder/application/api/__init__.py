from flask_restful import Api

api = Api(prefix='/api')

from application.api.auth import UserAPI
from application.api.auth import Auth
from application.api.admin import ApprovePro, CreateServices, FlagUser, Statistics
from application.api.professional import ServiceProApi
from application.api.uni import GetProfessionalDetails, Profile
from application.api.services import Services, GetService
from application.api.cust import Cust
from application.api.services import CreateServiceRequest, ServiceReport, CompleteRequest, FeedbackApi

api.add_resource(Auth, "/get_csrf_token", "/login", "/logout")
api.add_resource(UserAPI, "/register")
api.add_resource(ApprovePro, "/professional/status/<int:id>/<string:action>")
api.add_resource(ServiceProApi, "/create/service_pro", "/get/service_pro")
api.add_resource(CreateServices, "/create/service", "/update/service/<int:serv_id>", "/delete/service/<int:serv_id>")
api.add_resource(Services, "/services")
api.add_resource(GetService, "/services/<int:serv_id>")
api.add_resource(Cust, "/get/customer", "/create/customer")
api.add_resource(GetProfessionalDetails, "/get/professionals")
api.add_resource(Profile, "/profile/<int:id>")
api.add_resource(CompleteRequest, '/request/complete/<int:rqst_id>')
api.add_resource(FeedbackApi, '/request/feedback/<int:rqst_id>', '/feedback/<int:serv_pro_id>')
api.add_resource(CreateServiceRequest, '/customer/service-requests', "/book_service/<int:serv_pro_id>", '/request/<string:action>/<int:rqst_id>')
api.add_resource(ServiceReport, "/create-report", "/get-report/<task_id>")
api.add_resource(FlagUser, "/flag-user/<int:id>")
api.add_resource(Statistics, "/dashboard/stats/<string:stat_type>")
