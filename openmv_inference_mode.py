# Upload this to OpenMV camera
# Listens for 'CAPTURE\n' command and sends image back

import sensor
import image
import time
from pyb import USB_VCP

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((0, 30, 320, 160))
sensor.skip_frames(time=2000)

usb = USB_VCP()
print("OpenMV ready")

while True:
    if usb.any():
        cmd = usb.readline().decode().strip()

        if cmd == "CAPTURE":
            img = sensor.snapshot()
            img_bytes = img.compress(quality=95).bytearray()

            usb.write("OK\n")
            usb.write(len(img_bytes).to_bytes(4, "little"))
            usb.write(img_bytes)

    time.sleep_ms(50)
