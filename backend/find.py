# import re
#
# text = """
# data:"Indication: Post-op Knee Total Knee Arthroplasty, Left - left knee joint - Z47.1, Z96.652
# Instructions: evaluate and treat per diagnosis/objective exam
# Date of Surgery: 10/12/2022
# Restrictions: Weight bearing as tolerated.
# Recommend frequency of 1-2 times per week for 4-6 weeks.
#  - Therapeutic Exercises: All exercises prn per therapist.
#  - Manual Therapy: All manual therapy prn per therapist.
#  - Modalities: All modalities prn per therapist. All modalities prn per therapist.
# Provider: Aquino, Russell PA
# Perform at: Sforzo | Dillingham | Stewart Rehab
# Address: 5831 Bee Ridge Road Suite 300
# Sarasota, FL 34233
# Work: (941) 378-5100 ext 325
# Fax: (941) 960-1962"
# """
#
#
# regex_pattern = r'Indication:\s*(.*)'
#
# matches = re.search(regex_pattern, text)
# if matches:
#     extracted_data = matches.group(1)
#     print("Extracted Data:", extracted_data)
# else:
#     print("No match found.")

import re
import PyPDF2

# Open the PDF file
with open('PT_Rx_-_Shoulder_Arthroplasty_95221.pdf', 'rb') as file:
    # Create a PDF reader object
    reader = PyPDF2.PdfReader(file)

    # Extract text from all pages
    text = ""
    for page in reader.pages:
        text += page.extract_text()

# Your regex pattern
regex_pattern = r'Indication:\s*(.*)'

matches = re.search(regex_pattern, text)
if matches:
    extracted_data = matches.group(1)
    print("Extracted Data:", extracted_data)
else:
    print("No match found.")
