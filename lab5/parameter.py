import cv2

cap = cv2.VideoCapture(0)

for i in range(3):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera {i} works!")
        cap.release()

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    cv2.imshow("HSV - H", h)
    cv2.imshow("HSV - S", s)
    cv2.imshow("HSV - V", v)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cap.release()
    cv2.destroyAllWindows()
