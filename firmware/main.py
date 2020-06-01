"""Main file running on the scales ESP32."""
import time

import bluetooth
from machine import ADC, Pin

from ble_scales import BLEScales

# from filtering import KalmanFilter

ble = bluetooth.BLE()
scales = BLEScales(ble)
# kf = KalmanFilter(0.2, 0.5)
button_pin = Pin(23, Pin.IN)
vsens_pin = ADC(Pin(34))
vsens_pin.atten(ADC.ATTN_11DB)


def vsens_to_percent(v_adc):
    # battery_voltage = vsens_pin.read() / 572.1  # 2.08V measured = 2380 = 4.16V real
    # 2403 = 100%
    # 2346 = 94%
    # 2288 = 83%
    # 2231 = 72%
    # 2174 = 59%
    # 2117 = 50%
    # 2060 = 33%
    # 2002 = 15%
    # 1945 = 6%
    # 1888 = 0%
    if v_adc > 2346:
        val = int(0.105263 * v_adc - 153)
        return val if val <= 100 else 100
    if v_adc > 2288:
        return int(0.189655 * v_adc - 351)
    if v_adc > 2231:
        return int(0.192983 * v_adc - 359)
    if v_adc > 2174:
        return int(0.22807 * v_adc - 437)
    if v_adc > 2117:
        return int(0.157895 * v_adc - 284)
    if v_adc > 2060:
        return int(0.298246 * v_adc - 581)
    if v_adc > 2002:
        return int(0.310345 * v_adc - 606)
    if v_adc > 1945:
        return int(0.157895 * v_adc - 301)
    if v_adc >= 1888:
        return int(0.105263 * v_adc - 198)
    return 0


def main():
    bat_percent = vsens_to_percent(vsens_pin.read())
    print(bat_percent)
    scales.set_battery_level(bat_percent)

    start = time.ticks_ms()
    while True:
        time_delta = time.ticks_diff(time.ticks_ms(), start)
        if time_delta < 10000:
            scales.set_weight(0, notify=True)
        elif time_delta < 35000:
            scales.set_weight((time_delta - 10000) * 1.6 / 1000, notify=True)
        elif time_delta < 45000:
            scales.set_weight(40, notify=True)
        else:
            start = time.ticks_ms()

        if button_pin.value() == 1:
            start = time.ticks_ms()  # tare

        # filtered_weight = kf.update_estimate(filtered_weight)
        # scales.set_weight(filtered_weight, notify=True)
        time.sleep_ms(250)


if __name__ == "__main__":
    main()