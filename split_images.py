import cv2

image = cv2.imread("textures/spritesheet.png")
tmp = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
b, g, r = cv2.split(image)
rgba = [b,g,r, alpha]
img_h, img_w = image.shape[:2]
bl_w, bl_h = 32, 32
c = 0
for i in range(int(img_h/bl_h)):
  for j in range(int(img_w/bl_w)):
    cropped = image[i*bl_h:(i+1)* bl_h, j*bl_w:(j+1)*bl_w]
    c += 1
    cv2.imwrite(f"Fishes/fish_{c}.png", cropped)