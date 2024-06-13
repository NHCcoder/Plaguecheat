from ctypes import Structure, c_float, c_uint64


class Vec3(Structure):
    _fields_ = [("x", c_float), ("y", c_float), ("z", c_float)]


class Vec2(Structure):
    _fields_ = [("x", c_float), ("y", c_float)]


class C_UTL_VECTOR(Structure):
    _fields_ = [("Count", c_uint64), ("Data", c_uint64)]


class Offsets:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __getattr__(self, item):
        raise AttributeError(f"'Offsets' object has no attribute '{item}'")
    
    def add_offsets(self, offsets_dict):
        for key, value in offsets_dict.items():
            setattr(self, key, value)
