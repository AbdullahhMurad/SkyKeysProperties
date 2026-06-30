from datetime import datetime
from decimal import Decimal
from typing import Literal, Optional

from pydantic import BaseModel, Field


# ===========================================================================
# Employee schemas
# ===========================================================================

class EmployeeCreate(BaseModel):
    first_name:     str           = Field(..., max_length=100)
    middle_name:    Optional[str] = Field(None, max_length=100)
    last_name:      str           = Field(..., max_length=100)
    nationality:    str           = Field(..., max_length=100)
    image_filename: Optional[str] = Field(None, max_length=255)
    job_title:      Optional[str] = Field(None, max_length=150)
    bio:            Optional[str] = None
    email:          Optional[str] = Field(None, max_length=255)
    phone:          Optional[str] = Field(None, max_length=50)


class EmployeeUpdate(BaseModel):
    first_name:     Optional[str] = Field(None, max_length=100)
    middle_name:    Optional[str] = Field(None, max_length=100)
    last_name:      Optional[str] = Field(None, max_length=100)
    nationality:    Optional[str] = Field(None, max_length=100)
    image_filename: Optional[str] = Field(None, max_length=255)
    job_title:      Optional[str] = Field(None, max_length=150)
    bio:            Optional[str] = None
    email:          Optional[str] = Field(None, max_length=255)
    phone:          Optional[str] = Field(None, max_length=50)


class EmployeeRead(EmployeeCreate):
    id:         int
    created_at: datetime

    model_config = {"from_attributes": True}


# ===========================================================================
# Property schemas
# ===========================================================================

class PropertyCreate(BaseModel):
    emirate:          str                        = Field(..., max_length=100)
    master_community: str                        = Field(..., max_length=150)
    sub_community:    Optional[str]              = Field(None, max_length=150)

    bedrooms:         int                        = Field(..., ge=0)
    bathrooms:        int                        = Field(..., ge=0)
    square_feet:      Decimal                    = Field(..., gt=0)
    price:            Decimal                    = Field(..., gt=0)

    image_filename:   Optional[str]              = Field(None, max_length=255)
    listing_type:     Literal["sale", "rent"]

    title:            Optional[str]              = Field(None, max_length=255)
    description:      Optional[str]              = None
    is_featured:      bool                       = False
    is_active:        bool                       = True


class PropertyUpdate(BaseModel):
    emirate:          Optional[str]              = Field(None, max_length=100)
    master_community: Optional[str]              = Field(None, max_length=150)
    sub_community:    Optional[str]              = Field(None, max_length=150)

    bedrooms:         Optional[int]              = Field(None, ge=0)
    bathrooms:        Optional[int]              = Field(None, ge=0)
    square_feet:      Optional[Decimal]          = Field(None, gt=0)
    price:            Optional[Decimal]          = Field(None, gt=0)

    image_filename:   Optional[str]              = Field(None, max_length=255)
    listing_type:     Optional[Literal["sale", "rent"]] = None

    title:            Optional[str]              = Field(None, max_length=255)
    description:      Optional[str]              = None
    is_featured:      Optional[bool]              = None
    is_active:        Optional[bool]              = None


class PropertyRead(PropertyCreate):
    id:         int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

# from datetime import datetime
# from decimal import Decimal
# from typing import Literal, Optional

# from pydantic import BaseModel, Field


# # ===========================================================================
# # Employee schemas
# # ===========================================================================

# class EmployeeCreate(BaseModel):
#     first_name:     str           = Field(..., max_length=100)
#     middle_name:    Optional[str] = Field(None, max_length=100)
#     last_name:      str           = Field(..., max_length=100)
#     nationality:    str           = Field(..., max_length=100)
#     image_filename: Optional[str] = Field(None, max_length=255)
#     job_title:      Optional[str] = Field(None, max_length=150)
#     bio:            Optional[str] = None
#     email:          Optional[str] = Field(None, max_length=255)
#     phone:          Optional[str] = Field(None, max_length=50)


# class EmployeeUpdate(BaseModel):
#     first_name:     Optional[str] = Field(None, max_length=100)
#     middle_name:    Optional[str] = Field(None, max_length=100)
#     last_name:      Optional[str] = Field(None, max_length=100)
#     nationality:    Optional[str] = Field(None, max_length=100)
#     image_filename: Optional[str] = Field(None, max_length=255)
#     job_title:      Optional[str] = Field(None, max_length=150)
#     bio:            Optional[str] = None
#     email:          Optional[str] = Field(None, max_length=255)
#     phone:          Optional[str] = Field(None, max_length=50)


