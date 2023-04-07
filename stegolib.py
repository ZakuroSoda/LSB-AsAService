import sys
import numpy as np
from PIL import Image

np.set_printoptions(threshold=sys.maxsize)
PASSWORD = "$END$"

def Encode(src, dest, message):

    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size//n

    message += PASSWORD
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)

    if req_pixels > (total_pixels * 3):
        return None

    else:
        index=0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
                    index += 1

        array=array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        
        return dest


#decoding function
def Decode(src):

    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size//n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    hiddenmessage = ""
    for i in range(len(hidden_bits)):
        x = len(PASSWORD)
        if message[-x:] == PASSWORD:
            break
        else:
            message += chr(int(hidden_bits[i], 2))
            message = f'{message}'
            hiddenmessage = message
    #verifying the PASSWORD
    if PASSWORD in message:
        return hiddenmessage[:-x]
    else:
        return None