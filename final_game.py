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
cart_flipped = pg.transform.flip(cart, True, False)  # Flipped cart image for left direction
cartX = 380
cartY = 520
last_cart_dir = 'right'  # Track the last direction of the cart

plane = pg.image.load('plane.png')
planeX = 0
planeY = 5
pMovementX = 3.5
last_dirP = 'right'

mango = pg.image.load('mango.png')
mangoX = 0
mangoY = 0
status = 'falling'
mango_speed = 2  # Initial speed of the first mango

mangoX2 = 0
mangoY2 = 0
status2 = 'falling'
mango_speed2 = 3  # Initial speed of the second mango

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

# Game state variables
game_over = False
running = True

def collision():
    distance = math.sqrt(math.pow((cartX - mangoX), 2) + math.pow((cartY - mangoY), 2))
    return distance < 45

def collision2():
    distance = math.sqrt(math.pow((cartX - mangoX2), 2) + math.pow((cartY - mangoY2), 2))
    return distance < 45

# Updated fonts and colors
paused_font = pg.font.Font("freesansbold.ttf", 70)
guide_font = pg.font.Font("freesansbold.ttf", 55)
score_font = pg.font.Font("freesansbold.ttf", 35)
game_over_font = pg.font.Font("freesansbold.ttf", 100)
score_color = (255, 223, 0)  # Bright yellow color for score
life_color = (255, 69, 0)     # Red-orange color for life

movement_threshold = 10  # Minimum movement to consider a direction change

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

def display_game_over():
    window.blit(ground, (0, 0))

    # Render text surfaces
    game_over_message = game_over_font.render("GAME OVER", True, 'red')
    final_score_message = guide_font.render(f"Score: {score}", True, 'white')
    retry_message = guide_font.render("Press R to Restart", True, 'orange')

    # Centering the texts based on their widths
    game_over_x = (800 - game_over_message.get_width()) // 2
    final_score_x = (800 - final_score_message.get_width()) // 2
    retry_x = (800 - retry_message.get_width()) // 2

    # Display centered messages
    window.blit(game_over_message, (game_over_x, 150))
    window.blit(final_score_message, (final_score_x, 300))
    window.blit(retry_message, (retry_x, 400))
    pg.display.update()


while running:
    if game_over:
        display_game_over()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    # Reset game variables
                    score = 0
                    life = 3
                    mangoY = 0
                    mangoY2 = 0
                    mango_speed = 2
                    mango_speed2 = 3
                    cartX = 380
                    last_cart_dir = 'right'
                    game_over = False
        continue

    window.blit(ground, (0, 0))

    # Display score and life with updated colors and outline effect
    display_score = score_font.render(f"Score: {score}", True, score_color)
    display_life = score_font.render(f"Life: {life}", True, life_color)
    window.blit(display_score, (10, 570))
    window.blit(display_life, (665, 570))

    success, frame = cam.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            new_cartX = int((index_finger_tip.x) * 800)

            if new_cartX < cartX - movement_threshold:
                last_cart_dir = 'left'
            elif new_cartX > cartX + movement_threshold:
                last_cart_dir = 'right'
            cartX = new_cartX

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

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

    # Blit the cart based on the direction
    if last_cart_dir == 'right':
        window.blit(cart, (cartX, cartY))
    else:
        window.blit(cart_flipped, (cartX, cartY))

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

    # First mango falling with progressively faster speed
    if status == 'falling':
        mangoX = planeX
        mangoY += mango_speed
        window.blit(mango, (mangoX, mangoY))

    if mangoY >= 530:
        mangoY = 0
        status = 'falling'
        life -= 1
        mango_speed += 0.5
        sound = pg.mixer.Sound('lost.mp3')
        sound.play()
        if life == 0:
            game_over = True

    if collision():
        mangoY = 0
        mangoX = planeX
        status = 'falling'
        score += 1
        mango_speed += 0.5
        sound = pg.mixer.Sound('ding.mp3')
        sound.play()

    # Second mango falling with progressively faster speed
    if status2 == 'falling':
        mangoX2 = planeX
        mangoY2 += mango_speed2
        window.blit(mango, (mangoX2, mangoY2))

    if mangoY2 >= 530:
        mangoY2 = 0
        status2 = 'falling'
        life -= 1
        mango_speed2 += 0.5
        sound = pg.mixer.Sound('lost.mp3')
        sound.play()
        if life == 0:
            game_over = True

    if collision2():
        mangoY2 = 0 
        mangoX2 = planeX
        status2 = 'falling'
        score += 1
        mango_speed2 += 0.5
        sound = pg.mixer.Sound('ding.mp3')
        sound.play()

    clock.tick(60)
    pg.display.update()

cam.release()
cv2.destroyAllWindows()
