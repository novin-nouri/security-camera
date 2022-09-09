import cv2 as cv
import pyzbar.pyzbar as pyzbar
import os


class QrCode:
    """Class to detect QR code"""

    def __init__(self, name):
        self.name = name
        """Initializes a QrCode

        Arg:
            name: user name
        """

    def __repr__(self):
        return f"{self.__class__.__name__!r}({self.__dict__!r})"

    def detect_qrcode(self, frame):
        """Detect all qr codes if frame

        Arg:
            frame: Frame of video

        Return:
            If detect user QR code, return True, else return False
        """
        decoded_objects = pyzbar.decode(frame)
        if len(decoded_objects) != 0:
            for obj in decoded_objects:
                rec = obj.rect
                txt = str(obj.data)
                # remove 2 char at first and last char
                txt = txt[2:-1]
                cv.rectangle(frame,
                             pt1=(rec[0], rec[1]),
                             pt2=(rec[0] + rec[2], rec[1] + rec[3]),
                             color=(0, 0, 255),
                             thickness=2)
                authorised = self._authorised(frame, rec, txt)
                return authorised

    @staticmethod
    def _read_qr_code():
        """Read all QR code in (QR-code-files) forlder

        Return:
            A list of all image names in folder
        """
        qrcode_folder = r"files\QR-code_files"
        qrcode_names = []
        image_names = [img for img in os.listdir(qrcode_folder)]
        for img in image_names:
            img_address = f"{qrcode_folder}\{img}"
            image = cv.imread(img_address)
            decoded_objects = pyzbar.decode(image)
            if len(decoded_objects) != 0:
                for obj in decoded_objects:
                    txt = str(obj.data)
                    # remove 2 char at first and last char
                    txt = txt[2:-1]
                    # if txt not in qrcode_names:
                    qrcode_names.append(txt)
        return qrcode_names

    def _authorised(self, frame, rec, txt):
        """detect user Qr code and draw rectangle

        Args:
            frame: Frame of video
            rec: Dimensions of qrcode
            txt: Text of QR code

        Retrun:
            Return True if text of QR code == user name, eles return False
        """
        qrcode_names = self._read_qr_code()
        if txt in qrcode_names:
            cv.putText(frame,
                       text=txt,
                       org=(rec[0], rec[1] - 10),
                       fontFace=cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=0.7,
                       color=(0, 0, 255),
                       thickness=2)
            return True
        else:
            return False
