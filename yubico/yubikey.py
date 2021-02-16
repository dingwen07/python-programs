# https://yubico-client.readthedocs.io/en/latest/
# pip install yubico-client

import getpass
import yubico_client
from yubico_client import Yubico

client = Yubico('<API_CLIENT_ID>', '<API_SECRET_KEY>')
otpauth = False


def auth(id, otp_code):
    otpauth = False
    err_code = ''
    try:
        if otp_code[0:12] == id:
            otpauth = client.verify(otp_code)
        else:
            err_code = 'INVALID_ID'
    except Exception as excpt:
        err_code = excpt.args[0]
    finally:
        return otpauth, err_code

def getID(otp_code):
    id = otp_code[0:12]
    result = auth(id, otp_code)
    if not result[0]:
        print('Warning:', result[1])
    return id

if __name__ == "__main__":
    print(getID(getpass.getpass('Tap your YubiKey: ')))
    input()