from ChessGame import Chessboard
from ChessGame import ChessMove
from ChessGame import ChessPieceColor
from ChessGraph import Chessgraph
from ChessGame import ChessPieceType

class PGNReader:
    
    def __init__(self, chessGameURL):
        pgnFile = open(chessGameURL, "r")
        fileLines = pgnFile.readlines()
        gameLines = ""
        gameLineReached = False
        for i in range(0,len(fileLines)):
            #Recopilamos la fecha del juego
            if("Date" in fileLines[i]):
                self.date = fileLines[i].split("\"")[1]
            #Jugador blanco
            if("White" in fileLines[i] and not "Elo" in fileLines[i]):
                self.whitePlayer = fileLines[i].split("\"")[1]
            if("Black" in fileLines[i] and not "Elo" in fileLines[i]):
                self.blackPlayer = fileLines[i].split("\"")[1]
            
            if("Termination" in fileLines[i]):
                if(self.whitePlayer in fileLines[i]):
                    self.winner = "White"
                elif(self.blackPlayer in fileLines[i]):
                    self.winner = "Black"
            
            if("WhiteElo" in fileLines[i]):
                self.whiteElo = int(fileLines[i].split("\"")[1])
            
            if("BlackElo" in fileLines[i]):
                self.blackElo = int(fileLines[i].split("\"")[1])
            
            if(gameLineReached and i != len(fileLines)):
                gameLines = gameLines + fileLines[i] + " "
            elif(gameLineReached):
                gameLines = gameLines + fileLines[i]
            
            if(fileLines[i] == "\n"):
                gameLineReached = True
            
        self.gameLines = gameLines
        
        pgnFile.close()
        self.printGameInfo()
        self.parseMoves()
        
        
        
    
    
    def parseMoves(self):
        self.moves = []
        self.specialMoveValues = []
        board = Chessboard()
        
        stringMoves = self.gameLines.split(" ")
        moveCounter = 0
        for i in range(0,len(stringMoves)):
            #print(stringMoves[i])
            if(not "." in stringMoves[i] and not "-" in stringMoves[i] and stringMoves[i] != ""):
                moveString = stringMoves[i]
                moveString = moveString.replace('+','')
                moveString = moveString.replace('#','')
                moveString = moveString.replace('\n', '')
                moveString = moveString.replace('\r','')
                pieceType = self.parsePieceType(moveString)
                takeValue = self.parseTakeValue(moveString)
                moveSegment = moveString[-2:]
                file = moveSegment[0].upper()
                rank = int(moveSegment[1])
                pieceColor = -1
                if(moveCounter %2 == 0):
                    pieceColor = ChessPieceColor.WHITE
                else:
                    pieceColor = ChessPieceColor.BLACK
                piece = board.findPieceOfTypeThatCanGoToPosition(pieceType, file, rank, pieceColor)
                move = ChessMove([piece.file, piece.rank],[file, rank], takeValue)
                self.moves.append(move)
                board.makeMove(move, False)
                moveCounter += 1
                self.specialMoveValues.append(False)
                
            elif(not "." in stringMoves[i] and stringMoves[i] == "O-O"):
                #White is castling short
                if(moveCounter %2 == 0):
                    move1 = ChessMove(["E", 1],["G", 1], False)
                    move2 = ChessMove(["H",1],["F",1],False)
                    self.specialMoveValues.append(True)
                    self.specialMoveValues.append(True)
                    self.moves.append(move1)
                    self.moves.append(move2)
                    board.makeMove(move1, True)
                    board.makeMove(move2, True)
                    moveCounter += 1
                
                elif(moveCounter %2 == 1):
                    move1 = ChessMove(["E", 8],["G",8], False)
                    move2 = ChessMove(["H",8],["F",8], False)
                    self.specialMoveValues.append(True)
                    self.specialMoveValues.append(True)
                    self.moves.append(move1)
                    self.moves.append(move2)
                    board.makeMove(move1,True)
                    board.makeMove(move2, True)
                    moveCounter += 1
            
            elif(not "." in stringMoves[i] and stringMoves[i] == "O-O-O"):
                
                if(moveCounter %2 == 0):
                    move1 = ChessMove(["E", 1],["C", 1], False)
                    move2 = ChessMove(["A",1],["D",1],False)
                    self.specialMoveValues.append(True)
                    self.specialMoveValues.append(True)
                    self.moves.append(move1)
                    self.moves.append(move2)
                    board.makeMove(move1, True)
                    board.makeMove(move2, True)
                    moveCounter += 1
                
                elif(moveCounter %2 == 1):
                    move1 = ChessMove(["E", 8],["C",8], False)
                    move2 = ChessMove(["A",8],["D",8], False)
                    self.specialMoveValues.append(True)
                    self.specialMoveValues.append(True)
                    self.moves.append(move1)
                    self.moves.append(move2)
                    board.makeMove(move1,True)
                    board.makeMove(move2, True)
                    moveCounter += 1  
        board.displayBoard()
                    
    
    def parsePieceType(self, moveString):
        if(moveString[0] == "N"):
            return ChessPieceType.KNIGHT
        elif(moveString[0] == "B"):
            return ChessPieceType.BISHOP
        elif(moveString[0] == "R"):
            return ChessPieceType.ROOK
        elif(moveString[0] == "Q"):
            return ChessPieceType.QUEEN
        elif(moveString[0] == "K"):
            return ChessPieceType.KING
        else:
            return ChessPieceType.PAWN
    
    def parseTakeValue(self, moveString):
        if("x" in moveString):
            return True
        else:
            return False
                    
                    
                    
                
                
            
        
        
    
    def printGameInfo(self):
        s = ""
        s = s + "Date: "+self.date+"\n"
        s = s + "White: "+self.whitePlayer + "\n"
        s = s + "Black: "+self.blackPlayer + "\n"
        s = s + "Winner: "+self.winner + "\n"
        s = s + "White Elo: "+str(self.whiteElo) + "\n"
        s = s + "Black Elo: "+str(self.blackElo) + "\n"
        s = s + "Game: " +self.gameLines
        print(s)