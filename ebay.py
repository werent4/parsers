import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
#&_pgn=1
#search_url = 'https://www.ebay.com/sch/i.html?_nkw=smartphones'
def connect(url):
    response = requests.get(url)

    return response

def get_prod_list(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    product_list = soup.find_all('li', {'class' : 's-item'})

    return product_list


def get_data(product_list, data = []):

    for product in product_list:
        title = product.find('div', {'class' : 's-item__title'}).text

        price = product.find('span', {'class' : 's-item__price'}).text

        sold = str(product.find('span', {'class' : 's-item__dynamic s-item__quantitySold'}))
        match = re.search(r'(\d{1,3}(?:,\d{3})*)(\+)? sold', sold)
        if match:
            sold_text  = match.group(0)[0:-4]

        else:
            sold_text = sold

        data.append({'Title': title, 'Price': price, 'Sold': sold_text})

    return data

def data_to_excel(data):
    ebay_data = pd.DataFrame(data)
    output_file = 'ebay_data.xlsx'
    ebay_data.to_excel(output_file, index=False)  # write into Excel

def main():
    page = 1
    while True:
        url = 'https://www.ebay.com/sch/i.html?_nkw=smartphones' + f'&_pgn={page}'
        response = connect(url)
        prod_list = get_prod_list(response)

        if prod_list == []:
            break

        data = get_data(prod_list)

        print(f'finised with page :{page}')
        page += 1

    data_to_excel(data)


if __name__ == '__main__':
    main()
