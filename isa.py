#libraries
import math

#prompt
print("Choose units for the altitude")
print("1. Calculate ISA for altitude in meters")
print("2. Calculate ISA for altitude in feet")
print("3. Calculate ISA for altitude in FL")

n = float(input("Select option: "))
h = float(input("Enter altitude: "))

if n == 2:
    h = h*0.3048
elif n == 3:
    h = h*100*0.3048
else:
    h = h

#constants
g0 = 9.80665
R = 287.0
T0 = 288.15
p0 = 101325.0
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

#layer constants
p = 0
q = 0
Tfinal = 0
T1end = T0 + a1*h1
T2end = T1end
T3end = T2end + a3*(h3-h2)
T4end = T3end + a4*(h4-h3)
T5end = T4end
T6end = T5end + a6*(h6-h5)
T7end = T6end + a7*(h7-h6)
p1 = p0*(T1end/T0)**((-g0)/(R*a1))
p2 = p1*math.exp((-g0*(h2-h1))/(R*T2end))
p3 = p2*(T3end/T2end)**((-g0)/(R*a3))
p4 = p3*(T4end/T3end)**((-g0)/(R*a4))
p5 = p4*math.exp((-g0*(h5-h4))/(R*T5end))
p6 = p5*(T6end/T5end)**((-g0)/(R*a6))

#troposphere
if h0 < h <= h1:
    T1 = T0 + a1*h
    Tfinal = T1
    p = p0*(T1/T0)**((-g0)/(R*a1))
    q = p/(R*T1)

#tropopause
elif h1 < h <= h2: 
    T2 = T2end
    Tfinal = T2
    p = p1*math.exp((-g0*(h-h1))/(R*T2))
    q = p/(R*T2)

#stratosphere 1
elif h2 < h <= h3:
    T3 = T2end + a3*(h-h2)
    Tfinal = T3
    p = p2*(T3/T2end)**((-g0)/(R*a3))
    q = p/(R*T3)

#stratosphere 2
elif h3 < h <= h4:
    T4 = T3end + a4*(h-h3)
    Tfinal = T4
    p = p3*(T4/T3end)**((-g0)/(R*a4))
    q = p/(R*T4)

#stratopause
elif h4 < h <= h5:
    T5 = T4end
    Tfinal = T5
    p = p4*math.exp((-g0*(h-h4))/(R*T5))
    q = p/(R*T5)

#mesosphere 1
elif h5 < h <= h6:
    T6 = T5end + a6*(h-h5)
    Tfinal = T6
    p = p5*(T6/T5end)**((-g0)/(R*a6))
    q = p/(R*T6)

#mesosphere 2
elif h6 < h <= h7:
    T7 = T6end + a7*(h-h6)
    Tfinal = T7
    p = p6*(T7/T6end)**((-g0)/(R*a7))
    q = p/(R*T7)

print("Temperature:", Tfinal, "K")
print("Pressure:", p, "Pa")
print("Density:", q, "kg/m^3")