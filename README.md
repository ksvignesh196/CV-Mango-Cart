# Introduction
Computer Vision Mango Cart is the project for Introduction to Engineering we made. It is a simple game where the player uses their hand to control the movement of a cart which is used to catch mangoes dropped from a moving plane at increasing speeds.

# Usage
Clone the repo or download all the files manually.
Then install all the necessary python modules
```
pip install requirements.txt
```
Run 	`final_game.py`

# Technical Details
## Modules used:
- Pygame
- Math
- OpenCV
- Mediapipe

### **Pygame (`pg`)**:

Pygame is the main game framework here, handling almost all aspects of the game's operation. This code uses Pygame to set up the game window (`pg.display.set_mode`), control the game’s frame rate (`pg.time.Clock`), load and display images for elements like the ground, cart, plane, and mangoes (`pg.image.load`), and manage events such as keypresses and window closing. Pygame’s `mixer` module is also used to load and continuously play background music (`pg.mixer.music.load`) and to trigger sound effects when the player catches or misses a mango. The `pg.font.Font` feature customizes the font and size of text displayed in the game, including score, life, and game over messages.

### **Math (`math`)**:
The math module provides basic mathematical operations used for collision detection. The `collision()` and `collision2()` functions use `math.sqrt` and `math.pow` to calculate the distance between the cart and each mango. If this distance is less than a specific threshold (45 pixels), the program registers a successful "catch." This simple yet effective approach allows the game to check whether the mangoes are close enough to the cart to be caught, adding to the game’s interactive nature.

### **OpenCV (`cv2`)**:

OpenCV is used here to capture real-time video from the player’s webcam, enabling a unique, hands-on gameplay experience. The code initiates the camera (`cv2.VideoCapture(0)`), flips the frame horizontally (`cv2.flip`) for a mirror effect, and converts the frame to RGB (`cv2.cvtColor`) before processing it with Mediapipe. By using OpenCV to read the player's hand movements, this code lets the player control the cart’s position by moving their hand in front of the webcam, creating a direct and immersive control mechanism.

### **Mediapipe (`mp`)**:

Mediapipe's hand tracking feature is utilized to detect and follow the player's hand in real-time. The `Hands` solution tracks landmarks on the hand, specifically the index finger tip in this case, to control the cart. The code processes the hand landmarks in each frame to get the X-coordinate of the index finger tip, which is mapped to the cart’s position on the game screen. This enables intuitive hand-based control, where moving the hand left or right moves the cart accordingly. Mediapipe’s `drawing_utils` is also used to visually overlay the hand landmarks on the webcam feed for better user feedback.
