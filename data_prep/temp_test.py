import pandas as pd

df_etf = pd.read_csv("etf_scraping.csv")
list_etf = df_etf.to_dict('records')

df_holdings = pd.read_csv("holdings.csv")
list_holdings = df_holdings.to_dict('records')

for holding in list_holdings:
    name = str(holding['Holding Ticker'])
    name = name.replace(';', ' ')
    if ':' in name and '(' in name:
        split = name.split(' (')
        ticker_part = split[-1]
        long_name = split[0]
        if len(split) == 3:
            long_name = split[0] + ' (' + split[1]
        long_name = long_name.replace(':', ' ')
        if long_name.isupper():
            holding['r_name'] = long_name.title()
        else:
            holding['r_name'] = long_name
        ticker = ticker_part.split(':')[1]
        ticker = ticker.rstrip(ticker[-1])
        ticker = ticker.replace('*', '')
        holding['ticker'] = ticker
    else:
        name = name.replace(':', ' ')
        holding['r_name'] = name
        holding['ticker'] = ''

# with open("holdings_new.csv", "w") as file:
#     file.write("Matching Name;Holding;Ticker\n")
#     for holding in list_holdings:
#         file.write(f"{holding['Holding']};{holding['r_name']};{holding['ticker']}\n")


for etf in list_etf:
    finds = list(filter(lambda item: item['Holding'] == etf['Holding'], list_holdings))
    if len(finds) == 0:
        etf['Holding Ticker'] = ''
    else:
        etf['Holding'] = finds[0]['r_name']
        etf['Holding Ticker'] = finds[0]['ticker']


with open("etf_new.csv", "w") as file:
    file.write("Ticker;Title;Link;Holding Ticker;Holding;Weight\n")
    for etf in list_etf:
        file.write(f"{etf['Ticker']};{etf['Title']};{etf['Link']};"
                   f"{etf['Holding Ticker']};{etf['Holding']};{etf['Weight']}\n")