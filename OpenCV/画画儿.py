import numpy as np
import cv2
import math
oldx = oldy = -1

drawing = False
mode = True

img = np.ones((480, 640, 3), dtype=np.uint8) * 255

# 실행 함수
def useMouse():
    global mode, img
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', mouse_mode, img)

    while True:
        cv2.imshow('image', img)
        key = cv2.waitKey(0) & 0xFF
        # esc 누르면 종료
        if key == 27:
            break
        # a 키 누르면 모드 바뀜
        if key == ord('a'):
            mode = not mode

    cv2.destroyAllWindows()

# 사각형인지 원형 바꾸기 함수
def mouse_mode(event, x, y, flags, param):
    global oldx, oldy, drawing, mode, img

    # 클릭한 순간 그리기 모드로 전환, 클릭한 x, y 좌표 저장
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        oldx, oldy = x, y  
    # 마우스가 움직일 때
    elif event == cv2.EVENT_MOUSEMOVE:
        # 그리기 모드일 때
        if drawing:
            # 사각형
            if mode:
                cv2.rectangle(img, (oldx, oldy), (x, y), (0,0,0), -1)
                cv2.imshow('image', img)  
            # 원형
            else:
                r = ((oldx- x)**2 + (oldy - y)**2)
                r = int(math.sqrt(r))
                cv2.circle(img, (oldx, oldy), r, (0,0,0), -1)
                cv2.imshow('image', img)
    # 마우스 땔 때 그리기 모드 종료        
    elif event == cv2.EVENT_LBUTTONUP:
        if drawing:
            drawing = False
           

useMouse()