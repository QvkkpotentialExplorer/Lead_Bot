import apiclient
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

from google_api import GoogleSheetApi

CREDENTIALS_FILE = 'creds.json'
user_spreadsheet_id = '1SCQJB2xDVXhgEN9aiRgN5QNv_5994F4iYYohOYiUq2c'
user_spreadsheet_action_id = '1fQ5v5uLDdmDv7p9R-99FrrEC55BPEp0FhkGiSYyFEfc'

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])


httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets','v4',http = httpAuth)


