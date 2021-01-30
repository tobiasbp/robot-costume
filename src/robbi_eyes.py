import neopixel, utime
import microbit as mb

# Configuration variables
LED_STRIP_LENGTH = 24
LED_ADVANCE_RATE_MS = 1000 / 20  # 1000/HZ
# LED_REFRESH_RATE_MS = 50
LED_FADE_RATE_MS = 1000 / 40  # 1000/HZ
LED_STRIP_PIN = mb.pin0
LED_COLOR_INDEX = 0
# The available colors
LED_COLORS = [
    (250, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
]
NEXT_COLOR_BUTTON = mb.button_a

# Divide by higher number for longer tail
LED_FADE_SPEED = int(max(LED_COLORS[LED_COLOR_INDEX]) / 16)

# The LED strip
led_strip = neopixel.NeoPixel(LED_STRIP_PIN, LED_STRIP_LENGTH)

# make sure all LEDs are off.
led_strip.clear()
led_color = LED_COLORS[LED_COLOR_INDEX]
# Time stamps
ts_led_advance = 0
# ts_led_refresh = 0
ts_led_fade = 0

led_index = 0
while True:

    # Change color
    if NEXT_COLOR_BUTTON.was_pressed():
        if LED_COLOR_INDEX == len(LED_COLORS) - 1:
            LED_COLOR_INDEX = 0
        else:
            LED_COLOR_INDEX += 1
        LED_FADE_SPEED = int(max(LED_COLORS[LED_COLOR_INDEX]) / 16)
        # Update currently used color
        led_color = LED_COLORS[LED_COLOR_INDEX]

    # Advance to next LED
    if utime.ticks_diff(utime.ticks_ms(), ts_led_advance) > LED_ADVANCE_RATE_MS:
        ts_led_advance = utime.ticks_ms()
        # Update LED
        led_strip[led_index] = led_color
        # Calculate index of next LED
        if led_index == LED_STRIP_LENGTH - 1:
            led_index = 0
        else:
            led_index += 1

    # Lower intensity of all LEDs and write data to strip
    if utime.ticks_diff(utime.ticks_ms(), ts_led_fade) > LED_FADE_RATE_MS:
        ts_led_fade = utime.ticks_ms()
        for i in range(LED_STRIP_LENGTH):
            led_strip[i] = [
                v - LED_FADE_SPEED if v > LED_FADE_SPEED else 0 for v in led_strip[i]
            ]
        led_strip.show()
