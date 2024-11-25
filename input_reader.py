import pandas as pd
import os
import json

current_dirname = os.path.dirname(__file__)

def read_input_data():
    '''
    Reads the /data/input_data.json file.
    Returns: the dictionary of the JSON data.
    Raises an error if required information is not present.
    '''
    file_path = os.path.join(current_dirname, 'data\\input_data.json')
    print('Reading Input Data from:', file_path)
    input_file = open(file_path, 'r')
    input_data = json.loads(input_file.read())
    input_file.close()
    required_fields = ['participants_excel_file_name', 'email_subject', 'email_body', 'certificate_template_filename']
    if not set(required_fields).issubset(set(input_data.keys())):
        print('Required Fields in Input Data JSON file:', required_fields)
        raise Exception('Input Data JSON file does not contain all required fields`')
    print('Input Data:', input_data)
    return input_data

def find_big_name_len(participants_data):
    big_name_len=1
    for i in participants_data.index:
        name = participants_data['Name'][i]
        if len(name) > big_name_len:
            big_name_len = len(name)
    return big_name_len

def pad_names_with_spaces(participants_data):
    big_name_len = find_big_name_len(participants_data)
    for i in participants_data.index:
        name = participants_data['Name'][i]
        if len(name) < big_name_len:
            participants_data['Name'][i] = ' ' * ((big_name_len - len(name))//2 + 5) + name + ' ' * ((big_name_len - len(name))//2)
    return participants_data

def read_participants_data(excel_file_name):
    '''
    Input param_1: Excel File Name.
    Excel File must have either '.xlsx' or '.xls' extension.
    Excel File must be placed inside "data" folder.
    Adds a column "Email Sent" and saves it to the same excel.
    "Email Sent" column indicates the status of sending email.
    Adds a column "Remarks" and saves it to the same excel.
    "Remarks" column indicates the error messages, if any.
    Returns: updated excel file as a pandas DataFrame.
    '''
    # import data from excel file
    excel_file_path = os.path.join(current_dirname, 'data\\' + excel_file_name)
    print('Reading participants data from:', excel_file_path)
    participants_data = pd.read_excel(excel_file_path)
    participants_count = len(participants_data)
    print(f'Imported Excel Sheet having {participants_count} rows')
    participants_data['Name'] = participants_data['Name'].apply(lambda x: ' '.join([y[0].upper() + y[1:] for y in x.strip().lower().split(' ')]))
    participants_data=pad_names_with_spaces(participants_data)
    print(participants_data)
    # Check for required fields
    required_fields = ['Name', 'Email']
    if not set(required_fields).issubset(set(participants_data.columns)):
        print('Required Fields are:', required_fields)
        raise Exception('Required Fields not present')
    # add a 'Email Sent' column, if its not present
    if 'Email Sent' not in participants_data.columns:
        participants_data['Email Sent'] = ['No' for i in range(participants_count)]
    # add a 'Remarks' column, if its not present
    if 'Remarks' not in participants_data.columns:
        participants_data['Remarks'] = ['-None-' for i in range(participants_count)]
    # save to excel
    participants_data.to_excel(excel_file_path, index=False)
    return participants_data

if __name__ == '__main__':
    pass