
from threading import Thread
from comms import Message
import time


class DisplayAlgo:

    SHARINGAN_3_ROTATING = [0, 1, 2, 3]
    SHARINGAN_ROUND_3_ROTATING = [8, 9, 10, 11]
    PUPIL_DILATING = [4, 5, 6, 7, 6, 5]

    STOP_FLAG = False


    @staticmethod
    def play(sequences):
        while not DisplayAlgo.STOP_FLAG:
            for s in sequences:
                for idx in s:
                    Message.send(Message.led(idx))
                    time.sleep(0.2)


led_thread = Thread(target=DisplayAlgo.play, args=([
                                                    DisplayAlgo.SHARINGAN_ROUND_3_ROTATING],))
