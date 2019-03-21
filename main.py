from Application import *
from PhysicalObject import *
import os
def update(dt, game):
    game.update(dt)

def GetGraph(file = 'graph.txt'):
    graph = {}
    file = open('graph.txt', 'r')
    for line in file:
        [n1, n2] = line.split(' ')
        n1 = int(n1)
        n2 = int(n2)
        if(n1==n2):
            if (not (n1 in graph.keys())):
                graph[n1] = []
        else:
            if (Constants.DIRECTED):
                if(not (n1 in graph.keys())):
                    graph[n1] = [n2]
                elif(not (n2 in graph[n1])):
                    graph[n1].append(n2)
                if(not(n2 in graph.keys())):
                    graph[n2] = []
            else:
                if (not (n1 in graph.keys())):
                    graph[n1] = [n2]
                elif (not (n2 in graph[n1])):
                    graph[n1].append(n2)
                if (not (n2 in graph.keys())):
                    graph[n2] = [n1]
                elif (not (n1 in graph[n2])):
                    graph[n2].append(n1)
    print(graph)
    return graph

def GetMatrixGraph(file = 'Matgraph.txt'):
    graph = {}
    file = open(file, 'r')
    N = 0
    for n_i, line in enumerate(file, 1):
        if(n_i == 1):
            N = len(line.split(' '))
            print(N)
            for t in range(N):
                graph[t+1] = []
        i_con = line.split(' ')
        for t in range(len(i_con)):
            i_con[t] = int(i_con[t])
        for n_j, el in enumerate(i_con, 1):
            if(i_con[n_j-1] and n_i!=n_j):
                if (Constants.DIRECTED):
                    if(not (n_j in graph[n_i])):
                        graph[n_i].append(n_j)
                else:
                    if (not (n_j in graph[n_i])):
                        graph[n_i].append(n_j)
                    if (not (n_i in graph[n_j])):
                        graph[n_j].append(n_i)
    print(graph)
    return graph

def BuildRandomGraph():
    if(Constants.NEWRANDOM):
        file = open('RandomGraph.txt', 'w')
        N = Constants.RANDOMGRAPHSIZE
        print(N)
        Matrix = []
        for i in range(N):
            Matrix.append([])
        for i in range(N):
            for j in range(N):
                if(random() < Constants.PROBABILITY_FACTOR ):
                    Matrix[i].append(1)
                else:
                    Matrix[i].append(0)
        print(Matrix)
        for i in range(N):
            line = ''
            for j in range(N):
                line += str(Matrix[i][j])
                if(j!=N-1):
                    line += ' '
                else:
                    line += '\n'
            file.write(line)
        file.close()
    return 'RandomGraph.txt'

def BuildRandomKGraph(K = 6):
    if(Constants.NEWRANDOM):
        file = open('RandomGraph.txt', 'w')
        N = Constants.RANDOMGRAPHSIZE
        print(N)
        Matrix = []
        for i in range(N):
            Matrix.append([])
        for i in range(N):
            for j in range(N):
                for k in range(K):
                    APPENDED = False
                    if((i>= k/K * N and j>= k/K * N) and (i< (k+1)/K * N and j<(k+1)/K * N)):
                        if (random() < Constants.PROBABILITY_FACTOR):
                            Matrix[i].append(1)
                        else:
                            Matrix[i].append(0)
                        APPENDED = True
                        break
                if(not APPENDED):
                    Matrix[i].append(0)

        print(Matrix)
        for i in range(N):
            line = ''
            for j in range(N):
                line += str(Matrix[i][j])
                if (j != N - 1):
                    line += ' '
                else:
                    line += '\n'
            file.write(line)
        file.close()
    return 'RandomGraph.txt'


def renaming():
    path = 'source/Favorites/'
    for file_name in os.listdir(path):
        new_name = file_name.split('-')[1]
        new_name = 'source/Favorites/' + new_name + '.png'
        print(new_name)
        os.rename(path + file_name, new_name)
    #open('source/Favorites/icons8-3-100.png')

if __name__ == '__main__':

    # renaming()
    # print(cos(pi / 180 * 180))
    if(Constants.GRAPHTYPE == 0):
        file = 'graph.txt'
        graph = GetGraph(file)
    elif(Constants.GRAPHTYPE == 1):
        file = BuildRandomGraph()
        graph = GetMatrixGraph(file)
    elif (Constants.GRAPHTYPE == 2):
        file = BuildRandomKGraph(Constants.CC_NUMBER)
        graph = GetMatrixGraph(file)
    #file = 'RandomGraph.txt'

    #graph = GetGraph(file)
    GraphBuilder = Application(Constants.SIZE_X, Constants.SIZE_Y, graph)
    pyglet.clock.schedule_interval(update, 1 / 20, GraphBuilder)
    pyglet.app.run()


