from pathlib import Path
import pandas as pd

def pd_dataloader(path:str, delimiter:str=';'):
    """ Call example:
            from src.dataloader.dataloader import pd_dataloader
            df = pd_dataloader(path='data/labels.csv')
            df
        """
    root = Path(__file__).parents[2]
    data_path = root / path

    dataframe: pd.DataFrame = pd.read_csv(
            filepath_or_buffer=data_path,
            delimiter=delimiter)
    return dataframe

