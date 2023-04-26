import cv2
import numpy as np
import PIL.ImageFont as ImageFont
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image

# 비디오 불러오기
cap = cv2.VideoCapture('/home/oh/WorkSpace/Project_ws/02. OpenCV/OneDay/datas/video2.mp4')

# 동영상 저장공간 설정
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter('newvideo.avi', fourcc, fps, (width, height))

# 한글 사용하기 위한 설정
fontpath = "fonts/NanumGothic.ttf"
font = ImageFont.truetype(fontpath, 36)
text_position = (10, 50)
font_color = (255, 255, 255)
stroke_color = (0, 0, 0)
stroke_width = 2

# 5초 뒤에 다른 자막 삽입
switch_time = 5.0  
new_subtitle_text = "수정된 단어입니다.\n\ng -> gray\n\n밝기 조절 l, (;)\n\nq 입력시 종료"  # New subtitle text after switch_time

# 밝기 설정
brightness = 0
brightness_step = 10

# 여러가지 모드 설정
sobelMode = False
saveMode = False
grayscale = False
imagecale = False

# 이미지 삽입을 위한 이미지 불러오기
img_to_insert = cv2.imread('/home/oh/WorkSpace/Project_ws/02. OpenCV/OneDay/datas/image2.jpg')


while cap.isOpened():
    ret, frame = cap.read()
    # 이미지 불러오기 실패시 오류
    if not ret:
        break

    # 프레임에서 밝기 조절하기 위함
    frame = cv2.add(frame, brightness)
    
    # grayscale로 수정
    if grayscale:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        if sobelMode:
            frameg = cv2.Sobel(frame, -1, 1, 0, delta=128)
            
    #컬러 색일 때
    if not grayscale:
        if sobelMode:
            print('Warning! 현재 칼라 이미지입니다. Gray 색에서만 Sobel Mode가 가능합니다.')
      
    
    # 이미지 두두등장
    if imagecale:
        img_height, img_width, _ = img_to_insert.shape
        y = int(frame.shape[0] - img_height - 250)
        x = int(frame.shape[1] / 2 - img_width / 2) + 100
        frame[y:y+img_height, x:x+img_width] = img_to_insert
        
    # 현재 시간을 초로 계산
    current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0  
    if current_time >= switch_time:
        subtitle_text = new_subtitle_text
    else:
        subtitle_text = "현재 자막입니다. 5초 뒤에 바뀝니다.\n\ng -> gray\n\n밝기 조절 l, (;)\n\nq 입력시 종료"
    
    # 이미지에 폰트 삽입
    img_pil = Image.fromarray(frame)
    draw = ImageDraw.Draw(img_pil)
    draw.text(text_position, subtitle_text, font=font, fill=font_color, stroke_width=stroke_width, stroke_fill=stroke_color)
    frame = np.array(img_pil)
    
    # 동영상 저장 모드이면 저장 아니면 안함
    if saveMode:
        out.write(frame)
    
    key = cv2.waitKey(1) & 0xFF
    
    # key가 l이면 밝기 올라가고, (;)일 땐 밝기가 내려감.
    if key == ord('l'):
        brightness += brightness_step
    elif key == ord(';'):
        brightness -= brightness_step
    
    # key가 g이면 Gray 색으로 변환
    elif key == ord('g'):
        grayscale = not grayscale

    # key가 w이면 Gray 색으로 변환하고 이미지 삽입
    elif key == ord('w'):
        grayscale = True
        imagecale = not imagecale

    # key가 s이면 동영상 저장
    elif key == ord('s'):
        saveMode = not saveMode
        
    # key가 e이면 소벨 모드로 변환
    elif key == ord('e'):
        sobelMode = not sobelMode

    cv2.imshow('frame', frame)
    if key == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
