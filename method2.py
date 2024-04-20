import copy
import random
from time import time
import matplotlib.pyplot as plt
import networkx as nx


# Приспособляемость: особь приспособлена, если значение наибольшее
# Наследственность: мутация либо в течение жизни рандомно, либо при скрещивании
#                   мутация может присутствовать, а может отсутствовать (всегда разное влияние)


# Рекурсивная функция для выполнения глубинного поиска.
def dfs(graph, visited, start, end, path):
    visited[start] = True
    path.append(start)

    if start == end:
        return [path[:]]

    paths = []

    for i in range(len(graph[start])):
        if graph[start][i] != 0 and not visited[i]:
            paths.extend(dfs(graph, visited, i, end, path))

    path.pop()
    visited[start] = False

    return paths


# Определение функции приспособленности
# Значение приспособленности
# Длина максимального простого пути в графе
def calculate_fitness(graph):
    n = len(graph)
    longest_path = []

    for i in range(n):
        for j in range(n):
            if i != j and graph[i][j] != 0:
                visited = [False] * n
                paths = dfs(graph, visited, i, j, [])
                for path in paths:
                    if len(path) > len(longest_path):
                        longest_path = path

    return len(longest_path)


# Генерация случайного графа
# Создает двумерный массив с случайными значениями от 0 до 5
def generate_random_graph(nodes):
    graph = [[0 for _ in range(nodes)] for _ in range(nodes)]  # создаем пустую матрицу с нулями
    for i in range(nodes):
        for j in range(i + 1, nodes):  # обходим только верхний треугольник матрицы
            value = random.randint(0, 50)
            graph[i][j] = value
            graph[j][i] = value  # симметричность
    return graph


# Оператор кроссовера
def crossover(parent1, parent2):
    n = len(parent1)
    split_point = random.randint(1, n - 1)  # Случайная точка разделения
    child = parent1[:split_point] + parent2[split_point:]
    return child


# Оператор мутации
def mutate(graph):
    n = len(graph)
    i, j = random.sample(range(n), 2)
    # если центр - ничего не меняем
    # если ребро = 0, ставим 2, иначе уменьшаем на 1
    if i != j:
        value = random.randint(0, 5)
        # if graph[i][j] == 0:
        #     graph[i][j] = value
        #     graph[j][i] = value
        # else:
        #     graph[i][j] = abs(graph[i][j] - value)
        #     graph[j][i] = abs(graph[j][i] - value)
        print(f"GRAPH[{i}][{j}] = {graph[i][j]}")
    return graph


# если убрать копию графа, то популяция действительно будет улучшаться
# но веса будут уходить в огромный минус :D

# Функция генетического алгоритма
def genetic_algorithm(nodes, iterations):
    start_time = time()  # Запоминаем время начала выполнения
    population_size = 50  # Размер популяции
    population = [generate_random_graph(nodes) for _ in range(population_size)]  # Генерация начальной популяции

    fitness_values = []  # Список для хранения значений приспособленности
    time_values = []  # Список для хранения времени выполнения

    for _ in range(iterations):  # Цикл по числу итераций
        fitness_scores = [calculate_fitness(graph) for graph in
                          population]  # Рассчитываем приспособленность всех графов в популяции
        fitness_values.append(
            sum([1 if element == max(fitness_scores) else 0 for element in fitness_scores])
        )  # NEW: Запоминаем количество максимальных fitness_scores на каждой итерации
        time_values.append(time() - start_time)  # Запоминаем текущее время выполнени

        best_idx = fitness_scores.index(max(fitness_scores))  # Индекс лучшего графа
        new_population = [population[best_idx]]  # Новая популяция с лучшим графом

        while len(new_population) < population_size:  # Добавляем новые графы в популяцию
            parent1 = random.choice(population)  # Случайный родитель 1
            parent2 = random.choice(population)  # Случайный родитель 2
            child = crossover(parent1, parent2)  # Кроссовер
            child_copy = copy.deepcopy(child)
            child = random.choice([mutate(child_copy), child])  # Мутация по желанию
            new_population.append(child)

        # треть популяции случайным образом мутируем (на каждой итерации)
        for _ in range(population_size // 3):
            random_idx = random.randint(0, population_size - 1)
            random_idx_copy = copy.deepcopy(new_population[random_idx])
            new_population[random_idx] = mutate(random_idx_copy)

        population = new_population  # Обновляем популяцию

    best_graph = max(population, key=calculate_fitness)  # Ищем лучший граф в популяции
    return best_graph, fitness_values, time_values  # Возвращаем лучший граф, значения приспособленности и времени


# Настройка параметров и запуск алгоритма
nodes = 5  # Размер графа
iterations = 100  # Количество итераций
best_graph, fitness_values, time_values = genetic_algorithm(nodes, iterations)  # Запускаем алгоритм

# Построение графика времени
plt.plot(range(1, iterations + 1), time_values)
plt.xlabel('Кол-во итераций')
plt.ylabel('Время (сек)')
plt.title('Время vs. Кол-во итераций')
plt.show()

# Построение графика значения целевой функции
plt.plot(range(1, iterations + 1), fitness_values)
plt.xlabel('Кол-во итераций')
plt.ylabel('Значение приспособленности')
plt.title('Значение приспособленности vs. Кол-во итераций')
plt.show()

# Вывод графа


G = nx.Graph()

# Добавление вершин в граф
for i in range(len(best_graph)):
    G.add_node(i)

# Добавление ребер в граф
for i in range(len(best_graph)):
    for j in range(i + 1, len(best_graph)):
        if best_graph[i][j] != 0:
            G.add_edge(i, j, weight=best_graph[i][j])

# Рисование графа
pos = nx.spring_layout(G)  # Определение позиций вершин
nx.draw_networkx_nodes(G, pos, node_size=500)  # Рисование вершин
nx.draw_networkx_edges(G, pos)  # Рисование ребер
nx.draw_networkx_labels(G, pos)  # Добавление меток к вершинам
nx.draw_networkx_edge_labels(G, pos, edge_labels={(i, j): G[i][j]['weight'] for i, j in G.edges()},
                             font_color='red')  # Добавление меток к ребрам

plt.axis('off')  # Отключение осей координат
plt.show()
