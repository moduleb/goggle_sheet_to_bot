from dataclasses import make_dataclass

from app.config import config
import requests


class SheetService:
    def check_task(self):
        pass


    def get_sheet_obj(self):
        response = self.__get_response(config.RANGE)
        if not response:
            return
        data = self.__create_data(response)
        if not data:
            return
        Sheet = make_dataclass("Sheet", data.keys())
        sheet_obj = Sheet(**data)
        return sheet_obj

    # https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{sheet_name}!{range}?key={api_key}
    def __get_response(self, range_):
        TABLE_URL: str = f'https://sheets.googleapis.com/v4/spreadsheets/' \
                         f'{config.TABLE_ID}/values/' \
                         f'{config.SHEET_NAME}!' \
                         f'{range_}?' \
                         f'key={config.API_KEY}'
        return requests.get(TABLE_URL)

    def __create_data(self, response):
        data = response.json().get('values')
        data = dict(zip(data[0], data[1]))
        return data


sheet_service = SheetService()
