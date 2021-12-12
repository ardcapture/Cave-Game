import keyboard
import mouse
import time


while True:
    if keyboard.is_pressed("up"):
        print("up is pressed")
        time.sleep(0.5)


# print("keyboard test")



# recorded = keyboard.record(until='esc')


# print("recorded", recorded)