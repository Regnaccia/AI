from pathlib import Path

def generate_id() -> str:
    print("generating ID")
    file_path = Path(__file__).parent.parent / "Export" / "project_id.txt"
    file_path.parent.mkdir(parents=True, exist_ok=True) # Crea la cartella AI se non esiste
    print(file_path)
    if file_path.exists():
        print("file exist")
        content = file_path.read_text().strip().splitlines()
        last_id = int(content[-1]) if content else -1
        new_id = str(last_id + 1)
        # Usiamo 'a' per appendere il nuovo ID
        with open(file_path, "a") as f:
            f.write(f"\n{new_id}")
        return new_id
    else:
        file_path.write_text("0")
        return "0"