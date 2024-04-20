import random
import networkx as nx
import matplotlib.pyplot as plt
from time import time

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure

import form
from PyQt6 import QtCore, QtGui, QtWidgets
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QMessageBox, QVBoxLayout
# from PyQt5.QtGui import QTextCursor
import sys
from MplForWidget import MyMplCanavas


# Функция для создания графа
def create_graph(num_nodes):
    graph = nx.DiGraph()
    graph.add_nodes_from(range(num_nodes))
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < 0.4:  # Связываем узлы с некоторой вероятностью
                weight = random.randint(1, 10)  # Случайный вес ребра
                graph.add_edge(i, j, weight=weight)
    return graph

# Функция для вычисления пути по ребру с максимальным весом
def critical_path(graph):
    max_weight = 0
    critical_edges = []
    for edge in graph.edges(data=True):
        if edge[2]['weight'] > max_weight:
            max_weight = edge[2]['weight']
            critical_edges = [(edge[0], edge[1])]
        elif edge[2]['weight'] == max_weight:
            critical_edges.append((edge[0], edge[1]))
    return critical_edges

# Иммунный алгоритм для нахождения критического пути
def immune_algorithm(num_nodes, generations):
    best_path = None
    best_fitness = float('-inf')
    population = []
    start_time = time()
    fitness_values = [] # Для хранения значений fitness в каждом поколении
    time_values = []
    for _ in range(10):  # Начальная популяция
        population.append(create_graph(num_nodes))

    for _ in range(generations):
        for graph in population:
            fitness = 0
            for edge in critical_path(graph):
                fitness += graph[edge[0]][edge[1]]['weight']  # Суммируем вес критических ребер

            if fitness > best_fitness:  # Обновляем лучший путь
                best_fitness = fitness
                best_path = graph
        time_values.append(time() - start_time)
        fitness_values.append(best_fitness) # Сохраняем лучшее значение fitness каждого поколения

        # Мутация - меняем случайное ребро в случайном графе
        mutate_graph = random.choice(population)
        edges = list(mutate_graph.edges(data=True))
        edge_to_mutate = random.choice(edges)
        edge_to_mutate[2]['weight'] = random.randint(1, 10)

    return best_path, fitness_values, time_values

# Нахождение критического пути
# num_nodes = 10
# generations = 100
#

def immune_alg(best_path, fitness_values, time_values, num_nodes, generations):
    #best_path, fitness_values, time_values = immune_algorithm(num_nodes, generations)


    edges = critical_path(best_path)
    initial_graph = create_graph(num_nodes)
    nx.draw(initial_graph, with_labels=True, edge_color='black', node_color='violet', node_size=500, font_size=10, font_color='black')
    plt.title('Исходный граф')

    return plt

def immune_alg1(best_path, fitness_values, time_values, num_nodes, generations):
    #best_path, fitness_values, time_values = immune_algorithm(num_nodes, generations)



    initial_graph = create_graph(num_nodes)
    #nx.draw(initial_graph, with_labels=True, edge_color='black', node_color='violet', node_size=500, font_size=10, font_color='black')
    #plt.title('Исходный граф')

    fig = Figure()
    # fig = Figure()
    # x = [1,2,8,3,6]
    # y = [9,3,1,6,3]

    ax = fig.add_subplot()
    fig.draw(initial_graph)
    #ax.plot(initial_graph)
    return fig



def critical(best_path, fitness_values, time_values, num_nodes, generations):
    edges = critical_path(best_path)
    # Визуализация критического пути
    graph = nx.DiGraph()
    graph.add_nodes_from(range(num_nodes))
    graph.add_edges_from(edges)

    pos = nx.circular_layout(graph)
    nx.draw(graph, pos, with_labels=True, edge_color='b', node_color='violet', node_size=500, font_size=10, font_color='black')
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

    plt.title('Критический путь в графе')

    return plt

def grafik(best_path, fitness_values, time_values, num_nodes, generations):
    # Вывод графика зависимости времени и количества поколений
    plt.figure()
    plt.plot(range(1, generations+1), time_values)
    plt.xlabel('Поколения')
    plt.ylabel('Время')
    plt.title('График зависимости времени и количества поколений')
    return plt

def grafik1(best_path, fitness_values, time_values, num_nodes, generations):
    fig = Figure()
    # fig = Figure()
    # x = [1,2,8,3,6]
    # y = [9,3,1,6,3]

    ax = fig.add_subplot()
    #fig.draw(initial_graph)
    ax.plot(range(1, generations+1), time_values)
    # Вывод графика зависимости времени и количества поколений
    #plt.plot()
    #ax.xlabel('Поколения')
    #ax.ylabel('Время')
    #ax.title('График зависимости времени и количества поколений')
    return fig

class NavigationToolbar:
    pass


class Main_window(form.Ui_mainWindow):

    # Установка формы
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        # Добавляем функционал
        self.add_functions()

    # Обработчик событий
    def add_functions(self):
        # Кнопка 'Начать игру'
        self.pushButton.clicked.connect(self.imyn)

    # Имунный
    def imyn(self):

        generations = self.lineEdit.text()
        num_nodes = self.lineEdit_2.text()


        best_path, fitness_values, time_values = immune_algorithm(int(num_nodes), int(generations))
        #print(num_nodes)

        self.fig = grafik1(best_path, fitness_values,time_values, int(num_nodes), int(generations))
        ##print(self.fig)
        self.companovka_for_mpl = QtWidgets.QVBoxLayout(self.widget)
        #print(num_nodes)

        # fig = Figure()
        # x = [1,2,8,3,6]
        # y = [9,3,1,6,3]

        #ax = fig.add_subplot()
        #ax.plot(x,y)
        self.canavas = FigureCanvasQTAgg(self.fig)
        #print(num_nodes)
        self.companovka_for_mpl.addWidget(self.canavas)




def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Main_window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
     # num_nodes = 10
     # generation = 100
     # best_path, fitness_values, time_values = immune_algorithm(num_nodes, generation)
     # # print(num_nodes)
     #
     # res = immune_alg(best_path, fitness_values, time_values, num_nodes, generation)
     # res.show()
     #
     # res = critical(best_path, fitness_values, time_values, num_nodes, generation)
     # res.show()
     #
     # res = grafik(best_path, fitness_values, time_values, num_nodes, generation)
     # res.show()

     main()