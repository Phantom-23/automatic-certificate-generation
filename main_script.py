import os

import input_reader
import email_sender

current_dir = os.path.dirname(__file__)

def main():
    # read input data json file
    input_data = input_reader.read_input_data()
    participants_excel_file_name = input_data['participants_excel_file_name']
    participants_excel_file_path = os.path.join(current_dir, 'data\\' + participants_excel_file_name)
    # read excel
    participants_data = input_reader.read_participants_data(participants_excel_file_name)
    participants_count = len(participants_data)
    # TODO: generate certificates
    # send emails
    # TODO: change this attachments list
    attachments = ['certificate_1.jpg' for i in range(participants_count)]
    participants_data = email_sender.send_emails(participants_data, attachments, input_data)
    # update the excel file
    participants_data.to_excel(participants_excel_file_path, index=False)

if __name__ == '__main__':
    main()