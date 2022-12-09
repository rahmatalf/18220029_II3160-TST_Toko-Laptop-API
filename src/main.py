from fastapi import FastAPI, Path, Query, Body, Depends, HTTPException
from .model import *
from .auth.jwt_handler import signJWT
from .auth.jwt_bearer import jwtBearer
from .dbmodel import *
from .dbconfig import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
Base.metadata.create_all(bind=engine)
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close
users = []


#Tags: default
@app.get("/")
def home():
    return {"Hello": "Selamat datang di TokoLaptopAPI!"}

@app.get("/about")
def about():
    return {"About1": "API ini berisi data toko-toko yang menjual produk laptop dan data mengenai detail produk laptop yang tersedia",
            "About2": "API ini dapat digunakan untuk melihat detail toko atau laptop yang tersedia dan mencari laptop sesuai dengan kategori pada toko tertentu"}


#Tags: User
@app.post("/user/signup", tags=["User"])
def userSignUp(user: User = Body(default=None)):
    users.append(user)
    return signJWT(user.username)

@app.post("/user/login", tags=["User"])
def userLogin(user: UserLogin = Body(default=None)):
    if checkUser(user):
        return signJWT(user.username)
    else:
        raise HTTPException(
            status_code= 401,
            detail= "Informasi login salah, silakan coba lagi dengan informasi yang benar"
        )

def checkUser(data: UserLogin):
    for user in users:
        if user.username == data.username and user.password == data.password:
            return True
        else:
            return False


#Tags: Data Toko
@app.get("/dataToko/get/all", dependencies=[Depends(jwtBearer())], tags=["Data Toko"])
def getAllToko(db: Session = Depends(get_db)):
    return db.query(TokoDB).all()

@app.get("/dataToko/get/by-nama", dependencies=[Depends(jwtBearer())], tags=["Data Toko"])
def getTokoByNama(nama: str = Query(None, description="Nama toko"), db: Session = Depends(get_db)):
    if nama == None:
        return {"Error!": "Masukkan nama toko sebagai query!"}
    else:
        daftartoko = db.query(TokoDB)
        for toko in daftartoko:
            if toko.namatoko == nama:
                return db.query(TokoDB).filter(TokoDB.namatoko==nama).all()
        raise HTTPException(
            status_code= 404,
            detail= "Data tidak ditemukan"
        )

@app.get("/dataToko/get/by-kotakabupaten", dependencies=[Depends(jwtBearer())], tags=["Data Toko"])
def getTokoByKotaKabupaten(kotakabupaten: str = Query(None, description="Kota atau kabupaten toko"), db: Session = Depends(get_db)):
    if kotakabupaten == None:
        return {"Error!": "Masukkan kota atau kabupaten sebagai query!"}
    else:
        daftartoko = db.query(TokoDB)
        for toko in daftartoko:
            if toko.kotakabupaten == kotakabupaten:
                return db.query(TokoDB).filter(TokoDB.kotakabupaten==kotakabupaten).all()
        raise HTTPException(
            status_code= 404,
            detail= "Data tidak ditemukan"
        )

@app.post("/dataToko/add", dependencies=[Depends(jwtBearer())], tags=["Data Toko"])
def addToko(toko: Toko, db: Session = Depends(get_db)):
    toko_model = TokoDB()
    toko_model.namatoko = toko.nama
    toko_model.kotakabupaten = toko.kotakabupaten
    toko_model.alamat = toko.alamat
    db.add(toko_model)
    db.commit()
    return {"Success!": "Data toko berhasil ditambah!"}

@app.delete("/dataToko/delete", dependencies=[Depends(jwtBearer())], tags=["Data Toko"])
def deleteToko(id: int = Query(..., description="ID Toko yang hendak dihapus datanya"), db: Session = Depends(get_db)):
    toko = db.query(TokoDB).filter(TokoDB.idtoko==id).first()
    if toko is None:
        raise HTTPException(
            status_code= 404,
            detail= "Data tidak ditemukan"
        )
    db.query(TokoDB).filter(TokoDB.idtoko==id).delete()
    db.commit()
    return {"Success!": "Data toko berhasil dihapus!"}


#Tags: Data Laptop
@app.get("/dataLaptop/get/all", dependencies=[Depends(jwtBearer())], tags=["Data Laptop"])
def getAllLaptop(db: Session = Depends(get_db)):
    return db.query(LaptopDB).all()

@app.get("/dataLaptop/get/by-nama", dependencies=[Depends(jwtBearer())], tags=["Data Laptop"])
def getLaptopByNama(nama: str = Query(None, description="Nama laptop"), db: Session = Depends(get_db)):
    if nama == None:
        return {"Error!": "Masukkan nama laptop sebagai query!"}
    else:
        daftarlaptop = db.query(LaptopDB)
        for laptop in daftarlaptop:
            if laptop.namalaptop == nama:
                return db.query(LaptopDB).filter(LaptopDB.namalaptop==nama).all()
        raise HTTPException(
            status_code= 404,
            detail= "Data tidak ditemukan"
        )

@app.get("/dataLaptop/get/by-merek", dependencies=[Depends(jwtBearer())], tags=["Data Laptop"])
def getLaptopByMerek(merek: str = Query(None, description="Merek laptop"), db: Session = Depends(get_db)):
    if merek == None:
        return {"Error!": "Masukkan merek laptop sebagai query!"}
    else:
        daftarlaptop = db.query(LaptopDB)
        for laptop in daftarlaptop:
            if laptop.merek == merek:
                return db.query(LaptopDB).filter(LaptopDB.merek==merek).all()
        raise HTTPException(
            status_code= 404,
            detail= "Data tidak ditemukan"
        )

