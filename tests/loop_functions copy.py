import keyboard
import time


def main_menu(x):
  res = "main menu" + str(x)
  return res

def divide_by_two(x):
  return x/2

def square(x):
  return x**21

def invalid_op(x):
  raise Exception("Invalid operation")


ops = {
  "add_one": main_menu,
  "divide_by_two": divide_by_two,
  "square": square}

# The better way:
def model(x, chosen_operation="add_one"):

  chosen_operation_function = ops.get(chosen_operation, invalid_op)
  return chosen_operation_function(x)


def controller():
  print("controller")
  if keyboard.is_pressed("1"):
    res = "add one"
  elif keyboard.is_pressed("2"):
    res = "divide_by_two"
  elif keyboard.is_pressed("3"):
    res = "square"
  else:
    res = False
  print(res)
  return res

val = 4
event =  "add one"



run = True
while run:
  event = controller()
  val = model(val)
  print(val, event)
  time.sleep(1)