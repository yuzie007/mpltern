import numpy as np

import pytest
from matplotlib.transforms import IdentityTransform
from mpltern.ternary_axis import TernaryAxis


expected = [
    ["axis", "corner",   0,   0, "center", "bottom"],
    ["axis", "corner",   5,   5, "center", "bottom"],
    ["axis", "corner",  10,  10, "center", "bottom"],
    ["axis", "corner",  15,  15, "center", "bottom"],
    ["axis", "corner",  20,  20, "center", "bottom"],
    ["axis", "corner",  25,  25, "center", "bottom"],
    ["axis", "corner",  30,  30, "center", "bottom"],
    ["axis", "corner",  35,  35, "center", "bottom"],
    ["axis", "corner",  40,  40, "center", "bottom"],
    ["axis", "corner",  45,  45, "center", "bottom"],
    ["axis", "corner",  50,  50, "center", "bottom"],
    ["axis", "corner",  55,  55, "center", "bottom"],
    ["axis", "corner",  60,  60, "center", "bottom"],
    ["axis", "corner",  65,  65, "center", "bottom"],
    ["axis", "corner",  70,  70, "center", "bottom"],
    ["axis", "corner",  75,  75, "center", "bottom"],
    ["axis", "corner",  80,  80, "center", "bottom"],
    ["axis", "corner",  85,  85, "center", "bottom"],
    ["axis", "corner",  90,  90, "center", "bottom"],
    ["axis", "corner",  95, -85, "center", "top"],
    ["axis", "corner", 100, -80, "center", "top"],
    ["axis", "corner", 105, -75, "center", "top"],
    ["axis", "corner", 110, -70, "center", "top"],
    ["axis", "corner", 115, -65, "center", "top"],
    ["axis", "corner", 120, -60, "center", "top"],
    ["axis", "corner", 125, -55, "center", "top"],
    ["axis", "corner", 130, -50, "center", "top"],
    ["axis", "corner", 135, -45, "center", "top"],
    ["axis", "corner", 140, -40, "center", "top"],
    ["axis", "corner", 145, -35, "center", "top"],
    ["axis", "corner", 150, -30, "center", "top"],
    ["axis", "corner", 155, -25, "center", "top"],
    ["axis", "corner", 160, -20, "center", "top"],
    ["axis", "corner", 165, -15, "center", "top"],
    ["axis", "corner", 170, -10, "center", "top"],
    ["axis", "corner", 175,  -5, "center", "top"],
    ["axis", "corner", 180,   0, "center", "top"],
    ["axis", "corner", 185,   5, "center", "top"],
    ["axis", "corner", 190,  10, "center", "top"],
    ["axis", "corner", 195,  15, "center", "top"],
    ["axis", "corner", 200,  20, "center", "top"],
    ["axis", "corner", 205,  25, "center", "top"],
    ["axis", "corner", 210,  30, "center", "top"],
    ["axis", "corner", 215,  35, "center", "top"],
    ["axis", "corner", 220,  40, "center", "top"],
    ["axis", "corner", 225,  45, "center", "top"],
    ["axis", "corner", 230,  50, "center", "top"],
    ["axis", "corner", 235,  55, "center", "top"],
    ["axis", "corner", 240,  60, "center", "top"],
    ["axis", "corner", 245,  65, "center", "top"],
    ["axis", "corner", 250,  70, "center", "top"],
    ["axis", "corner", 255,  75, "center", "top"],
    ["axis", "corner", 260,  80, "center", "top"],
    ["axis", "corner", 265,  85, "center", "top"],
    ["axis", "corner", 270, -90, "center", "bottom"],
    ["axis", "corner", 275, -85, "center", "bottom"],
    ["axis", "corner", 280, -80, "center", "bottom"],
    ["axis", "corner", 285, -75, "center", "bottom"],
    ["axis", "corner", 290, -70, "center", "bottom"],
    ["axis", "corner", 295, -65, "center", "bottom"],
    ["axis", "corner", 300, -60, "center", "bottom"],
    ["axis", "corner", 305, -55, "center", "bottom"],
    ["axis", "corner", 310, -50, "center", "bottom"],
    ["axis", "corner", 315, -45, "center", "bottom"],
    ["axis", "corner", 320, -40, "center", "bottom"],
    ["axis", "corner", 325, -35, "center", "bottom"],
    ["axis", "corner", 330, -30, "center", "bottom"],
    ["axis", "corner", 335, -25, "center", "bottom"],
    ["axis", "corner", 340, -20, "center", "bottom"],
    ["axis", "corner", 345, -15, "center", "bottom"],
    ["axis", "corner", 350, -10, "center", "bottom"],
    ["axis", "corner", 355,  -5, "center", "bottom"],
    ["axis", "tick1",   0, -60, "center", "bottom"],
    ["axis", "tick1",   5, -55, "center", "bottom"],
    ["axis", "tick1",  10, -50, "center", "bottom"],
    ["axis", "tick1",  15, -45, "center", "bottom"],
    ["axis", "tick1",  20, -40, "center", "bottom"],
    ["axis", "tick1",  25, -35, "center", "bottom"],
    ["axis", "tick1",  30, -30, "center", "bottom"],
    ["axis", "tick1",  35, -25, "center", "bottom"],
    ["axis", "tick1",  40, -20, "center", "bottom"],
    ["axis", "tick1",  45, -15, "center", "bottom"],
    ["axis", "tick1",  50, -10, "center", "bottom"],
    ["axis", "tick1",  55,  -5, "center", "bottom"],
    ["axis", "tick1",  60,   0, "center", "bottom"],
    ["axis", "tick1",  65,   5, "center", "bottom"],
    ["axis", "tick1",  70,  10, "center", "bottom"],
    ["axis", "tick1",  75,  15, "center", "bottom"],
    ["axis", "tick1",  80,  20, "center", "bottom"],
    ["axis", "tick1",  85,  25, "center", "bottom"],
    ["axis", "tick1",  90,  30, "center", "bottom"],
    ["axis", "tick1",  95,  35, "center", "bottom"],
    ["axis", "tick1", 100,  40, "center", "bottom"],
    ["axis", "tick1", 105,  45, "center", "bottom"],
    ["axis", "tick1", 110,  50, "center", "bottom"],
    ["axis", "tick1", 115,  55, "center", "bottom"],
    ["axis", "tick1", 120,  60, "center", "bottom"],
    ["axis", "tick1", 125,  65, "center", "bottom"],
    ["axis", "tick1", 130,  70, "center", "bottom"],
    ["axis", "tick1", 135,  75, "center", "bottom"],
    ["axis", "tick1", 140,  80, "center", "bottom"],
    ["axis", "tick1", 145,  85, "center", "bottom"],
    ["axis", "tick1", 150,  90, "center", "bottom"],
    ["axis", "tick1", 155, -85, "center", "top"],
    ["axis", "tick1", 160, -80, "center", "top"],
    ["axis", "tick1", 165, -75, "center", "top"],
    ["axis", "tick1", 170, -70, "center", "top"],
    ["axis", "tick1", 175, -65, "center", "top"],
    ["axis", "tick1", 180, -60, "center", "top"],
    ["axis", "tick1", 185, -55, "center", "top"],
    ["axis", "tick1", 190, -50, "center", "top"],
    ["axis", "tick1", 195, -45, "center", "top"],
    ["axis", "tick1", 200, -40, "center", "top"],
    ["axis", "tick1", 205, -35, "center", "top"],
    ["axis", "tick1", 210, -30, "center", "top"],
    ["axis", "tick1", 215, -25, "center", "top"],
    ["axis", "tick1", 220, -20, "center", "top"],
    ["axis", "tick1", 225, -15, "center", "top"],
    ["axis", "tick1", 230, -10, "center", "top"],
    ["axis", "tick1", 235,  -5, "center", "top"],
    ["axis", "tick1", 240,   0, "center", "top"],
    ["axis", "tick1", 245,   5, "center", "top"],
    ["axis", "tick1", 250,  10, "center", "top"],
    ["axis", "tick1", 255,  15, "center", "top"],
    ["axis", "tick1", 260,  20, "center", "top"],
    ["axis", "tick1", 265,  25, "center", "top"],
    ["axis", "tick1", 270,  30, "center", "top"],
    ["axis", "tick1", 275,  35, "center", "top"],
    ["axis", "tick1", 280,  40, "center", "top"],
    ["axis", "tick1", 285,  45, "center", "top"],
    ["axis", "tick1", 290,  50, "center", "top"],
    ["axis", "tick1", 295,  55, "center", "top"],
    ["axis", "tick1", 300,  60, "center", "top"],
    ["axis", "tick1", 305,  65, "center", "top"],
    ["axis", "tick1", 310,  70, "center", "top"],
    ["axis", "tick1", 315,  75, "center", "top"],
    ["axis", "tick1", 320,  80, "center", "top"],
    ["axis", "tick1", 325,  85, "center", "top"],
    ["axis", "tick1", 330, -90, "center", "bottom"],
    ["axis", "tick1", 335, -85, "center", "bottom"],
    ["axis", "tick1", 340, -80, "center", "bottom"],
    ["axis", "tick1", 345, -75, "center", "bottom"],
    ["axis", "tick1", 350, -70, "center", "bottom"],
    ["axis", "tick1", 355, -65, "center", "bottom"],
    ["axis", "tick2",   0,  60, "center", "bottom"],
    ["axis", "tick2",   5,  65, "center", "bottom"],
    ["axis", "tick2",  10,  70, "center", "bottom"],
    ["axis", "tick2",  15,  75, "center", "bottom"],
    ["axis", "tick2",  20,  80, "center", "bottom"],
    ["axis", "tick2",  25,  85, "center", "bottom"],
    ["axis", "tick2",  30,  90, "center", "bottom"],
    ["axis", "tick2",  35, -85, "center", "top"],
    ["axis", "tick2",  40, -80, "center", "top"],
    ["axis", "tick2",  45, -75, "center", "top"],
    ["axis", "tick2",  50, -70, "center", "top"],
    ["axis", "tick2",  55, -65, "center", "top"],
    ["axis", "tick2",  60, -60, "center", "top"],
    ["axis", "tick2",  65, -55, "center", "top"],
    ["axis", "tick2",  70, -50, "center", "top"],
    ["axis", "tick2",  75, -45, "center", "top"],
    ["axis", "tick2",  80, -40, "center", "top"],
    ["axis", "tick2",  85, -35, "center", "top"],
    ["axis", "tick2",  90, -30, "center", "top"],
    ["axis", "tick2",  95, -25, "center", "top"],
    ["axis", "tick2", 100, -20, "center", "top"],
    ["axis", "tick2", 105, -15, "center", "top"],
    ["axis", "tick2", 110, -10, "center", "top"],
    ["axis", "tick2", 115,  -5, "center", "top"],
    ["axis", "tick2", 120,  -0, "center", "top"],
    ["axis", "tick2", 125,   5, "center", "top"],
    ["axis", "tick2", 130,  10, "center", "top"],
    ["axis", "tick2", 135,  15, "center", "top"],
    ["axis", "tick2", 140,  20, "center", "top"],
    ["axis", "tick2", 145,  25, "center", "top"],
    ["axis", "tick2", 150,  30, "center", "top"],
    ["axis", "tick2", 155,  35, "center", "top"],
    ["axis", "tick2", 160,  40, "center", "top"],
    ["axis", "tick2", 165,  45, "center", "top"],
    ["axis", "tick2", 170,  50, "center", "top"],
    ["axis", "tick2", 175,  55, "center", "top"],
    ["axis", "tick2", 180,  60, "center", "top"],
    ["axis", "tick2", 185,  65, "center", "top"],
    ["axis", "tick2", 190,  70, "center", "top"],
    ["axis", "tick2", 195,  75, "center", "top"],
    ["axis", "tick2", 200,  80, "center", "top"],
    ["axis", "tick2", 205,  85, "center", "top"],
    ["axis", "tick2", 210, -90, "center", "bottom"],
    ["axis", "tick2", 215, -85, "center", "bottom"],
    ["axis", "tick2", 220, -80, "center", "bottom"],
    ["axis", "tick2", 225, -75, "center", "bottom"],
    ["axis", "tick2", 230, -70, "center", "bottom"],
    ["axis", "tick2", 235, -65, "center", "bottom"],
    ["axis", "tick2", 240, -60, "center", "bottom"],
    ["axis", "tick2", 245, -55, "center", "bottom"],
    ["axis", "tick2", 250, -50, "center", "bottom"],
    ["axis", "tick2", 255, -45, "center", "bottom"],
    ["axis", "tick2", 260, -40, "center", "bottom"],
    ["axis", "tick2", 265, -35, "center", "bottom"],
    ["axis", "tick2", 270, -30, "center", "bottom"],
    ["axis", "tick2", 275, -25, "center", "bottom"],
    ["axis", "tick2", 280, -20, "center", "bottom"],
    ["axis", "tick2", 285, -15, "center", "bottom"],
    ["axis", "tick2", 290, -10, "center", "bottom"],
    ["axis", "tick2", 295,  -5, "center", "bottom"],
    ["axis", "tick2", 300,   0, "center", "bottom"],
    ["axis", "tick2", 305,   5, "center", "bottom"],
    ["axis", "tick2", 310,  10, "center", "bottom"],
    ["axis", "tick2", 315,  15, "center", "bottom"],
    ["axis", "tick2", 320,  20, "center", "bottom"],
    ["axis", "tick2", 325,  25, "center", "bottom"],
    ["axis", "tick2", 330,  30, "center", "bottom"],
    ["axis", "tick2", 335,  35, "center", "bottom"],
    ["axis", "tick2", 340,  40, "center", "bottom"],
    ["axis", "tick2", 345,  45, "center", "bottom"],
    ["axis", "tick2", 350,  50, "center", "bottom"],
    ["axis", "tick2", 355,  55, "center", "bottom"],
    ["bottom", "corner",   0,   0, "center", "bottom"],
    ["bottom", "corner",   5,   0, "center", "bottom"],
    ["bottom", "corner",  10,   0, "center", "bottom"],
    ["bottom", "corner",  15,   0, "right", "bottom"],
    ["bottom", "corner",  20,   0, "right", "bottom"],
    ["bottom", "corner",  25,   0, "right", "bottom"],
    ["bottom", "corner",  30,   0, "right", "bottom"],
    ["bottom", "corner",  35,   0, "right", "bottom"],
    ["bottom", "corner",  40,   0, "right", "bottom"],
    ["bottom", "corner",  45,   0, "right", "bottom"],
    ["bottom", "corner",  50,   0, "right", "bottom"],
    ["bottom", "corner",  55,   0, "right", "bottom"],
    ["bottom", "corner",  60,   0, "right", "bottom"],
    ["bottom", "corner",  65,   0, "right", "bottom"],
    ["bottom", "corner",  70,   0, "right", "bottom"],
    ["bottom", "corner",  75,   0, "right", "bottom"],
    ["bottom", "corner",  80,   0, "right", "center"],
    ["bottom", "corner",  85,   0, "right", "center"],
    ["bottom", "corner",  90,   0, "right", "center"],
    ["bottom", "corner",  95,   0, "right", "center"],
    ["bottom", "corner", 100,   0, "right", "center"],
    ["bottom", "corner", 105,   0, "right", "top"],
    ["bottom", "corner", 110,   0, "right", "top"],
    ["bottom", "corner", 115,   0, "right", "top"],
    ["bottom", "corner", 120,   0, "right", "top"],
    ["bottom", "corner", 125,   0, "right", "top"],
    ["bottom", "corner", 130,   0, "right", "top"],
    ["bottom", "corner", 135,   0, "right", "top"],
    ["bottom", "corner", 140,   0, "right", "top"],
    ["bottom", "corner", 145,   0, "right", "top"],
    ["bottom", "corner", 150,   0, "right", "top"],
    ["bottom", "corner", 155,   0, "right", "top"],
    ["bottom", "corner", 160,   0, "right", "top"],
    ["bottom", "corner", 165,   0, "right", "top"],
    ["bottom", "corner", 170,   0, "center", "top"],
    ["bottom", "corner", 175,   0, "center", "top"],
    ["bottom", "corner", 180,   0, "center", "top"],
    ["bottom", "corner", 185,   0, "center", "top"],
    ["bottom", "corner", 190,   0, "center", "top"],
    ["bottom", "corner", 195,   0, "left", "top"],
    ["bottom", "corner", 200,   0, "left", "top"],
    ["bottom", "corner", 205,   0, "left", "top"],
    ["bottom", "corner", 210,   0, "left", "top"],
    ["bottom", "corner", 215,   0, "left", "top"],
    ["bottom", "corner", 220,   0, "left", "top"],
    ["bottom", "corner", 225,   0, "left", "top"],
    ["bottom", "corner", 230,   0, "left", "top"],
    ["bottom", "corner", 235,   0, "left", "top"],
    ["bottom", "corner", 240,   0, "left", "top"],
    ["bottom", "corner", 245,   0, "left", "top"],
    ["bottom", "corner", 250,   0, "left", "top"],
    ["bottom", "corner", 255,   0, "left", "top"],
    ["bottom", "corner", 260,   0, "left", "center"],
    ["bottom", "corner", 265,   0, "left", "center"],
    ["bottom", "corner", 270,   0, "left", "center"],
    ["bottom", "corner", 275,   0, "left", "center"],
    ["bottom", "corner", 280,   0, "left", "center"],
    ["bottom", "corner", 285,   0, "left", "bottom"],
    ["bottom", "corner", 290,   0, "left", "bottom"],
    ["bottom", "corner", 295,   0, "left", "bottom"],
    ["bottom", "corner", 300,   0, "left", "bottom"],
    ["bottom", "corner", 305,   0, "left", "bottom"],
    ["bottom", "corner", 310,   0, "left", "bottom"],
    ["bottom", "corner", 315,   0, "left", "bottom"],
    ["bottom", "corner", 320,   0, "left", "bottom"],
    ["bottom", "corner", 325,   0, "left", "bottom"],
    ["bottom", "corner", 330,   0, "left", "bottom"],
    ["bottom", "corner", 335,   0, "left", "bottom"],
    ["bottom", "corner", 340,   0, "left", "bottom"],
    ["bottom", "corner", 345,   0, "left", "bottom"],
    ["bottom", "corner", 350,   0, "center", "bottom"],
    ["bottom", "corner", 355,   0, "center", "bottom"],
    ["bottom", "tick1",   0,   0, "left", "bottom"],
    ["bottom", "tick1",   5,   0, "left", "bottom"],
    ["bottom", "tick1",  10,   0, "left", "bottom"],
    ["bottom", "tick1",  15,   0, "left", "bottom"],
    ["bottom", "tick1",  20,   0, "left", "bottom"],
    ["bottom", "tick1",  25,   0, "left", "bottom"],
    ["bottom", "tick1",  30,   0, "left", "bottom"],
    ["bottom", "tick1",  35,   0, "left", "bottom"],
    ["bottom", "tick1",  40,   0, "left", "bottom"],
    ["bottom", "tick1",  45,   0, "left", "bottom"],
    ["bottom", "tick1",  50,   0, "center", "bottom"],
    ["bottom", "tick1",  55,   0, "center", "bottom"],
    ["bottom", "tick1",  60,   0, "center", "bottom"],
    ["bottom", "tick1",  65,   0, "center", "bottom"],
    ["bottom", "tick1",  70,   0, "center", "bottom"],
    ["bottom", "tick1",  75,   0, "right", "bottom"],
    ["bottom", "tick1",  80,   0, "right", "bottom"],
    ["bottom", "tick1",  85,   0, "right", "bottom"],
    ["bottom", "tick1",  90,   0, "right", "bottom"],
    ["bottom", "tick1",  95,   0, "right", "bottom"],
    ["bottom", "tick1", 100,   0, "right", "bottom"],
    ["bottom", "tick1", 105,   0, "right", "bottom"],
    ["bottom", "tick1", 110,   0, "right", "bottom"],
    ["bottom", "tick1", 115,   0, "right", "bottom"],
    ["bottom", "tick1", 120,   0, "right", "bottom"],
    ["bottom", "tick1", 125,   0, "right", "bottom"],
    ["bottom", "tick1", 130,   0, "right", "bottom"],
    ["bottom", "tick1", 135,   0, "right", "bottom"],
    ["bottom", "tick1", 140,   0, "right", "center"],
    ["bottom", "tick1", 145,   0, "right", "center"],
    ["bottom", "tick1", 150,   0, "right", "center"],
    ["bottom", "tick1", 155,   0, "right", "center"],
    ["bottom", "tick1", 160,   0, "right", "center"],
    ["bottom", "tick1", 165,   0, "right", "top"],
    ["bottom", "tick1", 170,   0, "right", "top"],
    ["bottom", "tick1", 175,   0, "right", "top"],
    ["bottom", "tick1", 180,   0, "right", "top"],
    ["bottom", "tick1", 185,   0, "right", "top"],
    ["bottom", "tick1", 190,   0, "right", "top"],
    ["bottom", "tick1", 195,   0, "right", "top"],
    ["bottom", "tick1", 200,   0, "right", "top"],
    ["bottom", "tick1", 205,   0, "right", "top"],
    ["bottom", "tick1", 210,   0, "right", "top"],
    ["bottom", "tick1", 215,   0, "right", "top"],
    ["bottom", "tick1", 220,   0, "right", "top"],
    ["bottom", "tick1", 225,   0, "right", "top"],
    ["bottom", "tick1", 230,   0, "center", "top"],
    ["bottom", "tick1", 235,   0, "center", "top"],
    ["bottom", "tick1", 240,   0, "center", "top"],
    ["bottom", "tick1", 245,   0, "center", "top"],
    ["bottom", "tick1", 250,   0, "center", "top"],
    ["bottom", "tick1", 255,   0, "left", "top"],
    ["bottom", "tick1", 260,   0, "left", "top"],
    ["bottom", "tick1", 265,   0, "left", "top"],
    ["bottom", "tick1", 270,   0, "left", "top"],
    ["bottom", "tick1", 275,   0, "left", "top"],
    ["bottom", "tick1", 280,   0, "left", "top"],
    ["bottom", "tick1", 285,   0, "left", "top"],
    ["bottom", "tick1", 290,   0, "left", "top"],
    ["bottom", "tick1", 295,   0, "left", "top"],
    ["bottom", "tick1", 300,   0, "left", "top"],
    ["bottom", "tick1", 305,   0, "left", "top"],
    ["bottom", "tick1", 310,   0, "left", "top"],
    ["bottom", "tick1", 315,   0, "left", "top"],
    ["bottom", "tick1", 320,   0, "left", "center"],
    ["bottom", "tick1", 325,   0, "left", "center"],
    ["bottom", "tick1", 330,   0, "left", "center"],
    ["bottom", "tick1", 335,   0, "left", "center"],
    ["bottom", "tick1", 340,   0, "left", "center"],
    ["bottom", "tick1", 345,   0, "left", "bottom"],
    ["bottom", "tick1", 350,   0, "left", "bottom"],
    ["bottom", "tick1", 355,   0, "left", "bottom"],
    ["bottom", "tick2",   0,   0, "right", "bottom"],
    ["bottom", "tick2",   5,   0, "right", "bottom"],
    ["bottom", "tick2",  10,   0, "right", "bottom"],
    ["bottom", "tick2",  15,   0, "right", "bottom"],
    ["bottom", "tick2",  20,   0, "right", "center"],
    ["bottom", "tick2",  25,   0, "right", "center"],
    ["bottom", "tick2",  30,   0, "right", "center"],
    ["bottom", "tick2",  35,   0, "right", "center"],
    ["bottom", "tick2",  40,   0, "right", "center"],
    ["bottom", "tick2",  45,   0, "right", "top"],
    ["bottom", "tick2",  50,   0, "right", "top"],
    ["bottom", "tick2",  55,   0, "right", "top"],
    ["bottom", "tick2",  60,   0, "right", "top"],
    ["bottom", "tick2",  65,   0, "right", "top"],
    ["bottom", "tick2",  70,   0, "right", "top"],
    ["bottom", "tick2",  75,   0, "right", "top"],
    ["bottom", "tick2",  80,   0, "right", "top"],
    ["bottom", "tick2",  85,   0, "right", "top"],
    ["bottom", "tick2",  90,   0, "right", "top"],
    ["bottom", "tick2",  95,   0, "right", "top"],
    ["bottom", "tick2", 100,   0, "right", "top"],
    ["bottom", "tick2", 105,   0, "right", "top"],
    ["bottom", "tick2", 110,   0, "center", "top"],
    ["bottom", "tick2", 115,   0, "center", "top"],
    ["bottom", "tick2", 120,   0, "center", "top"],
    ["bottom", "tick2", 125,   0, "center", "top"],
    ["bottom", "tick2", 130,   0, "center", "top"],
    ["bottom", "tick2", 135,   0, "left", "top"],
    ["bottom", "tick2", 140,   0, "left", "top"],
    ["bottom", "tick2", 145,   0, "left", "top"],
    ["bottom", "tick2", 150,   0, "left", "top"],
    ["bottom", "tick2", 155,   0, "left", "top"],
    ["bottom", "tick2", 160,   0, "left", "top"],
    ["bottom", "tick2", 165,   0, "left", "top"],
    ["bottom", "tick2", 170,   0, "left", "top"],
    ["bottom", "tick2", 175,   0, "left", "top"],
    ["bottom", "tick2", 180,   0, "left", "top"],
    ["bottom", "tick2", 185,   0, "left", "top"],
    ["bottom", "tick2", 190,   0, "left", "top"],
    ["bottom", "tick2", 195,   0, "left", "top"],
    ["bottom", "tick2", 200,   0, "left", "center"],
    ["bottom", "tick2", 205,   0, "left", "center"],
    ["bottom", "tick2", 210,   0, "left", "center"],
    ["bottom", "tick2", 215,   0, "left", "center"],
    ["bottom", "tick2", 220,   0, "left", "center"],
    ["bottom", "tick2", 225,   0, "left", "bottom"],
    ["bottom", "tick2", 230,   0, "left", "bottom"],
    ["bottom", "tick2", 235,   0, "left", "bottom"],
    ["bottom", "tick2", 240,   0, "left", "bottom"],
    ["bottom", "tick2", 245,   0, "left", "bottom"],
    ["bottom", "tick2", 250,   0, "left", "bottom"],
    ["bottom", "tick2", 255,   0, "left", "bottom"],
    ["bottom", "tick2", 260,   0, "left", "bottom"],
    ["bottom", "tick2", 265,   0, "left", "bottom"],
    ["bottom", "tick2", 270,   0, "left", "bottom"],
    ["bottom", "tick2", 275,   0, "left", "bottom"],
    ["bottom", "tick2", 280,   0, "left", "bottom"],
    ["bottom", "tick2", 285,   0, "left", "bottom"],
    ["bottom", "tick2", 290,   0, "center", "bottom"],
    ["bottom", "tick2", 295,   0, "center", "bottom"],
    ["bottom", "tick2", 300,   0, "center", "bottom"],
    ["bottom", "tick2", 305,   0, "center", "bottom"],
    ["bottom", "tick2", 310,   0, "center", "bottom"],
    ["bottom", "tick2", 315,   0, "right", "bottom"],
    ["bottom", "tick2", 320,   0, "right", "bottom"],
    ["bottom", "tick2", 325,   0, "right", "bottom"],
    ["bottom", "tick2", 330,   0, "right", "bottom"],
    ["bottom", "tick2", 335,   0, "right", "bottom"],
    ["bottom", "tick2", 340,   0, "right", "bottom"],
    ["bottom", "tick2", 345,   0, "right", "bottom"],
    ["bottom", "tick2", 350,   0, "right", "bottom"],
    ["bottom", "tick2", 355,   0, "right", "bottom"],
]


