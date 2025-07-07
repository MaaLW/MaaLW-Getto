from ..maafw import Rect

def is_in_rect(r: Rect):
    """
    Returns a function that checks if a given rectangle `r1` is completely
    within the boundaries of rectangle `r`.

    Parameters:
    - r: The reference rectangle within which the check is performed.

    Returns:
    - A function that takes a rectangle `r1` and returns True if `r1` is
      entirely within `r`, otherwise False.
    """

    def _is_in_rect(r1: Rect) -> bool:
        return max(r1.x, r1.x + r1.w) <= max(r.x, r.x + r.w) and min(r1.x, r1.x + r1.w) >= min(r.x, r.x + r.w) and\
              max(r1.y, r1.y + r1.h) <= max(r.y, r.y + r.h) and min(r1.y, r1.y + r1.h) >= min(r.y, r.y + r.h)
    return _is_in_rect