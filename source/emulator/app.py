# import cv2
# from werkzeug.wrappers import Request, Response
# from werkzeug.serving import run_simple
# from imutils.video import VideoStream
# import imagezmq


# def sendImagesToWeb():
#     cap = cv2.VideoCapture("./examples/image01.jpg")
#     while True:
#         isSuccess, frame = cap.read()
#         if not isSuccess:
#             cap = cv2.VideoCapture("./examples/image01.jpg")
#             isSuccess, frame = cap.read()
#         jpg = cv2.imencode(".jpg", frame)[1]
#         yield b"--frame\r\nContent-Type:image/jpeg\r\n\r\n" + jpg.tostring() + b"\r\n"


# @Request.application
# def application(request):
#     return Response(
#         sendImagesToWeb(), mimetype="multipart/x-mixed-replace; boundary=frame"
#     )


# if __name__ == "__main__":
#     run_simple("0.0.0.0", 30043, application)

# run this program on each RPi to send a labelled image stream
import socket
import time
import cv2
from imutils.video import VideoStream
import imagezmq

sender = imagezmq.ImageSender(connect_to="tcp://0.0.0.0:5556", REQ_REP=False)
rpi_name = socket.gethostname()  # send RPi hostname with each image
cap = cv2.VideoCapture("./examples/image01.jpg")
cap.set(3, 500)
cap.set(4, 500)
# picam = VideoStream(usePiCamera=True).start()
time.sleep(2.0)  # allow camera sensor to warm up
while True:  # send images as stream until Ctrl-C
    isSuccess, frame = cap.read()
    if not isSuccess:
        cap = cv2.VideoCapture("./examples/image01.jpg")
        isSuccess, frame = cap.read()
    sender.send_image(rpi_name, frame)
