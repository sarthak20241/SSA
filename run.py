import alfano as af
import monteCarlo as mc
import patera as pt
import calculateTcpa as tc


from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from astropy import units as u
import numpy as np
from scipy.optimize import minimize

import velocity_sample as vs

def getPrimaryVelocity(r):
    vsamp=vs.velocity_sample(r,r[1]-100,1)
    return vsamp[0]
def getSecondaryVelocity(r,vel):
    v=None
    
    # vsamp=vs.velocity_sample(coords,500,100)
    # print(vsamp)
    while v is None:
        
        vsamp=vs.velocity_sample(r,r[1]-100,100)
        
        for i in vsamp:
            
            print(i)
            x=i[0]-vel[0]
            y=i[1]-vel[1]
            z=i[2]-vel[2]
            if(x**2+y**2+z**2>5):
                v=i
                break
    
    return v
        


# Initial position and velocity vectors
r0_object1 = np.array([7500, 500, 320]) # in km
v0_object1 = np.array([12, 2, 2]) # in km/s

v0_obj1=getPrimaryVelocity(r0_object1)


# vsamp=vs.velocity_sample(r0_object1,500,100)
# print(vsamp)



deltaR=0.01 # 100 meters
r0_object2 = np.array([7500+deltaR, 500+deltaR, 320+deltaR]) 

v0_obj2= getSecondaryVelocity(r0_object2,v0_object1)

r0_object1 = np.array([7500, 500, 320]) * u.km
v0_object1 = np.array(v0_obj1) * u.km/u.s
s1=10 # radius of satellite

r0_object2 = np.array([7500+deltaR, 500+deltaR, 320+deltaR]) * u.km
v0_object2 = np.array(v0_obj2) * u.km / u.s
s2=1 # radius of debris

# Define initial orbits
orbit_object1 = Orbit.from_vectors(Earth, r0_object1, v0_object1)
orbit_object2 = Orbit.from_vectors(Earth, r0_object2, v0_object2)

tcpa=tc.calculate_tcpa(r0_object1, v0_object1, r0_object2, v0_object2)
print("Time of Closest Approach (TCPA):", tcpa)

# Propagate orbits to TCPA
propagated_object1 = orbit_object1.propagate(tcpa)
propagated_object2 = orbit_object2.propagate(tcpa)
# propagated_object1=orbit_object1
# propagated_object2=orbit_object2

cov_matrix_1=np.diag([0.1, 0.1, 0.1])
cov_matrix_2=np.diag([0.1, 0.1, 0.1])

error_covariance_relative = cov_matrix_1+cov_matrix_2
sigma_x, sigma_y, sigma_z = af.get_standard_deviations(error_covariance_relative) 

miss_vector=propagated_object1.r-propagated_object2.r

v_s=propagated_object1.v/(u.km/u.s)
v_d=propagated_object2.v/(u.km/u.s)
U = pt.calculate_U(v_s, v_d)



print("Miss Vector ",miss_vector)
v_r=propagated_object1.v-propagated_object2.v
print("Relative Velocity",v_r)

# encounter plane - j-k plane
projected_miss_vector=pt.projectOnEncounterPlane(miss_vector,U)
print("Projected Miss Vector",projected_miss_vector)

obj_radius = s1+s2 # radius of combined object


print("\n\n\nResults\n")
#Monte Carlo approach
collision_prob = mc.monte_carlo_collision_probability(propagated_object1, cov_matrix_1, propagated_object2, cov_matrix_2)
print(f"Monte Carlo Probability of Collision: {collision_prob:.4f}")

error_covariance_relative = (cov_matrix_1+cov_matrix_2)*100
sigma_x, sigma_y, sigma_z = af.get_standard_deviations(error_covariance_relative) 

#Alfano Approach

xm = abs(projected_miss_vector[1]*1000/u.km)    # x component or horizontal distance is along the j unit vector of projected
ym = abs(projected_miss_vector[2]*1000 /u.km)   # y component or vertical distance is along the k unit vector of projected
# how to project sigma x and sigma y
collision_prob = af.collision_probability(sigma_x, sigma_y, xm, ym, obj_radius)
print(f"Alfano Collision Probability: {collision_prob}")


# Patera Approach

q=np.array([xm,ym])

a, c, d, e, f, g, alpha, beta, T, qr = pt.calculate_collision_parameters(U, sigma_x, sigma_y, sigma_z, q)
qrs = pt.qrscaleY(qr, alpha, beta)
projected_r1=pt.projectOnEncounterPlane(r0_object1,U)
projected_r2=pt.projectOnEncounterPlane(r0_object2,U)
collision_probability = pt.calculate_collision_probability(alpha, beta, qr, qrs, obj_radius,projected_r1/u.km,projected_r2/u.km)
print("Patera Collision Probability:", collision_probability)
