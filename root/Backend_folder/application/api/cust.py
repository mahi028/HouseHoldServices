from application.modules.commit import commitdb, adddb, rollbackdb
from application.modals import  Customer
from flask import jsonify, abort
from flask_restful import Resource,  marshal_with, fields
from flask_jwt_extended import current_user
from application.modules.RBAC import cust_required
from application.form import CustomerRegisterationForm
from application import cache

cust_feilds = {
    "id": fields.Integer,
    "address": fields.String,
    "pin_code" : fields.Integer,
}

class Cust(Resource):
    @cust_required
    @cache.memoize(20)
    @marshal_with(cust_feilds)
    def get(self):
        cust = Customer.query.get(current_user.id)
        if cust:
            return cust
        abort(404, description="CustomerNotFound")

    @cust_required
    def post(self):
        user_id = current_user.id
        if Customer.query.get(user_id):
            abort(409, description="CustomerAlrreadyExist") 
        
        form = CustomerRegisterationForm()

        if form.validate_on_submit():
            pin_code = form.pin_code.data
            address = form.address.data
            try:
                new_cust = Customer(id = user_id, pin_code = pin_code, address = address)
                adddb(new_cust)
                commitdb()

            except Exception as err:
                rollbackdb()
                print(err)
                abort(500)
            
            else:
                return jsonify({"msg":"Success"})
        abort(400, description="FormFieldsMissing")