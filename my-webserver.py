#!/usr/bin/python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
from flask import Flask, escape, request, render_template

pins = {"green": 17, "red": 27}
pins_state = {"green": 0, "red": 0}

app = Flask(__name__, template_folder='.')
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for led_color in pins:
    GPIO.setup(pins[led_color], GPIO.OUT)
    GPIO.output(pins[led_color], pins_state[led_color])


@app.route('/')
def root():
    for led_color in pins:
        state = 1 if escape(request.args.get(led_color, "off")) == 'on' else 0
        pins_state[led_color] = state
        GPIO.output(pins[led_color], pins_state[led_color])

    return render_template('main.html', pins_state=pins_state)


def main():
    try:
        app.run(debug=False, host='0.0.0.0', port=5000)

    except KeyboardInterrupt:
        # If CTRL+C is pressed, exit cleanly:
        print("CTRL+C is pressed")
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
