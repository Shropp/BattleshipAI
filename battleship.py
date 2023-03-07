from dataclasses import dataclass, field
import numpy as np
from numpy.typing import NDArray
from typing import TypeAlias, Literal, List, Optional
from random import choice, seed

Direction: TypeAlias = Literal['x'] | Literal['y']

def other_direction(direction: Direction):
    return 'y' if direction == 'x' else 'x'

@dataclass
class Point:
    x: int
    y: int

    def __getitem__(self, direction: Direction):
        return self.x if direction == 'x' else self.y

x = Point(x=3,y=4)

@dataclass
class BattleshipPiece:
    id: int
    length: int
    hit_squares: List[Point] = field(default_factory=list)

    def is_sunk(self) -> bool: 
        return len(self.hit_squares) == self.length

class PieceDoesNotFitException(Exception):
    pass

class BattleshipBoard:
    PIECE_LENGTHS = [2, 3, 3, 4, 5]

    def __init__(self, board_size) -> None:
        self.grid = np.array([[None] * board_size] * board_size, dtype=object)
        self.pieces = []
        self.guesses = np.array([[False] * board_size] * board_size, dtype=bool)

    def __str__(self):
        # return "\n".join([" ".join([str(elem.id) if elem else "." for elem in row]) for row in self.grid])
        board = ""

        for row in self.grid:
            ids = [str(elem.id) if elem else "." for elem in row]
            board += " ".join(ids)
            board += "\n"
        
        return board

    def __repr__(self) -> str:
        return str(self)

    @property
    def board_size(self):
        return self.grid.shape[0]

    def guess(self, point) -> bool:
        if point in self.guesses:
            return False
        
        self.guesses.append(point)

        ship: Optional[BattleshipPiece] = self.grid[point.y, point.x]

        if not ship:
            return False

        ship.hit_squares.append(point)
        
        return True


    def place(self, piece: BattleshipPiece, start: Point, direction: Direction) -> bool:      
        if not self.can_place(piece.length, start, direction):
            return False
        
        # if direction == 'x':
        #     self.grid[start.x, start.y + i] = 

        return True

    def can_place(self, piece_length: int, start: Point, direction: Direction) -> bool:
        # Bounds check on the length and coordinates
        if start.x < 0 or start.x > self.board_size - 1 or start.y < 0 or start.y > self.board_size - 1 or \
                piece_length + start[direction] > self.board_size - 1:
            return False

        
        # Otherwise, check if any placement squres are occupied
        for i in range(piece_length):
            if (direction == 'x' and self.grid[start.y, start.x + i] is not None) or \
               (direction == 'y' and self.grid[start.y + i, start.x] is not None):
                return False
                
        return True
                
    def valid_piece_locations(self, length: int) -> List[List[Point]]:
        piecelist = []

        # Horizontal check
        for y in range(self.grid.shape[0]):
            for start in range(self.grid.shape[1] - length + 1):
                if self.can_place(length, Point(x=start, y=y), 'x'):
                    piecelist.append([Point(x=x, y=y) for x in range(start, start + length)])

        # Vertical check
        for x in range(self.grid.shape[1]):
            for start in range(self.grid.shape[0] - length + 1):
                if self.can_place(length, Point(x=x, y=start), 'y'):
                    piecelist.append([Point(x=x, y=y) for y in range(start, start + length)])



            # while start < self.grid.shape[1] - length + 1:
            #     if self.grid[y, start:start + length] == [None] * length:
            #         piecelist.append([(y, x) for x in range(start, start + length)])
            #     else:
            #         while self.grid[y, start] == None:
            #             start += 1
            #         while self.grid[y, start] != None:
            #             start += 1

        # Vertical check
        # for x in range(self.grid.shape[1]):
        #     start = 0
        #     while start < self.grid.shape[0] - length + 1:
        #         if self.grid[start:start + length, x] == [None] * length:
        #             piecelist.append([(y, x) for y in range(start, start + length)])
        #         else:
        #             while self.grid[start, x] == None:
        #                 start += 1
        #             while self.grid[start, x] != None:
        #                 start += 1

        if not piecelist:
            raise PieceDoesNotFitException("Piece of this length can't fit anywhere! OMG!")

        return piecelist

    def random_place(self, length):
        piecelocs = choice(self.valid_piece_locations(length))

        newpiece = BattleshipPiece(length=length, id=len(self.pieces))
        self.pieces.append(newpiece)

        for point in piecelocs:
            self.grid[point.y, point.x] = newpiece

def main():
    BOARD_SIZE = 10
    pieces = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    seed(4)

    myboard = BattleshipBoard(BOARD_SIZE)

    for piece in pieces:
        myboard.random_place(piece)
        print(myboard)
        print(myboard.pieces)


if __name__ == "__main__":
    main()