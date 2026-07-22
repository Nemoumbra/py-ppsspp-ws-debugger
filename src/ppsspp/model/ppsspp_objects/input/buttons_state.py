from dataclasses import dataclass


@dataclass
class ButtonsState:
    cross: bool
    circle: bool
    triangle: bool
    square: bool
    up: bool
    down: bool
    left: bool
    right: bool
    start: bool
    select: bool
    home: bool
    screen: bool
    note: bool
    ltrigger: bool
    rtrigger: bool
    hold: bool
    wlan: bool
    remote_hold: bool
    vol_up: bool
    vol_down: bool
    disc: bool
    memstick: bool
    forward: bool
    back: bool
    playpause: bool

    # Obscure unmapped keys according to PPSSPP (PPSSPP issue #17464)
    l2: bool
    l3: bool
    r2: bool
    r3: bool
