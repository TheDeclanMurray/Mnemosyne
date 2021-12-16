import numpy as np
def fuzzysearch(search, check):
    
    # Initialize matrix of zeros
    row = len(search)+1
    collumn = len(check)+1
    matrix = np.zeros((len(search)+1,len(check)+1),dtype = int)

    # Populate matrix of zeros with the indeces of each character of both strings
    for i in range(1, row):
        for k in range(1,collumn):
            matrix[i][0] = i
            matrix[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions    
    for cur_col in range(1, collumn):
        for cur_row in range(1, row):
            if search[cur_row-1] == check[cur_col-1]:
                cost = 0 # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
            else:
                cost = 2
            matrix[cur_row][cur_col] = min(matrix[cur_row-1][cur_col] + 1,      # Cost of deletions
                                 matrix[cur_row][cur_col-1] + 1,          # Cost of insertions
                                 matrix[cur_row-1][cur_col-1] + cost)     # Cost of substitutions

        return ((len(search)+len(check)) - matrix[cur_row][cur_col]) / (len(search)+len(check))

print(fuzzysearch("hi", "hello", True))