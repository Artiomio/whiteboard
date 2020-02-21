import random
import time

import cv2
import mss
import numpy as np

from flask import Flask, request, redirect, url_for, make_response, render_template

from waitress import serve

SCREEN_GRAB_RANGE = {"top": 0, "left": 0, "width": 1440, "height": 900}

ALLOWED_HOSTS = [ "127.0.0.1",
                  "78.37.40.126",    # Петин ip
                  "188.243.172.35",  # Мой внешний 
                  "192.168.1.17",    # Мой внутренний ip
                  "192.168.1.1",     # Роутер
                  "192.168.1.18",    # Blackbook
                  "192.168.1.198"]   # Дианин комп




app = Flask(__name__)

sct = mss.mss()





def get_screenshot(sct):
    try:
        # Get raw pixels from the screen, save it to a Numpy array
        monitor = SCREEN_GRAB_RANGE
        img = np.array(sct.grab(monitor))
    except:
        print("Error taking screenshot!")
        width = SCREEN_GRAB_RANGE["width"] - SCREEN_GRAB_RANGE["left"]
        height = SCREEN_GRAB_RANGE["height"] - SCREEN_GRAB_RANGE["top"]
        img = np.random.randint(0, 255, size=(100, 100, 3), dtype="uint8")

    return img


@app.route("/<url_code>/screenshot/")
def last_image(url_code):
    global secret_codes

    if url_code not in secret_codes:
        print("Неправильный секрет")
        return "Неправильный секрет!"


    #if request.remote_addr not in ALLOWED_HOSTS:
    #    return "Hello " + request.remote_addr


    start = time.time()
    img = get_screenshot(sct)
    print("IP address:", request.remote_addr)
    print("Time spent on retrieving desktop screenshot:", time.time() - start)



    start = time.time()
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 20]
    result, encimg_jpg = cv2.imencode('.jpg', img, encode_param)
    print("Time spent on compressing JPEG:", time.time() - start)

 
    """
    start = time.time()
    result, encimg_png = cv2.imencode('.png', img)
    print("Time spent on compressing PNG:", time.time() - start)
    """
    

    
    resp = make_response(encimg_jpg.tobytes())
    
    resp.content_type = "image/jpeg"
    print('jpeg data size:', len(encimg_jpg))
    #print('png data size:', len(encimg_png))





    return resp    



@app.route("/<url_code>/webcamshot/")
def webcam_image(url_code):
    global webcam, secret_codes
    #if request.remote_addr not in ALLOWED_HOSTS:
    #    print("Неразрешенный ip-адрес: ", request.remote_addr)
    #    return "Hello " + request.remote_addr
    if url_code not in secret_codes:
        print("Неправильный секрет", request.remote_addr)
        return "Неправильный секрет!"


    start = time.time()


    # global webcam_is_being_read
    #if webcam_is_being_read:
    #    print("Overlapping while reading webcam!***********************************************************")
    #webcam_is_being_read = True
    #webcam_is_being_read = True after webcam.read()

    ret, img = webcam.read()
    img = cv2.resize(img, (133, 100))


    print("IP address", request.remote_addr)
    print("Time spent on retrieving webcam image:", time.time() - start)



    start = time.time()
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, encimg = cv2.imencode('.jpg', img, encode_param)
    print("Time spent on compressing the image:", time.time() - start)

    resp = make_response(encimg.tobytes())
    
    resp.content_type = "image/jpeg"
    print('jpeg data size:', len(encimg))

    return resp    


# HTML page with our video stream
@app.route("/<url_code>/video")
def static_webcam_endpoint(url_code):
    print("Provided secret:", url_code)
    if url_code not in secret_codes:
        print("Неправильный секрет", request.remote_addr)
        return "Неправильный секрет!"

    return render_template('webcam.html', pause_in_milliseconds=1000)


# HTML page with the whiteboard
@app.route("/<url_code>/whiteboard")
def static_whiteboard_endpoint(url_code):
    print("Provided secret:", url_code)
    if url_code not in secret_codes:
        print("Неправильный секрет", request.remote_addr)

        return "Неправильный секрет!"

    return render_template('whiteboard.html', pause_in_milliseconds=2000)

@app.route("/<url_code>/")
def shorter(url_code):
    return static_whiteboard_endpoint(url_code)    



#webcam = cv2.VideoCapture(0)

secret_code = "".join([chr(random.randint(ord("A"), ord("Z"))) for _ in range(8)])
secret_codes = (secret_code, "roma")
#secret_codes = "PBZNYVCHSXKRN"
print("Secret code:", secret_codes)
print(f"http://banana.sknt.ru/{secret_codes}/whiteboard")

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=7893)
    import webbrowser
    port = 7893
    webbrowser.open(f"http://127.0.0.1:{port}/{secret_code}/whiteboard")

    serve(app, host='0.0.0.0', port=port)
