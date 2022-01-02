"""
Filename: gallegos-MP4.py
Author: Nicholai Gallegos
Date: 11/3/2021
"""
import qrcode
import base64
import hmac
import time
import struct
import hashlib
import sys


# Some constants for the protocol
TIME_STEP = 30  # time interval to use
T0 = 0  # Initial time to substract the current time from
DIGIT = 6  # Length to output for an OTP passcode


"""
Function: get_unix_time()
Description: Gets the system time since the epoch as an integer. Helper function
for TOTP and get_time_step.
"""
def get_unix_time():
    return int(time.time())


"""
Function: get_time_step()
Description: Get the current time interval as described by RFC 6238.  Helper
function for TOTP.  Returns an integer
"""
def get_time_step():
    return (get_unix_time() - T0) // TIME_STEP


"""
Function: hmac_sha1(base32 string, int)
Description: Generate an HMAC with SHA-1 as the hash.  This was the default
value for a hash in the RFC, so I went with SHA-1.  Returns a bytearray as the
HMAC.
"""
def hmac_sha1(k, c):
    h = hmac.new(base64.b32decode(k), '', hashlib.sha1)
    # Update the hmac object with a long long (8 byte) unsigned byte
    # representation of c.
    h.update(struct.pack(">Q", c))
    result = bytearray(h.digest())
    return result


"""
Function: HOTP(base32 string, int)
Description: Generates a HOTP value based on the specifcation in RFC 4226.
Returns an integer of length |DIGIT|
"""
def HOTP(k, c):
    # Get the HMAC
    hmac_result = hmac_sha1(k, c)
    # The following offset and bin_code were described in RFC 4226 HOTP
    offset = hmac_result[-1] & 0xf
    # bin_code comes directly from the RFC specification section 5.4 at this url
    # https://datatracker.ietf.org/doc/html/rfc4226#section-5.4
    bin_code = (((hmac_result[offset]  & 0x7f) << 24) \
            | ((hmac_result[offset+1] & 0xff) << 16) \
            | ((hmac_result[offset+2] & 0xff) <<  8) \
            | (hmac_result[offset+3] & 0xff))
    # Get a |DIGIT| length string
    hotp_pass = bin_code % 10**DIGIT
    return hotp_pass


"""
Function: TOTP()
Get a TOTP value, since TOTP is just HOTP with a time interval as the counter,
this function finds the time interval according to the RFC 6238 and passes it to
HOTP as the counter value.
"""
def TOTP(k):
    t = get_time_step()
    totp_pass = HOTP(k, t)
    return totp_pass


def main():
    # check for the correct number of arguments
    num_args = len(sys.argv)

    if num_args != 2:
        print("Error.  Correct Usage:")
        print("$> python gallegos-MP4.py [config file]")
        print("Example:")
        print("$> python gallegos-MP4.py example.config")
        print("This runs the TOTP script with the parameters specifed in")
        print("the file 'example.config'")
        quit()

    # Open the config file
    input_file = open(sys.argv[1], 'r')
    lines = input_file.readlines()

    # Get the secret from the file and encode it to base32 for uri
    secret = lines[0].strip()
    secret = secret.encode('utf-8')
    secret = base64.b32encode(secret)
    print("Secret: %s" % secret)

    # Get the account from the second line in the config file for the uri
    account = lines[1].strip()
    print("Account: %s" % account)

    # This follows the format specifed by Google Authenticator found here:
    # https://github.com/google/google-authenticator/wiki/Key-Uri-Format
    uri = 'otpauth://totp/GallegonOTP:'
    uri += account
    uri += '?secret='
    uri += secret
    uri += '&issuer=GallegonOTP'

    # Make the qrcode with the uri data.  Used qrcode package found here:
    # https://pypi.org/project/qrcode/

    # Get the intended file name of the qr code to save as from config
    qr_file_name = ("./%s" % lines[2].strip())
    img = qrcode.make(uri)
    type(img)  # qrcode.image.pil.PilImage
    img.save(qr_file_name)

    # Print the initial passcode
    passcode = TOTP(secret.encode('utf-8'))
    print("Passcode: %d" % passcode)

    print("Press Ctrl + c to exit.")
    print("This will loop indefinitely.  Updates passcode every interval.")

    prev = passcode
    # Print the passcodes as they update (every TIME_STEP seconds)
    while (1):
        passcode = TOTP(secret.encode('utf-8'))
        # Check if the passcode has updated
        if passcode != prev:
            prev = passcode
            print("Passcode: %d" % passcode)


main()
