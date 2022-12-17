
# pip install opencv-python
import cv2

# pip install imutils
import imutils

# pip install imutils
import pytesseract


# 이미지 입력을 받아 너비를 300픽셀로 조정
image = cv2.imread('imgs/test2.png')
image = imutils.resize(image, width=300 )
cv2.imshow("original image", image)
# cv2.waitKey(0)


# 입력 이미지를 그레이스케일로 변환
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("greyed image", gray_image)
# cv2.waitKey(0)

# 그레이스케일 이미지의 노이즈 줄이기
gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17) 
cv2.imshow("smoothened image", gray_image)
# cv2.waitKey(0)


# 스무딩된 이미지의 가장자리 감지
edged = cv2.Canny(gray_image, 30, 200) 
cv2.imshow("edged image", edged)
# cv2.waitKey(0)


# 가장자리 이미지에서 윤곽 찾기
cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
image1=image.copy()
cv2.drawContours(image1,cnts,-1,(0,255,0),3)
cv2.imshow("contours",image1)
# cv2.waitKey(0)


# 식별된 등고선 정렬
cnts = sorted(cnts, key = cv2.contourArea, reverse = True) [:30]
screenCnt = None
image2 = image.copy()
cv2.drawContours(image2,cnts,-1,(0,255,0),3)
cv2.imshow("Top 30 contours",image2)
# cv2.waitKey(0)


# 네 면이 있는 등고선 찾기
i=7
for c in cnts:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
        if len(approx) == 4: 
                screenCnt = approx
                # 번호판으로 식별된 직사각형 부분 자르기
                x,y,w,h = cv2.boundingRect(c) 
                new_img=image[y:y+h,x:x+w]
                cv2.imwrite('./'+str(i)+'.png',new_img)
                i+=1
                break

# 원본 이미지에 선택한 윤곽 그리기
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
cv2.imshow("image with detected license plate", image)
# cv2.waitKey(0)


# 잘린 번호판 이미지에서 텍스트 추출
Cropped_loc = '7.png'
cv2.imshow("cropped", cv2.imread(Cropped_loc))

# https://github.com/tesseract-ocr/tessdata/blob/main/kor.traineddata 다운받아서
plate = pytesseract.image_to_string(Cropped_loc, lang='kor', config='-c tessedit_char_whitelist=0123456789가나다라마바사아자거너더러머버서어저고노도로모보소오조구누두루무부수우주하허호배 --psm 7 --oem 3')
print("Number plate is:", plate)
# cv2.waitKey(0)
cv2.destroyAllWindows()