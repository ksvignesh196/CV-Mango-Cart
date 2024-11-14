import cv2
import numpy as np

cam = cv2.VideoCapture(0)


def nothing(yee):
    pass


cv2.namedWindow("Colour picker")
cv2.createTrackbar("A", "Colour picker", 0, 180, nothing)
cv2.createTrackbar("B", "Colour picker", 0, 255, nothing)
cv2.createTrackbar("C", "Colour picker", 120, 255, nothing)
cv2.createTrackbar("D", "Colour picker", 14, 180, nothing)
cv2.createTrackbar("E", "Colour picker", 255, 255, nothing)
cv2.createTrackbar("F", "Colour picker", 172, 255, nothing)

while True:
    _, frame = cam.read()

    a = cv2.getTrackbarPos("A", "Colour picker")
    b = cv2.getTrackbarPos("B", "Colour picker")
    c = cv2.getTrackbarPos("C", "Colour picker")
    d = cv2.getTrackbarPos("D", "Colour picker")
    e = cv2.getTrackbarPos("E", "Colour picker")
    f = cv2.getTrackbarPos("F", "Colour picker")

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([a, b, c])
    upper_red = np.array([d, e, f])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)

        x = approx.ravel()[0]
        y = approx.ravel()[1]
        if area > 400:
            cv2.drawContours(frame, [cnt], 0, (0, 0, 0), 3)
            if len(approx) == 4:
                move = 'left'
                cv2.putText(frame, "Rectangle", (x, y), cv2.FONT_HERSHEY_PLAIN, 1, 0)
            elif len(approx) == 3:
                move = 'right'
                cv2.putText(frame, "Triangle", (x, y), cv2.FONT_HERSHEY_PLAIN, 1, 0)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
