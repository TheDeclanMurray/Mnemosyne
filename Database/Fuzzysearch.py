import numpy as np
def fuzzysearch(search, check):
    '''
            calculates percent similarity between two words 

            :param search: word you are searching with
            :param check: word you are checking against
			:return: ratio of similarity
            :rtype: float
    '''

    # create base matrix
    row = len(search)+1
    collumn = len(check)+1
    matrix = np.zeros((len(search)+1,len(check)+1),dtype = int)

    if search == check:
        return 1

    # adding the indexs to matrix to be able iterate
    for i in range(1, row):
        for k in range(1,collumn):
            matrix[i][0] = i
            matrix[0][k] = k

    # iterate through matrix and add cost values
    for cur_col in range(1, collumn):
        for cur_row in range(1, row):
            if search[cur_row-1] == check[cur_col-1]: # if theyre the same letter dont add additonal cost
                cost = 0 
            else:
                cost = 2

            matrix[cur_row][cur_col] = min(matrix[cur_row-1][cur_col] + 1, matrix[cur_row][cur_col-1] + 1, matrix[cur_row-1][cur_col-1] + cost) # calculating minimum letter change cost

        return ((len(search)+len(check)) - matrix[cur_row][cur_col]) / (len(search)+len(check)) # output percent the words are similar in accorandce to levenshtein algorithm

