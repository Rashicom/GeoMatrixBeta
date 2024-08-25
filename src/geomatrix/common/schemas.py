from pydantic import BaseModel, EmailStr
from typing import List, Dict

class HtmlEmailSchema(BaseModel):
    subject:str
    recipients:List[EmailStr]
    template_body:Dict

class TextEmailSchema(BaseModel):
    subject:str
    recipients:List[EmailStr]
    body:str