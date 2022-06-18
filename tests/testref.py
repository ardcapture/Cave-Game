class car1():
    def __init__(self):
        self.color = 'blue'

car2 = car1

car2.color = 'red'

# print(car1.color)   



# for attr, value in car1.__dict__.items():
#         print(attr, value)





print(car2.__dict__)