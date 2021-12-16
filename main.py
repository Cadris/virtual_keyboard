import cv2
from cvzone.HandTrackingModule import HandDetector

# constant values
camera_window_length = 640  
camera_window_width = 480
video_cam_device = 0
key_text_thickness = 3
key_text_scale = 3
index_finger = 8
middle_finger = 12
thumb = 4
buttonList = []
keys = [["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L"],
        ["Z","X","C","V","B","N","M"]]

# settings for the camera
cap = cv2.VideoCapture(video_cam_device)
cap.set(3, camera_window_length)    # 3 -> For Length
cap.set(4, camera_window_width)     # 4 -> For Width
detector = HandDetector(detectionCon=0.8)   # set detector for the hand

# this handles the drawing of all the buttons
def drawAllButtons(img, buttonList):
    for i in range(len(buttonList)):
        for button in buttonList:
            x,y = button.pos
            w,h = button.size
            cv2.rectangle(img, button.pos, (x+w, y+h), (255, 0, 255), cv2.FILLED)
            cv2.putText(img, button.text, (x+5, y+40), cv2.FONT_HERSHEY_PLAIN, key_text_scale, (255, 255, 255), key_text_thickness)
        return img

# class to handle buttons
class Button():
    def __init__(self, pos, text, size=[50, 50]):
        self.pos = pos
        self.text = text
        self.size = size
    

# The Buttons create once :: Now Every time (Not recomended : Testing only)
for i in range(len(keys)):
    for x, key in enumerate(keys[i]):
        buttonList.append(Button([40+(x*60), 40+(i*60)], key))

# main function
while True:
    # capture vedio
    success, img = cap.read()
    img = cv2.flip(img,1)   # Flip camera to stop mirror effect (1 -> x-axis)

    hands, img = detector.findHands(img)   # find the hand in the supplied img=image(Vedio by cv2)

    # draw the buttons
    img = drawAllButtons(img, buttonList)

    # hands are detected
    if hands:
        # min number of hand = 1 hand : Now Handle only one hand
        hand1 = hands[0]
        hand1Type = hand1["type"]       # left, right = handType
        hand1lmList = hand1["lmList"]   # lmList = landmark list of the hand
        hand1bbox = hand1["bbox"]       # bbox = boundarybox info
        
        # this handles the hover of index finger = landmark[8]
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < hand1lmList[index_finger][0] < x+w and y < hand1lmList[index_finger][1] < y+h:
                cv2.rectangle(img, button.pos, (x+w, y+h), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x+5, y+40), cv2.FONT_HERSHEY_PLAIN, key_text_scale, (255, 255, 255), key_text_thickness)
                l, _  = detector.findDistance(hand1lmList[index_finger], hand1lmList[middle_finger])
                if l<30:
                    cv2.rectangle(img, button.pos, (x+w, y+h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x+5, y+40), cv2.FONT_HERSHEY_PLAIN, key_text_scale, (255, 255, 255), key_text_thickness)

    # show the vedio capture on screen
    cv2.imshow("Image", img)

    # delay
    cv2.waitKey(1)