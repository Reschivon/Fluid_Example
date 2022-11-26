import math
import random
import sys
from typing import List

import matplotlib.pyplot as plot
import matplotlib.pyplot as plt

# Constants
NUM_PARTICLES = 500
DT = 0.5
GRAVITY_FORCE = -1
WORLD_WIDTH_PIXELS = 128
WORLD_HEIGHT_PIXELS = 128
BOUNDARY_REP_WIDTH = 3
MIN_DISTANCE = 0.1
MAX_DISTANCE = 5
MAX_VEL = 23

MAX_DISTANCE_VISC = 20
VISCOSITY = 0.01

class Particle:
    def __init__(self, x_pos: float, y_pos: float):
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.x_vel = 0.0
        self.y_vel = 0.0

        self.next_force_x = 0.0
        self.next_force_y = 0.0


# Interactive Mode (Allow plots to be updated)
plot.ion()
# Allows the X button to work. Don't worry about how this works exactly unless you are interested
plot.gcf().canvas.mpl_connect('close_event', lambda event: sys.exit())

def draw(particles: List[Particle]):
    x_positions = [particle.x_pos for particle in particles]
    y_positions = [particle.y_pos for particle in particles]

    # Clear the plot
    plot.cla()
    # Draw each particle according to x_position and y_positions
    plot.scatter(x_positions, y_positions,
                 s=4,  # Each particle is 4px
                 c='b'  # Color them blue
                 )
    # Fix the x and y range of the plot (or else they'll change based on the data)
    plot.xlim(0, WORLD_WIDTH_PIXELS)
    plot.ylim(0, WORLD_HEIGHT_PIXELS)
    # Refresh with the new particles
    plot.pause(0.001)


def make_particles() -> List[Particle]:
    # Spawn particles at random positions
    particles_list: List[Particle] = []

    for i in range(NUM_PARTICLES):
        new_particle = Particle(random.random() * WORLD_WIDTH_PIXELS,
                                random.random() * WORLD_HEIGHT_PIXELS * 0.4)
        particles_list.append(new_particle)

    return particles_list

def update_particles(particles_list: List[Particle]):
    # Wipe forces
    for particle in particles_list:
        particle.next_force_x = 0
        particle.next_force_y = 0

    # Hold positions constant, compute force
    for particle in particles_list:

        # Gravity
        particle.next_force_y += GRAVITY_FORCE

        # Boundary condition
        if particle.y_pos < 0 + BOUNDARY_REP_WIDTH:
            particle.y_vel = 0 if particle.y_vel < 0 else particle.y_vel
            particle.next_force_y = 0.4

        if particle.x_pos < 0 + BOUNDARY_REP_WIDTH:
            particle.x_vel = 0 if particle.x_vel < 0 else particle.x_vel
            particle.next_force_x += 0.1

        if particle.x_pos > WORLD_WIDTH_PIXELS - BOUNDARY_REP_WIDTH:
            particle.x_vel = 0 if particle.x_vel > 0 else particle.x_vel
            particle.next_force_x -= 0.1

        # Pressure
        for particle2 in particles_list:
            dist = math.hypot(particle2.y_pos - particle.y_pos, particle2.x_pos - particle.x_pos)
            if MIN_DISTANCE < dist < MAX_DISTANCE:
                force = 1.0 / math.sqrt(dist)
                particle2.next_force_y += force * (particle2.y_pos - particle.y_pos) / dist
                particle2.next_force_x += force * (particle2.x_pos - particle.x_pos) / dist

        # Viscosity
        for particle2 in particles_list:
            dist = math.hypot(particle2.y_pos - particle.y_pos, particle2.x_pos - particle.x_pos)
            if MIN_DISTANCE < dist < MAX_DISTANCE_VISC:
                particle2.next_force_y += VISCOSITY * math.pow(particle2.y_vel - particle.y_vel, 1) / dist
                particle2.next_force_x += VISCOSITY * math.pow(particle2.x_vel - particle.x_vel, 1) / dist

    # Update positions
    for particle in particles_list:
        # Calculate velocity from force
        particle.x_vel += particle.next_force_x * DT
        particle.y_vel += particle.next_force_y * DT

        # Velocity police
        total_vel = math.hypot(particle.x_vel, particle.y_vel)
        if total_vel > MAX_VEL * DT:
            particle.y_vel /= total_vel
            particle.x_vel /= total_vel

        # Move particle by the value of its velocity
        particle.x_pos += particle.x_vel * DT
        particle.y_pos += particle.y_vel * DT

def main():
    particles_list = make_particles()

    # Update loop
    while True:
        draw(particles_list)
        update_particles(particles_list)

main()
