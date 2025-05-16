import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', "super secret key")
    # SQLALCHEMY_DATABASE_URI = (
    #     "mssql+pyodbc://@localhost/GreenLightDatabase?driver=ODBC+Driver+17+for+SQL+Server"
    # )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

