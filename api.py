# we will create an API endpoint for user registration and login using FASTAPI.

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import sqlite3
# from fastapi.security import OAuth2passwordBearer, OAuth2PasswordRequestForm


# import requests fastapi
# print(requests.__version__)

print ("FastAPI version:", FastAPI.__version__)
