def take_img(file_name):
    # Bash command for taking a picture with the webcam.
    command = "fswebcam -r 640x480 --jpeg 100 -D 0 -S 30 %s" % file_name

    # TODO implement call to the command
