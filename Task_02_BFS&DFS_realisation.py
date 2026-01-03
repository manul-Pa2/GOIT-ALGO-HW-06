#цей код - додаток до Task_01, я не хотів змішувати все в одну купу, тому сподіваюся правильно їх розділив
from collections import deque

def reconstruct_path(parent, start, goal):
    if goal not in parent:
        return None
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path

def bfs_path(G, start, goal):
    """BFS: знаходить шлях з мінімальною кількістю ребер (unweighted shortest by edges)."""
    q = deque([start])
    parent = {start: None}

    while q:
        v = q.popleft()
        if v == goal:
            break
        for nb in G.neighbors(v):                 # порядок сусідів важливий для "який саме" шлях знайдеться
            if nb not in parent:
                parent[nb] = v
                q.append(nb)

    return reconstruct_path(parent, start, goal)

def dfs_path(G, start, goal):
    """DFS: знаходить ПЕРШИЙ-ЛІПШИЙ шлях залежно від порядку обходу сусідів (не гарантує найкоротший)."""
    stack = [start]
    parent = {start: None}

    while stack:
        v = stack.pop()
        if v == goal:
            break

        # щоб DFS йшов "як рекурсивний" і був стабільний, додаємо сусідів у стек у зворотному порядку
        neighbors = list(G.neighbors(v))
        for nb in reversed(neighbors):
            if nb not in parent:
                parent[nb] = v
                stack.append(nb)

    return reconstruct_path(parent, start, goal)

def path_stats(G, path):
    """Повертає: (кількість ребер, сумарна вага)."""
    if not path:
        return None
    edges = len(path) - 1
    total_w = 0
    for a, b in zip(path, path[1:]):
        total_w += G[a][b]["weight"]
    return edges, total_w

def print_compare(G, start, goal):
    bp = bfs_path(G, start, goal)
    dp = dfs_path(G, start, goal)

    print(f"\n=== {start} -> {goal} ===")

    if bp is None:
        print("BFS: шлях не знайдено")
    else:
        e, w = path_stats(G, bp)
        print(f"BFS: ребер={e}, вага(хв)={w}")
        print("  " + " → ".join(bp))

    if dp is None:
        print("DFS: шлях не знайдено")
    else:
        e, w = path_stats(G, dp)
        print(f"DFS: ребер={e}, вага(хв)={w}")
        print("  " + " → ".join(dp))


# Кілька показових пар
pairs = [
    ("Академмістечко", "Видубичі"),
    ("Сирець", "Дніпро"),
    ("Героїв Дніпра", "Дніпро"),
    ("Героїв Дніпра", "Видубичі"),
]

for s, t in pairs:
    print_compare(G, s, t)
