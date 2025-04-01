import os
import re
from collections import defaultdict

def parse_file(path):
    try:
        with open(path, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
            if len(lines) < 5:
                return None
            return [float(line) for line in lines[:5]]
    except:
        return None

def parse_filename(name):
    match = re.match(r"\d+x\d+_(\d+)_\d+_(bfs|dfs|astr)_([a-z]+)_stats\.txt", name)
    if not match:
        return None
    depth_str, algo, param = match.groups()
    depth = int(depth_str.lstrip("0") or "0")  # np. "01" -> 1
    if algo == "astr":
        heur = {"manh": "manhattan", "hamm": "hamming"}.get(param)
        return algo, heur, None, depth
    else:
        return algo, None, param.upper(), depth

def load_metrics(folder):
    data = [defaultdict(lambda: defaultdict(lambda: defaultdict(list))) for _ in range(5)]

    for file in os.listdir(folder):
        if not file.endswith("_stats.txt"):
            continue
        parsed = parse_filename(file)
        if not parsed:
            continue
        algo, heur, order, depth = parsed
        key = heur if algo == "astr" else order
        if key is None:
            key = "ALL"
        path = os.path.join(folder, file)
        values = parse_file(path)
        if values is None:
            continue
        for i in range(5):
            data[i][algo][key][depth].append(values[i])
    return data

def prepare_avg(data_by_variant):
    avg_data = {}
    for variant, depths in data_by_variant.items():
        avg_data[variant] = {}
        for d, values in depths.items():
            if values:
                avg_data[variant][d] = sum(values) / len(values)
    return avg_data

def merge_variants(data_by_variant):
    merged = defaultdict(list)
    for depths in data_by_variant.values():
        for d, values in depths.items():
            merged[d].extend(values)
    return merged

def generate_metrics_avg_data(data):
    metrics_avg_data = []
    for i in range(5):
        metric_data = {}
        # general
        general = {}
        for algo in ["bfs", "dfs", "astr"]:
            merged = merge_variants(data[i][algo])
            general[algo.upper()] = {d: sum(v)/len(v) for d, v in merged.items() if v}
        metric_data["general"] = general
        metric_data["bfs"] = prepare_avg(data[i]["bfs"])
        metric_data["dfs"] = prepare_avg(data[i]["dfs"])
        metric_data["astr"] = prepare_avg(data[i]["astr"])
        metrics_avg_data.append(metric_data)
    return metrics_avg_data
