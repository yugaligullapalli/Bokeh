from random import Random
from decimal import Decimal, localcontext, ROUND_DOWN

rng = Random()

def seed(seed):
    rng.seed(seed)

# def anonymize(x, y, numDecimals = -3):
    # x = dropRandomizedDigits(x, numDecimals) + rng.random() * (10 ** numDecimals)
    # y = dropRandomizedDigits(y, numDecimals) + rng.random() * (10 ** numDecimals)
    # return (x, y)
    
# def dropRandomizedDigits(number, placeToRandomize):
    # print("changing " + str(number) + " at " + str(placeToRandomize))
    # with localcontext() as context:
        # context.rounding = ROUND_DOWN
        # print(context.rounding)
        # exponent = Decimal(str(10 ** placeToRandomize))
        # print(exponent)
        # val = float(Decimal(str(number)).quantize(exponent))
        # print(val)
        # return val

def anonymize(x, y, numDecimals=-3):
    if numDecimals>0 or numDecimals<-6 :
        print("Value of d should be between 0 and -6 ")
        assert(0)
    numToRandomize = 6 + numDecimals
    x = dropRandomizedDigits(x, numDecimals*-1)
    y = dropRandomizedDigits(y, numDecimals*-1)
    for i in range(numToRandomize):
        x += str(rng.randint(0, 9))
        y += str(rng.randint(0, 9))
    return (float(x), float(y))

def dropRandomizedDigits(number, placeToDrop):
    lhs, rhs = str(number).split('.')
    if placeToDrop == 0:
        return lhs + '.'
    return lhs + '.' + rhs[:placeToDrop]
        
