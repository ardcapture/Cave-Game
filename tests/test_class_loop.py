


GRID_SIZE = 32
WIDTH, HEIGHT = (GRID_SIZE*2) + (GRID_SIZE *
                                 35), (GRID_SIZE*2) + (GRID_SIZE * 22)

top_ofset = 5

objs = []



class MyClass():
    def __init__(self, drawable, position, dimentions):
        self.drawable = drawable
        self.position = position
        self.dimentions = dimentions


for x in range(GRID_SIZE, WIDTH, GRID_SIZE * 2):
    for y in range(GRID_SIZE * top_ofset, HEIGHT - (GRID_SIZE * 2), GRID_SIZE * 2):
        objs.append(MyClass(True, (x, y), (0, 0, 0)))




# objs = [MyClass(True, (x, y), (0, 0, 0)) for x in range(GRID_SIZE, WIDTH, GRID_SIZE * 2) for y in range(GRID_SIZE * top_ofset, HEIGHT - (GRID_SIZE * 2), GRID_SIZE * 2) if (x, y)]

# print(objs)

# positions_list = []
# for obj in objs:
#     positions_list.append(obj.position)
    # print(obj.drawable, obj.position, obj.dimentions)
    # print(obj.position)
    # other_object.add(obj)

positions_list = [obj.position for obj in objs]


print(positions_list)



# objs[0].do_sth()