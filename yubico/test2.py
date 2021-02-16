# https://yubico-client.readthedocs.io/en/latest/
# pip install yubico-client

import yubikey
from getpass import getpass

otp = getpass('Please enter OTP code: ')
print(yubikey.getID(otp))
print(yubikey.auth('vvbtrvcdetek',otp))
input()
