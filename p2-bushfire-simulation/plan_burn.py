from hidden import check_ignition, run_model

def plan_burn(f_grid, h_grid, i_threshold, town_cell):
    '''Determines the optimal cell(s) in a landscape in which to conduct a 
    prescribed burn in order to best protect a town from a future bushfire of 
    unknown timing and origin.'''
    
    x = town_cell[0]
    y = town_cell[1]
    size = len(f_grid)
    w_directions = ['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW', '', None]
    
    # Find valid prescribed burn cells 
    valid_cells = []
    test_cells = []
    for i in range(size):
        for j in range(size):
            if (i, j) != town_cell and f_grid[i][j] != 0:
                test_cells.append((i, j))
                outcome = run_model(
                                      f_grid, 
                                      h_grid, 
                                      i_threshold * 2, 
                                      None, 
                                      [(i, j)])
                f_grid_1 = outcome[0]
                if f_grid_1[x][y] != 0:
                    valid_cells.append((i, j))
    
    # For all valid burn cells, determine the proportion of scenarios in which
    # the town cell caught fire 
    scenarios = []
    for burn_cell in valid_cells:
        outcome = run_model(f_grid, h_grid, i_threshold*2, None, [burn_cell])
        f_grid_1 = outcome[0]
        b_count = 0
        for cell in test_cells:
            for w in w_directions:
                scenario = run_model(f_grid_1, h_grid, i_threshold, w, [cell])
                f_grid_2 = scenario[0]
                if f_grid_2[x][y] == 0:
                    b_count += 1
        b_proportion = b_count / (len(test_cells) * 9)
        scenarios.append((b_proportion, burn_cell))
    
    # Return the prescribed burn cells with the lowest proportion of scenarios
    # that result in the town cell burning
    scenarios = sorted(scenarios)
    min_proportion = scenarios[0][0]
    optimal_cells = [scenarios[0][1]]
    for k in range(1, len(scenarios)):
        if scenarios[k][0] == min_proportion:
            optimal_cells.append(scenarios[k][1])
        else:
            break
    
    return optimal_cells

