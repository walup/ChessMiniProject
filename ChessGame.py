import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
from PIL import Image
from matplotlib.patches import Rectangle
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)


class CoordinateTranslator:
    
    def __init__(self):
        self.fileNotation = ["A", "B", "C", "D", "E", "F", "G", "H"]
        self.matrixFileNotation = {}
        
        for i in range(0,8):
            self.matrixFileNotation[self.fileNotation[i]] = i
    
    def translateCoordinates(self, file, rank):
        return [8-rank, self.matrixFileNotation[file]]
    
    def reverseTranslateCoordinates(self, i, j):
        return [self.fileNotation[j], 8-i]
    
    def translateCoordinatesForImage(self, file, rank):
        return [self.matrixFileNotation[file], rank]
    

class ChessPieceType(Enum):
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5

class ChessPieceColor(Enum):
    WHITE = 0
    BLACK = 1
    
class ChessMove:
    
    def __init__(self, fromPosition, toPosition, take):
        self.fromPosition = fromPosition
        self.toPosition = toPosition
        self.take = take
        
    def __eq__(self, other):
        equalFromPosition = (self.fromPosition[0] == other.fromPosition[0] and self.fromPosition[1] == other.fromPosition[1])
        equalToPosition = (self.toPosition[0] == other.toPosition[0] and self.toPosition[1] == other.toPosition[1])
        equalTake = (self.take == other.take)
        return equalFromPosition and equalToPosition and equalTake
        

