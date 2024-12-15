from application.modules.hash import checkpw, hashpw
from application.modules.commit import commitdb, rollbackdb
from flask import abort
from flask_restful import fields
from application import db
from uuid import uuid4 as uid
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    user_name = db.Column(db.String, unique = True, nullable = False)
    role = db.Column(db.Integer, db.ForeignKey('role.id'), nullable = False)
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.LargeBinary, nullable = False)
    name = db.Column(db.String, nullable = False)
    contact_number = db.Column(db.String, nullable = False)
    date_created = db.Column(db.Date, default = datetime.now())
    profile_picture_path = db.Column(db.String, nullable = True, default = "http://localhost:5000/static/upload/user.png")
    flag_status = db.Column(db.Boolean, nullable = False, default = False)

    roles = db.relationship('Role', backref=db.backref('user', cascade="all, delete-orphan"))

    def check_pw(self, password: str) -> bool:
        return checkpw(password, self.password)

    def change_email(self, new_email):
        # do_mail_checking
        abort(501)

    def change_pw(self, prev_pass: str, new_pass: str):
        if self.check_pw(prev_pass):
            try:
                self.password = hashpw(new_pass)
                commitdb()
                return
            except Exception as err:
                rollbackdb()
                abort(500)
        else:
            print('Wrong old Password')
            ConnectionAbortedError(401)
    
    def change_profile_pic(self, new_path: str):
        try:
            self.profile_picture_path = new_path
            # delete old pic then commit
            commitdb()
        except Exception as err:
            rollbackdb()
            print(err)
            abort(500)
    
    def updateFlag(self):
        try:
            self.flag_status = not self.flag_status
            commitdb()
        except Exception as err:
            print(err)
            abort(500)
        else:
            return self.flag_status
        
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, autoincrement = True, primary_key=True)
    role_name = db.Column(db.String, unique = True, nullable = False)

class ServicePro(db.Model):
    __tablename__ = 'service_pro'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    service_pro_uid = db.Column(db.String, unique = True, nullable = False, default = lambda: str(uid()))
    desc = db.Column(db.String, nullable = False)
    serv_id = db.Column(db.Integer, db.ForeignKey('service.serv_id', ondelete='CASCADE'))
    experience = db.Column(db.String)
    service_area_pin_code = db.Column(db.Integer, nullable = False)
    rating = db.Column(db.Integer, nullable = False, default = 0)

    #Document for varification
    id_document_url = db.Column(db.String, nullable = False)

    status = db.Column(db.String, nullable = False, default = "Approval_Pending")
 
    service = db.relationship('Service', backref=db.backref('service_pro', cascade="all, delete-orphan"))
    user = db.relationship('User', backref=db.backref('service_pro', cascade="all, delete-orphan"))

    def changedesc(self, desc):
        try:
            self.desc = desc
            commitdb()
        except Exception as err:
            rollbackdb()
            print(err)
            abort(500)

    def approval_status(self, keyword: int):
        """
            0: "Reject",
            1: "Accept",
        """
        status_dict = {"accept": "Approved",
                        "reject": "Rejected",
                  }
        if keyword not in status_dict:
            print("Keyword not Present")
            abort(404, description="KeywordNotPresent")
        
        try:
            self.status = status_dict[keyword]
            commitdb()
        except Exception as err:
            rollbackdb()
            print(err)
            abort(500)

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    cust_uid = db.Column(db.String, unique = True, nullable = False, default = lambda: str(uid()))
    pin_code = db.Column(db.Integer, nullable = False)
    address = db.Column(db.String, nullable = False)

    user = db.relationship('User', backref=db.backref('customer', cascade="all, delete-orphan"))

