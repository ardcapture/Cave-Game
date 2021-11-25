# font = pygame.font.SysFont(None, 24)
# img = font.render('hello', True, BLUE)
# screen.blit(img, (20, 20))

# print(tuple([55] * 3))


mylist = []
def countdown(x):
    if (x < 256):
        res = countdown((x*2))
        if res >= 255:
            res += -1
        mylist.append(tuple([res] * 3))
    return x



countdown(1)
print("mylist", mylist)