class DummyAxes:
    corners = None
    _labelrotation = None


class DummyTernaryAxis:
    axis_name = 't'
    axes = DummyAxes


def _create_axis(rotation):
    from scipy.special import cosdg, sindg
    corners = np.array([
        (0.5, 1.0),
        (0.5 - 1.0 / np.sqrt(3.0), 0.0),
        (0.5 + 1.0 / np.sqrt(3.0), 0.0),
    ])
    rotation_matrix = ([
        [cosdg(rotation), -sindg(rotation)],
        [sindg(rotation),  cosdg(rotation)],
    ])
    self = DummyTernaryAxis()
    self.axes.corners = np.dot(rotation_matrix, corners.T).T
    self.axes.transAxes = IdentityTransform()
    self._label_rotation_mode = 'axis'
    return self


@pytest.mark.parametrize(
    'mode,label_position,rotation,label_rotation_ref,ha_ref,va_ref', expected)
def test_get_label_position(mode, label_position, rotation, label_rotation_ref,
                            ha_ref, va_ref):
    self = _create_axis(rotation)
    self.label_position = label_position
    self._label_rotation_mode = mode
    label_rotation, ha, va = TernaryAxis._get_label_rotation(self)
    assert (np.isclose(label_rotation, label_rotation_ref) and
            ha == ha_ref and va == va_ref)


def _create_references():
    for mode in ['axis', 'bottom']:
        for position in ['corner', 'tick1', 'tick2']:
            for rotation in range(0, 360, 5):
                self = _create_axis(rotation)
                self.label_position = position
                self._label_rotation_mode = mode
                label_rotation, ha, va = TernaryAxis._get_label_rotation(self)
                print('    ["{:s}", "{:s}", {:3.0f}, {:3.0f}, "{:s}", "{:s}"],'.format(
                    mode, position, rotation, label_rotation, ha, va))


if __name__ == '__main__':
    _create_references()
