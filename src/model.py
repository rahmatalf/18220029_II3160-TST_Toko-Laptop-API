from pydantic import BaseModel, Field


class Toko(BaseModel):
    nama: str
    kotakabupaten: str
    alamat: str

class Laptop(BaseModel):
    nama: str
    merek: str
    kategori: str
    cpu: str
    gpu: str
    ram: int
    penyimpanan: int

class User(BaseModel):
    nama: str = Field(default=None)
    username: str = Field(default=None)
    password: str = Field(default=None)
    class Config:
        the_schema = {
            "user_demo": {"nama": "Budi",
                          "username": "budi123",
                          "password": "budidoremi"}
        }

class UserLogin(BaseModel):
    username: str = Field(default=None)
    password: str = Field(default=None)
    class Config:
        the_schema = {
            "user_demo": {"username": "budi123",
                          "password": "budidoremi"}
        }
