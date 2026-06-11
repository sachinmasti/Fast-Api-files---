from colorama import Fore,Style,init
init(autoreset=True)

from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator
from typing import List,Dict,Any,Optional,Annotated

class addres_clf(BaseModel):
    city: str
    pincode: int
    street: str


class info(BaseModel):
    name : Annotated[str,Field(max_length=50,title='name of the patient',
                    description='plz enter the name of the patient',examples=['sachin','rohit','shreya'])]

    age : Annotated[int,Field(gt=0 , strict=True)]

    email : EmailStr
    booking_url: Optional[AnyUrl] = 'sachinmasti.www.com'
    salary:float
    weight:float
    allergies: Optional[List[str]] = Field(max_length=5,default='not any allergies')
    contact_info: Dict[str, Any]
    addres: addres_clf # Corrected: type hint for nested model

    @model_validator(mode='after')
    def validates(self):
        if self.age >= 60 and 'emergency no' not in self.contact_info:
            raise ValueError(f'{Fore.YELLOW} your age is grater than 60 so you have to be emergency contact nomber')
        return self
# def sachin(name:str,age:int):
#     '''iss type ke code main manually code likhana pada rahah hai
#         aur iss tarah bahot sa boiler code likhna padega agar data validation karna hai to
#         iss ko hi hum fix karenge using pydantic'''

#     print(__doc__)
#     if type(name) ==str and type(age) ==int:
#         return f'{name} is my name and {age} is my age'
#     else:
#         raise TypeError(f'{Fore.RED} you entered wrong type of values')


# print(sachin('veena','twenty'))

def func(info:info):
    line1 = f' {Fore.BLUE} my name is {Fore.LIGHTCYAN_EX} {info.name} {Style.RESET_ALL}  and my age is\
                {Fore.GREEN} {info.age} {Style.RESET_ALL}  my salary is {Fore.LIGHTMAGENTA_EX} {info.salary}'

    line2 = f' {Fore.BLUE} my weight is {Fore.GREEN} {info.weight} '

    line3 = f'{Fore.BLUE} my allergies is {Fore.YELLOW} {info.allergies} '

    line4 = f'{Fore.BLUE} my contact number is {Fore.LIGHTRED_EX} {info.contact_info} '

    lines5 = f'{Fore.BLUE} my email id is {Fore.LIGHTRED_EX} {info.email} '

    lines6 = f'{Fore.BLUE} where i booked is {Fore.LIGHTWHITE_EX} {str(info.booking_url)} ' # Corrected: removed trailing comma

    lines7 = f'my address is {info.addres.street}, {info.addres.city}, {info.addres.pincode}' # Corrected: access attributes

    return '\n'.join([line1, line2, line3, line4,lines5,lines6,lines7])

user_info = {
    'name': 'veena',
    'age': 20,
    'salary': 500000,
    'weight': 44.50,
    # 'allergies': ['dust', 'flue', 'heat'],
    'email': 'sachinmasti98@google.com',
    'booking_url': 'https://sachin.com',
    'contact_info': {'sachin': 7666243552},
    'addres': {'city':'delhi','pincode':1223,'street':'karolbag'}
}


massage = info(**user_info)


print(func(massage))
print(f'pin code is  {massage.addres.pincode}')