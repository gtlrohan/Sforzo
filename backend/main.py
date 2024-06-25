from flask import Flask, jsonify, request
import json
import os
from flask_cors import CORS
import requests
import pymongo
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

DB_NAME = "store_data"
COLLECTION_NAME = "patient_data"
client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.route("/")
def index():
    return jsonify({"message": "Welcome to Patient's data"})


@app.route("/load_data", methods=['GET'])
def load_data():
    # Using projection to exclude the _id field
    data = list(collection.find({}, {'_id': 0}))
    return jsonify({"data": data})



@app.route('/user_data/<int:user_id>')
def get_user_data(user_id):
    user = collection.find_one({"PatientID": user_id}, {'_id': 0})
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404


@app.route('/proxy-to-strataemr', methods=['POST'])
def proxy_to_strataemr():
    try:
        # Extract data from the request body
        data = request.json

        # Create a dynamic XML payload using the extracted data
        xml_payload = f"""<?xml version="1.0" encoding="utf-8"?>
        <Requests>
            <Header>
                <APIKey>cc7f22956f3811b029c83d938fc278e6-SDSMedicalTesting</APIKey>
            </Header>
            <ReferralRequest>
                <Organization>SDSMedical</Organization>
                <PartnerPrivateID></PartnerPrivateID>
                <FirstName>{data['Firstname']}</FirstName>
                <LastName>{data['Lastname']}</LastName>
                <MiddleInitial></MiddleInitial>
                <BirthDate>{data['DOB']}</BirthDate>
                <PatientStreetAddress>{data['Streetaddress']}</PatientStreetAddress>
                <PatientCity>{data['City']}</PatientCity>
                <PatientState>{data['State']}</PatientState>
                <PatientZip>{data['Zipcode']}</PatientZip>
                <Gender>{'1' if data['Gender'] == 'Male' else '0'}</Gender>
                <PatientPhone>{data['PhoneNumber'].replace('(', '').replace(')', '').replace(' ', '').replace('-', '')}</PatientPhone>
                <EmergencyContact></EmergencyContact>
                <EmergencyContactPhone></EmergencyContactPhone>
                <CaseDescription>{data['Case_Description'] + data['policy_payer'] + data['policy_subscriber_id']} </CaseDescription>
                <PatientType>PT</PatientType>
                <ServiceLocation>11</ServiceLocation>
                <From>
                    <Name>{data['Referred_By_Name']}</Name>
                    <Email></Email>
                    <Phone></Phone>
                </From>
            </ReferralRequest>
        </Requests>"""

        encoded_payload = 'xml=' + quote(xml_payload)
        url = "https://api.strataemr.com/Referral/V1.1/"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(url, headers=headers, data=encoded_payload)
        print(response.text)
        print(response.status_code)
        return jsonify({"status": response.status_code, "response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
