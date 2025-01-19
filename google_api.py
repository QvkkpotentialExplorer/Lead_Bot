class GoogleSheetApi:
    def __init__(self, service, spreadsheet_id: str):
        self.service = service
        self.spreadsheet_id = spreadsheet_id

    def start_user_sheet(self):
        body = {
            'values': [['ID', 'TG_ID', 'USERNAME', 'PHONE', 'URL', 'ПОЛУЧИЛ_ИНСТРУКЦИЮ', 'ЗАВЕРШИЛ']]}

        self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range="A1:G1",
            valueInputOption="RAW",
            body=body).execute()

    def start_user_action_sheet(self):
        body = {
            'values': [['ID', 'USER_ID', 'ДЕЙСТВИЕ', 'ВРЕМЯ']]}
        self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range="A1:D1",
            valueInputOption="RAW",
            body=body).execute()

    def add_user(self, id, tg_id, username, phone, account_url):
        body = {
            'values': [[f'{id}', f'{tg_id}', f'{username}', phone, account_url, 'Нет', 'Нет']]}
        self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=f"A{id + 1}:C{id + 1}",
            valueInputOption="RAW",
            body=body).execute()

    def get_instruction(self, id):
        range_ = f'F{id + 1}:F{id+1}'
        body = {'values': [['Да']]}
        self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=range_,
            valueInputOption="RAW",
            body=body).execute()

    def create_user_action(self, user_id, type_action, time):
        result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id,
                                                                range='A1:A100000')
        result = result.execute()  # Выполнение запроса

        # Получение всех значений из диапазона
        values = result.get('values', [])

        # Определяем количество строк (если в таблице есть данные)
        last_row = len(values)
        range_ = f'A{last_row + 1}:D{last_row + 1}'
        body = {'values': [[f'{last_row-1}', f'{user_id}', type_action, str(time).split('.')[0]]]}
        self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=range_,
            valueInputOption="RAW",
            body=body).execute()

    def get_complete(self, id):
        range_ = f'G{id + 1}'
        body = {'values': [['Да']]}
        self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=range_,
            valueInputOption="RAW",
            body=body).execute()
