
import time

import cv2
import mss
import numpy as np


from flask import Flask, request, redirect, url_for, make_response
app = Flask(__name__)

sct = mss.mss()
# Part of the screen to capture


def get_screenshot(sct):

    last_time = time.time()

    # Get raw pixels from the screen, save it to a Numpy array
    monitor = {"top": 0, "left": 0, "width": 1440, "height": 900}
    img = np.array(sct.grab(monitor))
 


    # Display the picture


    # Display the picture in grayscale
    # cv2.imshow('OpenCV/Numpy grayscale',
    #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))
        
    return img

@app.route("/screenshot/")
def last_image():

    img = get_screenshot(sct)

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, encimg = cv2.imencode('.jpg', img, encode_param)

    resp = make_response(encimg.tobytes())
    
    resp.content_type = "image/jpeg"
    return resp    


@app.route("/slideshow/")
def slide_show():
    html_text = """
                    <head>
                        <meta http-equiv="refresh" content="1">
                    </head>

                     <a href="."><img style='height: 100%; width: 100%; object-fit: contain' src="/screenshot" width="100%"> </a>
                """
    return html_text







if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7777)
