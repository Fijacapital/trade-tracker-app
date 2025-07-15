
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import gspread
from google.oauth2.service_account import Credentials

load_dotenv()

GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")

scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scope)
client = gspread.authorize(credentials)
sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1

app = FastAPI()

class Trade(BaseModel):
    trade_no: int
    stock_name: str
    cmp: float
    buy_price: float

@app.get("/")
def read_root():
    return {"message": "FijaCapital Trade Tracker API is running ✅"}

@app.get("/trades")
def get_trades():
    data = sheet.get_all_records()
    return {"trades": data}
