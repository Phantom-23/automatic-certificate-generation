import smtplib, ssl
import re
import os
import html2text
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

current_dir = os.path.dirname(__file__)

def get_complete_file_path(filename):
    return os.path.join(current_dir, 'certificates\\' + filename)

def read_credentials():
    '''
    Reads credentials from '.env' file.
    Raises error is required fields are not present.
    Returns a dictionary of credentials having 'email', 'password', 'host', 'port' fields
    '''
    required_fields = ['email', 'email_app_password', 'email_host', 'email_port']
    for key in required_fields:
        if os.getenv(key) is None:
            print('Required ENV Variables are:', required_fields)
            raise Exception('Required Environment Variables not present')
    credentials = {
        'email': os.getenv('email'),
        'password': os.getenv('email_app_password'),
        'host': os.getenv('email_host'),
        'port': int(os.getenv('email_port'))
    }
    print('Read Email Credentials')
    return credentials

def validate_email(email_to_test):
    '''
    Validates the provided email against a regex and returns a Boolean.
    Valid email: [atleast_one_char]@[atleast_one_char].[atleast_2_chars]
    '''
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(email_regex, email_to_test)

def attach_email_content(sender_email, receiver_email, receiver_name, input_data, attachment_file_name):
    '''
    Input param_1: sender email address.
    Input param_2: receiver email address.
    Input param_3: receiver's name.
    Input param_4: input_data dictionary.
    Input param_5: attachment filename.
    Attachment file is assumed to be inside 'certificates' folder.
    Returns: final message object
    '''
    message = MIMEMultipart('alternative')
    message['Subject'] = input_data['email_subject']
    message['From'] = sender_email
    message['To'] = receiver_email

    # get HTML and plain text
    email_html_file = open('email_template.html', 'r')
    email_html = str(email_html_file.read())
    # replace placeholders in html
    email_html = email_html.replace('{{NAME}}', receiver_name)
    email_html = email_html.replace('{{BODY}}', input_data['email_body'])
    plain_text = html2text.html2text(email_html)

    part1 = MIMEText(plain_text, 'text')
    part2 = MIMEText(email_html, 'html')
    message.attach(part1)
    message.attach(part2)

    # add attachment file
    attachment_path = get_complete_file_path(attachment_file_name)
    # Open attachment file in binary mode
    with open(attachment_path, 'rb') as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        attachment_part = MIMEBase('application', 'octet-stream')
        attachment_part.set_payload(attachment.read())
    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(attachment_part)
    # Add header as key/value pair to attachment part
    attachment_part.add_header(
        "Content-Disposition",
        f"attachment; filename= {attachment_file_name}",
    )
    # Add attachment to message
    message.attach(attachment_part)

    return message

def send_emails(participants, attachments, input_data):
    '''
    Input param_1: participants dataframe having atleast 'Email' and 'Name' fields.
    Input param_2: list of attachment names. Each item is the corresponding file name.
    Input param_3: dictionary of input data.
    Sends email along with the attachment and updates 'Email Sent', 'Remarks' columns.
    Returns: Updated dataframe
    '''
    # get credentials
    credentials = read_credentials()
    sender_email, password = credentials['email'], credentials['password']
    host, port = credentials['host'], credentials['port']
    
    # send emails
    failed_count = 0
    context = ssl.create_default_context()
    print('Starting to send emails, DONOT stop the script💥')
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(sender_email, password)
        for i in participants.index:
            # check if email was already sent
            if participants['Email Sent'][i] == 'Yes':
                continue
            receiver_email = participants['Email'][i]
            # check if receiver email is valid
            if not validate_email(receiver_email):
                print('Invalid email given, skipping')
                participants['Remarks'][i] = 'Invalid email'
                continue

            receiver_name = participants['Name'][i]

            # add plain text message, html message, attachments
            message = attach_email_content(sender_email, receiver_email, receiver_name, input_data, attachments[i])

            try:
                server.sendmail(sender_email, receiver_email, message.as_string())
                print('Sent to:', receiver_email)
                # update the participants dataframe that the email was sent
                participants['Email Sent'][i] = 'Yes'
            except Exception as err:
                failed_count += 1
                print('An error occurred while sending email to:', receiver_email)
                participants['Remarks'][i] = 'Error: ' + err
                print(err)
    
    if failed_count > 0:
        print(f'Failed to send emails to {failed_count} participants')
    else:
        print('All emails delivered')

    # return the updated dataframe
    return participants

if __name__ == '__main__':
    pass