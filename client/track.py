import cv2
from comms import Message

class TrackData:
    @classmethod
    def from_handLms(cls, handLms, img) -> None:
        self = cls()
        self.c_x = self.c_y = 0  # hand center 
        self.palm_height = 0
        
        avg_x = avg_y = avg_f_x = avg_f_y = count = 0
        for idx, lm in enumerate(handLms.landmark):
            h, w, _ = img.shape
            x, y = int(lm.x *w), int(lm.y*h)
            avg_x += x
            avg_y += y
            count += 1

            if idx == 0: # center 
                self.c_x, self.c_y = x, y
            if idx == 5:
                self.palm_height = self.c_y - y
            if idx > 4 and idx % 4 == 0:  # tip of 4 fingers
                avg_f_x += x
                avg_f_y += y
            
            cv2.circle(img, (x,y), 3, (255,0,255), cv2.FILLED)
                

        self.avg_x = avg_x // count
        self.avg_y = avg_y // count
        self.avg_f_x = avg_f_x // 4
        self.avg_f_y = avg_f_y // 4

        return self

class TrackingAlgo:
    @staticmethod
    def hand_finger_control(td0: TrackData, td: TrackData):
        if td.palm_height > 0 :
            dist_x = (td0.c_x - td.c_x) / td.palm_height # -3 - +3 
            scaled_dist_x = round(((dist_x + 3) / (3 + 3)) * 180)
            print(f"Sides {dist_x} {scaled_dist_x}")
            Message.send(Message.pnt(Message.PAN, 0, scaled_dist_x)) 
            Message.send(Message.pnt(Message.PAN, 1, scaled_dist_x))
        
            dist_y = (td.c_y - td.avg_f_y) / td.palm_height

            # TODO add part of this to the degrees 
            scaled_dist_x = round(((dist_x + 3) / (3 + 3)) * 180)
            print(f"dist_y {dist_y}")

            inverse_dist_y = 1 / dist_y # 0.5 - 1.5
            scaled_dist_y = round(((inverse_dist_y - 0.5) / (1.5 - 0.5)) * 180)

            if 0 < scaled_dist_y < 180:
                print(f"Fingers {scaled_dist_y} {td.avg_f_y - td0.avg_f_y}")
                Message.send(Message.pnt(Message.TILT, 0, scaled_dist_y))
                Message.send(Message.pnt(Message.TILT, 1, scaled_dist_y))