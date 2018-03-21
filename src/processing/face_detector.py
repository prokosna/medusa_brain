from logging import getLogger

import cv2
import numpy as np

logger = getLogger(__name__)

CLASSIFIER_PATH = './res/opencv/haarcascade_frontalface_alt.xml'


class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(CLASSIFIER_PATH)
        pass

    def detect(self, img):
        arr = np.fromstring(img, np.uint8)
        frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        thumbnails = []
        for (x, y, w, h) in faces:
            # detected = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # cv2.imwrite('detected_%s.jpg' % self.debug, detected)
            logger.debug('Face detected.')
            # cv2.imwrite('detected.jpg', frame[y:y + h, x:x + w])
            thumbnail = cv2.imencode('.jpg', frame[y:y + h, x:x + w])[1].tostring()
            thumbnails.append(thumbnail)
        return thumbnails
