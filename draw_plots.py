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
    depths = sorted({d for group in metric['general'].values() for d in group})
    x = np.array(depths)
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    # fig.suptitle(METRIC_NAMES[index])

    # Ogólny wykres BFS / DFS / A*
    width = 0.25
    for i, algo in enumerate(["BFS", "DFS", "ASTR"]):
        y = [metric["general"].get(algo, {}).get(d, 0) for d in depths]
        axs[0, 0].bar(x + (i - 1) * width, y, width, label=algo)
    axs[0, 0].set_title("Ogółem")
    # axs[0, 0].set_ylabel("Kryterium")
    axs[0, 0].set_ylabel(METRIC_NAMES[index])
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # A* Hamming vs Manhattan
    width = 0.3
    for i, heur in enumerate(["hamming", "manhattan"]):
        y = [metric["astr"].get(heur, {}).get(d, 0) for d in depths]
        axs[0, 1].bar(x + (i - 0.5) * width, y, width, label=heur.capitalize())
    axs[0, 1].set_title("A*")
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # BFS porządki
    bfs_variants = metric["bfs"]
    count = len(bfs_variants)
    width = 0.8 / count if count else 0.1
    for i, (label, series) in enumerate(bfs_variants.items()):
        y = [series.get(d, 0) for d in depths]
        axs[1, 0].bar(x - 0.4 + i * width, y, width, label=label)
    axs[1, 0].set_title("BFS")
    axs[1, 0].set_xlabel("Głębokość")
    # axs[1, 0].set_ylabel("Kryterium")
    axs[1, 0].set_ylabel(METRIC_NAMES[index])
    axs[1, 0].legend(ncol=4)
    axs[1, 0].grid(True)

    # DFS porządki
    dfs_variants = metric["dfs"]
    count = len(dfs_variants)
    width = 0.8 / count if count else 0.1
    for i, (label, series) in enumerate(dfs_variants.items()):
        y = [series.get(d, 0) for d in depths]
        axs[1, 1].bar(x - 0.4 + i * width, y, width, label=label)
    axs[1, 1].set_title("DFS")
    axs[1, 1].set_xlabel("Głębokość")
    # axs[1, 1].legend(ncol=4)
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
