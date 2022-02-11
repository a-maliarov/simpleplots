from simpleplots import Figure
from simpleplots.utils import frange
import math

def quarter_circle(position):
    xvalues = [v for v in frange(0, 1, 0.001)]
    yvalues = [round(math.sqrt(1 - v ** 2), 3) for v in xvalues]

    if position == 'bottom_right':
        return [(x, -y) for x, y in zip(xvalues, yvalues)]
    elif position == 'top_right':
        return [(x, y) for x, y in zip(xvalues, yvalues)]
    elif position == 'bottom_left':
        return [(-x, -y) for x, y in zip(xvalues, yvalues)]
    elif position == 'top_left':
        return [(-x, y) for x, y in zip(xvalues, yvalues)]

def half_circle(position):
    if position == 'right':
        bottom_right = quarter_circle('bottom_right')
        top_right = list(reversed(quarter_circle('top_right')))
        return bottom_right + top_right

    elif position == 'top':
        top_right = list(reversed(quarter_circle('top_right')))
        top_left = quarter_circle('top_left')
        return top_right + top_left

    elif position == 'bottom':
        bottom_right = list(reversed(quarter_circle('bottom_right')))
        bottom_left = quarter_circle('bottom_left')
        return bottom_right + bottom_left

    elif position == 'left':
        bottom_left = quarter_circle('bottom_left')
        top_left = list(reversed(quarter_circle('top_left')))
        return bottom_left + top_left

def letter_s(x, y):
    bl_qc = [(t[0] + x + 1, t[1] + y + 1) for t in quarter_circle('bottom_left')]
    r_hc = [(t[0] + x + 1, t[1] + y + 1) for t in half_circle('right')]
    l_hc = [(t[0] + x + 1, t[1] + y + 3) for t in half_circle('left')]
    tr_qc = [(t[0] + x + 1, t[1] + y + 3) for t in quarter_circle('top_right')]
    return list(reversed(bl_qc)) + r_hc + l_hc + tr_qc

def letter_i(x, y):
    return [(x, y), (x, y + 4)]

def letter_m(x, y):
    l_vl = [(x, y), (x, y + 4)]
    l_dl = [(x, y + 4), (x + 1, y + 2)]
    r_dl = [(x + 1, y + 2), (x + 2, y + 4)]
    r_vl = [(x + 2, y + 4), (x + 2, y)]
    return l_vl + l_dl + r_dl + r_vl

def letter_p(x, y):
    l_vl = [(x, y), (x, y + 4)]
    t_hl = [(x, y + 4), (x + 0.5, y + 4)]
    r_hc = [(t[0] + x + 0.5, t[1] + y + 3) for t in half_circle('right')]
    m_hl = [(x + 0.5, y + 2), (x, y + 2)]
    return l_vl + t_hl + list(reversed(r_hc)) + m_hl

def letter_l(x, y):
    l_vl = [(x, y + 4), (x, y)]
    b_hl = [(x, y), (x + 1.5, y)]
    return l_vl + b_hl

def letter_e(x, y):
    l_vl = [(x, y), (x, y + 4)]
    t_hl = [(x, y + 4), (x + 1.5, y + 4), (x, y + 4)]
    m_hl = [(x, y + 2), (x + 1.5, y + 2), (x, y + 2)]
    b_hl = [(x, y), (x + 1.5, y), (x, y)]
    return l_vl + t_hl + m_hl + b_hl

def letter_o(x, y):
    bl_qc = [(t[0] + x + 1, t[1] + y + 1) for t in quarter_circle('bottom_left')]
    l_vl = [(x, y + 2), (x, y + 3)]
    tl_qc = [(t[0] + x + 1, t[1] + y + 3) for t in quarter_circle('top_left')]
    tr_qc = [(t[0] + x + 1, t[1] + y + 3) for t in quarter_circle('top_right')]
    r_vl = [(x + 2, y + 3), (x + 2, y + 1)]
    br_qc = [(t[0] + x + 1, t[1] + y + 1) for t in quarter_circle('bottom_right')]
    return bl_qc + l_vl + list(reversed(tl_qc)) + tr_qc + r_vl + list(reversed(br_qc))

def letter_t(x, y):
    m_vl = [(x + 1, y), (x + 1, y + 4)]
    t_hl = [(x, y + 4), (x + 2, y + 4)]
    return m_vl + t_hl

letters = [
    letter_s(0, 6),
    letter_i(3, 6),
    letter_m(4, 6),
    letter_p(7, 6),
    letter_l(9.5, 6),
    letter_e(12, 6),
    letter_p(5, 1),
    letter_l(7.5, 1),
    letter_o(10, 1),
    letter_t(13, 1),
    letter_s(16, 1)
]

fig = Figure(size=(1920, 1080))

for letter in letters:
    xvalues = [round(v[0], 3) for v in letter]
    yvalues = [round(v[1], 3) for v in letter]
    fig.plot(xvalues, yvalues, color='red', linewidth=10)

# fig.show()
fig.save('logo.png')