class ChessPiece:
    
    def __init__(self, pieceType, pieceColor, pieceImageUrl, file, rank):
        self.pieceImage = Image.open(pieceImageUrl)
        self.pieceType = pieceType
        self.availableMoves = []
        self.file = file
        self.rank = rank
        self.pieceColor = pieceColor
        self.moveCount = 0
        
    
    def getPieceImage(self, width, height):
        return self.pieceImage.resize((width, height))
    
    def addMove(self, move):
        if(not move in self.availableMoves):
            self.availableMoves.append(move)
    
    def computeNewMoves(self, occupiedPositions, enemyPositions):
        self.availableMoves = []
        coordinateTranslator = CoordinateTranslator()
        boardPosition = coordinateTranslator.translateCoordinates(self.file, self.rank)
        
        #If it's the first move and the piece is a pawn
        if(self.moveCount == 0 and self.pieceType == ChessPieceType.PAWN):
            
            if(self.pieceColor == ChessPieceColor.WHITE):
                forwardMovePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0] - 1, boardPosition[1])
                twoForwardMovePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0] - 2, boardPosition[1])
                forwardMove = ChessMove([self.file, self.rank], forwardMovePosition, False)
                twoForwardMove = ChessMove([self.file, self.rank], twoForwardMovePosition, False)
                self.addMove(forwardMove)
                self.addMove(twoForwardMove)
                
                if(boardPosition[0] - 1 >= 0 and boardPosition[1] - 1 >= 0 and enemyPositions[boardPosition[0]-1, boardPosition[1]-1] == 1):
                    diagonalTakePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]-1, boardPosition[1]-1)
                    diagonalTake = ChessMove([self.file, self.rank], diagonalTakePosition, True)
                    self.addMove(diagonalTake)
                #Right diagonal take
                if(boardPosition[0]-1 >= 0 and boardPosition[1] + 1 <=7 and enemyPositions[boardPosition[0]-1, boardPosition[1] + 1] == 1):
                    diagonalTakePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]-1, boardPosition[1]+1)
                    diagonalTake = ChessMove([self.file, self.rank], diagonalTakePosition, True)
                    self.addMove(diagonalTake)
                
            elif(self.pieceColor == ChessPieceColor.BLACK):
                forwardMovePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]+1, boardPosition[1])
                twoForwardMovePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]+2, boardPosition[1])
                forwardMove = ChessMove([self.file, self.rank], forwardMovePosition, False)
                twoForwardMove = ChessMove([self.file, self.rank], twoForwardMovePosition, False)
                self.addMove(forwardMove)
                self.addMove(twoForwardMove)
                
                if(boardPosition[0] + 1 <= 7 and boardPosition[1] - 1 >= 0 and enemyPositions[boardPosition[0]+1, boardPosition[1]-1] == 1):
                    diagonalTakePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]+1, boardPosition[1]-1)
                    diagonalTake = ChessMove([self.file, self.rank], diagonalTakePosition, True)
                    self.addMove(diagonalTake)
                #Right diagonal take
                if(boardPosition[0]+1 <=7 and boardPosition[1] + 1 <=7 and enemyPositions[boardPosition[0]+1, boardPosition[1] + 1] == 1):
                    diagonalTakePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]+1, boardPosition[1]+1)
                    diagonalTake = ChessMove([self.file, self.rank], diagonalTakePosition, True)
                    self.addMove(diagonalTake)
        
        #Pawn movements
        elif(self.pieceType == ChessPieceType.PAWN):
            if(self.pieceColor == ChessPieceColor.WHITE):
                if(boardPosition[0]-1 >= 0 and occupiedPositions[boardPosition[0]-1, boardPosition[1]] == 0):
                    forwardMovePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0] - 1, boardPosition[1])
                    forwardMove = ChessMove([self.file, self.rank], forwardMovePosition, False)
                    self.addMove(forwardMove)
                #Left diagonal take
                if(boardPosition[0] - 1 >= 0 and boardPosition[1] - 1 >= 0 and enemyPositions[boardPosition[0]-1, boardPosition[1]-1] == 1):
                    diagonalTakePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]-1, boardPosition[1]-1)
                    diagonalTake = ChessMove([self.file, self.rank], diagonalTakePosition, True)
                    self.addMove(diagonalTake)
                #Right diagonal take
                if(boardPosition[0]-1 >= 0 and boardPosition[1] + 1 <=7 and enemyPositions[boardPosition[0]-1, boardPosition[1] + 1] == 1):
                    diagonalTakePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]-1, boardPosition[1]+1)
                    diagonalTake = ChessMove([self.file, self.rank], diagonalTakePosition, True)
                    self.addMove(diagonalTake)
                    
            elif(self.pieceColor == ChessPieceColor.BLACK):
                if(boardPosition[0]+1 <= 7 and occupiedPositions[boardPosition[0]+1, boardPosition[1]] == 0):
                    forwardMovePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0] + 1, boardPosition[1])
                    forwardMove = ChessMove([self.file, self.rank], forwardMovePosition, False)
                    self.addMove(forwardMove)
                #Left diagonal take
                if(boardPosition[0] + 1 <= 7 and boardPosition[1] - 1 >= 0 and enemyPositions[boardPosition[0]+1, boardPosition[1]-1] == 1):
                    diagonalTakePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]+1, boardPosition[1]-1)
                    diagonalTake = ChessMove([self.file, self.rank], diagonalTakePosition, True)
                    self.addMove(diagonalTake)
                #Right diagonal take
                if(boardPosition[0]+1 <=7 and boardPosition[1] + 1 <=7 and enemyPositions[boardPosition[0]+1, boardPosition[1] + 1] == 1):
                    diagonalTakePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]+1, boardPosition[1]+1)
                    diagonalTake = ChessMove([self.file, self.rank], diagonalTakePosition, True)
                    self.addMove(diagonalTake)
         
        #Knight Moves
        elif(self.pieceType == ChessPieceType.KNIGHT):
            
            #Vertical L movements
            if(boardPosition[0]+2 <= 7):
                if(boardPosition[1]+1 <= 7 and not(occupiedPositions[boardPosition[0]+2, boardPosition[1]+1] == 1 and enemyPositions[boardPosition[0]+2, boardPosition[1]+1] == 0)):
                    rightLPosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]+2, boardPosition[1]+1)
                    rightLMove = ChessMove([self.file, self.rank], rightLPosition, enemyPositions[boardPosition[0]+2, boardPosition[1]+1] == 1)
                    self.addMove(rightLMove)
                if(boardPosition[1]-1 >= 0 and not(occupiedPositions[boardPosition[0]+2, boardPosition[1]-1] == 1 and enemyPositions[boardPosition[0]+2, boardPosition[1]-1] == 0)):
                    leftLPosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]+2, boardPosition[1] - 1)
                    leftLMove = ChessMove([self.file, self.rank], leftLPosition, enemyPositions[boardPosition[0]+2, boardPosition[1]-1] == 1)
                    self.addMove(leftLMove)
        
            if(boardPosition[0]-2 >= 0):
                if(boardPosition[1]+1 <= 7 and not (occupiedPositions[boardPosition[0]-2, boardPosition[1]+1] == 1 and enemyPositions[boardPosition[0]-2, boardPosition[1]+1] == 0)):
                    rightLPosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]-2, boardPosition[1]+1)
                    rightLMove = ChessMove([self.file, self.rank], rightLPosition, enemyPositions[boardPosition[0]-2, boardPosition[1]+1] == 1)
                    self.addMove(rightLMove)
                if(boardPosition[1]-1 >= 0 and not (occupiedPositions[boardPosition[0]-2, boardPosition[1]-1] == 1 and enemyPositions[boardPosition[0]-2, boardPosition[1]-1] == 0)):
                    leftLPosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]-2, boardPosition[1] - 1)
                    leftLMove = ChessMove([self.file, self.rank], leftLPosition, enemyPositions[boardPosition[0]-2, boardPosition[1]-1] == 1)
                    self.addMove(leftLMove) 
                
            #Horizontal L movements
            
            if(boardPosition[1]+2 <= 7):
                if(boardPosition[0]+1 <= 7 and not (occupiedPositions[boardPosition[0]+1, boardPosition[1]+2] == 1 and enemyPositions[boardPosition[0]+1, boardPosition[1]+2] == 0)):
                    downLPosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]+1, boardPosition[1]+2)
                    downLMove = ChessMove([self.file, self.rank], downLPosition, enemyPositions[boardPosition[0]+1, boardPosition[1]+2] == 1)
                    self.addMove(downLMove)
                if(boardPosition[0]-1 >= 0 and not (occupiedPositions[boardPosition[0]-1, boardPosition[1]+2] == 1 and enemyPositions[boardPosition[0]-1, boardPosition[1]+2] == 0)):
                    upLPosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]-1, boardPosition[1] + 2)
                    upLMove = ChessMove([self.file, self.rank], upLPosition, enemyPositions[boardPosition[0]-1, boardPosition[1]+2] == 1)
                    self.addMove(upLMove)
            
            if(boardPosition[1]-2 >= 0):
                if(boardPosition[0]+1 <= 7 and not (occupiedPositions[boardPosition[0]+1, boardPosition[1]-2] == 1 and enemyPositions[boardPosition[0]+1, boardPosition[1]-2] == 0)):
                    downLPosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]+1, boardPosition[1]-2)
                    downLMove = ChessMove([self.file, self.rank], downLPosition, enemyPositions[boardPosition[0]+1, boardPosition[1]-2] == 1)
                    self.addMove(downLMove)
                if(boardPosition[0]-1 >= 0 and not (occupiedPositions[boardPosition[0]-1, boardPosition[1]-2] == 1 and enemyPositions[boardPosition[0]-1, boardPosition[1]-2] == 0 )):
                    upLPosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]-1, boardPosition[1] - 2)
                    upLMove = ChessMove([self.file, self.rank], upLPosition, enemyPositions[boardPosition[0]-1, boardPosition[1]-2] == 1)
                    self.addMove(upLMove)
        
        #Bishop movements
        elif(self.pieceType == ChessPieceType.BISHOP):
            #Inverted Forward Diagonal
            for i in range(0,8):
                if(boardPosition[0]-i >= 0 and boardPosition[0]-i <= 7 and boardPosition[1]-i >= 0 and boardPosition[1]-i <= 7 and i!= 0):
                    movePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]-i, boardPosition[1]-i)
                    move = ChessMove([self.file, self.rank], movePosition, enemyPositions[boardPosition[0]-i, boardPosition[1]-i] == 1)
                    if(occupiedPositions[boardPosition[0]-i, boardPosition[1]-i] == 1 and enemyPositions[boardPosition[0]-i, boardPosition[1]-i] == 0):
                        break
                    elif(occupiedPositions[boardPosition[0]-i, boardPosition[1]-i] == 1 and enemyPositions[boardPosition[0]-i, boardPosition[1]-i] == 1):
                        self.addMove(move)
                        break
                    else:
                        self.addMove(move)
            
            #Backwards diagonal
            for i in range(0,8):
                if(boardPosition[0]+i >= 0 and boardPosition[0]+i <= 7 and boardPosition[1]+i >= 0 and boardPosition[1]+i <= 7 and i!= 0):
                    movePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]+i, boardPosition[1]+i)
                    move = ChessMove([self.file, self.rank], movePosition, enemyPositions[boardPosition[0]+i, boardPosition[1]+i] == 1)
                    if(occupiedPositions[boardPosition[0]+i, boardPosition[1]+i] == 1 and enemyPositions[boardPosition[0]+i, boardPosition[1]+i] == 0):
                        break
                    elif(occupiedPositions[boardPosition[0]+i, boardPosition[1]+i] == 1 and enemyPositions[boardPosition[0]+i, boardPosition[1]+i] == 1):
                        self.addMove(move)
                        break
                    else:
                        self.addMove(move)

            for i in range(0,8):
                if(boardPosition[0]+i >= 0 and boardPosition[0]+i <= 7 and boardPosition[1]-i >= 0 and boardPosition[1]-i <= 7 and i!= 0):
                    movePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]+i, boardPosition[1]-i)
                    #print("Moves: "+str(self.moveCount) + " "+str(movePosition))
                    move = ChessMove([self.file, self.rank], movePosition, enemyPositions[boardPosition[0]+i, boardPosition[1]-i] == 1)
                    if(occupiedPositions[boardPosition[0]+i, boardPosition[1]-i] == 1 and enemyPositions[boardPosition[0]+i, boardPosition[1]-i] == 0):
                        break
                    elif(occupiedPositions[boardPosition[0]+i, boardPosition[1]-i] == 1 and enemyPositions[boardPosition[0]+i, boardPosition[1]-i] == 1):
                        self.addMove(move)
                        break
                    else:
                        self.addMove(move)
                        
            
            for i in range(0,8):
                if(boardPosition[0]-i >= 0 and boardPosition[0]-i <= 7 and boardPosition[1]+i >= 0 and boardPosition[1]+i <= 7 and i!= 0):
                    #print("Moves: "+str(self.moveCount) + " "+str(movePosition))
                    movePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]-i, boardPosition[1]+i)
                    move = ChessMove([self.file, self.rank], movePosition, enemyPositions[boardPosition[0]-i, boardPosition[1]+i] == 1)
                    if(occupiedPositions[boardPosition[0]-i, boardPosition[1]+i] == 1 and enemyPositions[boardPosition[0]-i, boardPosition[1]+i] == 0):
                        break
                    elif(occupiedPositions[boardPosition[0]-i, boardPosition[1]+i] == 1 and enemyPositions[boardPosition[0]-i, boardPosition[1]+i] == 1):
                        self.addMove(move)
                        break
                    else:
                        self.addMove(move)
            
            
        #Rook movements
        elif(self.pieceType == ChessPieceType.ROOK):
            for i in range(0,8):
                
                if(boardPosition[0]-i >= 0 and boardPosition[0]-i <= 7 and i!= 0):
                    movePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]-i, boardPosition[1])
                    move = ChessMove([self.file, self.rank], movePosition, enemyPositions[boardPosition[0]-i, boardPosition[1]] == 1)
                    if(occupiedPositions[boardPosition[0]-i, boardPosition[1]] == 1 and enemyPositions[boardPosition[0]-i, boardPosition[1]] == 0):
                        break
                    elif(occupiedPositions[boardPosition[0]-i, boardPosition[1]] == 1 and enemyPositions[boardPosition[0]-i, boardPosition[1]] == 1):
                        self.addMove(move)
                        break
                    else:
                        self.addMove(move)
                        
            for i in range(0,8):
                if(boardPosition[0]+i >= 0 and boardPosition[0]+i <= 7 and i!= 0):
                    movePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]+i, boardPosition[1])
                    move = ChessMove([self.file, self.rank], movePosition, enemyPositions[boardPosition[0]+i, boardPosition[1]] == 1)
                    if(occupiedPositions[boardPosition[0]+i, boardPosition[1]] == 1 and enemyPositions[boardPosition[0]+i, boardPosition[1]] == 0):
                        break
                    elif(occupiedPositions[boardPosition[0]+i, boardPosition[1]] == 1 and enemyPositions[boardPosition[0]+i, boardPosition[1]] == 1):
                        self.addMove(move)
                        break
                    else:
                        self.addMove(move)
                        
            
            for i in range(0,8):
                if(boardPosition[1]-i >= 0 and boardPosition[1]-i <= 7 and i!= 0):
                    movePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0], boardPosition[1]-i)
                    move = ChessMove([self.file, self.rank], movePosition, enemyPositions[boardPosition[0], boardPosition[1]-i] == 1)
                    if(occupiedPositions[boardPosition[0], boardPosition[1]-i] == 1 and enemyPositions[boardPosition[0], boardPosition[1]-i] == 0):
                        break
                    elif(occupiedPositions[boardPosition[0], boardPosition[1]-i] == 1 and enemyPositions[boardPosition[0], boardPosition[1]-i] == 1):
                        self.addMove(move)
                        break
                    else:
                        self.addMove(move)
                        
            
            for i in range(0,8):
                if(boardPosition[1]+i >= 0 and boardPosition[1]+i <= 7 and i!= 0):
                    movePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0], boardPosition[1]+i)
                    move = ChessMove([self.file, self.rank], movePosition, enemyPositions[boardPosition[0], boardPosition[1]+i] == 1)
                    if(occupiedPositions[boardPosition[0], boardPosition[1]+i] == 1 and enemyPositions[boardPosition[0], boardPosition[1]+i] == 0):
                        break
                    elif(occupiedPositions[boardPosition[0], boardPosition[1]+i] == 1 and enemyPositions[boardPosition[0], boardPosition[1]+i] == 1):
                        self.addMove(move)
                        break
                    else:
                        self.addMove(move)
                        
        elif(self.pieceType == ChessPieceType.QUEEN):
            #Queen is a combination of rook and bishop so i'll just copy both codes
            
            for i in range(0,8):
                if(boardPosition[0]-i >= 0 and boardPosition[0]-i <= 7 and boardPosition[1]-i >= 0 and boardPosition[1]-i <= 7 and i!= 0):
                    movePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]-i, boardPosition[1]-i)
                    move = ChessMove([self.file, self.rank], movePosition, enemyPositions[boardPosition[0]-i, boardPosition[1]-i] == 1)
                    if(occupiedPositions[boardPosition[0]-i, boardPosition[1]-i] == 1 and enemyPositions[boardPosition[0]-i, boardPosition[1]-i] == 0):
                        break
                    elif(occupiedPositions[boardPosition[0]-i, boardPosition[1]-i] == 1 and enemyPositions[boardPosition[0]-i, boardPosition[1]-i] == 1):
                        self.addMove(move)
                        break
                    else:
                        self.addMove(move)
            
            #Backwards diagonal
            for i in range(0,8):
                if(boardPosition[0]+i >= 0 and boardPosition[0]+i <= 7 and boardPosition[1]+i >= 0 and boardPosition[1]+i <= 7 and i!= 0):
                    movePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]+i, boardPosition[1]+i)
                    move = ChessMove([self.file, self.rank], movePosition, enemyPositions[boardPosition[0]+i, boardPosition[1]+i] == 1)
                    if(occupiedPositions[boardPosition[0]+i, boardPosition[1]+i] == 1 and enemyPositions[boardPosition[0]+i, boardPosition[1]+i] == 0):
                        break
                    elif(occupiedPositions[boardPosition[0]+i, boardPosition[1]+i] == 1 and enemyPositions[boardPosition[0]+i, boardPosition[1]+i] == 1):
                        self.addMove(move)
                        break
                    else:
                        self.addMove(move)

            for i in range(0,8):
                if(boardPosition[0]+i >= 0 and boardPosition[0]+i <= 7 and boardPosition[1]-i >= 0 and boardPosition[1]-i <= 7 and i!= 0):
                    movePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]+i, boardPosition[1]-i)
                    #print("Moves: "+str(self.moveCount) + " "+str(movePosition))
                    move = ChessMove([self.file, self.rank], movePosition, enemyPositions[boardPosition[0]+i, boardPosition[1]-i] == 1)
                    if(occupiedPositions[boardPosition[0]+i, boardPosition[1]-i] == 1 and enemyPositions[boardPosition[0]+i, boardPosition[1]-i] == 0):
                        break
                    elif(occupiedPositions[boardPosition[0]+i, boardPosition[1]-i] == 1 and enemyPositions[boardPosition[0]+i, boardPosition[1]-i] == 1):
                        self.addMove(move)
                        break
                    else:
                        self.addMove(move)
                        
            
            for i in range(0,8):
                if(boardPosition[0]-i >= 0 and boardPosition[0]-i <= 7 and boardPosition[1]+i >= 0 and boardPosition[1]+i <= 7 and i!= 0):
                    #print("Moves: "+str(self.moveCount) + " "+str(movePosition))
                    movePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]-i, boardPosition[1]+i)
                    move = ChessMove([self.file, self.rank], movePosition, enemyPositions[boardPosition[0]-i, boardPosition[1]+i] == 1)
                    if(occupiedPositions[boardPosition[0]-i, boardPosition[1]+i] == 1 and enemyPositions[boardPosition[0]-i, boardPosition[1]+i] == 0):
                        break
                    elif(occupiedPositions[boardPosition[0]-i, boardPosition[1]+i] == 1 and enemyPositions[boardPosition[0]-i, boardPosition[1]+i] == 1):
                        self.addMove(move)
                        break
                    else:
                        self.addMove(move)
                        
            
            for i in range(0,8):
                
                if(boardPosition[0]-i >= 0 and boardPosition[0]-i <= 7 and i!= 0):
                    movePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]-i, boardPosition[1])
                    move = ChessMove([self.file, self.rank], movePosition, enemyPositions[boardPosition[0]-i, boardPosition[1]] == 1)
                    if(occupiedPositions[boardPosition[0]-i, boardPosition[1]] == 1 and enemyPositions[boardPosition[0]-i, boardPosition[1]] == 0):
                        break
                    elif(occupiedPositions[boardPosition[0]-i, boardPosition[1]] == 1 and enemyPositions[boardPosition[0]-i, boardPosition[1]] == 1):
                        self.addMove(move)
                        break
                    else:
                        self.addMove(move)
                        
            for i in range(0,8):
                if(boardPosition[0]+i >= 0 and boardPosition[0]+i <= 7 and i!= 0):
                    movePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]+i, boardPosition[1])
                    move = ChessMove([self.file, self.rank], movePosition, enemyPositions[boardPosition[0]+i, boardPosition[1]] == 1)
                    if(occupiedPositions[boardPosition[0]+i, boardPosition[1]] == 1 and enemyPositions[boardPosition[0]+i, boardPosition[1]] == 0):
                        break
                    elif(occupiedPositions[boardPosition[0]+i, boardPosition[1]] == 1 and enemyPositions[boardPosition[0]+i, boardPosition[1]] == 1):
                        self.addMove(move)
                        break
                    else:
                        self.addMove(move)
                        
            
            for i in range(0,8):
                if(boardPosition[1]-i >= 0 and boardPosition[1]-i <= 7 and i!= 0):
                    movePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0], boardPosition[1]-i)
                    move = ChessMove([self.file, self.rank], movePosition, enemyPositions[boardPosition[0], boardPosition[1]-i] == 1)
                    if(occupiedPositions[boardPosition[0], boardPosition[1]-i] == 1 and enemyPositions[boardPosition[0], boardPosition[1]-i] == 0):
                        break
                    elif(occupiedPositions[boardPosition[0], boardPosition[1]-i] == 1 and enemyPositions[boardPosition[0], boardPosition[1]-i] == 1):
                        self.addMove(move)
                        break
                    else:
                        self.addMove(move)
                        
            
            for i in range(0,8):
                if(boardPosition[1]+i >= 0 and boardPosition[1]+i <= 7 and i!= 0):
                    movePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0], boardPosition[1]+i)
                    move = ChessMove([self.file, self.rank], movePosition, enemyPositions[boardPosition[0], boardPosition[1]+i] == 1)
                    if(occupiedPositions[boardPosition[0], boardPosition[1]+i] == 1 and enemyPositions[boardPosition[0], boardPosition[1]+i] == 0):
                        break
                    elif(occupiedPositions[boardPosition[0], boardPosition[1]+i] == 1 and enemyPositions[boardPosition[0], boardPosition[1]+i] == 1):
                        self.addMove(move)
                        break
                    else:
                        self.addMove(move)
            
            
                        
        elif(self.pieceType == ChessPieceType.KING):
            for i in range(-1,2):
                for j in range(-1,2):
                    if(boardPosition[0] + i >= 0 and boardPosition[0] + i <=7 and boardPosition[1]+j >= 0 and boardPosition[1]+j<=7):
                        movePosition = coordinateTranslator.reverseTranslateCoordinates(boardPosition[0]+i, boardPosition[1]+j)
                        move = ChessMove([self.file, self.rank], movePosition, enemyPositions[boardPosition[0], boardPosition[1]] == 1)
                        if(occupiedPositions[boardPosition[0]+i, boardPosition[1]+j] == 1 and enemyPositions[boardPosition[0]+i, boardPosition[1]+j] == 1):
                            self.addMove(move)
                        elif(occupiedPositions[boardPosition[0]+i, boardPosition[1]+j] == 0):
                            self.addMove(move)
        
    def movePiece(self, move, specialMove):    
        if(move in self.availableMoves and not specialMove):
            self.file = move.toPosition[0]
            self.rank = move.toPosition[1]
            self.moveCount += 1
            return True
        
        elif(specialMove):
            self.file = move.toPosition[0]
            self.rank = move.toPosition[1]
            self.moveCount += 1
            return True
        return False
    
    def printMoves(self):
        print(str(len(self.availableMoves))+ " moves")
        for i in range(0,len(self.availableMoves)):
            s = "["+str(self.availableMoves[i].toPosition[0])+","+str(self.availableMoves[i].toPosition[1])+"]"
            if(self.availableMoves[i].take):
                s = s + " take"
            print(s)

