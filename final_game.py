import pygame as pg
import math
import cv2
import mediapipe as mp

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

cam = cv2.VideoCapture(0)
cam.set(3, 320)
cam.set(4, 240)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

def collision():
    distance = math.sqrt(math.pow((cartX - mangoX), 2) + math.pow((cartY - mangoY), 2))
    return distance < 45

def collision2():
    distance = math.sqrt(math.pow((cartX - mangoX2), 2) + math.pow((cartY - mangoY2), 2))
    return distance < 45

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

    success, frame = cam.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            cartX = int((index_finger_tip.x) * 800)

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) == ord('q'):
        break

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pause()

    if cartX <= 0:
        cartX = 0
    elif cartX >= 736:
        cartX = 736

    window.blit(cart, (cartX, cartY))

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
    else:
        rotatedP = pg.transform.flip(plane, True, False)
        window.blit(rotatedP, (planeX, planeY))

    if status == 'falling':
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

    if collision():
        mangoY = 0
        mangoX = planeX
        status = 'falling'
        score += 1
        sound = pg.mixer.Sound('ding.mp3')
        sound.play()

    if status2 == 'falling':
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

    if collision2():
        mangoY2 = 0 
        mangoX2 = planeX
        status2 = 'falling'
        score += 1
        sound = pg.mixer.Sound('ding.mp3')
        sound.play()


    if status2 == 'not falling':
        mangoY2 += 2
        window.blit(mango, (mangoX2, mangoY2))

    window.blit(display_score, (0, 570))
    window.blit(display_life, (665, 570))
    clock.tick(60)
    pg.display.update()

cam.release()
cv2.destroyAllWindows()