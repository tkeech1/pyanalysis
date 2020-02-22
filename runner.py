from pyretriever.retriever import get_yahoo_data

data = get_yahoo_data(symbols=["SPY"], start_date="2020-01-01", end_date="2020-01-02",)

print(data)
