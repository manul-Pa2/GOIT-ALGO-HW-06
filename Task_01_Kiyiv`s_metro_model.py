# pip install networkx matplotlib pandas

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# 1) Створення графа (не на 100% відповідає дійсним гілкам метро)
G = nx.Graph(name="Kyiv Metro (simplified)")


# Червона лінія (не вся)
red = [
    "Академмістечко", "Святошин", "Берестейська", "Шулявська",
    "Політехнічний інститут", "Вокзальна", "Університет",
    "Театральна", "Хрещатик", "Арсенальна", "Дніпро"
]


# Синя лінія (не вся)
blue = [
    "Героїв Дніпра", "Мінська", "Оболонь", "Почайна",
    "Тараса Шевченка", "Контрактова площа", "Поштова площа",
    "Майдан Незалежності", "Площа Льва Толстого"
]

# Зелена лінія (не повна)
green = [
    "Сирець", "Дорогожичі", "Лук'янівська", "Золоті ворота",
    "Палац спорту", "Кловська", "Печерська", "Дружби народів",
    "Видубичі"
]

# Додаємо вершини з атрибутом "лінія"
for s in red:
    G.add_node(s, line="red")
for s in blue:
    G.add_node(s, line="blue")
for s in green:
    G.add_node(s, line="green")

# Ребра вздовж ліній (умовно 2 хв між сусідніми станціями)
def add_line_edges(stations, w=2):
    for a, b in zip(stations, stations[1:]):
        G.add_edge(a, b, weight=w, kind="line")

add_line_edges(red, w=2)
add_line_edges(blue, w=2)
add_line_edges(green, w=2)



# Пересадки (умовно 4-5 хв переходу)
transfers = [
    ("Театральна", "Золоті ворота"),
    ("Хрещатик", "Майдан Незалежності"),
    ("Палац спорту", "Площа Льва Толстого"),
]
for a, b in transfers:
    G.add_edge(a, b, weight=4, kind="transfer")


# 2) Візуалізація
pos = nx.spring_layout(G, seed=7)  # щоб картинка була стабільною

plt.figure(figsize=(12, 9))
nx.draw(G, pos, with_labels=True, font_size=9)
edge_labels = {(u, v): d["weight"] for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
plt.title("Спрощена транспортна мережа: Київське метро (частина)")
plt.axis("off")
plt.show()


# 3) Аналіз характеристик
n = G.number_of_nodes()
m = G.number_of_edges()
degrees = dict(G.degree())
avg_degree = sum(degrees.values()) / n
density = nx.density(G)
num_components = nx.number_connected_components(G)
avg_clustering = nx.average_clustering(G)

# Якщо граф зв'язний — порахуємо ще довжину найкоротших шляхів (з вагами)
if nx.is_connected(G):
    avg_shortest = nx.average_shortest_path_length(G, weight="weight")
    diameter = nx.diameter(G)  # топологічний (без ваг)
else:
    avg_shortest = None
    diameter = None

# “Хаби”/вузли-перехрестя:
deg_cent = nx.degree_centrality(G)
betw_cent = nx.betweenness_centrality(G, weight="weight", normalized=True)

summary = {
    "Вершини (nodes)": n,
    "Ребра (edges)": m,
    "Середній ступінь": round(avg_degree, 3),
    "Щільність (density)": round(density, 4),
    "Компонент зв'язності": num_components,
    "Сер. коеф. кластеризації": round(avg_clustering, 4),
    "Сер. довжина шляху (ваг.)": None if avg_shortest is None else round(avg_shortest, 3),
    "Діаметр (неваг.)": diameter,
}
print("=== ЗВЕДЕННЯ ===")
for k, v in summary.items():
    print(f"{k}: {v}")

df = pd.DataFrame({
    "Станція": list(G.nodes()),
    "Лінія": [G.nodes[s]["line"] for s in G.nodes()],
    "Ступінь (degree)": [degrees[s] for s in G.nodes()],
    "Degree centrality": [deg_cent[s] for s in G.nodes()],
    "Betweenness centrality": [betw_cent[s] for s in G.nodes()],
}).sort_values(by=["Ступінь (degree)", "Betweenness centrality"], ascending=False)

print("\n=== ТОП-10 СТАНЦІЙ (ступінь + betweenness) ===")
print(df.head(10).to_string(index=False))

# Окремо: просто список ступенів
print("\n=== СТУПІНЬ ВЕРШИН (відсортовано) ===")
for node, deg in sorted(degrees.items(), key=lambda x: x[1], reverse=True):
    print(f"{node:25} -> {deg}")
