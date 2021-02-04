def parse_scenario(filename):
    '''Validates the contents of the file and returns a dictionary containing 
    the values specifying a model scenario'''
    
    f = open(filename)
    contents = f.read().split()
    
    # validates size (positive integer)
    size = contents[0]
    if size.isdigit() is False or int(size) <= 0:
        return None
    size = int(size)
    
    dictionary = {}
    
    # parses and validates the initial fuel load and height of the cells
    f_grid = []
    h_grid = []
    
    for i in range(size):
        current_f = contents[1 + i].split(',')
        # ensures initial fuel load is a non-negative integer
        for f in current_f:
            if f.isdigit is False or int(f) < 0:
                return None
        current_f = [int(f) for f in current_f]
        f_grid.append(current_f)
        
        current_h = contents[1 + size + i].split(',')
        # ensures height is a positive integer 
        for h in current_h:
            if h.isdigit is False or int(h) <= 0:
                return None
        current_h = [int(h) for h in current_h]
        h_grid.append(current_h)
    
    dictionary['f_grid'] = f_grid
    dictionary['h_grid'] = h_grid
    
    # parses and validates that ignition threshold (positive integer < 8)
    i_threshold = contents[2*size + 1]
    if i_threshold.isdigit() is False or \
      int(i_threshold) > 8 or \
      int(i_threshold) <= 0:
        return None
    dictionary['i_threshold'] = int(i_threshold)
    
    # parses and validates wind direction
    wind_direction = contents[2*size + 2]
    valid_directions = ['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW', '', None]
    if wind_direction not in valid_directions:
        return None
    dictionary['w_direction'] = wind_direction
    
    # parses and validates coordinates or burning cells 
    k = 2*size + 3
    burn_seeds = []
    while k < len(contents):
        current_seed = contents[k].split(',')
        for s in current_seed:
            # ensures burn seeds are on the grid
            if int(s) < 0 or int(s) > size: 
                return None 
            # ensures burns seeds have non-zero initial fuel load 
            if f_grid[int(current_seed[0])][int(current_seed[1])] <= 0:
                return None
        current_seed = tuple(int(s) for s in current_seed)
        burn_seeds.append(current_seed)
        k += 1
    dictionary['burn_seeds'] = burn_seeds
        
    return dictionary 