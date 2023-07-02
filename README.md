## Crud Operation Using Flask server, jwt and mongo db.  

### install requirements
```sh
pip install -r requirements.txt
```
### Configure Database
#### From [db_config.json](src/db_config.json) configure datbase url, name, user and password 
```json
 {
   "db": {
            "url" : "mongodb://localhost:27017/",
            "name" :"db_name",  
            "user" :"",
            "password" :""
    }
 }
``` 

## In model update collection name and desire fields name and fields type. For example see users [model](src/models/users.py) file
#### From [model](src/models) folder write your individual model and configure db collection name, fields name and fields type
#### Example
##### In users [model](src/models/users.py) update collection name, fields name and fields type
```py
table_name = 'users'   # collection name
fields = {   
    "name": "string",
    "email":"string",
    "mobile": "number",
    "password": "string",
    "dob": "datetime",
    "profile": "string"
} 
```
#### List of users Routes
| Request | Endpoint |  Details |
| --- | --- | --- |
| `GET` | `http://127.0.0.1:5000/users`| Get All users|
| `GET` | `http://127.0.0.1:5000/users/user_id`| Get Single user|
| `POST` | `http://127.0.0.1:5000/users/cretae`| Insert One user|
| `PUT` | `http://127.0.0.1:5000/users/update/user_id`| Update One user|
| `DELETE` | `http://127.0.0.1:5000/users/update/user_id`| Delete One user|
| `POST` | `http://127.0.0.1:5000/upload/user_id`| update profile|
| `DELETE` | `http://127.0.0.1:5000/users/login`| login|
- To see route list type cli `flask routes`

### Lets run the App
```sh
python app.py
```
