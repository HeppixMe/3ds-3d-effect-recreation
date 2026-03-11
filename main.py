import numpy as np
import cv2
import pygame

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("3DS Effect Recreation")

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

kopfMittelpunkt = (0,0)

def map_range(x, a, b, c, d):
    # Normiere zunächst auf 0…1
    t = (x - a) / (b - a)
    # Skaliere in den Zielbereich
    return c + t * (d - c)


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

    if ret:
        frame_h, frame_w = frame.shape[:2]
        window_w, window_h = screen.get_size()

    paralax_kopf = 4
    paralax_paralax = 3
    kopfX = map_range(kopfMittelpunkt[0],0,frame_w,window_w/paralax_kopf,window_w-window_w/paralax_kopf)
    kopfY = window_h-map_range(kopfMittelpunkt[1],0,frame_h,window_h/paralax_kopf,window_h-window_h/paralax_kopf)
    paralaxX = map_range(kopfX, 0,window_w,window_w/paralax_paralax,window_w-window_w/paralax_paralax)
    paralaxY = map_range(kopfY, 0,window_h,window_h/paralax_paralax,window_h-window_h/paralax_paralax)

    screen.fill((0, 0, 0))
    # pygame.draw.circle(screen,(255,0,0),(paralaxX,paralaxY),3,3)
    # pygame.draw.line(screen,(200,200,200),(window_w/2,window_h/2),(kopfX,kopfY),10)
    # pygame.draw.line(screen,(200,200,200),(window_w/2,window_h/2),(kopfX-10,kopfY),5)
    # pygame.draw.line(screen,(200,200,200),(window_w/2,window_h/2),(kopfX+10,kopfY),5)
    # pygame.draw.line(screen,(200,200,200),(window_w/2,window_h/2),(kopfX,kopfY-10),5)
    # pygame.draw.line(screen,(200,200,200),(window_w/2,window_h/2),(kopfX,kopfY+10),5)
    # pygame.draw.circle(screen,(255,255,255),(kopfX,kopfY),11,11)
    paralax_w = 90
    pygame.draw.rect(screen,(200,0,0),(paralaxX-paralax_w,paralaxY-paralax_w,paralax_w*2,paralax_w*2), 5)
    pygame.draw.line(screen,(230,0,0),(kopfX-100,kopfY-100),(paralaxX-paralax_w,paralaxY-paralax_w),5)
    pygame.draw.line(screen,(230,0,0),(kopfX+100,kopfY-100),(paralaxX+paralax_w,paralaxY-paralax_w),5)
    pygame.draw.line(screen,(230,0,0),(kopfX-100,kopfY+100),(paralaxX-paralax_w,paralaxY+paralax_w),5)
    pygame.draw.line(screen,(230,0,0),(kopfX+100,kopfY+100),(paralaxX+paralax_w,paralaxY+paralax_w),5)
    pygame.draw.rect(screen,(255,0,0),(kopfX-100,kopfY-100,200,200), 5)


    pygame.display.flip()


cap.release()
cv2.destroyAllWindows()
pygame.quit()
