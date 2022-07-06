print('******************************')


def hello():
    print('hello')

def bye():
    print('bye')

def stink():
    print('stink')




print_functions_list = [
    hello,
    bye,
    stink,
    hello,
    stink
]


def run_fuctions(func_list):
    [func() for func in func_list]


run_fuctions(print_functions_list)


