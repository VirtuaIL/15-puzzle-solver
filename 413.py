import subprocess
import os

boards_folder = "413"

# Pobierz wszystkie pliki .txt z folderu boards/
board_files = sorted([
    f for f in os.listdir(boards_folder)
    if f.endswith(".txt")
])

print(f"Znaleziono {len(board_files)} plansz.\n")

for board_filename in board_files:
    print(f"→ Przetwarzanie: {board_filename}")

    # Obcinamy rozszerzenie .txt
    base_name = os.path.splitext(board_filename)[0]

    args = [
        "python", "main.py",
        "bfs",
        "UDLR",
        board_filename,
        # os.path.join(boards_folder, board_filename),  # pełna ścieżka do planszy
        f"{base_name}_bfs_udlr_sol.txt",
        f"{base_name}_bfs_udlr_stats.txt"
    ]

    result = subprocess.run(args, text=True)
    print("-" * 40)
