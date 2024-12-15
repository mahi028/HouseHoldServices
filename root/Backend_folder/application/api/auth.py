from application.modules.commit import commitdb, adddb, rollbackdb
from application.modals import  User
from application.modules.hash import hashpw
from flask import jsonify, request, current_app, abort
from flask_restful import Resource, marshal_with, fields, marshal
from flask_jwt_extended import create_access_token , current_user , jwt_required, set_access_cookies, unset_jwt_cookies 
from application.modules.RBAC import csrf_protected
from application.form import LoginForm, RegisterForm
from flask_wtf.csrf import generate_csrf
from werkzeug.utils import secure_filename
from uuid import uuid4
import os

user_feilds = {
    "id": fields.Integer,
    "user_name" : fields.String,
    "role": fields.Integer,
    "email" : fields.String,
    "name" : fields.String,
    "profile_picture_path" : fields.String,
}

class Auth(Resource):
    def get(self):
        """Returns CSRF Tokens for Non-Jwt-Protected Routes"""
        token = generate_csrf()
        return jsonify({'csrf_token': token})

    @csrf_protected
    def post(self):
        """Login"""
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(user_name = form.user_name.data, flag_status = False).one_or_404()
            if user and user.check_pw(form.password.data):   
                response = jsonify({"msg": "login successful", 'user': marshal(user, user_feilds)})
                access_token = create_access_token(identity=user)
                set_access_cookies(response, access_token)
                return response
            abort(401, description='Wrong Credentials or Used if Banned')
        print(form.errors)
        abort(400, description='Please provide all required details')

    @jwt_required()
    def delete(self):
        response = jsonify({"msg": "logout successful"})
        unset_jwt_cookies(response)
        return response

class UserAPI(Resource):
    @jwt_required()
    @marshal_with(user_feilds)
    def get(self):
        user = current_user
        return user

    @csrf_protected
    def post(self):
        """Register"""
        form = RegisterForm()

        if form.validate_on_submit():
            user = User.query.filter((User.user_name == form.user_name.data) | (User.email == form.email.data)).first()

            if user:
                abort(409, description="User Already Exist")
            
            if int(form.role.data) == 1:
                admin = User.query.filter_by(role = 1).first()
                if admin:
                    abort(409, description="AdminAlreadyExist")

            if form.password.data != form.conf_password.data:
                abort(409, description="PasswordDidNotMatch")
            
            image_file = request.files.get('image')

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
                
            new_user = User(user_name = form.user_name.data,
                            email = form.email.data, 
                            password = hashpw(form.password.data),
                            name = form.name.data,
                            contact_number = form.contact_num.data,
                            role = form.role.data,
                            profile_picture_path = "http://localhost:5000/static/upload/" + new_image_name
                            )
            try:
                image_file.save(image_path) 
                adddb(new_user)
                commitdb()

            except Exception as err:
                print(err)
                rollbackdb()
                abort(500)

            else:
                return "Success"#chnage it to json
        print(form.errors)
        abort(400, description="Invalid or Missing parameters")