import sensor
import image
import time

# =========================================================
# 1) CAMERA RESET
# =========================================================
# Always reset the camera first
sensor.reset()

# =========================================================
# 2) PIXEL FORMAT
# =========================================================
# GRAYSCALE  → 1 byte per pixel (fast, good for thresholding)
# RGB565    → color image (slower, bigger)
sensor.set_pixformat(sensor.GRAYSCALE)

# =========================================================
# 3) FRAME SIZE (BASE RESOLUTION)
# =========================================================
# QVGA  = 320 x 240
# VGA   = 640 x 480 (slower)
# QQVGA = 160 x 120 (faster)
sensor.set_framesize(sensor.QVGA)

# =========================================================
# 4) WINDOWING / ROI (CROP)
# =========================================================
# Format: (x_offset, y_offset, width, height)
#
# x_offset → how many pixels from LEFT to skip
# y_offset → how many pixels from TOP to skip
# width    → final image width
# height   → final image height
#
# IMPORTANT:
# - Windowing crops the sensor BEFORE snapshot
# - After this, img.width()  == width
# - After this, img.height() == height
#
# Example below:
# - Skip top 30 pixels
# - Keep full width
# - Capture 320 x 160 image
sensor.set_windowing((0, 30, 320, 160))

# =========================================================
# 5) AUTO-ADJUSTMENT STABILIZATION
# =========================================================
# Let camera settle exposure & gain
sensor.skip_frames(time=2000)

# =========================================================
# 6) PRINT DEBUG INFO (IDE TERMINAL)
# =========================================================
print("=== OpenMV Camera Debug ===")
print("Frame size enum:", sensor.get_framesize())
print("Windowing (ROI):", sensor.get_windowing())
print("===========================")

# =========================================================
# 7) LIVE DEBUG LOOP (IDE FRAME BUFFER)
# =========================================================
while True:

    # Capture one frame
    img = sensor.snapshot()

    # Current image size (AFTER windowing)
    w = img.width()     # == ROI width
    h = img.height()    # == ROI height

    # -----------------------------------------------------
    # A) DRAW ROI BORDER
    # -----------------------------------------------------
    # Shows exact capture area
    # thickness → border thickness in pixels
    img.draw_rectangle(
        0, 0, w, h,
        color=255,       # white (for grayscale)
        thickness=2
    )

    # -----------------------------------------------------
    # B) DRAW CENTER CROSSHAIR
    # -----------------------------------------------------
    # Helps align camera / objects
    cx = w // 2         # horizontal center
    cy = h // 2         # vertical center

    img.draw_cross(
        cx, cy,
        color=255,
        size=20,         # length of cross arms
        thickness=2
    )

    # -----------------------------------------------------
    # C) DRAW RESOLUTION TEXT
    # -----------------------------------------------------
    img.draw_string(
        2, 2,            # top-left corner
        "{}x{}".format(w, h),
        color=255,
        scale=1          # text size
    )

    # -----------------------------------------------------
    # D) OPTIONAL GRID (SPATIAL REFERENCE)
    # -----------------------------------------------------
    # Increase step for fewer lines
    # Decrease step for finer grid
    grid_step = 40

    for x in range(0, w, grid_step):
        img.draw_line(x, 0, x, h, color=128)

    for y in range(0, h, grid_step):
        img.draw_line(0, y, w, y, color=128)

    # -----------------------------------------------------
    # E) FRAME RATE CONTROL
    # -----------------------------------------------------
    # Higher → slower update
    # Lower  → faster update
    time.sleep_ms(50)
