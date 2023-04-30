"""
Дескриптор с комиссией
Часто при зачислении каких-то средств на счет с нас берут комиссию.
Давайте реализуем похожий механизм с помощью дескрипторов.
Напишите дескриптор Value, который будет использоваться в нашем классе Account
"""

class Value:
    def __init__(self):
        self.amount = None

    def __get__(self, obj, obj_type):
        return self.amount

    def __set__(self, obj, value):
        self.amount = value - (value * obj.commission)


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission


class ValueV2:

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, obj_type):
        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        obj.__dict__[self.name] = value * (1 - obj.commission)


class AccountV2:
    amount = ValueV2()

    def __init__(self, commission):
        self.commission = commission


if __name__ == '__main__':
    values = Account(0.1)
    values.amount = 100
    print('Account =', values.amount)

    values = AccountV2(0.1)
    values.amount = 100
    print('AccountV2 =', values.amount)