# class EmployeeRead(EmployeeCreate):
#     id:         int
#     created_at: datetime

#     model_config = {"from_attributes": True}


# # ===========================================================================
# # Property schemas
# # ===========================================================================

# class PropertyCreate(BaseModel):
#     emirate:          str                        = Field(..., max_length=100)
#     master_community: str                        = Field(..., max_length=150)
#     sub_community:    Optional[str]              = Field(None, max_length=150)

#     bedrooms:         int                        = Field(..., ge=0)
#     bathrooms:        int                        = Field(..., ge=0)
#     square_feet:      Decimal                    = Field(..., gt=0)
#     price:            Decimal                    = Field(..., gt=0)

#     image_filename:   Optional[str]              = Field(None, max_length=255)
#     listing_type:     Literal["sale", "rent"]

#     title:            Optional[str]              = Field(None, max_length=255)
#     description:      Optional[str]              = None
#     is_featured:      bool                       = False
#     is_active:        bool                       = True


# class PropertyUpdate(BaseModel):
#     emirate:          Optional[str]              = Field(None, max_length=100)
#     master_community: Optional[str]              = Field(None, max_length=150)
#     sub_community:    Optional[str]              = Field(None, max_length=150)

#     bedrooms:         Optional[int]              = Field(None, ge=0)
#     bathrooms:        Optional[int]              = Field(None, ge=0)
#     square_feet:      Optional[Decimal]          = Field(None, gt=0)
#     price:            Optional[Decimal]          = Field(None, gt=0)

#     image_filename:   Optional[str]              = Field(None, max_length=255)
#     listing_type:     Optional[Literal["sale", "rent"]] = None

#     title:            Optional[str]              = Field(None, max_length=255)
#     description:      Optional[str]              = None
#     is_featured:      Optional[bool]              = None
#     is_active:        Optional[bool]              = None


# class PropertyRead(PropertyCreate):
#     id:         int
#     created_at: datetime
#     updated_at: datetime

#     model_config = {"from_attributes": True}


# # from datetime import datetime
# # from decimal import Decimal
# # from typing import Literal, Optional

# # from pydantic import BaseModel, EmailStr, Field


# # # ===========================================================================
# # # Employee schemas
# # # ===========================================================================

# # class EmployeeCreate(BaseModel):
# #     first_name:     str           = Field(..., max_length=100)
# #     middle_name:    Optional[str] = Field(None, max_length=100)
# #     last_name:      str           = Field(..., max_length=100)
# #     nationality:    str           = Field(..., max_length=100)
# #     image_filename: Optional[str] = Field(None, max_length=255)
# #     job_title:      Optional[str] = Field(None, max_length=150)
# #     bio:            Optional[str] = None
# #     email:          Optional[str] = Field(None, max_length=255)
# #     phone:          Optional[str] = Field(None, max_length=50)


# # class EmployeeRead(EmployeeCreate):
# #     id:         int
# #     created_at: datetime

# #     model_config = {"from_attributes": True}


# # # ===========================================================================
# # # Property schemas
# # # ===========================================================================

# # class PropertyCreate(BaseModel):
# #     emirate:          str                        = Field(..., max_length=100)
# #     master_community: str                        = Field(..., max_length=150)
# #     sub_community:    Optional[str]              = Field(None, max_length=150)

# #     bedrooms:         int                        = Field(..., ge=0)
# #     bathrooms:        int                        = Field(..., ge=0)
# #     square_feet:      Decimal                    = Field(..., gt=0)
# #     price:            Decimal                    = Field(..., gt=0)

# #     image_filename:   Optional[str]              = Field(None, max_length=255)
# #     listing_type:     Literal["sale", "rent"]

# #     title:            Optional[str]              = Field(None, max_length=255)
# #     description:      Optional[str]              = None
# #     is_featured:      bool                       = False
# #     is_active:        bool                       = True


# # class PropertyRead(PropertyCreate):
# #     id:         int
# #     created_at: datetime
# #     updated_at: datetime

# #     model_config = {"from_attributes": True}
