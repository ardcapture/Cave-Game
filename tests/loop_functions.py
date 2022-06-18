# raw = 'asdfaa3fa!!!'
# functions = [str.isalnum, str.isalpha, str.isdigit, str.islower,  str.isupper]  # list of functions

# for fn in functions:     # iterate over list of functions, where the current function in the list is referred to as fn
#     for ch in raw:       # for each character in the string raw
#         if fn(ch):        
#             print(str(fn), True)
#             break



def add_one(x):
  return x + 1

def divide_by_two(x):
  return x/2

def square(x):
  return x**2

def invalid_op(x):
  raise Exception("Invalid operation")

# The better way:
def perform_operation(x, chosen_operation="add_one"):
  ops = {
    "add_one": add_one,
    "divide_by_two": divide_by_two,
    "square": square
  }
  
  chosen_operation_function = ops.get(chosen_operation, invalid_op)
  
  return chosen_operation_function(x)


print(perform_operation(4, "divide_by_two"))