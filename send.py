import cv2
from cvzone.PoseModule import PoseDetector
from twilio.rest import Client
import tkinter as tk
import threading
import os

account_sid = ''
auth_token = ''

def send_sms():
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='',
        body='Alert: Unknown human detected',
        to=''
    )
    print("SMS sent successfully!")
    print(message.sid) 

def start_surveillance():
    global surveillance_button, label
    label.config(text="Initiated...... (Wait for 4-5 sceonds)")
    threading.Thread(target=surveillance_system).start()
    surveillance_button.destroy()

def surveillance_system():
    detector = PoseDetector()
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    l = []
    flag = True
    while True:
        success, img = cap.read()
        display_img = img.copy() 
        display_img = detector.findPose(display_img)
        imlist, bbox = detector.findPosition(img)
        
        if len(imlist) > 0:
            if flag:
                flag = False
                send_sms()
                print("Human Detected - SMS sent")
                folder_path = "C://Users//amanm//Desktop//Surv_SYS//Caught u"
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                cv2.imwrite(os.path.join(folder_path, "detected_human.jpg"), img)
            l.append(1)
        cv2.imshow("Surveillance Screen", display_img)
        
        q = cv2.waitKey(1)
        if q == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    main_window.after(0, lambda: label.config(text="Surveillance ended"))


main_window = tk.Tk()
main_window.title("Surveillance Control")
main_window.geometry("300x100") 
label = tk.Label(main_window, text="Click the button to start the surveillance")
label.pack(pady=10)
surveillance_button = tk.Button(main_window, text="Start Surveillance", command=start_surveillance)
surveillance_button.pack(pady=5)
main_window.mainloop()
