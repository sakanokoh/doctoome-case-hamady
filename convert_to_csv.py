from pathlib import Path
import pandas as pd

sortie = Path("data_csv")
sortie.mkdir(exist_ok=True)

for fichier in Path("data").glob("*.parquet"):
    df = pd.read_parquet(fichier)
    df.to_csv(sortie / f"{fichier.stem}.csv", index=False)
    print(f"{fichier.stem}: {df.shape[0]} lignes, {df.shape[1]} colonnes")