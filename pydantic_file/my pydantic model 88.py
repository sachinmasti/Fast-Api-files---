from colorama import Fore,Style,init #importing coloroma module for colored output.
init(autoreset=True)

from pydantic import BaseModel,EmailStr,AnyHttpUrl,Field,field_validator,model_validator,computed_field  #import pydantic model for creating pydantic model.

from  typing import List,Dict,Annotated,Optional,Any

class adress_info(BaseModel):
    city:str
    pincode:int
    street:str



class info(BaseModel):
    name: Annotated[str,Field(max_length=50,description='enter your name',examples=['sachin','rohit','shreya'])]
    age: Annotated[int,Field(description='enter your age',strict=True)]
    email:EmailStr
    salary:Annotated[float,Field(description='enter your salary')]
    address : adress_info
    mobile_no:int = None
    contact_info:Dict[str,Any] = None

    @field_validator('name')
    @classmethod
    def name_valid(cls,value):
        valid_names = ['@','_','-']

        if any(char in value for char in valid_names):
        # for ch in valid_names:
        #     if ch in value:
                raise ValueError(f'{Fore.RED} you name not valid remove special characters')

        return value

    @model_validator(mode='after')
    def validates(self):
        # if self.age < 20 or self.age > 60:
        #     raise ValueError(f'{Fore.GREEN} you need to fill backup number in your contact info')
        # return self
        if (self.age < 20 or self.age > 60) and 'backup number' not in self.contact_info:
            raise ValueError(
                'You need to provide a backup number'
            )
        return  self

def user_info(user:info):
    return (f'{Fore.GREEN} user name is {user.name} \n '
            f'{Fore.BLUE} user age is {user.age} \n '
            f'{Fore.MAGENTA} user email is {user.email}\n '
            f'{Fore.YELLOW} user salary is {user.salary} \n'
            f'{Fore.BLUE} user address is {user.address}\n'
            f'{Fore.RED} user mobile no is {user.mobile_no}'
            f'{Fore.YELLOW} cantact info is {user.contact_info}')

data = {'name':'sachin88','age':24,'email':'sachinmasti98@gmail.com',
        'salary':400000,'address':{'city':'hasurcahmpu','street':'kranti nagar','pincode':416501},
        'mobile_no':7666243552}
user = info(**data)

print(user_info(user))

print(user.address.city)
