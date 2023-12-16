# Flask RESTful API

## Overview

This Flask application is a RESTful API that manages items, stores, tags, and user-related operations. The API utilizes Flask-Restful, SQLAlchemy for database interactions, and JSON Web Tokens (JWT) for user authentication.

# Project Structure

# Resources

1. **items.py**
   - Flask RESTful resource for handling operations on items.
   - Endpoints: GET, DELETE, UPDATE specific items, GET all items.

2. **stores.py**
   - Flask RESTful resource for handling operations on stores.
   - Endpoints: GET, DELETE, UPDATE specific stores, GET all stores.

3. **tags.py**
   - Flask RESTful resource for handling operations on tags.
   - Endpoints: GET tags in a store, POST a tag to a store, POST linking tags to items, DELETE a tag.

4. **users.py**
   - Flask RESTful resource for handling user-related operations.
   - Endpoints: User registration, login, token refresh, logout, user retrieval.




# Models

## ItemModel

### Description
The `ItemModel` represents an item in the store. It is designed to store information such as the item's name, description, price, and the store it belongs to. The model also handles the relationships with tags through a many-to-many relationship using the `ItemTags` model.

### Properties
- `id`: Integer, Primary Key, unique identifier for the item.
- `name`: String, unique name of the item.
- `description`: String, description of the item.
- `price`: Float, price of the item.
- `store_id`: Integer, Foreign Key (references `stores.id`), the ID of the store to which the item belongs.
- `store`: Relationship with `StoreModel`, representing the store to which the item belongs.
- `tags`: Relationship with `TagModel`, representing the tags associated with the item.

## ItemTags

### Description
The `ItemTags` model establishes a many-to-many relationship between items and tags. It serves as a link between `ItemModel` and `TagModel`.

### Properties
- `id`: Integer, Primary Key, unique identifier for the item-tag relationship.
- `item_id`: Integer, Foreign Key (references `items.id`), the ID of the item in the relationship.
- `tag_id`: Integer, Foreign Key (references `tags.id`), the ID of the tag in the relationship.

## StoreModel

### Description
The `StoreModel` represents a store in the system. It includes information about the store's name and maintains relationships with items and tags associated with the store.

### Properties
- `id`: Integer, Primary Key, unique identifier for the store.
- `name`: String, unique name of the store.
- `items`: Relationship with `ItemModel`, representing the items associated with the store.
- `tags`: Relationship with `TagModel`, representing the tags associated with the store.

## TagModel

### Description
The `TagModel` represents a tag that can be associated with items. It includes information about the tag's name and maintains relationships with items and the store to which it belongs.

### Properties
- `id`: Integer, Primary Key, unique identifier for the tag.
- `name`: String, unique name of the tag.
- `store_id`: Integer, Foreign Key (references `stores.id`), the ID of the store to which the tag belongs.
- `store`: Relationship with `StoreModel`, representing the store to which the tag belongs.
- `items`: Relationship with `ItemModel`, representing the items associated with the tag.

## UserModel

### Description
The `UserModel` represents a user in the system. It includes information about the user's username and password.

### Properties
- `id`: Integer, Primary Key, unique identifier for the user.
- `username`: String, unique username of the user.
- `password`: String, hashed password of the user.


## Usage

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:

   ```bash
   python app.py
   ```

3. Access the API at `http://localhost:5000`.


### Items

- **GET /item/<int:item_id>**: Get a specific item by item_id.

- **DELETE /item/<int:item_id>**: Delete a specific item by item_id (requires admin privilege).

- **PUT /item/<int:item_id>**: Update a specific item by item_id.

- **GET /item**: Get all items.

- **POST /item**: Create a new item.

### Stores

- **GET /store/<int:store_id>**: Get a specific store by store_id.

- **DELETE /store/<int:store_id>**: Delete a specific store by store_id (requires admin privilege).

- **PUT /store/<int:store_id>**: Update a specific store by store_id.

- **GET /store**: Get all stores.

- **POST /store**: Create a new store.

### Tags

- **GET /store/<int:store_id>/tag**: Get all tags in a specific store by store_id.

- **POST /store/<int:store_id>/tag**: Create a new tag in a specific store by store_id.

- **POST /item/<int:item_id>/tag/<string:tag_id>**: Add a specific tag to a specific item.

- **DELETE /item/<int:item_id>/tag/<string:tag_id>**: Remove a specific tag from a specific item.

- **GET /tag/<int:tag_id>**: Get a specific tag by tag_id.

- **DELETE /tag/<int:tag_id>**: Delete a specific tag by tag_id.

### Users

- **POST /register**: Register a new user.

- **POST /login**: Log in a user.

- **POST /refresh**: Refresh the access token.

- **POST /logout**: Log out a user.

- **GET /user/<int:user_id>**: Get a specific user by user_id.

- **DELETE /user/<int:user_id>**: Delete a specific user by user_id (requires admin privilege).


## Dependencies

- Flask
- Flask-Restful
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Passlib
- Flask-Smorest
- python-Dotenv
- SQLAlchemy
- Flask-Migrate
- Gunicorn
- Blocklist
- Psycopg2-Binary

## Contributing

Feel free to contribute to the development of this project. Create a pull request or open an issue for discussions.

## License

This project is licensed under the [GNU General Public License](LICENSE).


## Notes

- The API uses JWT for user authentication, and certain endpoints require admin privileges.
- Error handling is implemented to provide informative responses.
- The API is designed to manage stores, items, tags, and user authentication in a secure and efficient manner.

Feel free to explore the different endpoints and functionalities provided by the API!


## AUTHOR

- **Ogundare Olamide Emmanuel**
  - **GitHub:** [EmyCodes](https://github.com/EmyCodes)
  - **Twitter:** [@EmyCodes](https://twitter.com/EmyCodes)
  - **LinkedIn:** [EmyCodes](https://linkedin.com/in/emycodes)
