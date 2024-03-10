
import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


class Cell:
    def __init__(self, status, move):
        self.status = status
        self.movement = move

    def to_numeric(self):
        if self.status == 0:
            return 0
        elif self.status == 1:
            return 1
        elif self.status == 2:
            return 2
        else:
            return 0

def create_board(size):
    
    particles = np.random.choice(["up", "down", "left", "right", None], size=(size, size), p=[0.2, 0.2, 0.2, 0.2, 0.2])
    lattice_gas_automata = np.empty((size, size), dtype=object)
    
    for i in range(size):
        for j in range(size):
            lattice_gas_automata[i, j] = Cell(0, None)

    for i in range(size):
        for j in range(int(size/4)):
            move = particles[i, j]
            if move is not None:
               lattice_gas_automata[i, j] = Cell(1, move) 
                
    for i in range(int(size/2)-5):
        lattice_gas_automata[i, int(size/4)] = Cell(2, None) 
        lattice_gas_automata[size - 1 - i, int(size/4)] = Cell(2, None)
    
    return lattice_gas_automata

def handle_collisions(particle_objects, size):
    new_table = np.empty((size, size), dtype=object)

    for i in range(size):
        for j in range(size):
            new_table[i, j] = copy.deepcopy(particle_objects[i, j])

    for i in range(size):
        for j in range(size):
            if particle_objects[i, j].status == 1:
                move_direction = particle_objects[i, j].movement
                next_i, next_j = i, j
                if move_direction == "up":
                    next_i -= 1
                elif move_direction == "down":
                    next_i += 1
                elif move_direction == "right":
                    next_j += 1
                elif move_direction == "left":
                    next_j -= 1
                if next_i < 0 or next_i >= size or next_j < 0 or next_j >= size or particle_objects[next_i, next_j].status == 2:
                    if move_direction == "up":
                        new_table[i, j].movement = "down"
                    elif move_direction == "down":
                        new_table[i, j].movement = "up"
                    elif move_direction == "right":
                        new_table[i, j].movement = "left"
                    elif move_direction == "left":
                        new_table[i, j].movement = "right"
                elif particle_objects[next_i, next_j].status == 1 :
                    if move_direction == "up":
                        new_table[i, j].movement = "right"
                        new_table[next_i, next_j].movement = "left"
                    elif move_direction == "down":
                        new_table[i, j].movement = "left"
                        new_table[next_i, next_j].movement = "right"
                    elif move_direction == "right":
                        new_table[i, j].movement = "down"
                        new_table[next_i, next_j].movement = "up"
                    elif move_direction == "left":
                        new_table[i, j].movement = "up"
                        new_table[next_i, next_j].movement = "down"
                else:
                    tmp = new_table[next_i, next_j]
                    new_table[next_i, next_j] = new_table[i, j]
                    new_table[i, j] = tmp

    return new_table

def visualize_board(table, size):
    cmap = mcolors.ListedColormap(['white', 'green', 'black'])
    bounds = [0, 1, 2, 3]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)
    plt.ion()
    fig, ax = plt.subplots()  
    img = ax.imshow(np.zeros((size, size)), cmap=cmap, norm=norm)
    plt.show()

    while True:
        numeric_table = np.array([[cell.to_numeric() for cell in row] for row in table])
        
        img.set_array(numeric_table)
        plt.pause(0.1)
        table = handle_collisions(table, size)

def initialize_particles(size):
    particle_objects = create_board(size)
    visualize_board(particle_objects, size)

initialize_particles(100)


