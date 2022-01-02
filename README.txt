# TOTP-CS370
A TOTP application based on RFC 6238.

Some notes before running:
-This was coded in Python 2.7, I hoped that this would the script "play nice"
 with the flip server

-This uses a virtual environment to run.  This is the virtualenv package on the
 flip server.  To activate the virtual environment run this command in the
 terminal on flip:

    $> source ./bin/activate

    This should activate the virtual environment with the necessary packages
    to run the python script.

    If for some reason the virtual environment doesn't work, the following
    are required to run:

    qrcode, base64, hmac, time, struct, hashlib, sys

    The only package from this list that needs to
    explicitly installed is qrcode (https://pypi.org/project/qrcode/).
    It can be installed with:

        $> pip install qrcode[pil]

TO RUN THIS SCRIPT:
1. Activate the virtual environment
    $> source ./bin/activate
2. Create a configuration file
    The config file is used to set the secret, account, and qr-code file name.
    The config file is 3 lines and should follow the format:

    {secret}
    {account}
    {qr code file name}

    See example.config for an example of the configuration file.

3. On the flip server, enter this command in the terminal:
    $> python gallegos-MP4.py [config file]
    example:
    $> python gallegos-MP4.py example.config

    This will generate a qr code with parameters specified in the file
    example.config

The QR code will be saved in the same directory as gallegos-MP4.py.
