import time
import os
import json
from flask import Flask, request, jsonify
from models import users
from cache import rds, make_token, rds_hmset
import constant as cs
from openpyxl import Workbook
import pdfkit
from PyPDF2 import PdfReader, PdfWriter
users = users.Users()
def extendApplication(app):
    @app.route('/users/login', methods=['POST'])
    def login_user():
        if request.method == "POST":
            email = request.json.get('email')
            password = request.json.get('password')
            res = users.find_one({'email': email, 'password': password});
            print(email, password)

            if res['_id'] is False:
                return jsonify({'message': 'invalid email or password'}), 404

            token = make_token(email,res['_id'])
            rds_hmset(email, token)
            return jsonify({"token": token, "email": email}), 200

    @app.route('/upload/<string:user_id>/', methods=['POST'])
    def upload_file(user_id):
        name = request.values.get('filename')
        file = request.files['file']
        tail = allowed_file(file.filename)
        if file and tail:
            now = int(time.time())
            filename = name + '_' + str(now) + '.%s' % tail
            file.save(os.path.join('D:\python_mongodb\public', filename))
            response = users.updateOne(user_id, {'profile': filename})
            return jsonify(response), 200
        else:
            return jsonify({}), 200

    @app.route('/users', methods=['GET'])
    def get_users():
        return jsonify(users.find({})), 200

    @app.route('/users/fetch/<string:user_id>/', methods=['GET'])
    def get_user(user_id):
        return users.find_by_id(user_id), 200

    @app.route('/users/cretae', methods=['POST'])
    def add_users():
        if request.method == "POST":
            object = {
                'name': request.json.get('name'),
                'email': request.json.get('email'),
                'mobile': request.json.get('mobile'),
                'password': request.json.get('password'),
                'dob': request.json.get('dob')
            }

            print('object----',object)

            response = users.create(object)
            return response, 201

    @app.route('/users/update/<string:user_id>/', methods=['PUT'])
    def update_tasks(user_id):
        if request.method == "PUT":
            print('request.json---',user_id,request.json)
            name = request.json.get('name')
            mobile = request.json.get('mobile')
            response = users.update(user_id, {'name': name, 'mobile': mobile})
            return response, 201

    @app.route('/users/delete/<string:user_id>/', methods=['DELETE'])
    def delete_tasks(user_id):
        if request.method == "DELETE":
            users.delete(user_id)
            return "Record Deleted"
        
    @app.route('/users/downloadExcel', methods=['POST'])
    def download_users():
        if request.method == "POST":
            userList = users.find({}, {"_id":0, "name":1, "email":1, "mobile":1, "password": 1})
            print('-----',userList)
            json_data = json.dumps(userList)
            data = json.loads(json_data)

            # Create a new Workbook
            wb = Workbook()

            # Select the active worksheet
            ws = wb.active

            # Write header row
            header = list(data[0].keys())
            ws.append(header)

            # Write data rows
            for item in data:
                row = [item[key] for key in header]
                ws.append(row)

            # Save the workbook
            wb.save("example.xlsx")

            return "download sucess"
        
    @app.route('/users/downloadPDF', methods=['POST'])
    def download_pdf():
        if request.method == "POST":
            # install wkhtmltopdf and Specify the correct path to wkhtmltopdf.exe
            config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

            # Replace 'demo.html' with the actual path to your HTML file
            pdfkit.from_file('D:\\python_crud\\src\\router\\demo.html', 'out.pdf', configuration=config)

            input_pdf = "out.pdf"  # Path to your input PDF
            output_pdf = "out.pdf"  # Path to save the encrypted PDF

            # Set passwords
            user_password = "1234"  # Open key (user password)
            owner_password = "5678"  # Owner password (can remove restrictions)

            # Read the PDF
            reader = PdfReader(input_pdf)
            writer = PdfWriter()

            # Copy all pages to the writer
            for page in reader.pages:
                writer.add_page(page)

            # Set encryption with the passwords
            writer.encrypt(user_password=user_password, owner_password=owner_password)

            # Write the output PDF
            with open(output_pdf, "wb") as file:
                writer.write(file)

            print(f"Encrypted PDF saved as '{output_pdf}' with an open key.")

            print("PDF generated successfully!")

            return "download success"


def allowed_file(filename):
    tail = filename and '.' in filename and filename.rsplit('.', 1)[1]
    if tail and tail.lower() in cs.ALLOWED_EXTENSIONS:
        return tail
    else:
        return False