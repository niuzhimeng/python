from PIL import ImageGrab
from time import sleep
sleep(2)
pic = ImageGrab.grab()
pic.save('1.jpg')