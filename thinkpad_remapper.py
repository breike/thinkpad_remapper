#!/usr/bin/python3

# CC0, originally written by t184256.

# This is an example Python program for Linux that remaps a keyboard.
# The events (key presses releases and repeats), are captured with evdev,
# and then injected back with uinput.

# This approach should work in X, Wayland, anywhere!

# Also it is not limited to keyboards, may be adapted to any input devices.

# The program should be easily portable to other languages or extendable to
# run really any code in 'macros', e.g., fetching and typing current weather.

# The ones eager to do it in C can take a look at (overengineered) caps2esc:
# https://github.com/oblitum/caps2esc


# Import necessary libraries.
import atexit
# You need to install evdev with a package manager or pip3.
import evdev  # (sudo pip3 install evdev)

# making layered layout...
current_layer = 1

# key for switching to layers on pressing
layering_key = evdev.ecodes.KEY_SPACE

# also add ctrl mode for sequential hotkeys
ctrl_pressed = False

# also left alt mode...
alt_pressed = False

# shift mode
shift_pressed = False

# Define an example dictionary describing the remaps.
REMAP_TABLE = {
    # Let's swap A and B...
    evdev.ecodes.KEY_TAB: {
        1: evdev.ecodes.KEY_ESC,
        2: evdev.ecodes.KEY_LEFTALT
    },
    evdev.ecodes.KEY_LEFTALT: {
        1: evdev.ecodes.KEY_LEFTSHIFT,
        2: evdev.ecodes.KEY_LEFTSHIFT
    },
    evdev.ecodes.KEY_Q: {
        1: evdev.ecodes.KEY_Q,
        2: evdev.ecodes.KEY_F13
    },
    evdev.ecodes.KEY_W: {
        1: evdev.ecodes.KEY_W,
        2: evdev.ecodes.KEY_F15
    },
    evdev.ecodes.KEY_E: {
        1: evdev.ecodes.KEY_E,
        2: evdev.ecodes.KEY_UP
    },
    evdev.ecodes.KEY_R: {
        1: evdev.ecodes.KEY_R,
        2: evdev.ecodes.KEY_F16
    },
    evdev.ecodes.KEY_T: {
        1: evdev.ecodes.KEY_T,
        2: evdev.ecodes.KEY_HELP
    },
    evdev.ecodes.KEY_CAPSLOCK: {
        1: evdev.ecodes.KEY_MAIL,
        2: evdev.ecodes.KEY_LEFTCTRL
    },
    evdev.ecodes.KEY_A: {
        1: evdev.ecodes.KEY_A,
        2: evdev.ecodes.KEY_SEARCH,
    },
    evdev.ecodes.KEY_S: {
        1: evdev.ecodes.KEY_S,
        2: evdev.ecodes.KEY_LEFT
    },
    evdev.ecodes.KEY_D: {
        1: evdev.ecodes.KEY_D,
        2: evdev.ecodes.KEY_DOWN
    },
    evdev.ecodes.KEY_F: {
        1: evdev.ecodes.KEY_F,
        2: evdev.ecodes.KEY_RIGHT
    },
    evdev.ecodes.KEY_G: {
        1: evdev.ecodes.KEY_G,
        2: evdev.ecodes.KEY_F19
    },
    evdev.ecodes.KEY_C: {
        1: evdev.ecodes.KEY_C,
        2: evdev.ecodes.KEY_CALC
    },
    # ... and make the left Shift into a second Space.
    evdev.ecodes.KEY_LEFTSHIFT: {
        1: evdev.ecodes.KEY_SPACE,
        2: evdev.ecodes.KEY_SPACE
    },
    evdev.ecodes.KEY_7: {
        1: evdev.ecodes.KEY_BACKSPACE,
        2: evdev.ecodes.KEY_BACKSPACE
    },
    evdev.ecodes.KEY_6: {
        1: evdev.ecodes.KEY_BACKSPACE,
        2: evdev.ecodes.KEY_BACKSPACE
    },
    evdev.ecodes.KEY_8: {
        1: evdev.ecodes.KEY_INSERT,
        2: evdev.ecodes.KEY_INSERT
    },
    evdev.ecodes.KEY_Y: {
        1: evdev.ecodes.KEY_Y,
        2: evdev.ecodes.KEY_PAGEUP
    },
    evdev.ecodes.KEY_U: {
        1: evdev.ecodes.KEY_U,
        2: evdev.ecodes.KEY_1
    },
    evdev.ecodes.KEY_I: {
        1: evdev.ecodes.KEY_I,
        2: evdev.ecodes.KEY_2
    },
    evdev.ecodes.KEY_O: {
        1: evdev.ecodes.KEY_O,
        2: evdev.ecodes.KEY_3
    },
    evdev.ecodes.KEY_P: {
        1: evdev.ecodes.KEY_P,
        2: evdev.ecodes.KEY_4
    },
    evdev.ecodes.KEY_H: {
        1: evdev.ecodes.KEY_H,
        2: evdev.ecodes.KEY_PAGEDOWN
    },
    evdev.ecodes.KEY_J: {
        1: evdev.ecodes.KEY_J,
        2: evdev.ecodes.KEY_5
    },
    evdev.ecodes.KEY_K: {
        1: evdev.ecodes.KEY_K,
        2: evdev.ecodes.KEY_6
    },
    evdev.ecodes.KEY_L: {
        1: evdev.ecodes.KEY_L,
        2: evdev.ecodes.KEY_7
    },
    evdev.ecodes.KEY_SEMICOLON: {
        1: evdev.ecodes.KEY_SEMICOLON,
        2: evdev.ecodes.KEY_8
    },
    evdev.ecodes.KEY_X: {
        1: evdev.ecodes.KEY_X,
        2: evdev.ecodes.KEY_F17
    },
    evdev.ecodes.KEY_V: {
        1: evdev.ecodes.KEY_V,
        2: evdev.ecodes.KEY_F18
    },
    evdev.ecodes.KEY_N: {
        1: evdev.ecodes.KEY_N,
        2: evdev.ecodes.KEY_ENTER
    },
    evdev.ecodes.KEY_M: {
        1: evdev.ecodes.KEY_M,
        2: evdev.ecodes.KEY_9
    },
    evdev.ecodes.KEY_COMMA: {
        1: evdev.ecodes.KEY_COMMA,
        2: evdev.ecodes.KEY_0
    },
    evdev.ecodes.KEY_DOT: {
        1: evdev.ecodes.KEY_DOT,
        2: evdev.ecodes.KEY_MINUS
    },
    evdev.ecodes.KEY_SLASH: {
        1: evdev.ecodes.KEY_SLASH,
        2: evdev.ecodes.KEY_EQUAL
    },
    evdev.ecodes.KEY_1: {
        1: evdev.ecodes.KEY_1,
        2: evdev.ecodes.KEY_BRIGHTNESSUP
    },
    evdev.ecodes.KEY_2: {
        1: evdev.ecodes.KEY_2,
        2: evdev.ecodes.KEY_BRIGHTNESSDOWN
    },
    evdev.ecodes.KEY_3: {
        1: evdev.ecodes.KEY_3,
        2: evdev.ecodes.KEY_NEXTSONG
    },
    evdev.ecodes.KEY_4: {
        1: evdev.ecodes.KEY_4,
        2: evdev.ecodes.KEY_PREVIOUSSONG
    },
}
# The names can be found with evtest or in evdev docs.


