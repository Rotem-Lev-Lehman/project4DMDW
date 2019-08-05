def calculateMestimate(p,nc,n):
    m = 2  # constant in this program
    numerator = nc + m*p
    denominator = n + m
    mestimate = float(numerator)/denominator
    return mestimate