class Chessboard:
    
    def __init__(self):
        self.occupiedPositions = np.zeros((8,8))
        self.whitePiecesPositions = np.zeros((8,8))
        self.blackPiecesPositions = np.zeros((8,8))
        self.pieces = []
        self.boardWidth = 8
        self.boardHeight = 8
        self.whiteCellsColor = "#d9d4c7"
        self.blackCellsColor = "#44b1c2"
        self.taken = []
        self.moveCount = 0
        self.initializeBoard()
        
    #This function initializes the pieces in the right positions
    def initializeBoard(self):
        print("Board initialization")
        #White pawns
        coordinateTranslator = CoordinateTranslator()
        pawnFiles = ["A","B","C","D","E","F","G","H"]
        for i in range(0,len(pawnFiles)):
            pawn = ChessPiece(ChessPieceType.PAWN, ChessPieceColor.WHITE, "white_pawn.png", pawnFiles[i],2)
            matrixPosition = coordinateTranslator.translateCoordinates(pawnFiles[i], 2)
            self.pieces.append(pawn)
        
        #White Rooks
        rook1 = ChessPiece(ChessPieceType.ROOK, ChessPieceColor.WHITE, "white_rook.png", "A", 1)
        rook2 = ChessPiece(ChessPieceType.ROOK, ChessPieceColor.WHITE, "white_rook.png", "H", 1)
        self.pieces.append(rook1)
        self.pieces.append(rook2)
        
        #White knights
        knight1 = ChessPiece(ChessPieceType.KNIGHT, ChessPieceColor.WHITE, "white_knight.png", "B", 1)
        knight2 = ChessPiece(ChessPieceType.KNIGHT, ChessPieceColor.WHITE, "white_knight.png", "G", 1)
        self.pieces.append(knight1)
        self.pieces.append(knight2)
        
        #White bishop
        bishop1 = ChessPiece(ChessPieceType.BISHOP, ChessPieceColor.WHITE, "white_bishop.png", "C",1)
        bishop2 = ChessPiece(ChessPieceType.BISHOP, ChessPieceColor.WHITE, "white_bishop.png", "F", 1)
        self.pieces.append(bishop1)
        self.pieces.append(bishop2)
        
        #White queen
        whiteQueen = ChessPiece(ChessPieceType.QUEEN, ChessPieceColor.WHITE, "white_queen.png", "D", 1)
        self.pieces.append(whiteQueen)
        #White king
        whiteKing = ChessPiece(ChessPieceType.KING, ChessPieceColor.WHITE, "white_king.png", "E", 1)
        self.pieces.append(whiteKing)
        #Black pawns
        for i in range(0,len(pawnFiles)):
            pawn = ChessPiece(ChessPieceType.PAWN, ChessPieceColor.BLACK, "black_pawn.png", pawnFiles[i],7)
            matrixPosition = coordinateTranslator.translateCoordinates(pawnFiles[i], 7)
            self.pieces.append(pawn)
        
        #Black rooks
        rook1 = ChessPiece(ChessPieceType.ROOK, ChessPieceColor.BLACK, "black_rook.png", "A", 8)
        rook2 = ChessPiece(ChessPieceType.ROOK, ChessPieceColor.BLACK, "black_rook.png", "H", 8)
        self.pieces.append(rook1)
        self.pieces.append(rook2)
        
        #Black knight
        knight1 = ChessPiece(ChessPieceType.KNIGHT, ChessPieceColor.BLACK, "black_knight.png", "B", 8)
        knight2 = ChessPiece(ChessPieceType.KNIGHT, ChessPieceColor.BLACK, "black_knight.png", "G", 8)
        self.pieces.append(knight1)
        self.pieces.append(knight2)
        #Black bishop
        bishop1 = ChessPiece(ChessPieceType.BISHOP, ChessPieceColor.BLACK, "black_bishop.png", "C",8)
        bishop2 = ChessPiece(ChessPieceType.BISHOP, ChessPieceColor.BLACK, "black_bishop.png", "F", 8)
        self.pieces.append(bishop1)
        self.pieces.append(bishop2)
        
        #Black queen
        blackQueen = ChessPiece(ChessPieceType.QUEEN, ChessPieceColor.BLACK, "black_queen.png", "D", 8)
        self.pieces.append(blackQueen)
        
        #Black king
        blackKing = ChessPiece(ChessPieceType.KING, ChessPieceColor.BLACK, "black_king.png", "E", 8)
        self.pieces.append(blackKing)
        
        for i in range(0,len(self.pieces)):
            piece = self.pieces[i]
            matrixPosition = coordinateTranslator.translateCoordinates(piece.file, piece.rank)
            self.occupiedPositions[matrixPosition[0], matrixPosition[1]] = 1
            
            if(piece.pieceColor == ChessPieceColor.WHITE):
                self.whitePiecesPositions[matrixPosition[0], matrixPosition[1]] = 1
                
            
            elif(piece.pieceColor == ChessPieceColor.BLACK):
                self.blackPiecesPositions[matrixPosition[0], matrixPosition[1]] = 1
            
        self.recomputeAvailableMoves()
            
    
    def recomputeAvailableMoves(self):
        for i in range(0,len(self.pieces)):
            if(self.pieces[i].pieceColor == ChessPieceColor.WHITE):
                self.pieces[i].computeNewMoves(self.occupiedPositions, self.blackPiecesPositions)
                
            
            elif(self.pieces[i].pieceColor == ChessPieceColor.BLACK):
                self.pieces[i].computeNewMoves(self.occupiedPositions, self.whitePiecesPositions)
    
    def findPieceIndexAtPosition(self, file, rank):
        for i in range(0,len(self.pieces)):
            piece = self.pieces[i]
            if(piece.file == file and piece.rank == rank):
                return i
        
        return -1
    
    def findPieceAtPosition(self, file, rank):
        for i in range(0,len(self.pieces)):
            piece = self.pieces[i]
            if(piece.file == file and piece.rank == rank):
                return piece
        
        return -1
    
    def findPieceOfTypeThatCanGoToPosition(self, pieceType, file, rank, pieceColor, fromFile):
        for i in range(0,len(self.pieces)):
            piece = self.pieces[i]
            if(piece.pieceType == pieceType and piece.pieceColor == pieceColor):
                pieceMoves = piece.availableMoves
                for j in range(0,len(pieceMoves)):
                    if(pieceMoves[j].toPosition[0] == file and pieceMoves[j].toPosition[1] == rank):
                        if(fromFile != -1 and piece.file == fromFile):
                            return piece
                        elif(fromFile == -1):
                            return piece
    
    def findColorPieceIndexAtPosition(self, file, rank, color):
        for i in range(0,len(self.pieces)):
            piece = self.pieces[i]
            if(piece.file == file and piece.rank == rank and piece.pieceColor == color):
                return i
        
        return -1
                
        
    def makeMove(self, move, specialMove):
        
        moveStartFile = move.fromPosition[0]
        moveStartRank = move.fromPosition[1]
        coordinateTranslator = CoordinateTranslator()
        
        pieceIndex = self.findPieceIndexAtPosition(moveStartFile, moveStartRank)
        if(pieceIndex != -1):
            fromCoords = coordinateTranslator.translateCoordinates(moveStartFile, moveStartRank)
            toCoords = coordinateTranslator.translateCoordinates(move.toPosition[0], move.toPosition[1])
            #Movemos la pieza en nuestro tablero
            legalMove = self.pieces[pieceIndex].movePiece(move, specialMove)
            if(legalMove):
                self.moveCount = self.moveCount+1
                self.occupiedPositions[fromCoords[0], fromCoords[1]] = 0
                self.occupiedPositions[toCoords[0], toCoords[1]] = 1
                    
                if(self.pieces[pieceIndex].pieceColor == ChessPieceColor.WHITE):
                    self.whitePiecesPositions[fromCoords[0], fromCoords[1]] = 0
                    self.whitePiecesPositions[toCoords[0], toCoords[1]] = 1
                        
                    if(move.take):
                        enemyIndex = self.findColorPieceIndexAtPosition(move.toPosition[0],move.toPosition[1], ChessPieceColor.BLACK)
                        self.blackPiecesPositions[toCoords[0], toCoords[1]] = 0
                        self.recomputeAvailableMoves()
                        self.taken.append(self.pieces.pop(enemyIndex))
                    else:
                        self.recomputeAvailableMoves()
                    
                elif(self.pieces[pieceIndex].pieceColor == ChessPieceColor.BLACK):
                    self.blackPiecesPositions[fromCoords[0], fromCoords[1]] = 0
                    self.blackPiecesPositions[toCoords[0], toCoords[1]] = 1
                    
                    if(move.take):
                        enemyIndex = self.findColorPieceIndexAtPosition(move.toPosition[0],move.toPosition[1], ChessPieceColor.WHITE)
                        self.whitePiecesPositions[toCoords[0], toCoords[1]] = 0
                        self.recomputeAvailableMoves()
                        self.taken.append(self.pieces.pop(enemyIndex))
                        
                    else:
                        self.recomputeAvailableMoves()
                    
            else:
                print("Ilegal Move")
                
        
    def displayBoard(self):
        fig, ax = plt.subplots(figsize = (5,5))
        for i in range(0,self.boardWidth):
            for j in range(0,self.boardHeight):
                if((i%2 == 0 and j%2 == 1) or (i%2 == 1 and j%2 == 0)):
                    ax.add_patch(Rectangle((i,j), 1,1, facecolor = self.whiteCellsColor, fill = True, edgecolor = "none"))
                else:
                    ax.add_patch(Rectangle((i,j),1,1,facecolor = self.blackCellsColor, fill = True, edgecolor = "none"))
        coordTranslator = CoordinateTranslator()
        for i in range(0,len(self.pieces)):
            piece = self.pieces[i]
            pieceimage = piece.getPieceImage(200,200)
            imageBox = OffsetImage(pieceimage, zoom = 0.15)
            pieceCoordinates = coordTranslator.translateCoordinatesForImage(piece.file, piece.rank)
            
            annotationBox = AnnotationBbox(imageBox, (pieceCoordinates[0]+0.5,pieceCoordinates[1]-1+0.5), frameon = False)
            ax.add_artist(annotationBox)
        
        xTickPositions = [i + 0.5 for i in range(0,8)]
        yTickPositions = [i+0.5 for i in range(0,8)]
        yTickText = [str(i) for i in range(1,9)]
        
        ax.set_xlim([0,self.boardWidth])
        ax.set_ylim([0,self.boardHeight])
        ax.set_xticklabels(coordTranslator.fileNotation)
        ax.set_xticks(xTickPositions)
        ax.set_yticks(yTickPositions)
        ax.set_yticklabels(yTickText)