# Crypto-Wallet

## Overview 

Welcome to Crypto Wallet! This project is all about helping you understand your crypto journey. Dive into your transaction history, track your portfolio, and make informed decisions in the dynamic crypto world.

## Features

- **Real-time Crypto Price**
- **Wallet Performance:** Check out how well you're doing given the current crypto prices.
- **Purchase Scenarios:** Calculeta new average prices after buying certain amounts of the crypto, given its current price.

***For now!***

## Getting Started

1. Clone the repository:

    ```bash
    git clone https://github.com/AndreiCanovas/crypto-wallet.git
    ```

2. install the requirements with:

    ```python
    pip install -r requirements_dev.txt
    ```

3. Save your data orders.csv file at:

    ```
    crypto-wallet
    │
    ├── data
    │   ├── orders.csv <-- Your order's history!
    │   └── .gitkeep
    .
    ```

    orders.csv metadata:

    | data | moeda | preco | quantidade | liquido |
    | :--: | :---: | :---: | :--------: | :-----: |
    | 2023-11-20 | ETH | 9.61 | .001 | .00099 |
    | ... | ... | ... | ... | ... |
    | 2023-01-01 | ETH | 6.34 | .001 | .00099 |

    where:

    - **data:** Date when the order was executed.
    - **moeda:** The cryptocurrency (symbol) bought.
    - **preco:** Price in Brazilian reais (symbol: BRL).
    - **quantidade:** Total bought.
    - **liquido:** Total that remains (crypto) after order taxes and other discounts.

4. Run the wallet:

    ```bash
    python wallet
    ```