@app.get("/dataLaptop/get/by-kategori", dependencies=[Depends(jwtBearer())], tags=["Data Laptop"])
def getLaptopByKategori(kategori: str = Query(None, description="Kategori laptop"), db: Session = Depends(get_db)):
    if kategori == None:
        return {"Error!": "Masukkan kota atau kabupaten sebagai query!"}
    else:
        daftarlaptop = db.query(LaptopDB)
        for laptop in daftarlaptop:
            if laptop.kategori == kategori:
                return db.query(LaptopDB).filter(LaptopDB.kategori==kategori).all()
        raise HTTPException(
            status_code= 404,
            detail= "Data tidak ditemukan"
        )

@app.post("/dataLaptop/add", dependencies=[Depends(jwtBearer())], tags=["Data Laptop"])
def addLaptop(laptop: Laptop, db: Session = Depends(get_db)):
    laptop_model = LaptopDB()
    laptop_model.namalaptop = laptop.nama
    laptop_model.merek = laptop.merek
    laptop_model.kategori = laptop.kategori
    laptop_model.cpu = laptop.cpu
    laptop_model.gpu = laptop.gpu
    laptop_model.ram = laptop.ram
    laptop_model.penyimpanan = laptop.penyimpanan
    db.add(laptop_model)
    db.commit()
    return {"Success!": "Data laptop berhasil ditambah!"}

@app.delete("/dataLaptop/delete", dependencies=[Depends(jwtBearer())], tags=["Data Laptop"])
def deleteLaptop(id: int = Query(..., description="ID Laptop yang hendak dihapus datanya"), db: Session = Depends(get_db)):
    laptop = db.query(LaptopDB).filter(LaptopDB.idlaptop==id).first()
    if laptop is None:
        raise HTTPException(
            status_code= 404,
            detail= "Data tidak ditemukan"
        )
    db.query(LaptopDB).filter(LaptopDB.idlaptop==id).delete()
    db.commit()
    return {"Success!": "Data laptop berhasil dihapus!"}


# Stok Laptop
@app.get("/stokLaptop/get/all", dependencies=[Depends(jwtBearer())], tags=["Stok Laptop"])
def getAllStok(db: Session = Depends(get_db)):
    return db.query(LaptopDB, TokoDB, MenjualDB.stok).join(MenjualDB, MenjualDB.idlaptop==LaptopDB.idlaptop).join(TokoDB, TokoDB.idtoko==MenjualDB.idtoko).all()

@app.get("/stokLaptop/get/by-kategorikotakabupaten", dependencies=[Depends(jwtBearer())], tags=["Stok Laptop"])
def getStokByKategoriKotaKabupaten(kategori: str = Query(None, description="Kategori laptop"), kotakabupaten: str = Query(None, description="Kota atau kabupaten toko"), db: Session = Depends(get_db)):
    if (kategori == None) or (kotakabupaten == None):
        return {"Error!": "Masukkan query dengan lengkap!"}
    else:
        daftarlaptop = db.query(LaptopDB)
        daftartoko = db.query(TokoDB)
        listlaptop = []
        listtoko = []
        for laptop in daftarlaptop:
            if laptop.kategori == kategori:
                listlaptop.append(laptop.idlaptop)
        for toko in daftartoko:
            if toko.kotakabupaten == kotakabupaten:
                listtoko.append(toko.idtoko)
        if (len(listlaptop)==0) or (len(listtoko)==0):
            raise HTTPException(
                status_code= 404,
                detail= "Data tidak ditemukan"
            )
        return db.query(LaptopDB, TokoDB, MenjualDB.stok).join(MenjualDB, MenjualDB.idlaptop==LaptopDB.idlaptop).join(TokoDB, TokoDB.idtoko==MenjualDB.idtoko).filter(LaptopDB.kategori==kategori).filter(TokoDB.kotakabupaten==kotakabupaten).all()

@app.get("/stokLaptop/get/by-merekkotakabupaten", dependencies=[Depends(jwtBearer())], tags=["Stok Laptop"])
def getStokByMerekKotaKabupaten(merek: str = Query(None, description="Merek laptop"), kotakabupaten: str = Query(None, description="Kota atau kabupaten toko"), db: Session = Depends(get_db)):
    if (merek == None) or (kotakabupaten == None):
        return {"Error!": "Masukkan query dengan lengkap!"}
    else:
        daftarlaptop = db.query(LaptopDB)
        daftartoko = db.query(TokoDB)
        listlaptop = []
        listtoko = []
        for laptop in daftarlaptop:
            if laptop.merek == merek:
                listlaptop.append(laptop.idlaptop)
        for toko in daftartoko:
            if toko.kotakabupaten == kotakabupaten:
                listtoko.append(toko.idtoko)
        if (len(listlaptop)==0) or (len(listtoko)==0):
            raise HTTPException(
                status_code= 404,
                detail= "Data tidak ditemukan"
            )
        return db.query(LaptopDB, TokoDB, MenjualDB.stok).join(MenjualDB, MenjualDB.idlaptop==LaptopDB.idlaptop).join(TokoDB, TokoDB.idtoko==MenjualDB.idtoko).filter(LaptopDB.merek==merek).filter(TokoDB.kotakabupaten==kotakabupaten).all()

@app.post("/stokLaptop/add", dependencies=[Depends(jwtBearer())], tags=["Stok Laptop"])
def addStok(idtoko: int, idlaptop: int, stok: int, db: Session = Depends(get_db)):
    stok_model = MenjualDB()
    stok_model.idtoko = idtoko
    stok_model.idlaptop = idlaptop
    stok_model.stok = stok
    db.add(stok_model)
    db.commit()
    return {"Success!": "Data stok berhasil ditambah!"}