class Service(db.Model):
    __tablename__ = 'service'
    serv_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String, nullable = False, unique = True)
    desc = db.Column(db.String, nullable = False)
    base_price = db.Column(db.Integer, nullable = False)
    min_time = db.Column(db.Integer, nullable = False)
    image_url = db.Column(db.String, nullable = True, default = "http://localhost:5000/static/upload/service.jpeg")

    def updateServices(self, form, image_url = None):
        service_fields = {
                            'serv_id': fields.Integer, 
                            'name': fields.String,
                            'desc': fields.String,
                            'base_price': fields.Integer,
                            'min_time': fields.Integer,
                            'image_url': fields.String,
                        }
        if form.name.data:
            try:
                self.name = form.name.data
                commitdb()
            except Exception as err:
                print(err)
                rollbackdb()
                abort(500, "SomethingWentWronmg")
            
        if form.desc.data:
            try:
                self.desc = form.desc.data
                commitdb()
            except Exception as err:
                print(err)
                rollbackdb()
                abort(500, "SomethingWentWronmg")

        if form.base_price.data:
            try:
                self.base_price = int(form.base_price.data)
                commitdb()
            except Exception as err:
                print(err)
                rollbackdb()
                abort(500, "SomethingWentWronmg")
            
        if form.min_time.data:
            try:
                self.min_time = int(form.min_time.data)
                commitdb()
            except Exception as err:
                print(err)
                rollbackdb()
                abort(500, "SomethingWentWronmg")

        if image_url:
            try:
                self.image_url = image_url
                commitdb()
            except Exception as err:
                print(err)
                rollbackdb()
                abort(500, "SomethingWentWronmg")

        return {"msg":"ServiceUpdated"}
        
class ServiceRequest(db.Model):
    __tablename__ = 'service_request'
    rqst_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete='CASCADE'))
    serv_pro_id = db.Column(db.Integer, db.ForeignKey('service_pro.id', ondelete='CASCADE'))
    serv_id = db.Column(db.Integer, db.ForeignKey('service.serv_id', ondelete='CASCADE'))
    service_msg = db.Column(db.String, nullable=True)
    status = db.Column(db.String, nullable=False, default="Pending")  
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())  
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())  
    completed_at = db.Column(db.DateTime, nullable=True)  
    total_cost = db.Column(db.Float, nullable=True)  
    
    # Relationships
    customer = db.relationship('Customer', backref=db.backref('service_request', cascade="all, delete-orphan"))
    service_pro = db.relationship('ServicePro', backref=db.backref('service_request', cascade="all, delete-orphan"))
    service = db.relationship('Service', backref=db.backref('service_request', cascade="all, delete-orphan"))

    def changeStatus(self, action, ext_cost = None):
        match action:
            case "accept":
                try:
                    self.status = 'Ongoing'
                    commitdb()
                except Exception as err:
                    rollbackdb()
                    print(err)
                    abort(500)

            case "reject":
                try:
                    self.status = 'Cancelled'
                    commitdb()
                except Exception as err:
                    rollbackdb()
                    print(err)
                    abort(500)

            case "complete":
                try:
                    self.total_cost = self.service.base_price + ext_cost
                    self.status = 'Completed'
                    self.completed_at = datetime.now()
                    commitdb()
                except Exception as err:
                    rollbackdb()
                    print(err)
                    abort(500)
            case _:
                abort(400, description="Invalid Argument")

class Feedback(db.Model):
    __tablename__ = "feedback"
    feedback_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    rqst_id = db.Column(db.Integer, db.ForeignKey('service_request.rqst_id', ondelete='CASCADE'))
    serv_pro_id = db.Column(db.Integer, db.ForeignKey('service_pro.id', ondelete='CASCADE'))
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete='CASCADE'))
    feedback_by = db.Column(db.Integer, nullable=False)
    feedback_rating = db.Column(db.Integer, nullable=False)
    feedback_comment = db.Column(db.String, nullable=True)

    service_request = db.relationship('ServiceRequest', backref=db.backref('feedback', cascade="all, delete-orphan"))
    service_pro = db.relationship('ServicePro', backref=db.backref('feedback', cascade="all, delete-orphan"))
    cust = db.relationship('Customer', backref=db.backref('feedback', cascade="all, delete-orphan"))