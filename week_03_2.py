"""
Классы и наследование
"""
import os.path
import csv

CAR_TYPES = {'Car': 'car', 'Truck': 'truck', 'SpecMachine': 'spec_machine'}
PHOTO_FILE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif')


class CarBase:
    def __init__(self, brand: str, photo_file_name: str, carring: float):
        self.car_type = None
        self.photo_file_name = photo_file_name
        self.brand = brand
        self.carring = float(carring)

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]


class Car(CarBase):

    def __init__(self, brand: str, photo_file_name: str, carring: float, passenger_seats_count: int):
        super().__init__(brand, photo_file_name, carring)
        self.car_type = CAR_TYPES['Car']
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):

    def __init__(self, brand: str, photo_file_name: str, carring: float, body_whl: str):
        super().__init__(brand, photo_file_name, carring)
        self.car_type = CAR_TYPES['Truck']
        self.body_width = 0.0
        self.body_height = 0.0
        self.body_length = 0.0
        self.body_volume = 0.0

        if body_whl:
            self.set_truck_body(body_whl)

    def set_truck_body(self, body_whl):
        try:
            l, w, h = map(float, body_whl.split('x'))
        except ValueError:
            l, w, h = 0.0, 0.0, 0.0

        self.body_width = w
        self.body_height = h
        self.body_length = l
        self.body_volume = l * w * h

    def get_body_volume(self):
        return self.body_volume


class SpecMachine(CarBase):
    def __init__(self, brand: str, photo_file_name: str, carring: float, extra: str):
        super().__init__(brand, photo_file_name, carring)
        self.extra = extra


def get_car_list(file_name: str):
    cars_and_spec_machine = []
    with open(file_name, encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)
        for row in reader:
            item = get_cars_from_csv_row(row)
            if item:
                cars_and_spec_machine.append(item)
    return cars_and_spec_machine


def get_cars_from_csv_row(row):

    if len(row) != 7 and row[0] not in CAR_TYPES.values():
        return

    car_type, brand, passenger_sc, photo, body_whl, carrying, extra = row

    if os.path.splitext(photo)[1] not in PHOTO_FILE_EXTENSIONS:
        return

    if not (brand and photo and carrying):
        return

    try:
        carrying = float(carrying)
    except ValueError:
        return

    if car_type == CAR_TYPES['Car']:
        try:
            passenger_sc = int(passenger_sc)
        except ValueError:
            return None
        return Car(brand, photo, carrying, passenger_sc)

    if car_type == CAR_TYPES['Truck']:
        return Truck(brand, photo, carrying, body_whl)

    if car_type == CAR_TYPES['SpecMachine']:
        if not extra:
            return None
        return SpecMachine(brand, photo, carrying, extra)


if __name__ == '__main__':
    cars = get_car_list('file.csv')

    for i in cars:
        if i.car_type == CAR_TYPES['Car']:
            print(i.car_type, i.brand, i.get_photo_file_ext(), i.carring, i.passenger_seats_count, sep=', ')
        elif i.car_type == CAR_TYPES['Truck']:
            print(i.car_type, i.brand, i.get_photo_file_ext(), i.carring, i.body_length, i.get_body_volume(), sep=', ')
        else:
            print(i.car_type, i.brand, i.get_photo_file_ext(), i.carring, i.extra, sep=', ')
