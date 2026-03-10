from pathlib import Path

def get_dataset_folders(dataset_root="dataset"):
    root = Path(dataset_root)
    if not root.exists():
        return []
    return [p.name for p in root.iterdir() if p.is_dir()]