# The keyboard name we will intercept the events for. Obtainable with evtest.
MATCH = 'AT Translated Set 2 keyboard'
# Find all input devices.
devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
# Limit the list to those containing MATCH and pick the first one.
kbd = [d for d in devices if MATCH in d.name][0]
atexit.register(kbd.ungrab)  # Don't forget to ungrab the keyboard on exit!
kbd.grab()  # Grab, i.e. prevent the keyboard from emitting original events.


soloing_caps = False  # A flag needed for CapsLock example later.

# Create a new keyboard mimicking the original one.
with evdev.UInput.from_device(kbd, name='kbdremap') as ui:
    for ev in kbd.read_loop():  # Read events from original keyboard.
        if ev.type == evdev.ecodes.EV_KEY:  # Process key events.
            if ev.code == evdev.ecodes.KEY_PAUSE and ev.value == 1:
                # Exit on pressing PAUSE.
                # Useful if that is your only keyboard. =)
                # Also if you bind that script to PAUSE, it'll be a toggle.
                break
            
            # selecting 2 layer if layering key pressed
            elif ev.code == layering_key and (ev.value == 1 or ev.value == 2):
                current_layer = 2
            # or selecting 1 on releasing
            elif ev.code == layering_key and ev.value == 0:
                current_layer = 1
            elif ev.code in REMAP_TABLE:
                if ctrl_pressed and ev.code != evdev.ecodes.KEY_LEFTSHIFT and ev.code != evdev.ecodes.KEY_RIGHTSHIFT:
                    ui.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTCTRL, ev.value)
                if alt_pressed and ev.code != evdev.ecodes.KEY_LEFTSHIFT and ev.code != evdev.ecodes.KEY_RIGHTSHIFT:
                    ui.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTALT, ev.value)
                if shift_pressed and ev.code != evdev.ecodes.KEY_LEFTALT and ev.code != evdev.ecodes.KEY_LEFTCTRL and ev.code != layering_key:
                    ui.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTSHIFT, ev.value)
                # Lookup the key we want to press/release instead...
                remapped_code = REMAP_TABLE[ev.code][current_layer]
                # And do it.
                if remapped_code == evdev.ecodes.KEY_LEFTCTRL:
                    ctrl_pressed = True
                elif remapped_code == evdev.ecodes.KEY_LEFTALT:
                    alt_pressed = True
                elif remapped_code == evdev.ecodes.KEY_LEFTSHIFT and (ev.value == 1 or ev.value == 2):
                    shift_pressed = True
                elif remapped_code == evdev.ecodes.KEY_LEFTSHIFT and ev.value == 0:
                    shift_pressed = False
                else:
                    if ctrl_pressed:
                        ui.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTCTRL, 1)
                    if alt_pressed:
                        ui.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTALT, 1)
                    if shift_pressed:
                        ui.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTSHIFT, 1)
                    if ev.value == 1:
                        ui.write(evdev.ecodes.EV_KEY, remapped_code, 1)
                        ui.write(evdev.ecodes.EV_KEY, remapped_code, 0)
                    elif: ev.value == 2
                        ui.write(evdev.ecodes.EV_KEY, remapped_code, 2)
                        ui.write(evdev.ecodes.EV_KEY, remapped_code, 0)
                    if ctrl_pressed:
                        ui.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTCTRL, 0)
                    if alt_pressed:
                        ui.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTALT, 0)
                    if shift_pressed:
                        ui.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTSHIFT, 0)
                    if current_layer > 1:
                        ui.write(evdev.ecodes.EV_KEY, remapped_code, 0)
            elif ev.code == evdev.ecodes.KEY_LEFTCTRL and ev.value == 1:
                ctrl_pressed = True
            elif ev.code == evdev.ecodes.KEY_LEFTALT and ev.value == 1:
                alt_pressed = True
            elif ev.code == evdev.ecodes.KEY_LEFTSHIFT and (ev.value == 1 or ev.value == 2):
                shift_pressed = True
            else:
                if ctrl_pressed:
                    ui.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTCTRL, ev.value)
                    if ev.value == 0:
                        ctrl_pressed = False
                if alt_pressed:
                    ui.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTALT, ev.value)
                    if ev.value == 0:
                        alt_pressed = False
                if shift_pressed:
                    ui.write(evdev.ecodes.EV_KEY, evdev.ecodes.KEY_LEFTSHIFT, ev.value)
                    if ev.value == 0:
                        shift_pressed = False
                # Passthrough other key events unmodified.
                ui.write(evdev.ecodes.EV_KEY, ev.code, ev.value)
            # If we just pressed (or held) CapsLock, remember it.
            # Other keys will reset this flag.
            soloing_caps = (ev.code == evdev.ecodes.KEY_CAPSLOCK and ev.value)
        else:
            # Passthrough other events unmodified (e.g. SYNs).
            ui.write(ev.type, ev.code, ev.value)
