from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db import Base

class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    url = Column(String(255), unique=True, index=True)
    about = Column(Text, nullable=True)

    products = relationship("Product", back_populates="brand", cascade="all, delete-orphan")
    policies = relationship("PolicyDB", back_populates="brand", uselist=False, cascade="all, delete-orphan")
    contact = relationship("ContactDB", back_populates="brand", uselist=False, cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    price = Column(String(50))
    url = Column(String(255))
    brand_id = Column(Integer, ForeignKey("brands.id"))

    brand = relationship("Brand", back_populates="products")


class PolicyDB(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    privacy_policy = Column(String(255))
    return_policy = Column(String(255))
    brand_id = Column(Integer, ForeignKey("brands.id"))

    brand = relationship("Brand", back_populates="policies")


class ContactDB(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    emails = Column(JSON)
    phones = Column(JSON)
    address = Column(Text, nullable=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))

    brand = relationship("Brand", back_populates="contact")
