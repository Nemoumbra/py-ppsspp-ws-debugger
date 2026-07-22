from dataclasses import dataclass
from enum import StrEnum


@dataclass
class RegisterCategory:
    id: int
    name: str
    register_names: list[str]
    uint_values: list[int]
    float_values: list[str]


class GPR(StrEnum):
    zero = "zero"
    at = "at"

    # Return values
    v0 = "v0"
    v1 = "v1"

    # a0-a3 (arg regs)
    a0 = "a0"
    a1 = "a1"
    a2 = "a2"
    a3 = "a3"

    # t0-t7 (temp regs)
    t0 = "t0"
    t1 = "t1"
    t2 = "t2"
    t3 = "t3"
    t4 = "t4"
    t5 = "t5"
    t6 = "t6"
    t7 = "t7"

    # s0-s7 (saved regs)
    s0 = "s0"
    s1 = "s1"
    s2 = "s2"
    s3 = "s3"
    s4 = "s4"
    s5 = "s5"
    s6 = "s6"
    s7 = "s7"

    # t8-t9 (temp regs)
    t8 = "t8"
    t9 = "t9"

    # kernel
    k0 = "k0"
    k1 = "k1"

    # special
    gp = "gp"
    sp = "sp"
    fp = "fp"
    ra = "ra"
    pc = "pc"

    # Mult/div registers
    hi = "hi"
    lo = "lo"


# Could've been called FPR, but alas, that's what's displayed in PPSSPP's Windows debugger
class FPU(StrEnum):
    f0 = "f0"
    f1 = "f1"
    f2 = "f2"
    f3 = "f3"
    f4 = "f4"
    f5 = "f5"
    f6 = "f6"
    f7 = "f7"
    f8 = "f8"
    f9 = "f9"
    f10 = "f10"
    f11 = "f11"
    f12 = "f12"
    f13 = "f13"
    f14 = "f14"
    f15 = "f15"
    f16 = "f16"
    f17 = "f17"
    f18 = "f18"
    f19 = "f19"
    f20 = "f20"
    f21 = "f21"
    f22 = "f22"
    f23 = "f23"
    f24 = "f24"
    f25 = "f25"
    f26 = "f26"
    f27 = "f27"
    f28 = "f28"
    f29 = "f29"
    f30 = "f30"
    f31 = "f31"

# No VFPU, this is too much
