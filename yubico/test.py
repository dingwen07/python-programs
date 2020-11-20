# https://yubico-client.readthedocs.io/en/latest/
# pip install yubico-client

import getpass
import yubico_client
from yubico_client import Yubico

client = Yubico('42160', 'QdFqJ0hpRN3EFddDOfThTAL/4Hs=')
otpauth = False

try:
    otpauth = client.verify(getpass.getpass('Please enter OTP code: '))
    #otpauth = client.verify('cccccciittvfentguuknnhflnrdnkjtgjfnhiurrihde')
except Exception as excpt:
    print(excpt.args[0])

print(otpauth)
