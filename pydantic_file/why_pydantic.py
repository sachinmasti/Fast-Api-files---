from colorama import Fore,Style,init
init(autoreset=True)
from pydantic import BaseModel


class info(BaseModel):
    name:str
    age:int
    salary:int

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
    return (
        f'my name is {Fore.CYAN} {info.name} {Style.RESET_ALL} '
        f' and my age is {Fore.GREEN} {info.age} {Style.RESET_ALL} '
        f' my salary is {Fore.LIGHTMAGENTA_EX} {info.salary}'
    )

user_info = {'name':'veena','age':20,'salary':500000}

massage = info(**user_info)
print(func(massage))