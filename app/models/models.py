from sqlalchemy import (
    Boolean, Column, Integer, SmallInteger,
    Numeric, String, Text, TIMESTAMP, func,
)

from app.core.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id             = Column(Integer, primary_key=True, index=True)
    first_name     = Column(String(100), nullable=False)
    middle_name    = Column(String(100), nullable=True)
    last_name      = Column(String(100), nullable=False)
    nationality    = Column(String(100), nullable=False)
    image_filename = Column(String(255), nullable=True)
    job_title      = Column(String(150), nullable=True)
    bio            = Column(Text,        nullable=True)
    email          = Column(String(255), nullable=True)
    phone          = Column(String(50),  nullable=True)
    created_at     = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)


class Property(Base):
    __tablename__ = "properties"

    id               = Column(Integer, primary_key=True, index=True)

    # Location
    emirate          = Column(String(100), nullable=False)
    master_community = Column(String(150), nullable=False)
    sub_community    = Column(String(150), nullable=True)

    # Property details
    bedrooms         = Column(SmallInteger, nullable=False)
    bathrooms        = Column(SmallInteger, nullable=False)
    square_feet      = Column(Numeric(10, 2), nullable=False)
    price            = Column(Numeric(15, 2), nullable=False)

    # Media
    image_filename   = Column(String(255), nullable=True)

    # Listing classification
    listing_type     = Column(String(10), nullable=False)   # 'sale' | 'rent'

    # Descriptive fields
    title            = Column(String(255), nullable=True)
    description      = Column(Text,        nullable=True)
    is_featured      = Column(Boolean, nullable=False, default=False)
    is_active        = Column(Boolean, nullable=False, default=True)
    sort_order = Column(SmallInteger, nullable=False, default=0)
    # Timestamps
    created_at       = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at       = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class PropertyImage(Base):
    __tablename__ = "property_images"

    id           = Column(Integer, primary_key=True, index=True)
    property_id  = Column(Integer, nullable=False, index=True)
    image_url    = Column(String(500), nullable=False)
    sort_order   = Column(SmallInteger, nullable=False, default=0)
    created_at   = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)


class AdminUser(Base):
    __tablename__ = "admin_users"

    id              = Column(Integer, primary_key=True, index=True)
    username        = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role            = Column(String(20), nullable=False, default="admin")
    is_active       = Column(Boolean, nullable=False, default=True)
    created_at      = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)


class Developer(Base):
    __tablename__ = "developers"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(150), nullable=False)
    logo_url   = Column(String(500), nullable=True)
    is_active  = Column(Boolean, nullable=False, default=True)
    sort_order = Column(SmallInteger, nullable=False, default=0)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)


class SiteSetting(Base):
    __tablename__ = "site_settings"

    key        = Column(String(100), primary_key=True)
    value      = Column(Text, nullable=True)
    label      = Column(String(150), nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)