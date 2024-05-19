import pandas as pd
from bs4 import BeautifulSoup
import warnings
import requests

COMPANY_NAME = 'SHOP'

# Begin with income_statement

# Send a GET request to the URL
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
}

income_statement_url = f'https://finance.yahoo.com/quote/{COMPANY_NAME}/financials?p={COMPANY_NAME}'

page = requests.get(income_statement_url, headers=headers)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(page.text, 'html.parser')

# ## Find relevant data structures for financials
div_list = []

# Find all HTML data structures that are divs
for div in soup.find_all('div'):
    # Get the contents and titles
    div_list.append(div.string)

    # Prevent duplicate titles
    if not div.string == div.get('title'):
        div_list.append(div.get('title'))

# ## Filter out irrelevant data
# Exclude 'Operating Expenses' and 'Non-recurring Events'
div_list = [incl for incl in div_list if incl not in
            ('Operating Expenses', 'Non-recurring Events', 'Expand All')]

# Filter out 'empty' elements
div_list = list(filter(None, div_list))

# Filter out functions
div_list = [incl for incl in div_list if not incl.startswith('(function')]

# Sublist the relevant financial information
income_list = div_list[13: -5]

# Insert "Breakdown" to the beginning of the list to give it the proper stucture
income_list.insert(0, 'Breakdown')
# ## Create a DataFrame of the financial data

# Store the financial items as a list of tuples
income_data = list(zip(*[iter(income_list)] * 6))

# Create a DataFrame
income_df = pd.DataFrame(income_data)

# Make the top row the headers
headers = income_df.iloc[0]
income_df = income_df[1:]
income_df.columns = headers
income_df.set_index('Breakdown', inplace=True, drop=True)

warnings.warn('Amounts are in thousands.')

print(income_df)

