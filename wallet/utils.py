import requests
import pandas as pd
from typing import Union
from datetime import datetime, timedelta

from rich import print
from rich.rule import Rule
from rich.table import Table


def make_rich_table(df: pd.DataFrame) -> Table:
    """Create a rich-text table representation from a Pandas DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame to be converted into a rich-text table.

    Returns
    -------
    Table
        A rich-text table representation of the input DataFrame.
    """

    df_str = df.fillna("N/A").applymap(str)
    
    # Create a Rich Table
    table = Table(show_header=True, header_style="bold")

    # Add columns to the table
    for column in df_str.columns:
        table.add_column(column, justify='right')

    # Add rows to the table
    for _, row in df_str.iterrows():
        table.add_row(*row)
        
    return table

def get_crypto_historical_data(crypto_symbol: str, days=7):
    """_summary_

    Parameters
    ----------
    crypto_symbol : str
        _description_
    days : int, optional
        _description_, by default 7

    Returns
    -------
    _type_
        _description_
    """
    
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_symbol}/market_chart"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    params = {
        "vs_currency": "brl",
        "from": int(start_date.timestamp()),
        "to": int(end_date.timestamp())
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        prices = data["prices"]
        price_data = {
            datetime.fromtimestamp(item[0] / 1000).strftime('%Y-%m-%d'): item[1] 
            for item in prices
        }
        return price_data
    else:
        print("Error: Unable to fetch data.")
        return None
    
def get_crypto_data(crypto_symbol: str) -> Union[float, None]:
    """Retrieve current price data for a specified cryptocurrency 
    in Brazilian Real (BRL) from the CoinGecko API.

    Parameters
    ----------
    crypto_symbol : str
        The symbol or identifier of the cryptocurrency for which to fetch data.

    Returns
    -------
    Union[float, None]
        The current price of the specified cryptocurrency in BRL. 
        Returns None if the data cannot be fetched.

    Notes
    -----
    This function utilizes the CoinGecko API to retrieve real-time price information
    for the specified cryptocurrency.

    Example
    -------
    >>> get_crypto_data("bitcoin")
    340000.0
    """
    
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": crypto_symbol,
        "vs_currencies": "brl",
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if crypto_symbol in data:
            return data[crypto_symbol]
        else:
            return None
    else:
        print("Error: Unable to fetch data.")
        return None
    
def get_new_preco_medio(
    total_brl_order: float, preco_med: float, total_xrp: float, 
    preco_med_order: float =None, taxa_order: str =.993
) -> dict:
    """Calculate the new average price (preco_medio) and total XRP holdings after a new order.

    Parameters
    ----------
    total_brl_order : float
        The total amount in BRL spent on the new order.
    preco_med : float
        The current average price (preco_medio) of XRP holdings.
    total_xrp : float
        The total amount of XRP holdings before the new order.
    preco_med_order : float, optional
        The average price of XRP in BRL for the new order. 
        If not provided, it is fetched using the 'ripple' symbol, by default None.
    taxa_order : str, optional
        The transaction fee or tax rate for the new order, by default 0.993.

    Returns
    -------
    dict
        A dictionary containing the new total XRP holdings ('total_xrp_order') 
        and the updated average price ('new_preco_med').
    """
   
    if not preco_med_order:
        preco_med_order = get_crypto_data('ripple')
        preco_med_order = preco_med_order['brl']
        
    total_xrp_order = (total_brl_order * taxa_order) / preco_med_order

    return {
        'total_xrp_order': total_xrp_order,
        'new_preco_med': (
            ((preco_med * total_xrp) + (preco_med_order * total_xrp_order)) / 
            (total_xrp + total_xrp_order)
        )
    }

def get_total_brl_order(
    preco_med_target: float, preco_med: float, total_xrp: float, 
    preco_med_order: float =None, taxa_order: float =.993
) -> float:
    """Calculate the total amount in BRL needed to reach a target average price.

    Parameters
    ----------
    preco_med_target : float
        The target average price (preco_medio) you want to achieve.
    preco_med : float
        The current average price (preco_medio) of XRP holdings.
    total_xrp : float
        The total amount of XRP holdings.
    preco_med_order : float, optional
        The average price of XRP in BRL for a new order. 
        If not provided, it is fetched using the 'ripple' symbol, by default None.
    taxa_order : float, optional
        The transaction fee or tax rate for the new order, by default 0.993.

    Returns
    -------
    float
        The total amount in BRL needed to reach the target average price.
    """

    if not preco_med_order:
        preco_med_order = get_crypto_data('ripple')
        preco_med_order = preco_med_order['brl']

    total_xrp_order = (
        ((preco_med * total_xrp) - (preco_med_target * total_xrp)) / 
        (preco_med_target - preco_med_order)
    )

    return (total_xrp_order * preco_med_order) / taxa_order

def get_summary(preco_med: float, total_brl: float, total_xrp: float, xrp=None):
    """Generate a summary analysis of XRP wallet performance and potential buying scenarios.

    Parameters
    ----------
    preco_med : float
        The current average price (preco_medio) of XRP holdings.
    total_brl : float
        The total amount in BRL spent on XRP.
    total_xrp : float
        The total amount of XRP holdings.
    xrp : float, optional
        The current price of XRP in BRL. If not provided, 
        it is fetched using the 'ripple' symbol, by default None.
    """

        
    if not xrp:
        xrp = get_crypto_data('ripple')
        xrp = xrp['brl']

    # analise de performance atual:
    lucro_perc = (xrp/preco_med) - 1
    if lucro_perc > 0:
        c = 'green b'
    else:
        c = 'red b'

    # analise de compra de novos montantes pelo preco atual:
    l_montante = [m for m in range(500, 5500, 500)]
    l_preco_med = pd.DataFrame(
        [get_new_preco_medio(m, preco_med, total_xrp, xrp) for m in l_montante], 
        index=l_montante
    )
    l_preco_med['perc_melhoria'] = abs(((l_preco_med['new_preco_med'] - preco_med) / preco_med) * 100)
    
    l_preco_med = round(l_preco_med.reset_index().rename({'index': 'total_BRT'}, axis=1), 2)
    
    table = make_rich_table(l_preco_med)
    total = round(total_brl * (1 + lucro_perc), 2)
    lucro = round(total_brl * lucro_perc, 2)
    rendimento = round(lucro_perc * 100, 2)
    
    print('\n', Rule('XRP Wallet'), '\n')
    print(f'[white]XRP (base): {xrp:>16} [BRL][/white]')
    print("_" * 35, '\n')
    print(f'[white]Preço Médio: {round(preco_med, 2):>15} [BRL][/white]')
    print(f'. total:[white]{total:>20}[/white] [BRL]')
    print(f'. lucro:[{c}]{lucro:>20}[/{c}] [BRL]')
    print(f'. rendimento:[{c}]{rendimento:>15}[/{c}] [ % ]')
    print("_" * 35, '\n')
    print(f'[white]Total XRP: {round(total_xrp, 2):>17} [XRP][/white]')
    print(f'[white]Total Comprado: {round(total_brl, 2):>12} [XRP][/white]')
    print(f'\n\n[b]Comprando XRP (atual):\n[/b]')
    print(table)
    print(Rule(), '\n')
