import cv2
from cvzone.HandTrackingModule import HandDetector

camera_window_length = 640  
camera_window_width = 480
video_cam_device = 0
key_text_thickness = 3
key_text_scale = 3
buttonList = []
keys = [["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L"],
        ["Z","X","C","V","B","N","M"]]

cap = cv2.VideoCapture(video_cam_device)
cap.set(3, camera_window_length)    # 3 -> For Length
cap.set(4, camera_window_width)     # 4 -> For Width
detector = HandDetector(detectionCon=0.8)   # set detector for the hand


# class to handle buttons
class Button():
    def __init__(self, pos, text, size=[50, 50]):
        self.pos = pos
        self.text = text
        self.size = size
    
        x,y = self.pos
        w,h = self.size
        cv2.rectangle(img, self.pos, (x+w, y+h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, self.text, (self.pos[0]+5, self.pos[1]+40), cv2.FONT_HERSHEY_PLAIN, key_text_scale, (255, 255, 255), key_text_thickness)
        # return img


# main function
while True:
    # capture vedio
    success, img = cap.read()
    img = cv2.flip(img,1)   # Flip camera to stop mirror effect (1 -> x-axis)

    hands, img = detector.findHands(img)   # find the hand in the supplied img=image(Vedio by cv2)

    # The Buttons create once :: Now Every time (Not recomended : Testing only)
    for i in range(len(keys)):
        for x, key in enumerate(keys[i]):
            buttonList.append(Button([40+(x*60), 40+(i*60)], key))

    # hands are detected
    if hands:
        # min number of hand = 1 hand
        hand1 = hands[0]
        hand1Type = hand1["type"]       # left, right = handType
        hand1lmList = hand1["lmList"]   # lmList = landmark list of the hand
        hand1bbox = hand1["bbox"]       # bbox = boundarybox info



    # show the vedio capture on screen
    cv2.imshow("Image", img)

    # delay
    cv2.waitKey(1)