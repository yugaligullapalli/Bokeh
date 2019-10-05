from decimal import Decimal, localcontext, ROUND_DOWN

def _truncate(number, places):
    with localcontext() as context:
        context.rounding = ROUND_DOWN
        exponent = Decimal(str(10 ** - places))
        return float(Decimal(str(number)).quantize(exponent))


def seed(seed):
    pass

def anonymize(x, y, numDecimals = 0):
    x = _truncate(x, numDecimals)
    y = _truncate(y, numDecimals)
    return (x, y)
