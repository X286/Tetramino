#coding=utf-8
import numpy
import os
from matrix import *


def ret_figure():
    line = numpy.array([
        [[0, 0, 0], [0, 0, 0], [0, 0, 1], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 1], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 1], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 1], [0, 0, 0]]
    ])

    square = numpy.array([
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 1], [0, 0, 1], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 1], [0, 0, 1], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    ])
    trangle = numpy.array([
        [[0, 0, 0], [0, 0, 1], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 1], [0, 0, 1], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 1], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    ])
    corner_left = numpy.array([
        [[0, 0, 0], [0, 0, 0], [0, 0, 1], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 1], [0, 0, 1]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 1]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    ])
    corner_right = numpy.array([
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 1]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 1], [0, 0, 1]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 1], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    ])
    G_block_left = numpy.array([
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 1], [0, 0, 1], [0, 0, 1]],
        [[0, 0, 0], [0, 0, 1], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    ])
    G_block_right = numpy.array([
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 1], [0, 0, 1], [0, 0, 1]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 1]],
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    ])
    chosed = random.choice([[line, 'line'], [square, 'square'], [trangle, 'trangle'], [corner_left, 'corner_left'],
                            [corner_right, 'corner_right'], [G_block_left, 'G_block_left'],
                            [G_block_right, 'G_block_right']])
    return chosed


