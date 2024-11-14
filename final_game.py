import pygame as pg
import math
import cv2
import numpy as np

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
move = 'right'

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
life = 1000

pg.mixer.music.load('main.mp3')
pg.mixer.music.play(-1)

cam = cv2.VideoCapture(0)
cam.set(3, 320)
cam.set(4, 240)


def nothing(yee):
    pass


# cv2.namedWindow("Colour picker")
# cv2.createTrackbar("A", "Colour picker", 0, 180, nothing)
# cv2.createTrackbar("B", "Colour picker", 67, 255, nothing)
# cv2.createTrackbar("C", "Colour picker", 125, 255, nothing)
# cv2.createTrackbar("D", "Colour picker", 22, 180, nothing)
# cv2.createTrackbar("E", "Colour picker", 255, 255, nothing)
# cv2.createTrackbar("F", "Colour picker", 255, 255, nothing)


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
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                quit()

            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_c:
                    paused = False
                if ev.key == pg.K_q:
                    quit()

        window.blit(ground, (0, 0))
        paused_message = paused_font.render("GAME PAUSED!", True, 'orange')
        guide_message = guide_font.render("C to continue", True, 'orange')
        guide_message2 = guide_font.render("Q to quit", True, 'orange')
        window.blit(paused_message, (130, 110))
        window.blit(guide_message, (230, 250))
        window.blit(guide_message2, (230, 340))
        pg.display.update()


running = True
while running:
    window.blit(ground, (0, 0))
    display_score = score_font.render(f"Score: {score}", True, 'white', 'black')
    display_life = score_font.render(f"life: {life}", True, 'white', 'black')

    _, frame = cam.read()

    # a = cv2.getTrackbarPos("A", "Colour picker")
    # b = cv2.getTrackbarPos("B", "Colour picker")
    # c = cv2.getTrackbarPos("C", "Colour picker")
    # d = cv2.getTrackbarPos("D", "Colour picker")
    # e = cv2.getTrackbarPos("E", "Colour picker")
    # f = cv2.getTrackbarPos("F", "Colour picker")

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([47, 19, 107])
    upper_red = np.array([89, 255, 170])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((6, 6), np.uint8)
    mask = cv2.erode(mask, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        if area > 500:
            cv2.drawContours(frame, [cnt], 0, (0, 0, 0), 3)
            if len(approx) == 4:
                move = 'left'
                cv2.putText(frame, "Rectangle", (x, y), cv2.FONT_HERSHEY_PLAIN, 1, 0)
            elif len(approx) == 3:
                move = 'right'
                cv2.putText(frame, "Triangle", (x, y), cv2.FONT_HERSHEY_PLAIN, 1, 0)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) == ord('q'):
        break

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pause()

    if move == 'right':
        movementX += 0.2
        last_dirC = 'right'
    elif move == 'left':
        movementX -= 0.2
        last_dirC = 'left'

    cartX += movementX
    if cartX <= 0:
        cartX = 0

    elif cartX >= 736:
        cartX = 736

    if move == 'right':
        rotated = pg.transform.rotate(cart, 0)
        window.blit(rotated, (cartX, cartY))

    elif move == 'left':
        rotated = pg.transform.flip(cart, True, False)
        window.blit(rotated, (cartX, cartY))

    planeX += pMovementX
    if planeX <= 0:
        pMovementX = 3
        last_dirP = 'right'

    elif planeX >= 736:
        pMovementX = -3
        last_dirP = 'left'

    if last_dirP == 'right':
        rotatedP = pg.transform.rotate(plane, 0)
        window.blit(rotatedP, (planeX, planeY))

    elif last_dirP == 'left':
        rotatedP = pg.transform.flip(plane, True, False)
        window.blit(rotatedP, (planeX, planeY))

    if status is 'falling':
        mangoX = planeX
        mangoY += 2
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
        mangoY += 2
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
        mangoY2 += 2
        window.blit(mango, (mangoX2, mangoY2))

    window.blit(display_score, (0, 570))
    window.blit(display_life, (665, 570))
    clock.tick(60)
    pg.display.update()

cam.release()
cv2.destroyAllWindows()
