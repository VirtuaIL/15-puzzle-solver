import matplotlib.pyplot as plt
import numpy as np
from data_preparation import load_metrics, generate_metrics_avg_data

FOLDER = "./stats"
METRIC_NAMES = [
    "Długość rozwiązania",
    "Liczba stanów odwiedzonych",
    "Liczba stanów przetworzonych",
    "Maksymalna głębokość rekursji",
    "Czas działania [ms]"
]

data = load_metrics(FOLDER)
metrics_avg_data = generate_metrics_avg_data(data)

def draw_metric(index):

    metric = metrics_avg_data[index]

    all_depths = set()

    for algo_data in metric["general"].values():
        for depth in algo_data:
            all_depths.add(depth)
    depths = sorted(all_depths)
    x = np.array(depths)

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    # Ogólny wykres BFS / DFS / A*
    width = 0.25
    algos = ["BFS", "DFS", "ASTR"]

    for i in range(len(algos)):
        algo = algos[i]
        y = []
        for depth in depths:
            value = metric["general"].get(algo, {}).get(depth, 0)
            y.append(value)
        axs[0, 0].bar(x + (i - 1) * width, y, width, label=algo)

    axs[0, 0].set_title("Ogółem")
    axs[0, 0].set_ylabel(METRIC_NAMES[index])
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # A* Hamming vs Manhattan
    width = 0.3
    heuristics = ["hamming", "manhattan"]
    for i in range(len(heuristics)):
        heur = heuristics[i]
        y = []
        for depth in depths:
            value = metric["astr"].get(heur, {}).get(depth, 0)
            y.append(value)
        axs[0, 1].bar(x + (i - 0.5) * width, y, width, label=heur.capitalize())
    axs[0, 1].set_title("A*")
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # BFS - warianty porządków
    bfs_variants = metric["bfs"]
    bfs_labels = list(bfs_variants.keys())
    count = len(bfs_labels)
    width = 0.8 / count if count > 0 else 0.1
    for i in range(count):
        label = bfs_labels[i]
        series = bfs_variants[label]
        y = []
        for depth in depths:
            value = series.get(depth, 0)
            y.append(value)
        axs[1, 0].bar(x - 0.4 + i * width, y, width, label=label)

    axs[1, 0].set_title("BFS")
    axs[1, 0].set_xlabel("Głębokość")
    axs[1, 0].set_ylabel(METRIC_NAMES[index])
    axs[1, 0].legend(ncol=4)
    axs[1, 0].grid(True)

    # DFS - warianty porządków
    dfs_variants = metric["dfs"]
    dfs_labels = list(dfs_variants.keys())
    count = len(dfs_labels)
    width = 0.8 / count if count > 0 else 0.1

    for i in range(count):
        label = dfs_labels[i]
        series = dfs_variants[label]
        y = []
        for depth in depths:
            value = series.get(depth, 0)
            y.append(value)
        axs[1, 1].bar(x - 0.4 + i * width, y, width, label=label)
    axs[1, 1].set_title("DFS")
    axs[1, 1].set_xlabel("Głębokość")
    # axs[1,1].legend(ncol=4)
    axs[1, 1].grid(True)

    if index in [1, 2, 4]:  # odwiedzone, przetworzone, czas
        for ax in axs.flat:
            ax.set_yscale("log")

    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()


# Wywołanie dla wszystkich metryk
for i in range(5):
    draw_metric(i)
