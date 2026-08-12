# from pydantic import BaseModel

# class ComplaintRequest(BaseModel):
#     complaint: str
#     address: str

from pydantic import BaseModel
from typing import List

class ComplaintRequest(BaseModel):
    complaint: str
    address: str

class BulkComplaintRequest(BaseModel):
    complaints: List[ComplaintRequest]