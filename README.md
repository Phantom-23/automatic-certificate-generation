# Automated Certificate Generator & Emailer

## Usage instructions:

> 📝 **NOTE:** Please follow the below instructions properly to avoid any errors.

- Install the necessary Python packages by running `pip install -r requirements.txt` command in the command line, in the root directory.

- In the root directory, create a `.env` file and add the following environment variables, which are need for sending emails.
```
email="USE_TURING_HUT_OFFICIAL_EMAIL"
email_app_password="USE_APP_PASSWORD_FOR_THE_PRESENT_DEVICE"
email_host="smtp.gmail.com"
email_port="465"
```
In the above environment, make sure you replace values of `email` and `email_app_password`.

- Place the participant's excel sheet inside `data` folder, and make sure it has a `.xlsx` or `.xls` extension.

- In `data/input_data.json` file, mandatorily fill in the following with the correct details:
```json
{
    "participants_excel_file_name": "FILE_NAME_WITH_EXTENSION",
    "email_subject": "EMAIL_SUBJECT_GOES_HERE",
    "email_body": "EMAIL_BODY_GOES_HERE"
}
```
For the email body, seperate new lines with a `\n`. Note that in the `participants_excel_file_name` field, the filename should be the one present inside `data` folder and only specify the file name with extension, not the file path.

- The participants excel file must have atleast `Name` and `Email` columns. Note that these column names are *case-sensitive*.