
import pytest
from photowebpage import image_selection

def test_calculate_aspect():
    w, h = 1920, 1080
    asp_w, asp_h = image_selection._calculate_aspect(w, h)#
    assert asp_w == 16
    assert asp_h == 9

