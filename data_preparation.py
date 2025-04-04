import os
import re
from collections import defaultdict

def parse_file(path):
    try:
        with open(path, "r") as f:
            lines = []
            for line in f:
                stripped = line.strip() #problem z enterem na końcu
                if stripped != "":
                    lines.append(stripped)

            if len(lines) < 5:
                return None

            result = []
            for i in range(5):
                result.append(float(lines[i]))

            return result
    except:
        return None
# zwraca listę [1.0, 4.0, 2.0, 1.0, 0.380]


def parse_filename(name):
    try:
        # 4x4_07_00212_bfs_uldr_stats.txt
        parts = name.split("_",4)
        # 0. 4x4
        # 1. 07
        # 2. 00212
        # 3. bfs
        # 4. uldr_stats.txt

        if len(parts) != 5 or not parts[4].endswith(".txt"):
            return None

        depth_str = parts[1]
        algo = parts[3]
        param = parts[4]

        depth = int(depth_str.lstrip("0"))  # np. "07" -> 7

        param = param.replace("_stats.txt", "")

        if algo == "astr":
            heur = {"manh": "manhattan", "hamm": "hamming"}.get(param)
            return algo, heur, None, depth
        else:
            # param,upper() - kolejnosc (np uldr)
            return algo, None, param.upper(), depth

    except:
        return None

def load_metrics(folder):

    # data
    # │
    # ├── [0]
    # │   └── "bfs"
    # │       ├── "LURD"
    # │       │   └── 3: [100, 150]
    # │       └── "RDLU"
    # │           └── 2: [200]

    data = []
    # 0 - długość rozwiązania
    # 1 - liczba stanów odwiedzonych
    # 2 - liczba stanów przetworzonych
    # 3 - maksymalna głębokość rekursji
    # 4 - czas działania [ms]
    for _ in range(5):
        # 1 - BFS/DFS/A*
        # 2 - Hamm/Manh/Order
        # 3 - Depth
        # 4 - Wyniki z data
        data.append(defaultdict(lambda: defaultdict(lambda: defaultdict(list))))

    for file in os.listdir(folder):
        if not file.endswith(".txt"):
            continue

        parsed = parse_filename(file)
        if not parsed:
            continue

        algo, heur, order, depth = parsed

        if algo == "astr":
            key = heur
        else:
            key = order

        if key is None:
            key = "ALL"

        path = os.path.join(folder, file)
        values = parse_file(path)
        if values is None:
            continue

        for i in range(5):
            data[i][algo][key][depth].append(values[i])

    return data

# def print_metrics(data):
#
#     metryka = ["Długość rozwiązania", "Liczba stanów odwiedzonych", "Liczba stanów przetworzonych", "Maksymalna głębokość rekursji", "Czas działania [ms]"]
#
#     for i, metric in enumerate(data):
#         print(f"\n{metryka[i]}:")
#
#         for algo in metric:
#             print(f"    Algorytm: {algo}")
#
#             for key in metric[algo]:
#                 print(f"      Klucz: {key}")
#
#                 for depth in sorted(metric[algo][key]):
#                     values = metric[algo][key][depth]
#                     print(f"        Głębokość {depth}: {values}")

def prepare_avg(data_by_variant):
    avg_data = {}

    # {
    #     "LURD": {
    #         3: 12.0,
    #         4: 21.0
    #     },
    # }

    # wariant: LURD, RDLU, manh,hamm..
    for variant in data_by_variant:
        depths = data_by_variant[variant]
        avg_data[variant] = {}

        for depth in depths:
            values = depths[depth] #wartości

            if values:
                total = 0
                for val in values:
                    total += val
                avg = total / len(values)

                avg_data[variant][depth] = avg

    return avg_data

def merge_variants(data_by_variant):

    # spaja wszystkie warianty(LUDR itd) w jeden i grupuje wyniki po głębokości

    # OUT:
    # {
    #     3: [10, 12, 14],
    #     4: [20],
    #     5: [30]
    # }

    merged = defaultdict(list)

    for variant in data_by_variant.values():

        for depth in variant:

            values = variant[depth]

            for val in values:
                merged[depth].append(val)

    return merged

def generate_metrics_avg_data(data):

    # data[metryka][algorytm][wariant][głębokość]

    # data[0]["bfs"]["LURD"][3] = [10, ... , 14]
    # data[1]["astr"]["manh"][5] = [1.5, ... ,1.6]

    # zapisuje ogólne średnie dla każdego algorytmu

    # i dopisuje do tego średnie dla każdego algorytmu z prepare_avg

    # i robię to dla każdej metryki czyli 5 razy

    metrics_avg_data = []

    for i in range(5):
        metric_data = {}

        # general
        general = {}

        for algo in ["bfs", "dfs", "astr"]:

            # grupy po głębokościach
            merged = merge_variants(data[i][algo])

            average = {}
            for depth, values in merged.items():
                if values:
                    total = sum(values)
                    avg = total / len(values)
                    average[depth] = avg

            general[algo.upper()] = average


        metric_data["general"] = general

        metric_data["bfs"] = prepare_avg(data[i]["bfs"])
        metric_data["dfs"] = prepare_avg(data[i]["dfs"])
        metric_data["astr"] = prepare_avg(data[i]["astr"])

        metrics_avg_data.append(metric_data)

    return metrics_avg_data


# def main():
#     # parse_filename("4x4_07_00212_dfs_uldr_stats.txt")
#     data = load_metrics("./stats")
#     print_metrics(data)
#
# if __name__ == "__main__":
#     main()