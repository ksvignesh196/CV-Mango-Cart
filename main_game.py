import pygame as pg
import math

pg.init()

clock = pg.time.Clock()

window = pg.display.set_mode((800, 600))
pg.display.set_caption("falling mango!")

ground = pg.image.load("gnd.png")

icon = pg.image.load('icon.png')
pg.display.set_icon(icon)

cart = pg.image.load("cart.png")
cartX = 380
cartY = 520
movementX = 0
last_dirC = 'right'

plane = pg.image.load('plane.png')
planeX = 0
planeY = 5
pMovementX = 3.5
last_dirP = 'right'

mango = pg.image.load('mango.png')
mangoX = 0
mangoY = 0
status = 'falling'

mangoX2 = 0
mangoY2 = 0
status2 = 'falling'

score = 0
life = 3

pg.mixer.music.load('main.mp3')
pg.mixer.music.play(-1)


def collision():
    distance = math.sqrt(math.pow((cartX - mangoX), 2) + math.pow((cartY - mangoY), 2))
    if distance < 45:
        return True
    else:
        return False


def collision2():
    distance = math.sqrt(math.pow((cartX - mangoX2), 2) + math.pow((cartY - mangoY2), 2))
    if distance < 45:
        return True
    else:
        return False


paused_font = pg.font.Font("freesansbold.ttf", 70)
guide_font = pg.font.Font("freesansbold.ttf", 55)
score_font = pg.font.Font("freesansbold.ttf", 30)


def pause():
    paused = True
    while paused:
        window.blit(ground, (0, 0))
        paused_message = paused_font.render("GAME PAUSED!", True, 'orange')
        guide_message = guide_font.render("C to continue", True, 'orange')
        guide_message2 = guide_font.render("Q to quit", True, 'orange')
        window.blit(paused_message, (130, 110))
        window.blit(guide_message, (230, 250))
        window.blit(guide_message2, (230, 340))
        pg.display.update()

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                quit()

            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_c:
                    paused = False
                if ev.key == pg.K_q:
                    quit()


running = True
while running:
    window.blit(ground, (0, 0))
    display_score = score_font.render(f"Score: {score}", True, 'white', 'black')
    display_life = score_font.render(f"life: {life}", True, 'white', 'black')

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                movementX -= 5
                last_dirC = 'left'
            elif event.key == pg.K_d or event.key == pg.K_RIGHT:
                movementX += 5
                last_dirC = 'right'

            elif event.key == pg.K_ESCAPE:
                pause()

        if event.type == pg.KEYUP:
            if event.key == pg.K_a or event.key == pg.K_d or event.key == pg.K_RIGHT or event.key == pg.K_LEFT:
                movementX = 0

    cartX += movementX
    if cartX <= 0:
        cartX = 0
    elif cartX >= 736:
        cartX = 736

    if last_dirC == 'right':
        rotated = pg.transform.rotate(cart, 0)
        window.blit(rotated, (cartX, cartY))

    elif last_dirC == 'left':
        rotated = pg.transform.flip(cart, True, False)
        window.blit(rotated, (cartX, cartY))

    planeX += pMovementX
    if planeX <= 0:
        pMovementX = 3.5
        last_dirP = 'right'

    if planeX >= 736:
        pMovementX = -3.5
        last_dirP = 'left'

    if last_dirP == 'right':
        rotatedP = pg.transform.rotate(plane, 0)
        window.blit(rotatedP, (planeX, planeY))

    if last_dirP == 'left':
        rotatedP = pg.transform.flip(plane, True, False)
        window.blit(rotatedP, (planeX, planeY))

    if status is 'falling':
        mangoX = planeX
        mangoY += 4
        window.blit(mango, (mangoX, mangoY))

    if mangoY >= 530:
        mangoY = 0
        status = 'falling'
        life -= 1
        sound = pg.mixer.Sound('lost.mp3')
        sound.play()
        if life == 0:
            break

    if status2 is 'falling':
        mangoX2 = planeX
        mangoY2 += 3
        window.blit(mango, (mangoX2, mangoY2))

    if mangoY2 >= 530:
        mangoY2 = 0
        status2 = 'falling'
        life -= 1
        sound = pg.mixer.Sound('lost.mp3')
        sound.play()
        if life == 0:
            break

    coll = collision()
    if coll:
        mangoY = planeY
        mangoX = planeX
        status = 'not falling'
        score += 1
        sound = pg.mixer.Sound('ding.mp3')
        sound.play()

    if status is 'not falling':
        mangoY += 3
        window.blit(mango, (mangoX, mangoY))

    coll2 = collision2()
    if coll2:
        mangoY2 = planeY
        mangoX2 = planeX
        status2 = 'not falling'
        score += 1
        sound = pg.mixer.Sound('ding.mp3')
        sound.play()

    if status2 is 'not falling':
        mangoY2 += 3
        window.blit(mango, (mangoX2, mangoY2))

    window.blit(display_score, (0, 570))
    window.blit(display_life, (719, 570))
    clock.tick(60)
    pg.display.update()
