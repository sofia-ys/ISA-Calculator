import numpy as np

# constants
g0 = 9.80665
R = 287
T0 = 288.15
p0 = 101325
a1 = -0.0065
a3 = 0.0010
a4 = 0.0028
a6 = -0.0028
a7 = -0.0020
h0 = 0
h1 = 11000
h2 = 20000
h3 = 32000
h4 = 47000
h5 = 51000
h6 = 71000
h7 = 86000

# temperature function
def temperature(T0, a, h1, h0):
    T = T0 + a * (h1 - h0)
    return T

# gradient pressure function
def pressure(p0, T1, T0, a):
    p1 = p0 * (T1 / T0)**(-g0 / (a * R))
    return p1

# gradient density function
def density(p1, T1):
    rho1 = p1 / (R * T1)
    return rho1

# isothermal functions
def isothermal(T, h1, h0, p0, rho0):
    p1 = p0 * np.e**((- g0 / (R * T)) * (h1 - h0))
    rho1 = rho0 * np.e**((- g0 / (R * T)) * (h1 - h0))
    return p1, rho1

# response function
def response(T, p, rho):
    print("Temperature:", T, "K")
    print("Pressure:", p, "Pa")
    print("Density:", rho, "kg/m^3")

# prompt
print("Choose units for the altitude")
print("1. Calculate ISA for altitude in meters")
print("2. Calculate ISA for altitude in feet")
print("3. Calculate ISA for altitude in FL")

n = float(input("Select option: "))
h = float(input("Enter altitude: "))

if n == 2:
    h = h*0.3048  # converting from feet
elif n == 3:
    h = h*100*0.3048  # converting from FL
else:
    h = h

status = True
while status:

    # troposphere
    T = max(temperature(T0, a1, h, h0), temperature(T0, a1, h1, h0))  # T decreases over troposphere
    p = pressure(p0, T, T0, a1)
    rho = density(p, T)
    if h0 <= h <= h1:
        response(T, p, rho)
        status = False
    
    # tropopause
    p, rho = max(isothermal(T, h, h1, p, rho), isothermal(T, h2, h1, p, rho))
    if h1 < h <= h2: 
        response(T, p, rho)
        status = False
    
    #stratosphere 1 
    T0 = T
    T = min(temperature(T0, a3, h, h2), temperature(T0, a3, h3, h2))  # T increases over stratosphere
    p = pressure(p, T, T0, a3)
    rho = density(p, T)
    if h2 < h <= h3:
        response(T, p, rho)
        status = False

    #stratosphere 2
    T0 = T
    T = min(temperature(T0, a4, h, h3), temperature(T0, a4, h4, h3))  # T increases over stratosphere
    p = pressure(p, T, T0, a4)
    rho = density(p, T)
    if h3 < h <= h4:
        response(T, p, rho)
        status = False

    #stratopause
    p, rho = max(isothermal(T, h, h4, p, rho), isothermal(T, h5, h4, p, rho))
    if h4 < h <= h5:
        response(T, p, rho)
        status = False

    #mesosphere 1
    T0 = T
    T = max(temperature(T0, a6, h, h5), temperature(T0, a6, h6, h5))  # T decreases over mesosphere
    p = pressure(p, T, T0, a6)
    rho = density(p, T)
    if h5 < h <= h6:
        response(T, p, rho)
        status = False

    #mesosphere 2
    T0 = T
    T = max(temperature(T0, a7, h, h6), temperature(T0, a7, h7, h6))  # T decreases over mesosphere
    p = pressure(p, T, T0, a7)
    rho = density(p, T)
    if h6 < h <= h7:
        response(T, p, rho)
        status = False