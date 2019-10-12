import subprocess
import threading


def take_img(file_name):
    # Bash command for taking a picture with the webcam.
    # command = "fswebcam -r 640x480 --jpeg 100 -D 0 -S 30 %s" % file_name

    subprocess.run(["fswebcam", "-r", "-b", "640x480", "--no-banner",
                    "--jpeg", "100", "-D", "0", "-S", "30", file_name])


class Imaging(threading.Thread):
    def __init__(self):
        self.running = True
        self.picNo = 1
        threading.Thread.__init__(self)

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            take_img("img/shot_%d.jpeg" % self.picNo)
            self.picNo += 1
