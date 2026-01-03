import heapq
import math
import pandas as pd

def dijkstra(G, source, weight="weight"):
    """
    Дейкстра для графа з додатними вагами:
      dist[v]  - найкоротша відстань (сума ваг) від source до v
      parent[v] - попередник v у найкоротшому шляху 
    """
    dist = {v: math.inf for v in G.nodes()}
    parent = {source: None}
    dist[source] = 0

    pq = [(0, source)]  # (distance, vertex)
    visited = set()

    while pq:
        cur_d, v = heapq.heappop(pq)
        if v in visited:
            continue
        visited.add(v)

        # обробка помилки меншого значення
        if cur_d > dist[v]:
            continue

        for nb in G.neighbors(v):
            w = G[v][nb].get(weight, 1)      # якщо раптом нема weight
            nd = cur_d + w
            if nd < dist[nb]:
                dist[nb] = nd
                parent[nb] = v
                heapq.heappush(pq, (nd, nb))

    return dist, parent

def restore_path(parent, source, target):
    """Відновлює шлях source->target по parent (якщо reachable)."""
    if target not in parent and target != source:
        return None
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = parent.get(cur)
    path.reverse()
    if path and path[0] == source:
        return path
    return None

def all_pairs_dijkstra(G, weight="weight"):
    """
    Запускає Дейкстру з кожної вершини.
    Повертає:
      all_dist[src][dst] = найкоротша відстань
      all_parent[src] = parent-словник для відновлення шляхів від src
    """
    all_dist = {}
    all_parent = {}
    for src in G.nodes():
        dist, parent = dijkstra(G, src, weight=weight)
        all_dist[src] = dist
        all_parent[src] = parent
    return all_dist, all_parent

# Рахуємо всі найкоротші відстані
all_dist, all_parent = all_pairs_dijkstra(G, weight="weight")

# Матриця відстаней (хвилини)
stations = list(G.nodes())
dist_matrix = pd.DataFrame(
    [[all_dist[a][b] for b in stations] for a in stations],
    index=stations,
    columns=stations
)

print("\n=== МАТРИЦЯ НАЙКОРОТШИХ ВІДСТАНЕЙ (хв) ===")
print(dist_matrix.to_string())

# Як отримати маршрут
def show_shortest_route(src, dst):
    parent = all_parent[src]
    path = restore_path(parent, src, dst)
    if path is None:
        print(f"{src} -> {dst}: шляху немає")
        return
    time_min = all_dist[src][dst]
    print(f"\nНайкоротший шлях (Дейкстра) {src} -> {dst}: {time_min} хв")
    print("  " + " → ".join(path))

# Приклади:
show_shortest_route("Академмістечко", "Видубичі")
show_shortest_route("Героїв Дніпра", "Дніпро")
show_shortest_route("Сирець", "Дніпро")

