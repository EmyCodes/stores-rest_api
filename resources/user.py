#!/usr/bin/python3

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token, get_jwt, jwt_required, create_refresh_token, get_jwt_identity
)

from db import db
from blocklist import BLOCKLIST
from models import UserModel
from schemas import UserSchema


# Blueprint for the Users
blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    """User Registration Class for registering users with username and password"""
    @blp.arguments(UserSchema)
    def post(self, user_data):
        """
        User Registration Endpoint
        Args:
            user_data (dict): The username and password of the user
            Returns: The user with the given username or 409 if already exists
        """
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists.")
        
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        ) # Create a new User instance

        db.session.add(user)
        db.session.commit()
        
        # return {
        #     "message": "User created Successfully!"
        # }, 201
        return [
            "User Registered Sucessfully",
            {
                "id": user.id,
                "username": user.username
            }
        ], 201



@blp.route("/login")
class UserLogin(MethodView):
    """User Login Class for logging in users with username and password"""
    @blp.arguments(UserSchema)
    def post(self, user_data):
        """
        User Login Endpoint
        Args:
            user_data (dict): The username and password of the user
            Returns: The user with the given username or 401 if invalid
        """
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first() # Get the user from the database

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token} # Return the access token
        
        abort(401, message="Invalid Creditials.")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    """Refresh Token Class for refreshing access tokens when expired"""
    @jwt_required(refresh=True)
    def post(self):
        """
        Refresh Token Endpoint for refreshing access tokens when expired
        Returns: A new access token
        """
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt(["jti"])
        BLOCKLIST.add(jti)
        return {"access_token": new_token}


@blp.route("/logout")
class UserLogout(MethodView):
    """
    User Logout Class for logging out users by adding the token to the blocklist
    """
    @jwt_required()
    def post(self):
        """
        User Logout Endpoint for logging out users by adding the token to the blocklist
        Returns: A message for successfully logging out
        """
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return { 
            "message": "Successfully logged Out"
        }


@blp.route("/user/<int:user_id>")
class User(MethodView):
    """User Class for getting and deleting users by id"""
    @blp.response(200, UserSchema)
    def get(self, user_id):
        """
        User Endpoint for getting users by id
        Args:
            user_id (int): The id of the user
            Returns: The user with the given id or 404 if not found
        """
        user = UserModel.query.get_or_404(user_id)
        return user
    
    # @jwt_required()
    def delete(self, user_id):
        """
        User Endpoint for deleting users by id
        Args:
            user_id (int): The id of the user
            Returns: The user with the given id or 401 if not admin
        """
        # jwt = get_jwt()
        # if not jwt.get("is_admin"):
        #     abort(401, message="Admin privilege reqiuired.")

        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {
            "mesaage": "User deleted"
        }, 200


# @blp.route("/user")
# class UserList(MethodView):
#     @blp.response(200, UserSchema(many=True))
#     def get(self):
#         user = UserModel.query.all()
#         return user