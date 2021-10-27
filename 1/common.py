import math


def expectation(values):
    return sum(values) / len(values)


def dispersion(values, expectation_by_values):
    values_sum = 0
    for value in values:
        values_sum += value ** 2 - expectation_by_values ** 2
    return values_sum / len(values)


def correlation_coefficient(x, y):
    xy = [x_i * y_i for x_i, y_i in zip(x, y)]
    m_xy = expectation(xy)
    m_x = expectation(x)
    m_y = expectation(y)

    r = (m_xy - m_x * m_y) / math.sqrt(dispersion(x, m_x) * dispersion(y, m_y))
    return r


def get_m_interval(values):
    z = 1.96
    n = len(values)
    exp = expectation(values)
    disp = dispersion(values, exp)
    left = exp - z * disp / n ** 0.5
    right = exp + z * disp / n ** 0.5

    return left, right
