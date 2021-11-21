import json
from fastapi import FastAPI, HTTPException

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "natasyazzhr"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

with open("pembayaran.json", "r") as read_file:
    data = json.load(read_file)
app = FastAPI()

#Show possible method
@app.get('/metodePembayaran')
async def payment_method():
    method = {"Cash", "Cashless"}
    return method

#Read Data Total
@app.get('/pembayaran/{hargaTotal}')
async def read_payment():
    harga = data["pembayaran"][len(data["pembayaran"])-1]["hargaTotal"]
    pajak = data["pembayaran"][len(data["pembayaran"])-1]["pajak"]
    return harga + pajak

#Add new Data
@app.post('/pembayaran')
async def add_payment(hargaTotal: int, metodePembayaran: str):
    idBayar=1
    if(len(data["pembayaran"])>0):
        idBayar=data["pembayaran"][len(data["pembayaran"])-1]["idBayar"]+1
    new_data={'idBayar':idBayar, 'hargaTotal': hargaTotal, 'pajak': int(hargaTotal*0.1), 'metodePembayaran': metodePembayaran, 'statusBayar': "Unpaid"}
    data['pembayaran'].append(dict(new_data))

    with open("pembayaran.json", "w") as write_file:
        json.dump(data,write_file,indent=4)
    return{"message": "Data added successfully"}
    write_file.close()

#Update status Bayar
@app.put('/pembayaran/{statusBayar}')
async def update_menu():
    idBayar=1
    for payment in data['pembayaran']:
        if payment['statusBayar'] == "Unpaid":
            idBayar = idBayar
            break
        else:
            idBayar = idBayar+1

    for payment_status in data['pembayaran']:
        if payment_status['idBayar'] == idBayar:
            payment_status['statusBayar']= "Paid"
            with open("pembayaran.json", "w") as write_file:  
                json.dump(data,write_file, indent=4)
            return{"message": "Data updated successfully"}

