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

    def _read_yolov3_files(self):
        """Read (coco.names), (yolov3.cfg) and (yolov3_4.weights)

        Return:
            Network object that ready to do forward, throw an exception in
            failure cases.
        """
        # Read 80 class names (like dog, car, ...)
        class_files = r"files\yolov3_files\coco.names"
        with open(class_files, "r") as f:
            self.classes_names = f.read().rstrip("\n").split("\n")
        # yolo cfg-weights files
        model_configration = r"files\yolov3_files\yolov3.cfg"
        model_weights = r"files\yolov3_files\yolov3_4.weights"
        # reads a network model stored in Darknet model files
        net = self._network_model(model_configration, model_weights)
        return net

    @staticmethod
    def _network_model(cfg, weights):
        """Reads a network model stored in Darknet model files.

        Return:
            Network object that ready to do forward, throw an exception in
            failure cases.
        """
        net = cv.dnn.readNetFromDarknet(cfg, weights)
        return net

    def make_480p(self):
        """If we use video, this function will execute.
        change the resolution of video to 480p
        """
        self.capture.set(3, 640)
        self.capture.set(4, 480)

    def show_frame(self, net):
        """Show each frame of video, detect theft, show fps and
        show authorised

        Arg:
            net: processing with CPU or cuda(GPU)

        Return:
            Frame of video
        """
        _, frame = self.capture.read()
        # frame = cv.flip(frame, 1)
        start_object_detect = self._start_detect_object(frame)
        if start_object_detect:
            # Find object in frame
            outputs = self._find_outputs(frame, net, mean=[0, 0, 0])
            theft_detection = self._find_object(frame,
                                                outputs,
                                                self.conf_threshold,
                                                self.nms_threshold)
            # find theft
            if theft_detection:
                self._send_notification(frame)
        self._description_bar(frame)
        return frame

    def _start_detect_object(self, frame):
        """Check for authorised with qr code

        Return:
            True, if authorised == True
            False, if authorised == False
        """
        qr_code = QrCode(name="novin")
        if not self.authorised:
            detect_qrcode_in_frame = qr_code.detect_qrcode(frame)
            if detect_qrcode_in_frame:
                if self.first_detect_time == 0:
                    self.autorised = True
                    self.first_detect_time = time.time()
                    return True
                elif self.first_detect_time != 0:
                    current_time = time.time()
                    diff_time = current_time - self.first_detect_time
                    if diff_time >= 3:
                        self.authorised = True
                        self.first_detect_time = time.time()
                        return True
            elif not detect_qrcode_in_frame:
                return False

        elif self.authorised:
            detect_qrcode_in_frame = qr_code.detect_qrcode(frame)
            if detect_qrcode_in_frame:
                current_time = time.time()
                diff_time = int(current_time - self.first_detect_time)
                if diff_time >= 3:
                    self.authorised = False
                    self.first_detect_time = time.time()
                    return False
            else:
                return True

    @staticmethod
    def _find_outputs(frame,
                      net,
                      scalefactor=1 / 255,
                      size=(320, 320),
                      mean=None,
                      swapRB=True,
                      crop=False):
        """First create creates 4-dimensional blob from image and
        execute forward pass.

        Args:
            frame: Frame of video
            scalefactor: Basically multiplies(scales) our image channels. and
                remember that it scales it down by a factor of 1/n, where n is
                the scalefactor you provided.
            size: Spatial size for output frame(image).
            mean: Scalar with mean values which are subtracted from channels.
                values are intended to be in (mean_R, mean-G, mean-B) order
                if frame(image) has BGR ordering and swapRB is True.
            swapRB: Flag which indicates that swap first and last channels
                in 3-channel image is necessary.
            crop: Flag which indicates whether frame(image) will be cropped
                after resize or not.

        Return:
            Runs forward pass to compute output of layer.
        """
        # First we must convert it to blob fromat,cuz network understand it
        # and retrun 4-dimensional Mat with NCHW imensions order
        blob = cv.dnn.blobFromImage(frame,
                                    scalefactor,
                                    size,
                                    mean,
                                    swapRB,
                                    crop)
        net.setInput(blob)
        # name of each layer
        layer_names = net.getLayerNames()
        output_names = [layer_names[i - 1] for i in
                        net.getUnconnectedOutLayers()]
        outputs = net.forward(output_names)
        return outputs

    def _find_object(self, frame, outputs, conf_threshold, nms_threshold):
        """Detect main object(like "person") and target object(like"dog")
        and if two object approach each other, detect theft.

        Args:
            frame: Frame of video
            outputs: Runs forward pass to compute output of layer
            conf_threshold: Used to filter boxes by score.
            nms_threshold: A threshold used in non maximum suppressin.

        Return:
            If target object(like "dog") and main object(like "person")
            approach each other, return True. else return False.
        """
        person_obj = []
        target_obj = []
        bbox, class_ids, confs = self._extract_outputs(frame,
                                                       outputs,
                                                       conf_threshold)
        # Performs non maximum suppression given boxes and corresponding scores
        indices = cv.dnn.NMSBoxes(bbox, confs, conf_threshold, nms_threshold)
        if len(indices) > 0:
            for index in indices:
                detect_object = self.classes_names[class_ids[index]]
                # if detect main target(like "person")
                if detect_object == self.main_target:
                    person_obj = [bbox[index][num] for num in range(4)]
                    self._draw_rectangle(frame,
                                         person_obj,
                                         class_ids,
                                         index,
                                         confs)
                # if detect target object(like "dog")
                elif detect_object == self.target_object:
                    target_obj = [bbox[index][num] for num in range(4)]
                    self._draw_rectangle(frame,
                                         target_obj,
                                         class_ids,
                                         index,
                                         confs)
                # if detect target object(like "dog") and main object
                # (like "person") simultaneously
                if len(person_obj) != 0 and len(target_obj) != 0:
                    theft_detection = self._theft_detection(person_obj,
                                                            target_obj)
                    return theft_detection

    @staticmethod
    def _extract_outputs(frame, outputs, conf_threshold):
        """Detect (x, y, w, h) of shape of object and save a confidence and
        class id

        Args:
            frame: Frame of video
            outputs: Runs forward pass to compute output of layer.
            conf_threshold: Used to filter boxes by score.

        Returns:
            bbox: (x, y, w, h) of shape
            class_ids: Id of class names
            confs: Used to filter boxes by score
        """
        h_frame, w_frame = frame.shape[:2]
        bbox = []
        class_ids = []
        confs = []
        # This loop 3 time will be execute
        for output in outputs:
            for dtction in output:
                scores = dtction[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > conf_threshold:
                    w, h = int(dtction[2] * w_frame), int(dtction[3] * h_frame)
                    x, y = int((dtction[0] * w_frame) - w / 2), int(
                        (dtction[1] * h_frame) - h / 2)
                    bbox.append([x, y, w, h])
                    class_ids.append(class_id)
                    confs.append(float(confidence))
        return bbox, class_ids, confs

    def _theft_detection(self, person_obj, trget_obj):
        """Detect theft

           Args:
               person_obj: Dimensions of main object
               trget_obj: Dimensions of target object

           Return:
               Retrun True, if detect theft.else retrun False
           """
        intersection_x_axis = self._intersection_axis(person_obj,
                                                      trget_obj,
                                                      axis="x")
        if len(intersection_x_axis) != 0:
            intersection_y_axis = self._intersection_axis(person_obj,
                                                          trget_obj,
                                                          axis="y")
            if len(intersection_y_axis) != 0:
                self.color = (0, 0, 255)
                return True
            else:
                self.color = (255, 0, 255)
                return False
        else:
            self.color = (255, 0, 255)
            return False

    @staticmethod
    def _intersection_axis(person_obj, trgt_obj, axis="x"):
        """It checks whether our two objects have the same coordinates or not

        Args:
            person_obj: Dimensions of main object
            trgt_obj: Dimensions of target object
            axis: check from x_axis or y_axis, default="x"

        Return:
            A list of common coordinates of our two objects
        """
        # For x axis
        if axis == "x":
            i, j = 0, 2
        else:
            # for y axis
            i, j = 1, 3
        x_or_y_person = person_obj[i]
        xw_or_yh_person = person_obj[i] + person_obj[j]
        x_or_y_target = trgt_obj[i]
        xw_yh_target = trgt_obj[i] + trgt_obj[j]
        person_x_or_y_range = [i for i in range(x_or_y_person, xw_or_yh_person + 1)]
        target_x_or_y_range = [i for i in range(x_or_y_target, xw_yh_target + 1)]
        intersection_axis = [item for item in person_x_or_y_range
                             if item in target_x_or_y_range]
        return intersection_axis

    def _draw_rectangle(self, frame, obj, class_ids, index, confs):
        """This function draw rectangle for desired object in frame of video

        Args:
            frame: Frame of video
            obj: Desired object
            class_ids: Id of class name
            index: Index in class names(exp== 80 index in class names is car)
            confs: Percentage of correct diagnosis
        """
        x, y, w, h = obj
        xw, yh = x + w, y + h

        cv.rectangle(frame, obj, self.color, 1)
        # Top left x,y
        cv.line(frame, (x, y), (x + 24, y), self.color, 3)
        cv.line(frame, (x, y), (x, y + 24), self.color, 3)
        # top right x1,y
        cv.line(frame, (xw, y), (xw - 24, y), self.color, 3)
        cv.line(frame, (xw, y), (xw, y + 24), self.color, 3)
        # bottom left x,y1
        cv.line(frame, (x, yh), (x + 24, yh), self.color, 3)
        cv.line(frame, (x, yh), (x, yh - 24), self.color, 3)
        # bottom right x1,y1
        cv.line(frame, (xw, yh), (xw - 24, yh), self.color, 3)
        cv.line(frame, (xw, yh), (xw, yh - 24), self.color, 3)

        txt = f"{self.classes_names[class_ids[index]]} " \
              f"{int(confs[index] * 100)}%"
        cv.putText(frame,
                   text=txt,
                   org=(obj[0], obj[1] - 10),
                   fontFace=cv.FONT_HERSHEY_SIMPLEX,
                   fontScale=0.5,
                   color=self.color,
                   thickness=1)

    def _send_notification(self, frame):
        """If theft detection is True this function will be execute

        Arg:
            frame: Frame of video
        """
        sms_class = Sms(phone_number=self.sms_information["phone_number"],
                        api=self.sms_information["api"])
        # For first time
        if self.first_time == 0:
            sms_class.send_sms()
            self.first_time = time.time()
        else:
            second_time = time.time()
            diff = second_time - self.first_time
            # after 5 min, again resend sms (5min * 60sec = 300sec)
            if diff >= 300:
                sms_class.send_sms()
                self.first_time = time.time()

    def _description_bar(self, frame):
        """Show time, authorised text and FPS at top of frame

        Arg:
            frame: Frame of video
        """
        self._black_bar(frame)
        self._date_time(frame)
        self._show_authorised_txt(frame)
        self._compute_fps(frame)

    @staticmethod
    def _black_bar(frame):
        """Create black rectangle at top of frame

        Arg:
            frame: Frame of video
        """
        cv.rectangle(frame,
                     pt1=(0, 0),
                     pt2=(640, 20),
                     color=(0, 0, 0),
                     thickness=-1)

    @staticmethod
    def _date_time(frame):
        """Show time at top of frame

        Arg:
            frame: Frame of video
        """
        date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        cv.putText(frame,
                   text=date_time,
                   org=(5, 15),
                   fontFace=cv.FONT_HERSHEY_SIMPLEX,
                   fontScale=0.5,
                   color=(255, 255, 255),
                   thickness=1)

    def _show_authorised_txt(self, frame):
        """Show authorised text at top of frame (like: authorised=True)

        Arg:
            frame: Frame of video
        """
        msg = "No"
        if self.authorised:
            msg = "Yes"
        txt = f"Authorised={msg}"
        cv.putText(frame,
                   text=txt,
                   org=(290, 15),
                   fontFace=cv.FONT_HERSHEY_SIMPLEX,
                   fontScale=0.5,
                   color=(255, 255, 255),
                   thickness=1)

    def _compute_fps(self, frame):
        """Show FPS at top of frame

        Arg:
            frame: Frame of video
        """
        # FPS
        current_time = time.time()
        fps = 1 / (current_time - self.previous_time)
        self.previous_time = current_time
        txt = f"FPS={str(int(fps))}"
        cv.putText(frame,
                   text=txt,
                   org=(570, 15),
                   fontFace=cv.FONT_HERSHEY_SIMPLEX,
                   fontScale=0.5,
                   color=(255, 255, 255),
                   thickness=1)
