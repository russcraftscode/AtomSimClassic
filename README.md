# AtomSimClassic
A simulation of atoms and subatomic particles using classical mechanics.

## Overview
This program simulates particle interactions in a classical (Newtonian) mechanics.
It allows users to add and observe protons, neutrons, and electrons interacting under electrostatic and strong forces.  
Because this uses classical mechanics this is not an accurate representation of the particles of an atom. 
However, classical mechanics are far easier to observe and understand than quantum probability waves. 
This program will also show the limits of classical mechanics and why they cannot be used to describe what we know must 
be occuring in an atom. 

## Features
- **Graphical Representation**: Particles are displayed on a Tkinter canvas with interactive controls.
- **Particle Types**:
    - **Protons** (Red, positively charged, influenced by both electrostatic and strong force)
    - **Neutrons** (Yellow, neutral, influenced by strong force)
    - **Electrons** (Blue, negatively charged, influenced by electrostatic force)
- **Forces Implemented**:
    - **Electrostatic force** Implements Coulomb's Law
    - **Strong nuclear force** Uses a simplified short-range formula. Does not simulate gluons because that would
  require quantum mechanics.
- **Orbital Motion**:
    - Simple Orbital Model prevents an electron from moving to close to an atomic nucleus by halting its motion
    - Standard Orbital Model prevents an electron from falling into a nucleus by redirecting its velocity to a tangent
when it gets too close to a nucleus.
    - Use the standard orbitals model to see electrons orbiting a nucleus 
    - Use simple orbitals to create molecules out of multiple atoms

## Installation and Execution
### Prerequisites
Ensure you have **Python 3.x** installed.  
It uses the tk library, so it should run in on a default python install.


### Particle Behavior
- **Motion**: Particles move based on velocity and acceleration.
- **Forces**:
    - **Electrostatic force** follows an inverse square law.
    - **Strong force** applies an attractive interaction at short distances.
- **Collisions**:
    - Particles bounce off the canvas edges.
    - Neutrons and protons experience inelastic interactions when too close.

## License
This project is **open-source** and free to use under the GPL licence.
