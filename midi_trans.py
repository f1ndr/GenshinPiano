import pywinio
import time
import atexit
import pygame
import pygame.midi

# KeyBoard Commands
# Command port
KBC_KEY_CMD = 0x64
# Data port
KBC_KEY_DATA = 0x60

g_winio = None


def get_winio():
    global g_winio

    if g_winio is None:
        g_winio = pywinio.WinIO()

        def __clear_winio():
            global g_winio
            g_winio = None

        atexit.register(__clear_winio)

    return g_winio


def wait_for_buffer_empty():
    """
    Wait keyboard buffer empty
    """

    winio = get_winio()

    dw_reg_val = 0x02
    while dw_reg_val & 0x02:
        dw_reg_val = winio.get_port_byte(KBC_KEY_CMD)


def key_down(scancode):
    winio = get_winio()

    wait_for_buffer_empty()
    winio.set_port_byte(KBC_KEY_CMD, 0xd2)
    wait_for_buffer_empty()
    winio.set_port_byte(KBC_KEY_DATA, scancode)


def key_up(scancode):
    winio = get_winio()

    wait_for_buffer_empty()
    winio.set_port_byte(KBC_KEY_CMD, 0xd2)
    wait_for_buffer_empty()
    winio.set_port_byte(KBC_KEY_DATA, scancode | 0x80)


def key_press(scancode, press_time=0.2):
    key_down(scancode)
    time.sleep(press_time)
    key_up(scancode)


dic = {48: 0x2c, 50: 0x2d, 52: 0x2e, 53: 0x2f, 55: 0x30, 57: 0x31, 59: 0x32,
       60: 0x1e, 62: 0x1f, 64: 0x20, 65: 0x21, 67: 0x22, 69: 0x23, 71: 0x24,
       72: 0x10, 74: 0x11, 76: 0x12, 77: 0x13, 79: 0x14, 81: 0x15, 83: 0x16}
"""
dic = {48: 'z', 50: 'x', 52: 'c', 53: 'v', 55: 'b', 57: 'n', 59: 'm',
       60: 'a', 62: 's', 64: 'd', 65: 'f', 67: 'g', 69: 'h', 71: 'j',
       72: 'q', 74: 'w', 76: 'e', 77: 'r', 79: 't', 81: 'y', 83: 'u'}
"""


def print_device_info():
    pygame.midi.init()
    _print_device_info()
    pygame.midi.quit()


def _print_device_info():
    for i in range(pygame.midi.get_count()):
        r = pygame.midi.get_device_info(i)
        (interf, name, device_input, device_output, opened) = r

        in_out = ""
        if device_input:
            in_out = "(input)"
        if device_output:
            in_out = "(output)"

        print(
            "idx%2i: interface: %s, name: %s, opened: %s # %s"
            % (i, interf, name, opened, in_out)
        )


def input_main(device_id=None):
    pygame.init()
    """
    event_get = pygame.event.get
    event_post = pygame.event.post
    """

    pygame.midi.init()

    _print_device_info()

    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id

    print("using input_id: %s" % input_id)
    i = pygame.midi.Input(input_id)

    pygame.display.set_mode((1, 1))

    while True:
        if i.poll():
            me = i.read(1)
            if me[0][0][0] == 144:
                key_press(dic[me[0][0][1]])


if __name__ == '__main__':
    print_device_info()
    print("\nPlease input the index of your device:", end=" ")
    try:
        input_main(int(input()))
    except ValueError:
        print("Input an invalid device id")
    except pygame.midi.MidiException:
        print("Select device is not a valid input device")
