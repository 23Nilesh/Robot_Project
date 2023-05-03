from playsound import playsound
import pygame
import random
import gtts
import os
# Made by us
import coordinate_finder
import camera_inp
import distance
import Detect

global calibration, count
count = 0
calibration = False

# import faceCam
Detect.detect_init()
pygame.init()
coordinates = []

res = (1280, 720)
color = (255, 255, 255)
screen = pygame.display.set_mode(res)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)
width = screen.get_width()
height = screen.get_height()
alphabets = [0, 0, 0, 0, 0, 0]

screen = pygame.display.set_mode(res)
smallfont = pygame.font.SysFont('Corbel', 300)


def aph():
    index = 0
    for i in range(6):
        index = 64 + random.randint(1, 26)
        alphabets[i] = chr(index)


def letter():
    ltr = random.randint(0, 5)
    return ltr


def dupli():
    for i in range(6):
        if alphabets[i] == alphabets[ltr]:
            if i == ltr:
                continue
            else:
                if alphabets[i] == "A":
                    alphabets[i] = "B"
                else:
                    alphabets[i] = chr(ord(alphabets[i]) - 1)


def calibration_():
    global coordinates
    clock = pygame.time.Clock()
    fps = 10
    clock.tick(fps)
    global calibration
    global count
    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            pygame.quit()
    # red

    if count >= 0 and count < 10:
        screen.fill((255, 0, 0))

    if count == 12:
        camera_inp.get_img(0)
    # camera_inp.get_img(0)
    if count >= 15 and count < 20:
        # blue
        print("green")
        screen.fill((0, 255, 0))

    if count == 22:
        # camera_inp.get_img(1)
        camera_inp.get_img(2)
    if count >= 28 and count < 35:
        # blue
        print("blue")
        screen.fill((0, 0, 255))

    if count == 38:
        # camera_inp.get_img(1)
        camera_inp.get_img(1)
    # faceCam.end()
    if count >= 39:
        coordinates, coordinate_game = coordinate_finder.read_images()
        distance.take_dist(coordinate_game)
    if distance.dist_status():
        calibration = True
    print(count)


def game_init():
    mouse = pygame.mouse.get_pos()
    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            pygame.quit()

    screen.fill((60, 25, 60))

    pygame.draw.rect(screen, color_dark, [20, 20, width / 3 - 30, height / 2 - 40])
    pygame.draw.rect(screen, color_dark, [width / 3 + 20, 20, (width) / 3 - 30, (height / 2) - 40])
    pygame.draw.rect(screen, color_dark, [(width * 2 / 3) + 20, 20, width / 3 - 40, height / 2 - 40])

    pygame.draw.rect(screen, color_dark, [20, height / 2 + 10, width / 3 - 30, height / 2 - 30])
    pygame.draw.rect(screen, color_dark, [width / 3 + 20, height / 2 + 10, (width) / 3 - 30, height / 2 - 30])
    pygame.draw.rect(screen, color_dark, [(width * 2 / 3) + 20, height / 2 + 10, width / 3 - 40, height / 2 - 30])
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
    if i == 1:
        # code for game instruction
        t2 = gtts.gTTS("choose alphabet " + alphabets[ltr])
        t2.save("command.mp3")
        playsound("command.mp3")
        if os.path.exists("command.mp3"):
            os.remove("command.mp3")
    pygame.display.update()


# coordinates = [[[20, 20], [width/3 -10, height / 2 - 20]],
#                    [[width / 3 + 20, 20], [(width) *2/ 3 - 10,  height / 2 - 20]],
#                    [[(width * 2 / 3) + 20, 20], [width-20, height / 2 - 20]],
#                    [[20,height / 2 +10], [width/3 -10, height  - 20]],
#                    [[width / 3 + 20, height / 2 +10], [(width) *2/ 3 - 10, height  - 20]],
#                    [[(width * 2 / 3) + 20, height / 2 +10], [width-20, height  - 20]]]


i = 1
ltr = letter()
aph()
dupli()

t1 = gtts.gTTS("Welcome to Real sense based gaming console")
# # t1 = gtts.gTTS("Welcome")
t1.save("welcome.mp3")
# t1.save("welcome.mp3")
playsound("welcome.mp3")
t3 = gtts.gTTS("correct")
t3.save("correct.mp3")
t4 = gtts.gTTS("wrong")
t4.save("wrong.mp3")
while True:

    if calibration == False:
        print("calibration")
        calibration_()
    if calibration == True:
        print("game runing")
        game_init()
        i += 1
        Detect.main()

        if (Detect.hand_detected()):
            if (Detect.compare_dist()):
                coord = Detect.pixel_coordinate()
                if ((coord[0] >= coordinates[ltr][0][0] and coord[0] <= coordinates[ltr][1][0]) and (
                        coord[1] >= coordinates[ltr][0][1] and coord[1] <= coordinates[ltr][1][1])):
                    playsound("correct.mp3")
                    i = 1
                    ltr = letter()  # new correct letter
                    aph()  # new alphabet array
                    dupli()  # replacing duplicates
                else:
                    print(coordinates[ltr], "game")
                    playsound("wrong.mp3")
                    i = 1

    # for mouse (on pc)
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         running = False
    #     elif event.type == pygame.MOUSEBUTTONDOWN:
    #         x, y = pygame.mouse.get_pos()
    #         coord=[x,y]
    #         print(coord)
    #         if((coord[0]>=coordinates[ltr][0][0] and coord[0]<=coordinates[ltr][1][0]) and(coord[1]>=coordinates[ltr][0][1] and coord[1]<=coordinates[ltr][1][1])):
    #
    #             playsound("correct.mp3")
    #
    #             i=1
    #             ltr=letter()
    #             aph()
    #             dupli()
    #         else:
    #             print(coordinates[ltr])
    #
    #             playsound("wrong.mp3")
    #
    #             i=1

    # if (click_):
    # call function that gives you the coordinates in list format as finger_coord
    # if ltr[0][upper]>finger_coord(x) > ltr[0][lower] and ltr[ 1][upper]>finger_coord(y) > ltr[1][lower]
    # means selected correct
    #        i=1
    #         ltr=letter()
    #         aph()
    #         dupli()
    #     else
    #         sound of wrong:
    #         i=1

    # if(i>1):
    #     # have to add touch command at the time of integration
    #     #code ready to take input form user
    #     # continue

    count = count + 1
    pygame.display.update()