def __main__ ():
    bglist, bgcount = os.listdir ('res'), 5
    pygame.init()
    img = pygame.image.load('tetra.png')
    width, height = 800, 600
    FPS = pygame.time.Clock()
    pygame.display.set_caption('Tetra')
    pygame.display.set_icon(img)
    screen = pygame.display.set_mode((width, height))
    isLive = True
    background = GameObject (0,0, width, height)
    background.image = pygame.image.load('res\\'+bglist[bgcount])
    pygame.mixer.init()
    music_counter = 0.05
    pygame.mixer.music.load ('music\cuttedTheme.wav')
    pygame.mixer.music.set_volume(music_counter)
    pygame.mixer.music.play(-1)
    sound_counter = 0.3
    removeLine_sound = pygame.mixer.Sound ('sound/removeLine.wav')
    removeLine_sound.set_volume(sound_counter)
    layBrick = pygame.mixer.Sound ('sound/linePlace.wav')
    layBrick.set_volume(sound_counter)
    # objects
    #draw net
    horisontal_netWork = Net(250, 20, 242, 530, 3, 24)
    speed = 24

    # DrawWalls
    walls = pygame.sprite.Group()
    Wall_down  = GameObject (252, 548, 242, 3, color='#FF00FF')
    Wall_left  = GameObject (248, 20, 3, 530, color='#FF00FF')
    Wall_right = GameObject (250+240, 20, 3, 527, color='#FF00FF')
    walls.add(Wall_down, Wall_left, Wall_right)
    # end draw walls

    matrix = Matrix(348, 22, 22, 22, 2, ret_figure())
    figure = Figure (matrix)


    #Text
    score = 0
    text = Text(24, color='#FE2E64')
    GameOver = Text (52, color='#AAAAFF')
    GameOver.text = 'Game Over'
    pause_text = Text(52, color='#00bb00')
    pause_text.text = 'Pause!'
    #Game over varible
    is_over = False

    # Event figure down
    MoveFigure_down = pygame.USEREVENT + 1
    counter, counter_slot, pause = 1000, 0, False
    pygame.time.set_timer(MoveFigure_down, counter)
    group = pygame.sprite.Group()

    # rotete func
    def rotate():
        if is_over == False:
            if figure.matrix.matrix_name == 'line':
                if figure.rotateCount == 1:
                    figure.rotate(numpy.array([
                        [[0], [0], [1], [0]],
                        [[0], [0], [1], [0]],
                        [[0], [0], [1], [0]],
                        [[0], [0], [1], [0]]
                    ]))
                    figure.rotateCount = 0

                elif figure.rotateCount == 0:
                    figure.rotate(numpy.array([
                            [[0], [0], [0], [0]],
                            [[1], [1], [1], [1]],
                            [[0], [0], [0], [0]],
                            [[0], [0], [0], [0]]
                        ]))
                    if (pygame.sprite.groupcollide(figure.figure, walls, 0, 0)) or (pygame.sprite.groupcollide(figure.figure, group, 0, 0)):
                        figure.rotate(numpy.array([
                            [[0], [0], [1], [0]],
                            [[0], [0], [1], [0]],
                            [[0], [0], [1], [0]],
                            [[0], [0], [1], [0]]
                        ]))
                    else:
                        figure.rotateCount += 1

            elif figure.matrix.matrix_name == 'trangle':
                if figure.rotateCount == 0:
                    figure.rotate(numpy.array([
                        [[0], [1], [1], [1]],
                        [[0], [0], [1], [0]],
                        [[0], [0], [0], [0]],
                        [[0], [0], [0], [0]]
                    ]))
                    if (pygame.sprite.groupcollide(figure.figure, walls, 0, 0)) or (pygame.sprite.groupcollide(figure.figure, group, 0, 0)):
                        figure.rotate(numpy.array([
                            [[0], [1], [0], [0]],
                            [[0], [1], [1], [0]],
                            [[0], [1], [0], [0]],
                            [[0], [0], [0], [0]]
                        ]))
                    else:
                        figure.rotateCount += 1

                elif figure.rotateCount == 1:
                    figure.rotate(numpy.array([
                        [[0], [0], [0], [1]],
                        [[0], [0], [1], [1]],
                        [[0], [0], [0], [1]],
                        [[0], [0], [0], [0]]
                    ]))

                    figure.rotateCount += 1

                elif figure.rotateCount == 2:
                    figure.rotate(numpy.array([
                        [[0], [0], [0], [0]],
                        [[0], [0], [1], [0]],
                        [[0], [1], [1], [1]],
                        [[0], [0], [0], [0]]
                    ]))
                    if (pygame.sprite.groupcollide(figure.figure, walls, 0, 0)) or (
                    pygame.sprite.groupcollide(figure.figure, group, 0, 0)):
                        figure.rotate(numpy.array([
                            [[0], [0], [0], [1]],
                            [[0], [0], [1], [1]],
                            [[0], [0], [0], [1]],
                            [[0], [0], [0], [0]]
                        ]))
                    else:
                        figure.rotateCount += 1

                elif figure.rotateCount == 3:
                    figure.rotate(numpy.array([
                        [[0], [1], [0], [0]],
                        [[0], [1], [1], [0]],
                        [[0], [1], [0], [0]],
                        [[0], [0], [0], [0]]
                    ]))

                    figure.rotateCount = 0

            elif figure.matrix.matrix_name == 'corner_left':
                if figure.rotateCount == 1:
                    figure.rotate(numpy.array([
                        [[0], [0], [1], [0]],
                        [[0], [0], [1], [1]],
                        [[0], [0], [0], [1]],
                        [[0], [0], [0], [0]]
                    ]))
                    figure.rotateCount = 0

                elif figure.rotateCount == 0 :
                    figure.rotate(numpy.array([
                        [[0], [0], [0], [0]],
                        [[0], [0], [1], [1]],
                        [[0], [1], [1], [0]],
                        [[0], [0], [0], [0]]
                    ]))
                    if (pygame.sprite.groupcollide(figure.figure, walls, 0, 0)) or (pygame.sprite.groupcollide(figure.figure, group, 0, 0)):
                        figure.rotate(numpy.array([
                            [[0], [0], [1], [0]],
                            [[0], [0], [1], [1]],
                            [[0], [0], [0], [1]],
                            [[0], [0], [0], [0]]
                        ]))
                    else:
                        figure.rotateCount = 1

            elif figure.matrix.matrix_name == 'corner_right':
                if figure.rotateCount == 1:
                    figure.rotate(numpy.array([
                        [[0], [0], [0], [1]],
                        [[0], [0], [1], [1]],
                        [[0], [0], [1], [0]],
                        [[0], [0], [0], [0]]
                    ]))
                    figure.rotateCount = 0

                elif figure.rotateCount == 0:
                    figure.rotate(numpy.array([
                        [[0], [0], [0], [0]],
                        [[0], [1], [1], [0]],
                        [[0], [0], [1], [1]],
                        [[0], [0], [0], [0]]
                    ]))
                    if (pygame.sprite.groupcollide(figure.figure, walls, 0, 0)) or (pygame.sprite.groupcollide(figure.figure, group, 0, 0)):
                        figure.rotate(numpy.array([
                            [[0], [0], [0], [1]],
                            [[0], [0], [1], [1]],
                            [[0], [0], [1], [0]],
                            [[0], [0], [0], [0]]
                        ]))
                    else:
                        figure.rotateCount += 1


            elif figure.matrix.matrix_name == 'G_block_left':

                if figure.rotateCount == 0:
                    figure.rotate(numpy.array([
                        [[0], [1], [1], [0]],
                        [[0], [0], [1], [0]],
                        [[0], [0], [1], [0]],
                        [[0], [0], [0], [0]]
                    ]))

                    figure.rotateCount += 1

                elif figure.rotateCount == 1:
                    figure.rotate(numpy.array([
                        [[0], [0], [0], [1]],
                        [[0], [1], [1], [1]],
                        [[0], [0], [0], [0]],
                        [[0], [0], [0], [0]]
                    ]))
                    if (pygame.sprite.groupcollide(figure.figure, walls, 0, 0)) or (
                    pygame.sprite.groupcollide(figure.figure, group, 0, 0)):
                        figure.rotate(numpy.array([
                            [[0], [1], [1], [0]],
                            [[0], [0], [1], [0]],
                            [[0], [0], [1], [0]],
                            [[0], [0], [0], [0]]
                        ]))
                    else:
                        figure.rotateCount += 1

                elif figure.rotateCount == 2:
                    figure.rotate(numpy.array([
                        [[0], [0], [1], [0]],
                        [[0], [0], [1], [0]],
                        [[0], [0], [1], [1]],
                        [[0], [0], [0], [0]]
                    ]))
                    figure.rotateCount += 1

                elif figure.rotateCount == 3:
                    figure.rotate(numpy.array([
                        [[0], [0], [0], [0]],
                        [[0], [1], [1], [1]],
                        [[0], [1], [0], [0]],
                        [[0], [0], [0], [0]]
                    ]))
                    if (pygame.sprite.groupcollide(figure.figure, walls, 0, 0)) or (
                            pygame.sprite.groupcollide(figure.figure, group, 0, 0)):
                        figure.rotate(numpy.array([
                            [[0], [0], [1], [0]],
                            [[0], [0], [1], [0]],
                            [[0], [0], [1], [1]],
                            [[0], [0], [0], [0]]
                        ]))
                    else:
                        figure.rotateCount = 0


            elif figure.matrix.matrix_name == 'G_block_right':

                if figure.rotateCount == 0:
                    figure.rotate(numpy.array([
                        [[0], [0], [1], [0]],
                        [[0], [0], [1], [0]],
                        [[0], [1], [1], [0]],
                        [[0], [0], [0], [0]]
                    ]))
                    figure.rotateCount += 1

                elif figure.rotateCount == 1:
                    figure.rotate(numpy.array([
                        [[0], [1], [0], [0]],
                        [[0], [1], [1], [1]],
                        [[0], [0], [0], [0]],
                        [[0], [0], [0], [0]]
                    ]))
                    if (pygame.sprite.groupcollide(figure.figure, walls, 0, 0)) or (
                            pygame.sprite.groupcollide(figure.figure, group, 0, 0)):
                        figure.rotate(numpy.array([
                            [[0], [0], [1], [0]],
                            [[0], [0], [1], [0]],
                            [[0], [1], [1], [0]],
                            [[0], [0], [0], [0]]
                        ]))
                    else:
                        figure.rotateCount += 1

                elif figure.rotateCount == 2:
                    figure.rotate(numpy.array([
                        [[0], [0], [1], [1]],
                        [[0], [0], [1], [0]],
                        [[0], [0], [1], [0]],
                        [[0], [0], [0], [0]]
                    ]))

                    figure.rotateCount += 1


                elif figure.rotateCount == 3:
                    figure.rotate(numpy.array([
                        [[0], [0], [0], [0]],
                        [[0], [1], [1], [1]],
                        [[0], [0], [0], [1]],
                        [[0], [0], [0], [0]]
                    ]))
                    if (pygame.sprite.groupcollide(figure.figure, walls, 0, 0)) or (
                            pygame.sprite.groupcollide(figure.figure, group, 0, 0)):
                        figure.rotate(numpy.array([
                            [[0], [0], [1], [1]],
                            [[0], [0], [1], [0]],
                            [[0], [0], [1], [0]],
                            [[0], [0], [0], [0]]
                        ]))

                    else:

                        figure.rotateCount = 0


    while (isLive):
        FPS.tick(60)
        key_press = pygame.key.get_pressed()
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isLive = False
            if event.type == MoveFigure_down :
                if is_over == False:
                    figure.moveLine_down(speed)
                    if pygame.sprite.groupcollide(figure.figure, walls, 0, 0) or pygame.sprite.groupcollide(figure.figure, group, 0, 0) :
                        figure.moveLine_up(speed)

                        for sprite in figure.figure:
                            group.add(sprite)
                        matrix = Matrix(348, 22, 22, 22, 2, ret_figure())
                        figure = Figure(matrix)
                        layBrick.play()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    rotate ()
                if event.key == pygame.K_RIGHT:
                    if is_over == False and counter > 0:
                        figure.moveLine_right(speed)
                        if pygame.sprite.groupcollide(figure.figure, walls, 0, 0) or pygame.sprite.groupcollide(figure.figure, group, 0, 0):
                            figure.moveLine_left(speed)

                if event.key == pygame.K_LEFT:
                    if is_over == False and counter > 0:
                        figure.moveLine_left(speed)
                        if pygame.sprite.groupcollide(figure.figure, walls, 0, 0) or pygame.sprite.groupcollide(figure.figure, group, 0, 0):
                            figure.moveLine_right(speed)

                if event.key == pygame.K_r:
                    is_over = False
                    group.empty()
                    score = 0
                    matrix = Matrix(348, 22, 22, 22, 2, ret_figure())
                    figure = Figure(matrix)
                    speed = 24
                    text.text = "Score: " + str(score)

                #music voliume
                if event.key == pygame.K_EQUALS:
                    music_counter += 0.05
                    if music_counter >=1:
                        music_counter == 1
                    pygame.mixer.music.set_volume(music_counter)
                if event.key == pygame.K_MINUS:
                    music_counter -= 0.05
                    if music_counter < 0.0:
                        music_counter = 0.0
                    pygame.mixer.music.set_volume(music_counter)
                # sound_voliume
                if  event.key == pygame.K_p:
                    sound_counter += 0.1
                    if sound_counter >= 1.0:
                        sound_counter = 1.0
                    removeLine_sound.set_volume(sound_counter)
                    layBrick.set_volume(sound_counter)

                if event.key == pygame.K_o:
                    sound_counter -= 0.1
                    if sound_counter <= 0.0:
                        sound_counter = 0.0
                    removeLine_sound.set_volume(sound_counter)
                    layBrick.set_volume(sound_counter)



                if event.key == pygame.K_SPACE:
                    if pause == False:
                        counter_slot = counter
                        counter = 0
                        pygame.time.set_timer(MoveFigure_down, counter)
                        pause = True
                    else:
                        counter = counter_slot
                        pygame.time.set_timer(MoveFigure_down, counter)
                        pause = False

        if key_press[pygame.K_DOWN]:
            if is_over == False and counter > 0 :
                if not figure.figure.empty():
                    figure.moveLine_down(speed)
                if pygame.sprite.groupcollide(figure.figure, walls, 0, 0) or pygame.sprite.groupcollide(figure.figure, group, 0, 0) :
                    figure.moveLine_up(speed)
                    for sprite in figure.figure:
                        group.add(sprite)
                    matrix = Matrix(348, 22, 22, 22, 2, ret_figure())
                    figure = Figure(matrix)
                    layBrick.play()

        #lines remove
        line1 = []
        collapse = False
        for sprite in group:
            if sprite.rect.x == 252:
                line1.append([sprite.rect.x, sprite.rect.y])
        for count in line1:
            remove_line = []
            for x in range(count[0], 492, 24):
                for sprite in group:
                    if sprite.rect.x == x:
                        if sprite.rect.y == count[1]:
                            remove_line.append(sprite)
            #remove_line.sort()
            if len(remove_line) >= 10:
                score += 100
                text.text = 'Score: ' + str(score)
                group.remove(remove_line)
                for sprt in group:
                    if remove_line[0].rect.y > sprt.rect.y:
                        sprt.rect.y += speed
                if score % 1000 == 0:
                    if counter > 100:
                        counter -= 50
                        pygame.time.set_timer(MoveFigure_down, counter)

                        if len(bglist) -1 == bgcount:
                            bgcount = 0
                            print bgcount, bglist
                        else:
                            bgcount += 1
                        background.image = pygame.image.load('res\\' + bglist[bgcount])

                collapse = True
            if collapse == True:
                removeLine_sound.play()


        # --- end line remove
        walls.draw(screen)
        background.draw(screen)
        horisontal_netWork.draw(screen)
        figure.figure.draw(screen)
        text.writeOn(screen, (40, 150))

        group.draw(screen)
        if pause:
            pause_text.writeOn(screen, (width / 3, height/ 3))
        # -- Game over
        for sprt in group:
            if sprt.rect.y < 40:
                GameOver.writeOn(screen, (width / 3, height/ 3))
                is_over = True
                # -- end over
        pygame.display.flip()

__main__()
