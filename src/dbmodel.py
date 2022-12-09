from sqlalchemy import Column, column, Table, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .dbconfig import Base


# association_table = Table(
#     'menjual',
#     Base.metadata,
#     Column('idtoko', ForeignKey('toko.idtoko')),
#     Column('idlaptop', ForeignKey('laptop.idlaptop')),
#     Column('stok', Integer())
# )

class MenjualDB(Base):
    __tablename__ = 'menjual'
    idtoko = Column(ForeignKey('toko.idtoko'), primary_key=True)
    idlaptop = Column(ForeignKey('laptop.idlaptop'), primary_key=True)
    stok = Column(Integer())


class TokoDB(Base):
    __tablename__ = 'toko'
    idtoko = Column(Integer(), primary_key=True)
    namatoko = Column(String())
    kotakabupaten = Column(String())
    alamat = Column(String())

    laptop = relationship(
        'LaptopDB',
        secondary=MenjualDB.__table__,
        back_populates='toko'
    )


class LaptopDB(Base):
    __tablename__= 'laptop'
    idlaptop = Column(Integer(), primary_key=True)
    namalaptop = Column(String())
    merek = Column(String())
    kategori = Column(String())
    cpu = Column(String())
    gpu = Column(String())
    ram = Column(Integer())
    penyimpanan = Column(Integer())

    toko = relationship(
        'TokoDB',
        secondary=MenjualDB.__table__,
        back_populates='laptop'
    )
