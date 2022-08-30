import requests


class Sms:
    """Class to send sms"""

    def __init__(self, phone_number, api):
        self.phone_number = phone_number
        self.api = api
        """Initializes a Sms

        Args:
            phone_number: User's phone number for recieve sms
            api: Users's API for send sms
        """

    def __repr__(self):
        return f"{self.__class__.__name__!r}({self.__dict__!r})"

    def send_sms(self):
        """Send sms to user"""
        message = f"Security Camera: Hi,we find a person near your object."
        data = {"from": "30004967666666",
                "to": self.phone_number,
                "text": message}
        response = requests.post(url=self.api, json=data)
        print("response= ", response)
