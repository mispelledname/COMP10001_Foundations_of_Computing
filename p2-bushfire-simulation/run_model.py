from reference import check_ignition

def run_model(f_grid, h_grid, i_threshold, w_direction, burn_seeds):
    '''Takes in the current state of the landscape and returns a tuple 
    containing (a) the final state of the landscape after the fire has stopped 
    burning, and (b) the total number of cells that have been burnt.'''
    
    # Case where nothing is burning 
    if not burn_seeds:
        return (f_grid, 0)
    
    # Keep track of how many cells have been burnt
    burnt_cells = set(burn_seeds)
    
    # Iterate until nothing is burning
    while burn_seeds:
        # Create b_grid from burn_seeds
        size = len(f_grid)
        b_grid = []
        for x in range(size):
            row = []
            for y in range(size):
                if (x, y) in burn_seeds:
                    row.append(True)
                else:
                    row.append(False)
            b_grid.append(row)
        
        # Update b_grid and f_grid for the next time step
        new_b_grid = []
        for x in range(size):
            row = []
            for y in range(size):
                # check ignition function for cells not currently burning
                if (x, y) not in burn_seeds:
                    row.append(check_ignition(
                                                     b_grid, 
                                                     f_grid, 
                                                     h_grid, 
                                                     i_threshold, 
                                                     w_direction, 
                                                     x, 
                                                     y))
                # update fuel of burning cells and see if they continue burning
                else:
                    f_grid[x][y] -= 1
                    if f_grid[x][y] == 0:
                        row.append(False)
                    else:
                        row.append(True)
            new_b_grid.append(row)
        b_grid = new_b_grid
    
        # Update burn seeds for next time step and keep track of cells burnt
        burn_seeds = []
        for x in range(size):
            for y in range(size):
                if b_grid[x][y]:
                    burn_seeds.append((x, y))
                    burnt_cells.add((x, y))
    
    return (f_grid, len(burnt_cells))