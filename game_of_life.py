def count_neighbours(cells, i, j, I, J):
    nn = 0
    for ki in [-1, 0, 1]:
        for kj in [-1, 0, 1]:
            if ki == kj == 0: continue
            elif i + ki <0  : continue
            elif j + kj <0  : continue      
            elif i + ki >= I: continue
            elif j + kj >= J: continue
            else:
                nn += cells[i+ki][j+kj]
    return nn
    
def extend_borders(cells):
    """ Return a cells matrix with +1 padding on each side,
        also returns I, J dim of the new matrix.
    """
    I, J = len(cells), len(cells[0])
    for i in range(I):
        cells[i][0:0] = [0]
        cells[i].append(0)
    J = J+2
    I = I+2
    cells[0:0] = [[0] * J]
    cells.append([0] * J)
    return cells, I, J

def get_generation(cells, generations):
    # check for empty
    if not cells: return cells
    # the game want us to waste space
    from copy import deepcopy
    cells = deepcopy(cells)
    # some new cells may grow out of index, extend now, crop later
    for epoch in range(generations):
        cells, I, J = extend_borders(cells)
        # next gen cells will be stored as tuples
        nxt = []
        for i in range(I):
            for j in range(J):
                nn = count_neighbours(cells, i, j, I, J)
                if (cells[i][j] and nn==2) or nn==3:
                    nxt.append((i,j))
        # if not next; return [[]] as asked
        if not nxt: return [[]]
        # create next generation matrix
        cells = []
        for i in range(I):
            cells.append([0] * J)
        for c in nxt:
            i, j = c
            cells[i][j] = 1
        # now we need to crop next gen matrix
        # truncate first on the column axis
        get_column = lambda j, cs: [cs[j] for cs in cells]
        # crop from the left
        while 1:
            if not any(get_column(0, cells)):
                map(lambda l: l.pop(0), cells)
            else: break
        # crop from the right
        while 1:
            if not any(get_column(-1, cells)):
                map(lambda l: l.pop(-1), cells)
            else: break
        # crop from the top
        while 1:
            if not any(cells[0]): cells.pop(0)
            else: break
        # crop from bottom
        while 1:
            if not any(cells[-1]): cells.pop(-1)
            else: break
    return cells
    
    
#####
##### This script assumes an initial matrix with alive cells.
#####
#####
