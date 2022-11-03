##############################
# Urban Riders Part-2        #
# MD MEZBAH UDDIN            #
# Nantong University(China)  #
# CSE                        #
#                            #
##############################

import hashlib
from random import random, randint,choice
from brta import BRTA
from vehicles import Bike, Car, Cng
from ride_manager import uber
import threading

class UserAlreadyExists(Exception):
    def __init__(self,email, *args: object):
        print(f'User:{email} already exists')
        super().__init__(*args)

license_authority = BRTA()
class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        pwd_encrypted = hashlib.md5(password.encode()).hexdigest()
        already_exists = False
        with open('users.txt', 'r') as file:
            # file.write(f'{email} {pwd_encrypted}')
            if email in file.read():
                already_exists = True
        file.close()
        # print(self.name, 'user created')
    
    @staticmethod
    def log_in(email, password):
        stored_password = ''
        with open('users.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if email in line:
                    stored_password = line.split(' ')[1]
        file.close()
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        if hashed_password == stored_password:
            print('valid user')
            return True
        else:
            print('invalid user')
            return False
        # print('password found', stored_password)

class Rider(User):
    def __init__(self, name, email, password, location, balance):
        self.location = location
        self.balance = balance
        self.__trip_history = []
        super().__init__(name, email, password)

    def set_location(self, location):
        self.location = location

    def get_location(self):
        return self.location

    def request_trip(self, destination):
        pass

    def get_trip_history(self):
        return self.__trip_history

    def start_a_trip(self, fare,trip_info):
        print(f'A trip started for {self.name}')
        self.balance -= fare
        self.__trip_history.append(trip_info)

class Driver(User):
    def __init__(self, name, email, password, location, license):
        super().__init__(name, email, password)
        self.location = location
        self.__trip_history = []
        self.license = license
        self.valid_driver = license_authority.validate_license(email, license)
        self.earning = 0
        self.vehicle = None

    def take_driving_test(self):
        result = license_authority.take_driving_test(self.email)
        if result == False:
            # print('Sorry you failed, try again')
            self.license = None
        else: 
            self.license = result
            self.valid_driver = True

    def register_a_vehicle(self, vehicle_type, license_plate, rate):
        if self.valid_driver is True:
            if vehicle_type == 'car':
                self.vehicle = Car(vehicle_type, license_plate, rate, self)
                uber.add_a_vehicle(vehicle_type, self.vehicle)
            elif vehicle_type == 'bike':
                self.vehicle = Bike(vehicle_type, license_plate, rate, self)
                uber.add_a_vehicle(vehicle_type,self.vehicle)
            else:
                self.vehicle = Cng(vehicle_type,license_plate,rate,self)
                uber.add_a_vehicle(vehicle_type, self.vehicle)
        else:
            # print('you are not a valid driver')
            pass

    def start_a_trip(self,start, destination, fare,trip_info):
        self.earning += fare
        self.location = destination
        self.__trip_history.append(trip_info)
        #start thread
        trip_thread = threading.Thread(target=self.vehicle.start_driving,args=(start,destination,))
        trip_thread.start()
        # self.vehicle.start_driving(start,destination)
        
# hero = User('Hero Alom','hero@alom.com','heroOhHero')
# User.log_in('hero@alom.com','heroOhHero')

# kuber = Driver('kuber Maji','kuber@gmail.com','kopilaJaisna',54,4556)

# result=license_authority.validate_license(kuber.email,kuber.license)
# print(result)
# kuber.take_driving_test()
# result=license_authority.validate_license(kuber.email,kuber.license)
# print(result)

rider1 = Rider('rider1', 'rider1@gmail.com', 'rider1', randint(0, 30), 1000)
rider2 = Rider('rider2', 'rider2@gmail.com', 'rider2', randint(0, 30), 5000)
rider3 = Rider('rider3', 'rider3@gmail.com', 'rider3', randint(0, 30), 5000)
rider4 = Rider('rider4', 'rider4@gmail.com', 'rider4', randint(0, 30), 5000)
rider5 = Rider('rider5', 'rider3@gmail.com', 'rider5', randint(0, 30), 5000)

vehicle_type = ['car','bike','cng']

for i in range(1,100):
    driver1 = Driver(f'driver{i}', f'driver{i}@gmail.com', f'driver{i}', randint(0, 100), randint(1000,9999))
    driver1.take_driving_test()
    driver1.register_a_vehicle(choice(vehicle_type),randint(10000, 99999),10)

# driver2 = Driver('driver2', 'driver2@gmail.com', 'driver2', randint(0, 30), 5645)
# driver2.take_driving_test()
# driver2.register_a_vehicle('car', 1245, 10)

# driver3 = Driver('driver3', 'driver3@gmail.com', 'driver3', randint(0, 30), 5645)
# driver3.take_driving_test()
# driver3.register_a_vehicle('car', 2145, 10)

# driver4 = Driver('driver4', 'driver4@gmail.com', 'driver4', randint(0, 30), 5645)
# driver4.take_driving_test()
# driver4.register_a_vehicle('car', 3245, 10)

print(uber.get_available_cars())

uber.find_a_vehicle(rider1,choice(vehicle_type),randint(1,100))
uber.find_a_vehicle(rider2,choice(vehicle_type),randint(1,100))
uber.find_a_vehicle(rider3,choice(vehicle_type),randint(1,100))
uber.find_a_vehicle(rider4,choice(vehicle_type),randint(1,100))
uber.find_a_vehicle(rider5,choice(vehicle_type),randint(1,100))
# uber.find_a_vehicle(rider1,'car',randint(1,100))
# uber.find_a_vehicle(rider2,'cng',randint(1,100))

print(rider1.get_trip_history())
print(uber.total_income())