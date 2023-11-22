import yaml
import pandas as pd
from typer import Typer, Argument
from utils import get_summary


app = Typer()

@app.command()
def main(xrp: float = Argument(None)):
    
    with open('wallet/config.yml') as file:
        config = yaml.safe_load(file)
    
    orders_path = config['orders_path']
    
    orders = pd.read_csv(orders_path)

    orders['quantidade_brl'] = orders['quantidade'] * orders['preco']
    orders['liquido_brl'] = orders['liquido'] * orders['preco']

    total_xrp = orders['liquido'].sum()
    total_brl = orders['liquido_brl'].sum()
    preco_med = total_brl / total_xrp

    get_summary(preco_med, total_brl, total_xrp, xrp)
    
if __name__ == '__main__':
    app()
