from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set the upload folder path
app.config['UPLOAD_FOLDER'] = r"D:\sathish.vs\bankpage_hackathon\INPUT_IMAGE"

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def hoster():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="#10773.R",
        database="loan_application_db"
    )

@app.route('/')
def index():
    return render_template('confirm.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Retrieve form data
        bank_name = request.form.get('bank-name')
        application_number = request.form.get('application-number')
        application_date = request.form.get('application-date')
        full_name = request.form.get('full-name')
        age = request.form.get('age')
        dob = request.form.get('dob')
        email = request.form.get('email')
        phone = request.form.get('phone')
        father_name = request.form.get('fathername')
        mother_name = request.form.get('mothername')
        nationality = request.form.get('nationality')
        state = request.form.get('state')
        district = request.form.get('district')
        area = request.form.get('area')
        street_name = request.form.get('street-name')
        pincode = request.form.get('pincode')
        loan_purpose = request.form.get('loan-purpose')
        loan_amount = request.form.get('loan-amount')
        loan_term = request.form.get('loan-term')

        # Save uploaded files
        files = {
            'photo': request.files['photo-upload'],
            'income_proof': request.files['income-proof'],
            'aadhar_proof': request.files['aadhar-proof'],
            'digital_sign': request.files['digital-sign']
        }

        for key, file in files.items():
            if file and file.filename:
                # Sanitize filename to avoid invalid characters
                filename = file.filename.replace(" ", "_")
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                try:
                    file.save(file_path)
                except OSError as e:
                    logging.error(f"Failed to save {key} at {file_path}: {e}")
                    return f"Failed to save {key}: {e}", 500

        # Connect to the database
        conn = hoster()
        cursor = conn.cursor()

        # Insert form data into the database
        insert_query = """
        INSERT INTO loan_applications 
        (bank_name, application_number, application_date, full_name, age, dob, email, phone, father_name, mother_name,
        nationality, state, district, area, street_name, pincode, loan_purpose, loan_amount, loan_term) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (
            bank_name, application_number, application_date, full_name, age, dob, email, phone, father_name, mother_name,
            nationality, state, district, area, street_name, pincode, loan_purpose, loan_amount, loan_term
        ))

        # Commit the transaction
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

        logging.info("Data inserted successfully into the database.")

        return "Form submitted successfully!"

    except mysql.connector.Error as err:
        logging.error(f"Database error: {err}")
        return f"Database error: {err}", 500
    except Exception as e:
        logging.error(f"An error occurred during form submission: {e}")
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
