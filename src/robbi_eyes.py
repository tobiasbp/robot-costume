import neopixel, utime
import microbit as mb

# Configuration variables
LED_STRIP_LENGTH = 24
LED_ADVANCE_RATE_MS = 50
# LED_REFRESH_RATE_MS = 50
LED_FADE_RATE_MS = 50
LED_STRIP_PIN = mb.pin0
LED_COLOR = (20, 0, 0)

# Divide by higher number for longer tail
LED_FADE_SPEED = int(max(LED_COLOR) / 6)

# The LED strip
led_strip = neopixel.NeoPixel(LED_STRIP_PIN, LED_STRIP_LENGTH)

# make sure all LEDs are off.
led_strip.clear()

# Time stamps
ts_led_advance = 0
# ts_led_refresh = 0
ts_led_fade = 0

led_index = 0
while True:
    # Advance to next LED
    if utime.ticks_diff(utime.ticks_ms(), ts_led_advance) > LED_ADVANCE_RATE_MS:
        ts_led_advance = utime.ticks_ms()
        # mb.display.set_pixel(led_index,0,9)
        led_strip[led_index] = LED_COLOR
        # Calculate index of next LED
        if led_index < LED_STRIP_LENGTH - 1:
            led_index += 1
        else:
            led_index = 0

    # Write data to LED strip
    """
    if utime.ticks_diff(utime.ticks_ms(), ts_led_refresh) > LED_REFRESH_RATE_MS:
        ts_led_refresh = utime.ticks_ms()
        led_strip.show()
    """

    # Lower intensity of all LEDs and write data to strip
    if utime.ticks_diff(utime.ticks_ms(), ts_led_fade) > LED_FADE_RATE_MS:
        ts_led_fade = utime.ticks_ms()
        for i in range(LED_STRIP_LENGTH):
            led_strip[i] = [
                v - LED_FADE_SPEED if v > LED_FADE_SPEED else 0 for v in led_strip[i]
            ]
        led_strip.show()

    """
    eye[0] = LED_COLOR
    eye.show()
    utime.sleep_ms(200)
    eye[0] = (0,0,0)
    eye.show()
    utime.sleep_ms(200)
    """
