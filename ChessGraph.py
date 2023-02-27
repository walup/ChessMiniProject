from ChessGame import CoordinateTranslator
import matplotlib.pyplot as plt
import numpy as np
from ChessGame import ChessPieceColor


class ChessNode:
    
    def __init__(self, name, x, y, nodeColor):
        self.id = name
        self.x = x
        self.y = y
        self.color = nodeColor
    
    def __eq__(self, other):
        return self.id == other.id

        
class ChessConnection:
    def __init__(self, fromNodeId, toNodeId, connectionWeight):
        self.fromNodeId = fromNodeId
        self.toNodeId = toNodeId
        self.connectionWeight = connectionWeight
    
    def __eq__(self, other):
        return self.fromNodeId == other.fromNodeId and self.toNodeId == other.toNodeId
    

class Chessgraph:
    
    def __init__(self):
        self.restartGraph()
        self.nodesColor = "#b38aff"
        self.connectionColor = "#8ad4ed"
        
    
    
    def restartGraph(self):
        self.nodes = []
        self.connections = {}
        
    
    def addNode(self, node):
        if(not node in self.nodes):
            self.nodes.append(node)
            self.connections[node.id] = []
    
    def getNode(self, nodeId):
        for i in range(0,len(self.nodes)):
            if(self.nodes[i].id == nodeId):
                return self.nodes[i]
        
        return -1
    
    def containsNode(self, nodeId):
        for i in range(0,len(self.nodes)):
            if(self.nodes[i].id == nodeId):
                return True
        
        return False
    
    def initializeFromChessboard(self, chessboard):
        self.restartGraph()
        coordinateTranslator = CoordinateTranslator()
        #We add the nodes
        for i in range(0,8):
            for j in range(0,8):
                chessCoords = coordinateTranslator.reverseTranslateCoordinates(i,j)
                chessCoords2 = coordinateTranslator.translateCoordinatesForImage(chessCoords[0], chessCoords[1])
                nodeName = chessCoords[0] +str(chessCoords[1])
                node = ChessNode(nodeName, chessCoords2[0], chessCoords2[1],self.nodesColor)
                self.addNode(node)
        
        #Connections according to pieces
        pieces = chessboard.pieces
        nPieces = len(pieces)
        for i in range(0,nPieces):
            piece = pieces[i]
            pieceMoves = piece.availableMoves
            for j in range(0,len(pieceMoves)):
                move = pieceMoves[j]
                fromPosition = move.fromPosition
                toPosition = move.toPosition
                fromPositionId = fromPosition[0] +str(fromPosition[1])
                toPositionId = toPosition[0] +str(toPosition[1])
                #For now all connections will have equal weight
                self.addConnection(fromPositionId, toPositionId, 1)
    
    def initializeFromChessboardColored(self, chessboard, piecesColor):
        self.restartGraph()
        coordinateTranslator = CoordinateTranslator()
        for i in range(0,8):
            for j in range(0,8):
                chessCoords = coordinateTranslator.reverseTranslateCoordinates(i,j)
                chessCoords2 = coordinateTranslator.translateCoordinatesForImage(chessCoords[0], chessCoords[1])
                nodeName = chessCoords[0] + str(chessCoords[1])
                node = ChessNode(nodeName, chessCoords2[0], chessCoords[1], self.nodesColor)
                self.addNode(node)
        
        pieces = chessboard.pieces
        nPieces = len(pieces)
        for i in range(0,nPieces):
            piece = pieces[i]
            if((piecesColor == ChessPieceColor.WHITE and piece.pieceColor == ChessPieceColor.WHITE) or (piecesColor == ChessPieceColor.BLACK and piece.pieceColor == ChessPieceColor.BLACK)):
                pieceMoves = piece.availableMoves
                for j in range(0,len(pieceMoves)):
                    move = pieceMoves[j]
                    fromPosition = move.fromPosition
                    toPosition = move.toPosition
                    fromPositionId = fromPosition[0] + str(fromPosition[1])
                    toPositionId = toPosition[0] + str(toPosition[1])
                    #All weights are 1 in this initial version of the code
                    self.addConnection(fromPositionId, toPositionId, 1)
            
                    
    
    def addConnection(self, startNodeId, endNodeId, weight):
        if(self.containsNode(startNodeId) and self.containsNode(endNodeId)):
            newConnection = ChessConnection(startNodeId, endNodeId, weight)
            if(not newConnection in self.connections[startNodeId]):
                self.connections[startNodeId].append(newConnection)
    
    def getAllConnections(self):
        connections = []
        for i in range(0,len(self.nodes)):
            nodeConnections = self.connections[self.nodes[i].id]
            for j in range(0,len(nodeConnections)):
                connections.append(nodeConnections[j])
        
        return connections
    
                
    def displayGraph(self):
        plt.figure(figsize = (7,7))
        
        #We get all the connections
        connections = self.getAllConnections()
        for i in range(0,len(connections)):
            connection = connections[i]
            nodeStart = self.getNode(connection.fromNodeId)
            nodeEnd = self.getNode(connection.toNodeId)
            
            plt.plot([nodeStart.x, nodeEnd.x], [nodeStart.y, nodeEnd.y], color = self.connectionColor, linewidth = 5, alpha = 0.5)
        
        #Draw nodes
        for i in range(0,len(self.nodes)):
            node = self.nodes[i]
            plt.plot(node.x, node.y, color = node.color, markersize = 30, marker = "o")
            plt.text(node.x,node.y, node.id, horizontalalignment = "center", verticalalignment = "center")
    
    def getDegreeDistribution(self):
        degreeDistribution = np.zeros(64)
        for i in range(0,len(self.nodes)):
            connections = self.connections[self.nodes[i].id]
            degreeDistribution[len(connections)] += 1
        
        return list(range(0,64)), degreeDistribution
    
    def getMeanDegree(self):
        xVals, yVals = self.getDegreeDistribution()
        if(sum(yVals) > 0):
            yVals = yVals/sum(yVals)
            meanDegree = 0
            for i in range(0,len(xVals)):
                meanDegree = meanDegree + xVals[i]*yVals[i]
            
            return meanDegree
        
        return 0
        
        
            