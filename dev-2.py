from functools import reduce
from operator import add
from maa.define import Rect

def is_in_rect(r: Rect):
    def _is_in_rect(r1: Rect) -> bool:
        return max(r1.x, r1.x + r1.w) <= max(r.x, r.x + r.w) and min(r1.x, r1.x + r1.w) >= min(r.x, r.x + r.w) and\
              max(r1.y, r1.y + r1.h) <= max(r.y, r.y + r.h) and min(r1.y, r1.y + r1.h) >= min(r.y, r.y + r.h)
    return _is_in_rect

if __name__ == "__main__":
    r1 = Rect(100,120,200,220)
    for n in range(5):
        rt = (r1,) * n
        print(rt)
        print("Sum1: ", reduce(add, rt, Rect()))
        print("Sum2: ", sum(rt, Rect()))
    r2 = Rect(110,120,20,20)
    r3 = Rect(99,120,200,220)
    print(is_in_rect(r1)(r2))
    print(is_in_rect(r1)(r3))