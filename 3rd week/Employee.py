from abc import ABC, abstractmethod

from enum import Enum

class Positions (Enum):
    JUNIOR = "Junior"
    SEMISENIOR = "Semi Senior"
    SENIOR = "Senior"

class Employee (ABC):

    def __init__(self, id: int, name: str, vacation_days_left: int = 7) -> None:
        self.__id = id
        self.__name = name
        self.__vacation_days_left = vacation_days_left
        self.__salary = 0.0
    
    def get_id(self) -> int:
        return self.__id

    def get_name(self) -> str:
        return self.__name
    
    def get_salary(self) -> float:
        return self.__salary
    
    def set_salary(self, salary: float) -> None:
        self.__salary = salary
    
    def get_vacation_days_left(self) -> int:
        return self.__vacation_days_left
    
    def set_vacation_days_left(self, days: int) -> None:
        self.__vacation_days_left = days

    @abstractmethod
    def calculate_salary(self):
        pass

    @abstractmethod
    def show_info(self):
        pass

class FullTimeEmployee (Employee):

    def __init__(self, id: int, name: str, position: Positions, years_exp: int, vacation_days_left: int = 7) -> None:
        super().__init__(id, name, vacation_days_left)
        self.__position = position
        self.set_years_exp(years_exp)

    def get_position(self):
        return self.__position.value

    def set_position(self, position: Positions):
        self.__position = position
    
    def get_years_exp(self):
        return self.__years_exp

    def set_years_exp(self, years: int):
        if(years>20) and (years<0):
            raise ValueError("Los años de experiencia deben estar entre 0 y 20")
        else:
            self.__years_exp = years


    def calculate_salary(self):
        salary = 0
        if(self.__position == Positions.JUNIOR):
            salary += 4000
        elif(self.__position == Positions.SEMISENIOR):
            salary += 9000
        else:
            salary += 15000
        salary += self.__years_exp*1000
        self.set_salary(salary)

    def show_info(self):
        print(f"Est@ emplead@ a tiempo completo es {self.get_name()}, con id de {self.get_id()}. \nLe quedan {self.get_vacation_days_left()} días de vacaciones libres. \nSu posición es de {self.get_position()} y su salario de ${self.get_salary():.2f}")

            
class HalfTimeEmployee (Employee):

    def __init__(self, id: int, name: str, position: Positions, years_exp: int, vacation_days_left: int = 7) -> None:
        super().__init__(id, name, vacation_days_left)
        self.__position = position
        self.set_years_exp(years_exp)

    def get_position(self):
        return self.__position.value

    def set_position(self, position):
        self.__position = position
    
    def get_years_exp(self):
        return self.__years_exp

    def set_years_exp(self, years):
        if(years>15) and (years<0):
            raise ValueError("Los años de experiencia deben estar entre 0 y 15")
        else:
            self.__years_exp = years


    def calculate_salary(self):
        salary = 0
        if(self.__position == Positions.JUNIOR):
            salary += 3000
        elif(self.__position == Positions.SEMISENIOR):
            salary += 6000
        else:
            salary += 10000
        salary += self.__years_exp*500
        self.set_salary(salary)
        

    def show_info(self):
        print(f"Est@ emplead@ a medio tiempo es {self.get_name()}, con id de {self.get_id()}. \nLe quedan {self.get_vacation_days_left()} días de vacaciones libres. \nSu posición es de {self.get_position()} y su salario de ${self.get_salary():.2f}")        

class ContractorEmployee (Employee):

    def __init__(self, id: int, name: str, years_exp: int, vacation_days_left: int = 7) -> None:
        super().__init__(id, name, vacation_days_left)
        self.set_years_exp(years_exp)
    
    def get_years_exp(self):
        return self.__years_exp

    def set_years_exp(self, years):
        if(years>10) and (years<0):
            raise ValueError("Los años de experiencia deben estar entre 0 y 15")
        else:
            self.__years_exp = years

    def calculate_salary(self):
        salary = 2000
        salary += self.__years_exp*300/self.get_vacation_days_left()
        self.set_salary(salary)

    def show_info(self):
        print(f"Est@ emplead@ contratista es {self.get_name()}, con id de {self.get_id()}. \nLe quedan {self.get_vacation_days_left()} días de vacaciones libres. \nSu salario es de ${self.get_salary():.2f}")



def display_employee_info(employees):
    if not employees:
        print("No employees to display\n")
        return

    print("Employee Information:")
    for employee in employees:
        employee.calculate_salary()
        employee.show_info()
        print("----------------------")
      
emp1 = FullTimeEmployee(10035, "Alan Brito", Positions.SENIOR, 12)
emp2 = HalfTimeEmployee(20034, "Helen Chufe", Positions.SEMISENIOR, 5)
emp3 = ContractorEmployee(90092, "Susana Horia", 8)

employees = [emp1, emp2, emp3]
display_employee_info(employees)


