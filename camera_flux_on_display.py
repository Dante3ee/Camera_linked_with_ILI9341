from machine import Pin, SPI
import ili9341
import camera
import time
import gc

# SPI config  (26000000works 30000000works | 1baud = 1bit/sec)
spi = SPI(2, baudrate=30000000, polarity=0, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12))

# Screen init (pins here 
display = ili9341.ILI9341(spi=spi, cs=Pin(15), dc=Pin(0), rst=Pin(2), w=320, h=240, r=1)

# testing the screen
display.fill_rectangle(0, 0, 320, 240, ili9341.color565(0, 0, 0))
print("Display ready")

# Init camera in RGB565 mode (the pins here are the default on the Freenove ESP32-WROVER CAM)
camera.init(0, d0=4, d1=5, d2=18, d3=19, d4=36, d5=39, d6=34, d7=35,
            format=camera.RGB565, framesize=camera.FRAME_QVGA, 
            xclk_freq=camera.XCLK_20MHz,
            href=23, vsync=25, reset=-1, pwdn=-1,
            sioc=27, siod=26, xclk=21, pclk=22, fb_location=camera.PSRAM)
print("Camera ready")

while True:
    buffer = camera.capture()  # Capture as RGB565
    if buffer:
        try:
            display._writeblock(0, 0, 319, 239, buffer)
            
        except Exception as e:
            print("Display method failed:", e)
    
        print(f"Displayed frame: {len(buf)} bytes")
        del buf
        gc.collect()
    else:
        print("No frame")
    # I have no clue on how much the esp32 is capable in terms of fps
    time.sleep(0.02)
