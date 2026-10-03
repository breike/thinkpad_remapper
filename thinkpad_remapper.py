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
import sys
# You need to install evdev with a package manager or pip3.
import evdev  # (sudo pip3 install evdev)

# making layered layout...
current_layer = 1

# Keys that switch to a layer while held: holding the layering key
# selects the corresponding layer, releasing it falls back to layer 1.
# Space -> layer 2 (page/nav), Compose -> layer 3 (media/launch).
layering_keys = {evdev.ecodes.KEY_SPACE: 2, evdev.ecodes.KEY_COMPOSE: 3}

# If True, one-shot modifiers (layer-2 CapsLock -> Ctrl, Tab -> Alt) act
# like sticky keys: releasing the source key keeps the modifier armed, so
# the next key pressed still gets paired with it. If False, the source key
# must be held until the next key is pressed.
STICKY_MODIFIERS = True

# shift mode
shift_pressed = False

# Define an example dictionary describing the remaps.
REMAP_TABLE = {
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
        2: evdev.ecodes.KEY_F13,
        3: evdev.ecodes.KEY_TAB     # Compose-held: Tab
    },
    evdev.ecodes.KEY_W: {
        1: evdev.ecodes.KEY_W,
        2: evdev.ecodes.KEY_F15
    },
    evdev.ecodes.KEY_E: {
        1: evdev.ecodes.KEY_E,
        2: evdev.ecodes.KEY_UP,
        3: evdev.ecodes.KEY_MEDIA,   # Compose-held: XF86Go
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
        2: evdev.ecodes.KEY_F14
    },
    evdev.ecodes.KEY_S: {
        1: evdev.ecodes.KEY_S,
        2: evdev.ecodes.KEY_LEFT,
        3: evdev.ecodes.KEY_KPRIGHTPAREN,   # Compose-held: XF86HomePage (I180)
    },
    evdev.ecodes.KEY_D: {
        1: evdev.ecodes.KEY_D,
        2: evdev.ecodes.KEY_DOWN,
        3: evdev.ecodes.KEY_EXIT,   # Compose-held: XF86AudioStop (I174)
    },
    evdev.ecodes.KEY_F: {
        1: evdev.ecodes.KEY_F,
        2: evdev.ecodes.KEY_RIGHT,
        3: evdev.ecodes.KEY_SEARCH,  # Compose-held: XF86Search
    },
    evdev.ecodes.KEY_G: {
        1: evdev.ecodes.KEY_G,
        2: evdev.ecodes.KEY_BOOKMARKS
    },
    evdev.ecodes.KEY_B: {
        1: evdev.ecodes.KEY_B,
        2: evdev.ecodes.KEY_REDO
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
        2: evdev.ecodes.KEY_FORWARD
    },
    evdev.ecodes.KEY_Z: {
        1: evdev.ecodes.KEY_Z,
        2: evdev.ecodes.KEY_EJECTCD
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


def find_target_keyboard():
    """Find the first device whose name contains MATCH."""
    for fn in evdev.list_devices():
        try:
            device = evdev.InputDevice(fn)
        except OSError:
            continue  # device disappeared in the meantime
        if device.name and MATCH in device.name:
            return device
        device.close()
    sys.exit(f"error: no input device name contains {MATCH!r}")


kbd = find_target_keyboard()
atexit.register(kbd.ungrab)  # Don't forget to ungrab the keyboard on exit!
kbd.grab()  # Grab, i.e. prevent the keyboard from emitting original events.

# Layer each key was pressed in. On release the remapped key is looked up
# in this layer, not in the layer at the moment of release: keys can be
# released in any order, and releasing the layering key first must not
# change what a still-held key emits on release.
key_layers = {}

# One-shot ctrl/alt modes: a key remapped onto a modifier (e.g. layer-2
# CapsLock -> Ctrl, Tab -> Alt) is swallowed while held, and the modifier
# is injected together with the very next key pressed instead. States:
#   idle  - nothing pending
#   armed - modifier swallowed, waiting to be paired with the next key
#   <int> - modifier was injected paired with the key of this code; that
#           key's release also releases the modifier
mod_tracker = {
    evdev.ecodes.KEY_LEFTCTRL: "idle",
    evdev.ecodes.KEY_LEFTALT: "idle",
}


def inject(ui, types):
    """Inject the given (type, code, value) events, then sync the batch."""
    for ev_type, code, value in types:
        ui.write(ev_type, code, value)
    ui.syn()


def flush_modifier(ui, code, value):
    """Pair an armed one-shot modifier with this key press, if any.

    Returns True when the key was injected as part of the pair and the
    caller must not inject it again.
    """
    if value == 0:
        # Release closes the pair: the key, then its modifier.
        for mod in (evdev.ecodes.KEY_LEFTCTRL, evdev.ecodes.KEY_LEFTALT):
            if mod_tracker[mod] == code:
                inject(ui, [(evdev.ecodes.EV_KEY, code, 0),
                            (evdev.ecodes.EV_KEY, mod, 0)])
                mod_tracker[mod] = "idle"
                return True
        return False
    if value != 1:
        return False
    for mod in (evdev.ecodes.KEY_LEFTCTRL, evdev.ecodes.KEY_LEFTALT):
        if mod_tracker[mod] == "armed":
            inject(ui, [(evdev.ecodes.EV_KEY, mod, 1),
                        (evdev.ecodes.EV_KEY, code, 1)])
            mod_tracker[mod] = code  # which key must release it
            return True
    return False


def handle_event(ui, ev):
    """Process one event from the grabbed keyboard, emitting into `ui`.

    Returns False when the main loop should exit (PAUSE pressed).
    """
    global current_layer, key_layers, mod_tracker
    # Passthrough other events unmodified (e.g. SYNs).
    if ev.type != evdev.ecodes.EV_KEY:
        inject(ui, [(ev.type, ev.code, ev.value)])
        return True

    # Exit on pressing PAUSE. Useful if that is your only keyboard. =)
    # Also if you bind that script to PAUSE, it'll be a toggle.
    if ev.code == evdev.ecodes.KEY_PAUSE and ev.value == 1:
        return False

    # A layering key switches the layer while held and is swallowed,
    # including its auto-repeat, so holding it never leaks keys.
    if ev.code in layering_keys:
        if ev.value == 1:
            current_layer = layering_keys[ev.code]
        elif ev.value == 0:
            current_layer = 1
        return True

    if ev.code in REMAP_TABLE:
        # Remember the layer this key was pressed in.
        if ev.value == 1:
            key_layers[ev.code] = current_layer
        layer = key_layers.get(ev.code, 1)
        remapped_code = REMAP_TABLE[ev.code][layer]
        if remapped_code in mod_tracker:
            if ev.value == 1:
                # Swallow the modifier keypress; it will be injected
                # together with the next key.
                mod_tracker[remapped_code] = "armed"
            elif ev.value == 0:
                # Tapped on its own or already released with its paired
                # key: nothing arrives here to release.
                if not STICKY_MODIFIERS:
                    mod_tracker[remapped_code] = "idle"
            # Auto-repeat: a virtual modifier key has no repeats.
        elif ev.value == 2:
            # Forward the repeat so autorepeat keeps working.
            inject(ui, [(evdev.ecodes.EV_KEY, remapped_code, 2)])
        elif flush_modifier(ui, remapped_code, ev.value):
            pass  # this key went out paired with a one-shot modifier
        else:
            inject(ui, [(evdev.ecodes.EV_KEY, remapped_code, ev.value)])
        if ev.value == 0:
            key_layers.pop(ev.code, None)
    elif ev.code in (evdev.ecodes.KEY_LEFTCTRL, evdev.ecodes.KEY_LEFTALT):
        # A real modifier key cancels an armed one-shot of itself,
        # so pressing Ctrl manually means plain Ctrl.
        if mod_tracker[ev.code] == "armed":
            mod_tracker[ev.code] = "idle"
        inject(ui, [(evdev.ecodes.EV_KEY, ev.code, ev.value)])
    elif flush_modifier(ui, ev.code, ev.value):
        pass  # passthrough key went out paired with a one-shot modifier
    else:
        # Passthrough other key events unmodified.
        inject(ui, [(evdev.ecodes.EV_KEY, ev.code, ev.value)])
    return True


# Create a new keyboard mimicking the original one.
with evdev.UInput.from_device(kbd, name='kbdremap') as ui:
    print(f"remapping {kbd.name} as kbdremap; press PAUSE to quit")
    for ev in kbd.read_loop():
        if not handle_event(ui, ev):
            break
