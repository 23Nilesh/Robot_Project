import pygame
import sys
import random
import gtts
from playsound import playsound
# import coordinate_finder
# import camera_inp
import time
import faceCam
pygame.init()

global count
count = 0
global calibration
calibration=False
res = (1280, 720)
color = (255, 255, 255)
screen = pygame.display.set_mode(res)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)
width = screen.get_width()
height = screen.get_height()
alphabets=[0,0,0,0,0,0]

screen = pygame.display.set_mode(res)
smallfont = pygame.font.SysFont('Corbel', 300)

def aph():
    index=0
    i=0
    for i in range(6):

        index=64+random.randint(1,26)
        alphabets[i]=chr(index)


aph()

def letter():

    ltr= random.randint(0,5)
    return ltr
ltr=letter()

def dupli():
    for i in range(6):
        if(alphabets[i]==alphabets[ltr]):
            if(i==ltr):
                continue
            else:
                if(alphabets[i]=="A"):
                    alphabets[i]="B"
                else :
                    alphabets[i]=chr(ord(alphabets[i])-1)
dupli()



def calibration_():
    clock = pygame.time.Clock()
    fps = 10
    clock.tick(fps)
    global calibration
    global count
    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            pygame.quit()
    #red

    if(count>=0 and count<10):
        screen.fill((255, 0, 0))

    if(count==12):
        faceCam.get_img(0)
    # camera_inp.get_img(0)
    if(count>=15 and count<20):
        # blue
        print("green")
        screen.fill((0, 255, 0))


    if(count==22):
    # camera_inp.get_img(1)
        faceCam.get_img(1)
    if (count>=28 and count<35):
        # blue
        print("blue")
        screen.fill((0, 0, 255))

    if (count==38):
        # camera_inp.get_img(1)
        faceCam.get_img(2)
    # faceCam.end()
    if(count==44):
        calibration=True
    print(count)




coordinates = [[[20, width / 3 - 20], [20, height / 2 - 40]], [[width / 3 + 20, (width)/3 -20], [20,(height/2) -40]], [[(width *2/ 3) +20,width/3 -40], [20,(height/2) -40]],
               [[20, width / 3 - 20], [height / 2,height/2 -20]],[[width / 3 + 20, (width)/3 -20], [height / 2,height/2 -20]],
               [[(width *2/ 3) +20,width/3 -40], [height / 2,height/2 -20]]]
i=0
# t1 = gtts.gTTS("Welcome to Real sense based gaming console")
# t1 = gtts.gTTS("Welcome")
#
# t1.save("welcome.mp3")
# playsound("welcome.mp3")


while True:

    if(calibration==False):
        calibration_()
    if(calibration==True):
        mouse = pygame.mouse.get_pos()
        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()

            if ev.type == pygame.MOUSEBUTTONDOWN:

        # if width / 4 <= mouse[0] <= width / 4 + 240 and height / 3 <= mouse[1] <= height / 3 + 440:
                print("click")

        screen.fill((60, 25, 60))

        pygame.draw.rect(screen, color_dark, [20, 20, width / 3 - 20, height / 2 - 40])
        pygame.draw.rect(screen, color_dark, [width / 3 + 20, 20, (width) / 3 - 20, (height / 2) - 40])
        pygame.draw.rect(screen, color_dark, [(width * 2 / 3) + 20, 20, width / 3 - 40, height / 2 - 40])

        pygame.draw.rect(screen, color_dark, [20, height / 2, width / 3 - 20, height / 2 - 20])
        pygame.draw.rect(screen, color_dark, [width / 3 + 20, height / 2, (width) / 3 - 20, height / 2 - 20])
        pygame.draw.rect(screen, color_dark, [(width * 2 / 3) + 20, height / 2, width / 3 - 40, height / 2 - 20])
        # if width / 4 <= mouse[0] <= width / 4 + 240 and height / 3 <= mouse[1] <= height / 3 + 440:
        #     pygame.draw.rect(screen, color_light, [width / 4, height / 3, 440, 640])
        #
        # else:
        #     pygame.draw.rect(screen, color_dark, [width / 4, height / 3, 240, 440])

        # superimposing the text onto our button
        screen.blit(smallfont.render(alphabets[0], True, color), (100, 80))
        screen.blit(smallfont.render(alphabets[1], True, color), (width / 3 + 120, 80))
        screen.blit(smallfont.render(alphabets[2], True, color), (width * 2 / 3 + 120, 80))

        screen.blit(smallfont.render(alphabets[3], True, color), (100, height / 2 + 60))
        screen.blit(smallfont.render(alphabets[4], True, color), (width / 3 + 120, height / 2 + 60))
        screen.blit(smallfont.render(alphabets[5], True, color), (width * 2 / 3 + 120, height / 2 + 60))

        if (i == 1):
            # code for game instruction
            t2 = gtts.gTTS("choose alphabet " + alphabets[ltr])
            t2.save("command.mp3")
            playsound("command.mp3")

        # if(i>1):
        #     # have to add touch command at the time of integration
        #     #code ready to take input form user
        #     # continue
        i += 1
    count=count+1
    pygame.display.update()
