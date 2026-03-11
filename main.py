import numpy as np
import cv2
import pygame

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("3DS Effect Recreation")

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

kopfMittelpunkt = (0,0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 7)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
        cv2.circle(frame, (round(x+w/2),round(y+h/2)),3, (0,255,0), 5)
        kopfMittelpunkt = (round(x+w/2),round(y+h/2))
        roi_gray = gray[y:y+w, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

    print(kopfMittelpunkt)

    screen.fill((0, 0, 0))
    pygame.display.flip()


cap.release()
cv2.destroyAllWindows()
pygame.quit()
