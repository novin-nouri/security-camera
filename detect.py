import cv2 as cv
import time
import numpy as np
import datetime
from qr_code import QrCode
from sms import Sms


class BaseDetect:
    def __init__(self):
        self.classes_names = []
        self.previous_time = 0
        self.authorised = False
        self.first_time = 0
        self.first_detect_time = 0
        self.color = (255, 0, 255)
        self.conf_threshold = 0.5
        self.nms_threshold = 0.3


class Detect(BaseDetect):
    """Class to show frames and detect theft"""

    def __init__(self,
                 main_target,
                 target_object,
                 camera,
                 sms_information,
                 cuda="CPU"):
        self.main_target = main_target
        self.target_object = target_object
        self.camera = camera
        self.sms_information = sms_information
        self.cuda = cuda
        self.capture = cv.VideoCapture(self.camera)
        super().__init__()
        """Initializes a Detect

          Args:
              main_target: It is an object that when it comes close to our 
                  desired device, it considers it as a thief.(like "person")  
              target_object: It is the object that we want to protect . 
                  (like "dog", "car", ...)
              camera: The camera we want to use it.
              sms_information: Include Phone number and api of user
              cuda: For run with (CPU/GPU)
          """

    def __repr__(self):
        return f"{self.__class__.__name__!r}({self.__dict__!r})"

    def processing(self):
        """Ask network to use specific computation backend where it supported.

        Return:
            net, processing with (CPU) or cuda(GPU)
        """
        net = self._read_yolov3_files()
        # Use GPU(hight fps)
        if self.cuda == "GPU":
            net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
            net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)
        # use CPU(low fps)
        else:
            net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
            net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)
        return net
