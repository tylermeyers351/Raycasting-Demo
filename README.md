Raycasting Demo

Implementation of a raycasting algorithm to familiarize myself with the pygame library. This is not my code and was mostly borrowed from a Youtube tutorial called "Simple raycasting with PyGame" by Code Monkey King. I simply followed his tutorial and tweaked it to my liking to better comprehend the process of raycasting.

For me, learning how to code a simple raycasting algortithm (utilizing Pygame) was an excellent introduction to old-school game development, and allowed me to explore a simple, yet incredibly effective algorithm that creates an illusion of a 3d environment.



History of Raycasting

Raycasting is a rendering technique used in early video games to create the illusion of three-dimensional environments. It involves casting virtual rays from a player's perspective into the game world to determine what objects or walls are visible and at what distance. This technique was popularized by games like Wolfenstein 3D and Doom.

The code behind raycasting involves several steps. First, the game defines a 2D grid that represents the game world. Each cell in the grid contains information about the type of object or wall present. The player's position and viewing direction are also known.

To perform raycasting, the game traces a series of horizontal or vertical rays from the player's position, representing lines of sight. As each ray progresses through the game world, it checks the grid cells it passes through to determine if it hits an object or a wall. The distance to the nearest object is calculated based on the ray's length.

Based on the distance, the game can determine the height and position of objects or walls on the screen. This information is used to render the 3D view, typically using a technique called textured walls, where 2D images are stretched onto the walls to give the illusion of depth.

Overall, raycasting was a significant milestone in the history of video game graphics, demonstrating the potential for creating immersive 3D environments on relatively limited hardware.

