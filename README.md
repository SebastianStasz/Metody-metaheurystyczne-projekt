# [Archived] Vehicle Routing Problem Solver

**Vehicle Routing Problem Solver** is a Python-based solution to optimize vehicle routing for a set of cities with varying demands. The project aims to solve a real-world **vehicle routing problem (VRP)** using evolutionary algorithms and a genetic algorithm-inspired approach. The solution is optimized by minimizing the total distance traveled while ensuring that each vehicle does not exceed its capacity.

## Key Features:
- **Genetic Algorithm** to optimize vehicle routes.
- Solves a **vehicle routing problem (VRP)** for multiple cars delivering to various cities.
- Calculates distances using **Geopy** for real-world accuracy.
- Provides a visual representation of routes on a map using **Matplotlib**.
- Flexible with configurable parameters such as **number of cars**, **single car capacity**, and **number of generations**.

## Core Components:
1. **Chromosome Class (Genetic Algorithm)**:
   - Generates initial random solutions and performs mutations to find the optimal routes.
   - Calculates fitness for each solution based on total distance and the maximum distance of a vehicle.
   
2. **Routes Calculation**:
   - Optimizes routes using a **genetic algorithm** approach by iterating through generations and evolving solutions.
   
3. **Distance Calculation**:
   - Uses **Geopy** to compute the geodesic distance between cities for accurate route planning.
   
4. **Results Presentation**:
   - Outputs a detailed summary of the best solution, including the routes for each vehicle, total distance, and capacity.
   - Visualizes the routes on a map using **Matplotlib**.
