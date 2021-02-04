def check_ignition(b_grid, f_grid, h_grid, i_threshold, w_direction, i, j):
    '''Takes in the current state of the grid at time t and coordinates i and j 
    of a cell and determines if the cell will catch fire at time t + 1'''
    
    # Check if specified cell has fuel load
    if f_grid[i][j] == 0: 
        return False
    
    # Case where specified cell is currently burning (cell will not ignite)
    if b_grid[i][j]:
        return False
    
    # Determine which are adjacent to the cell, including the effects of wind
    adjacent_cells = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            adjacent_cells.append([x, y])
    adjacent_cells.remove([0, 0])
    
    wind_switcher = {
                     '': [],
                     None: [],
                     'N': [[-2, -1], [-2, 0], [-2, 1]],
                     'NE': [[-2, 1], [-2, 2], [-1, 2]],
                     'E': [[-1, 2], [0, 2], [1, 2]],
                     'SE': [[1, 2], [2, 2], [2, 1]],
                     'S': [[2, -1], [2, 0], [2, 1]],
                     'SW': [[1, -2], [2, -2], [2, -1]],
                     'W': [[-1, -2], [0, -2], [1, -2]],
                     'NW': [[-1, -2], [-2, -2], [-2, -1]]
    }
   
    for wind_reach in wind_switcher[w_direction]:
        adjacent_cells.append(wind_reach)   
    
    adjacent_cells = [[i + x, j + y] for [x, y] in adjacent_cells]
    
    # Determine which of the adjacent cells are currently burning
    grid_size = len(b_grid)
    burning_cells = []
    for [x, y] in adjacent_cells:
        if (0 <= x < grid_size) and (0 <= y < grid_size):
            if b_grid[x][y]:
                burning_cells.append([x, y])
    
    # Determine the ignition factor contributed by each burning cell
    cell_height = h_grid[i][j]
    ignition_factor = 0
    for [x, y] in burning_cells:
        height = h_grid[x][y]
        if height == cell_height:
            ignition_factor += 1
        elif height < cell_height:
            ignition_factor += 2
        elif height > cell_height:
            ignition_factor += 0.5
      
    # Returns True if ignition factor exceeds ignition threshold 
    if ignition_factor >= i_threshold: 
        return True
    return False 