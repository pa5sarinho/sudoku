import requests
import numpy as np
from bs4 import BeautifulSoup

class Sudoku:

    def __init__(self, arr=np.zeros((9, 9)).astype(np.int8)):
        '''
        initializes an empty (zeros) 2D array for the puzzle (or one given by the user),
        another empty 2D array for the solved puzzle,
        and what will be final combination of the two (a completely solved game with no zeros)
        numpy array of 8 bit integers, 9x9
        '''
        self.grid = arr
        self.solution = np.zeros((9, 9)).astype(np.int8)
        self.solvedGame = np.zeros((9, 9)).astype(np.int8)

    def __str__(self):
        s=''
        for i in range(9):
            for e in self.grid[i]:
                # formats the string output: 5 spaces per number, right alignment
                s += f"{str(e):>5}"
            s += '\n\n'

        return s

    def extract(self) -> np.ndarray:
        '''
        Simple web scraping function to return a sudoku grid (numpy array) from the internet
        Highly dependent on the html of the page
        (if the website ever stops working or changes its code,
        changes will be necessary to adapt to another one)

        changes the grid attribute and returns it
        '''

        html = requests.get("https://five.websudoku.com/").text
        soup = BeautifulSoup(html, 'html.parser')

        row = 0
        column = 0

        for i in range(81):

            if (i > 1) and i % 9 == 0:
                row += 1
                column = 0

            cell = 'f{0}{1}'.format(column, row)

            cellValue = soup.find(id=cell).get('value')
            
            if cellValue == None:
                cellValue = 0

            self.grid[column, row] = int(cellValue)

            column += 1

        return self.grid

    def solve(self) -> np.ndarray:
        '''
        this function solves the sudoku puzzle in self.grid
        changes the solution and solvedGame attributes and returns them
        '''
        
        self.solvedGame = self.grid
        square = self.solvedGame[:3, :3]

        # 2D list of numpy arrays of what could be the answer
        possibleNumbersList = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        while True:
            row = 0
            item_index = 0
            for i in range(81):
                # loop that checks every cell in the grid
                # resetting the column indexing each row, and jumping to the next one:
                if (i > 1) and i % 9 == 0:
                        row += 1
                        item_index = 0

                # cheking on what interval the cell is
                if (row < 3) & (item_index < 3):
                    square = self.solvedGame[:3, :3]
                elif (row < 3) & np.logical_and(item_index >= 3, item_index < 6):
                    square = self.solvedGame[:3, 3:6]
                elif (row < 3) & (item_index >= 6):
                    square = self.solvedGame[:3, 6:]
                elif np.logical_and(row >= 3, row < 6) & (item_index < 3): 
                    square = self.solvedGame[3:6, :3]
                elif np.logical_and(row >= 3, row < 6) & np.logical_and(item_index >= 3, item_index < 6): 
                    square = self.solvedGame[3:6, 3:6]
                elif np.logical_and(row >= 3, row < 6) & (item_index >= 6): 
                    square = self.solvedGame[3:6, 6:]
                elif (row >= 6) & (item_index < 3): 
                    square = self.solvedGame[6:, :3]
                elif (row >= 6) & np.logical_and(item_index >= 3, item_index < 6):
                    square = self.solvedGame[6:, 3:6]
                elif (row >= 6) & (item_index >= 6): 
                    square = self.solvedGame[6:, 6:]

                if self.solvedGame[row, item_index] == 0:
                    # possible values array (resets every loop)
                    possible_values = np.arange(1, 10, dtype=np.int8)
                    square_numbers = list()
                    for array in range(3):
                        for num in square[array]:
                            if num != 0:
                                square_numbers.append(num)

                    for v in range(9):
                        # first it checks if v is in the current row, then column, then interval (square)
                        if (v+1 in self.solvedGame[row]) or (v+1 in self.solvedGame[:, item_index]) or (v+1 in square_numbers):
                            index = np.where(possible_values == v+1)
                            # if it is, it's not a possible number for the cell. removes it from the array
                            possible_values = np.delete(possible_values, index)

                    possibleNumbersList[row][item_index] = possible_values
                    
                    # saving the cells with only 1 possible value to the solution array
                    if possible_values.size == 1:
                        self.solution[row, item_index] = possible_values[0]

                item_index += 1
                self.solvedGame = self.solution + self.grid

            if 0 not in self.solvedGame:
                break

        return self.solution
