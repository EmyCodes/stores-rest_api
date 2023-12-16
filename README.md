## stores-rest_api README

# Overview

    This repository contains a Flask RESTful API for managing stores, items, tags, and user authentication. The API uses Flask-Smorest for creating a RESTful API, Flask-JWT-Extended for user authentication, and SQLAlchemy for interacting with a relational database.

# Project Structure
    **resources/**: Contains the main code files for different resources like items, stores, tags, and users.
        **item_resource.py**: Defines the RESTful API endpoints for managing items.
        **store_resource.py**: Defines the RESTful API endpoints for managing stores.
        **tag_resource.py**: Defines the RESTful API endpoints for managing tags.
        **user_resource.py**: Defines the RESTful API endpoints for user registration, login, and management.

    **db.py**: Contains the configuration for the SQLAlchemy database.

    **blocklist.py**: Manages the blocklist for JWT tokens to handle user logout.

    **models.py**: Defines the SQLAlchemy models for the database tables.

    **schemas.py**: Contains the marshmallow schemas for serializing and deserializing data.

# Dependencies

    Flask
    Flask-Smorest
    Flask-JWT-Extended
    SQLAlchemy
    Passlib
    Marshmallow