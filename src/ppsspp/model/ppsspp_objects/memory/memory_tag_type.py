from enum import StrEnum


class MemoryTagType(StrEnum):
    write = "write"
    texture = "texture"
    alloc = "alloc"
    suballoc = "suballoc"
    free = "free"
    subfree = "subfree"
