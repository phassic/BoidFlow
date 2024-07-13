


https://github.com/user-attachments/assets/484e8051-acd3-4eec-b99b-3bac944fe2eb



**Dynamic Boid Simulation**

This project is a dynamic Boid simulation created using Pygame. Boids are autonomous agents that simulate the flocking behavior seen in birds, fish, and other animals. The simulation features interactive sliders that allow users to adjust the weights of various behaviors such as alignment, cohesion, separation, attraction to food, boundary avoidance, and more.




**Features**

Interactive Simulation: Adjust behaviors in real-time using sliders.
Boid Flocking: Realistic simulation of flocking behavior.
Food Attraction: Boids are attracted to food items placed by the user.
Boundary Avoidance: Boids avoid the edges of the screen.
Trail Effect: Boids leave trails for a visual effect.
Spatial Partitioning: Optimized performance using a grid for spatial partitioning.

**Prerequisites**

Python 3.x

Pygame

**Installation**
Clone the repository:

git clone https://github.com/phassic/dynamicboidsimulation.git

cd dynamicboidsimulation

**Install Pygame:**
pip install pygame

**Usage**
Run the simulation:

python3 boid_simulation.py

**Interacting with the Simulation:**
Click on the simulation area to add food positions.
Adjust the sliders at the bottom of the window to change the weights of various behaviors.
Alignment: Aligns boids with their neighbors.
Cohesion: Moves boids towards the center of mass of their neighbors.
Separation: Moves boids away from each other to avoid crowding.
Attraction: Attracts boids towards food positions.
Boundary Avoidance: Keeps boids within the screen boundaries.
Current: Simulates the effect of a current on the boids' movement.
Memory: Influences boids to move away from their previous positions.

**Code Overview**
Initialization and Setup
Pygame Initialization: Initializes Pygame modules.
Display Setup: Creates the display window with a simulation area and a UI area.
Colors: Defines various colors used in the simulation.
Boid and Slider Classes
Slider Class: Manages interactive sliders for adjusting behavior weights.
Boid Class: Represents individual boids with properties and behaviors.
Main Game Loop
Creating Boids: Initializes the boids.
Food Positions: Manages food positions.
Spatial Partitioning: Optimizes performance using a grid.
UI Sliders: Creates sliders for adjusting behavior weights.
Main Loop: Handles events, updates boids, manages food interactions, and renders the UI.
Cleanup
Pygame Quit: Cleans up Pygame resources upon exiting the main loop.
Example

**License**

This project is licensed under the MIT License. See the LICENSE file for details.

**Acknowledgments**

Pygame community for providing an  library for game development.
Craig Reynolds for the original Boid algorithm.

Contributing

Feel free to submit issues, fork the repository, and send pull requests. For major changes, please open an issue first to discuss what you would like to change.
