import os
from dataclasses import dataclass
from environs import Env

Env.read_env()

@dataclass
class Config():
    TOKEN: str = os.environ.get("TOKEN")
    API_KEY: str = os.environ.get("API_KEY")
    TABLE_ID: str = "1da440eI1D4o6eQaPmdJ-6TqxQ2E9KzuQ9XyyTFoZQ7E"
    SHEET_NAME: str = "Sheet1"
    RANGE = "A1:E2"
    ADMIN_TEL_ID: int = 5312665858



"""
sheet_id	 -	ID таблицы*, который вы можете скопировать из адреса URL.
sheet_name -	Название листа в таблице; например, Contacts или Sheet1.
range -	Координаты ячейки или ячеек, из которых берутся данные запроса в формате нотации Google Sheets;  например, E1:F21.
api_key -	Ваш ключ API из настроек проекта в Google Cloud.
"""
config = Config()