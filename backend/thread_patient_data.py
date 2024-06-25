import requests
import json
import pymongo
import threading
from dotenv import load_dotenv

load_dotenv()

def fetch_patient_data(start_page, end_page):
    db = "store_data"
    table = "patient_data"
    conn = pymongo.MongoClient("mongodb+srv://rohannagadiya:sPQQNqNbp2vE3A3Z@database.56qutkr.mongodb.net/")
    mydb = conn[db]
    conn = mydb[table]

    for page in range(start_page, end_page):
        url = f"https://sdsortho.ema.md/ema/ws/v3/patients?selector=lastName,firstName,mrn,pmsId,dateOfBirth,preferredPhoneNumber,phoneNumbers,email,establishedPatient,dateLastVisit,encryptedId,statementNumber&where=&paging.pageSize=25&paging.pageNumber={page}&sorting.sortBy=lastName&sorting.sortOrder=ASC&showInactive=false"
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=E32F4FDE38F04167801E08FD398E5BEE; CSID=HZFF064F9A5F7C4574BEC52B2CDFE1A0F7; gdpr=provider; AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; OAuth_Token_Request_State=55c674a8-3c56-49aa-8493-70ab06ac5ea5; _hp2_ses_props.2907378054=%7B%22ts%22%3A1715257429104%2C%22d%22%3A%22sdsortho.ema.md%22%2C%22h%22%3A%22%2Fema%2Fweb%2Fpractice%2Fstaff%22%2C%22g%22%3A%22%23%2Fpractice%2Fstaff%2Fdashboard%22%7D; _hp2_id.2907378054=%7B%22userId%22%3A%228057059477829397%22%2C%22pageviewId%22%3A%222444957116832765%22%2C%22sessionId%22%3A%223927966963520501%22%2C%22identity%22%3A%22sdsortho.ema.md-19333733%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%7D; AWSALBAPP-0=AAAAAAAAAABjMmDoy7+7qtpUYRoH6UVWQDYfLj2g9iho4ZwGL5EFss1hjH9PJ/VT9pHMpspIxbhex+PuXRw+jWMRFWH1bh2pyNFZRDM3HzKquef/N+Ijn12uBCsiqS/1Yl2JkPwO4vhnfDk=',
            'Host': 'sdsortho.ema.md',
            'Referer': 'https://sdsortho.ema.md/ema/web/practice/staff',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        }

        response = requests.get(url=url, headers=headers)
        print(response.status_code)

        data = json.loads(response.text)

        if not data:
            break
        item1 = {}
        for item in data:
            try:
                patient_id = item['id']
                if conn.find_one({'PatientID': patient_id}):
                    print(f"Patient ID {patient_id} already in database.")
                    continue
                item1['PatientID'] = patient_id
            except Exception as e:
                patient_id = ""
            try:
                firstname = item['firstName']
                item1['Firstname'] = firstname
            except Exception as e:
                firstname = ""

            try:
                lastname = item['lastName']
                item1['Lastname'] = lastname
            except Exception as e:
                lastname = ""
            try:
                DOB = item['displayDateOfBirth']
                item1['DOB'] = DOB
            except Exception as e:
                print(e)

            try:
                phone_number = item['phoneNumbers'][0]['formattedPhoneNumber']
                item1['PhoneNumber'] = phone_number
            except Exception as e:
                print(e)

            url1 = f"https://sdsortho.ema.md/ema/ws/v3/patients/{patient_id}?selector=prefix,firstName,middleName,lastName,suffix,phoneNumbers,addressPrimary,preferredPhone,email,emailAlt,maritalStatus,inactiveInsuranceGroups(policies(groupNumber,patientRelationshipToPolicyHolder,policyHolderSsn,policyHolderDateOfBirth,policyHolderFirstName,policyHolderMiddleName,policyHolderLastName)),ungroupedInsurancePolicies(groupNumber,patientRelationshipToPolicyHolder,policyHolderSsn,policyHolderDateOfBirth,policyHolderFirstName,policyHolderMiddleName,policyHolderLastName),activeInsuranceGroups(policies(groupNumber,patientRelationshipToPolicyHolder,policyHolderSsn,policyHolderDateOfBirth,policyHolderFirstName,policyHolderMiddleName,policyHolderLastName)),allInsurancePolicies(groupNumber,patientRelationshipToPolicyHolder,policyHolderSsn,policyHolderDateOfBirth,policyHolderFirstName,policyHolderMiddleName,policyHolderLastName)"

            response1 = requests.get(url=url1, headers=headers)
            print(response1.status_code)

            # address data and payer data of patient
            data1 = json.loads(response1.text)

            try:
                streeadress = data1['addressPrimary']['street1']
                item1['streetaddress'] = streeadress
            except Exception as e:
                streeadress = ""

            try:
                gender = data1['gender']
                item1['gender'] = gender
            except Exception as e:
                gender = ""

            try:
                city = data1['addressPrimary']['city']
                item1['city'] = city
            except Exception as e:
                city = ""

            try:
                zipcode = data1['addressPrimary']['zipcode']
                item1['zipcode'] = zipcode
                if not zipcode:
                    zipcode = ''
            except Exception as e:
                zipcode = ""

            try:
                state = data1['addressPrimary']['state']
                item1['state'] = state
            except Exception as e:
                state = ""

            try:
                streeadress2 = data1['addressPrimary']['street2']
                if not streeadress2:
                    streeadress2 = ""
            except Exception as e:
                streeadress2 = ""

            try:
                item1['status'] = "pending"
            except Exception as e:
                print(e)

            # subscriber_id = ['ungroupedInsurancePolicies'][0]['policyNumber']
            try:
                conn.insert_one(dict(item1))
                TGREEN = '\033[1;32m'
                print(TGREEN + '\rData Inserted ...')
                print(page)
            except Exception as e:
                print("Status_Update_duplicate")
                print(e)

def main():
    NUM_THREADS = 25
    START_PAGE = 1608
    END_PAGE = 1609
    PAGES_PER_THREAD = (END_PAGE - START_PAGE) // NUM_THREADS

    threads = []

    for i in range(NUM_THREADS):
        start = START_PAGE + i * PAGES_PER_THREAD
        end = START_PAGE + (i+1) * PAGES_PER_THREAD

        if i == NUM_THREADS - 1:
            # Ensure the last thread picks up any remaining pages
            end = END_PAGE

        t = threading.Thread(target=fetch_patient_data, args=(start, end))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    print("All threads completed.")


if __name__ == "__main__":
    main()
