import numpy as np

# constants
g0 = 9.80665  # gravity [m/s^2]
R = 287.0  # specific gas constant for dry air [J/(kg·K)]
T0 = 288.15  # sea level standard temperature [K]
p0 = 101325  # sea level standard pressure [Pa]

# layer boundaries [m]
layers = [
    {"h": 0,     "a": -0.0065},
    {"h": 11000, "a": 0},
    {"h": 20000, "a": 0.0010},
    {"h": 32000, "a": 0.0028},
    {"h": 47000, "a": 0},
    {"h": 51000, "a": -0.0028},
    {"h": 71000, "a": -0.0020},
    {"h": 86000, "a": None}  # End of model
]

# isa functions
def temperature(T_base, lapse, h, h_base):
    T = T_base + lapse * (h - h_base)
    return T

def pressure_gradient(p_base, T, T_base, lapse):
    p = p_base * (T / T_base) ** (-g0 / (lapse * R))
    return p

def pressure_isothermal(p_base, T, h, h_base):
    p = p_base * np.exp(-g0 * (h - h_base) / (R * T))
    return p

def density(p, T):
    rho = p / (R * T)
    return rho

def isa_layer(h, T_base, p_base, h_base, lapse):
    if lapse == 0:  # isothermal
        p = pressure_isothermal(p_base, T_base, h, h_base)
        T = T_base
    else:
        T = temperature(T_base, lapse, h, h_base)
        p = pressure_gradient(p_base, T, T_base, lapse)
    rho = density(p, T)
    return T, p, rho

# input
print("Choose units for the altitude:")
print("1. Meters")
print("2. Feet")
print("3. Flight Level (FL)")

unit_choice = float(input("Select option: "))
altitude = float(input("Enter altitude: "))

if unit_choice == 2:
    altitude = altitude * 0.3048  # feet to meters
elif unit_choice == 3:
    altitude = altitude * 100 * 0.3048  # FL to meters

# computation

T_base = T0
p_base = p0
h_base = 0

for i in range(len(layers) - 1):
    h_next = layers[i + 1]["h"]
    lapse = layers[i]["a"]

    if altitude <= h_next:
        T, p, rho = isa_layer(altitude, T_base, p_base, h_base, lapse)
        break
    else:
        # Compute top of layer values to use as next base
        T_top, p_top, _ = isa_layer(h_next, T_base, p_base, h_base, lapse)
        T_base = T_top
        p_base = p_top
        h_base = h_next
else:
    print("Altitude exceeds model limit (86,000 m)")
    exit()

# output
print("Temperature:", T, "K")
print("Pressure:", p, "Pa")
print("Density:", rho, "kg/m³")