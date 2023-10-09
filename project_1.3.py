import requests
from bs4 import BeautifulSoup
from mysql import connector
from mysql.connector import errorcode
import re

# THIS IS THE FINAL VERSION OF SYSTEM2

config = {
    'user': 'root',
    'password': '12345',
    'host': '127.0.0.1',
    'database': 'truecar',
    'raise_on_warnings': True
}

# To handle connection errors, use the try statement and catch all errors using the errors.Error exception:
try:
    cnx = connector.connect(**config)
    print('Connected to MySql Server.')

    my_cursor = cnx.cursor(buffered=True)

    '''my_cursor.execute('CREATE DATABASE IF NOT EXISTS truecar ')
    cnx.commit()'''

    '''my_cursor.execute('CREATE TABLE IF NOT EXISTS cars (name VARCHAR(100) NOT NULL,'
                      'model SMALLINT NOT NULL,'
                      'miles FLOAT NOT NULL,'
                      'city VARCHAR(50) NOT NULL,'
                      'price FLOAT NOT NULL,'
                      'UNIQUE (name, model, miles, city, price))')
    cnx.commit()'''

    # ------------------------------------------------------------------------------------------------------------------

    response = requests.get('https://www.truecar.com/used-cars-for-sale/listings/?buyOnline=true')
    print(response)
    soup = BeautifulSoup(response.text, 'html.parser')

    # find the last pages number
    a = soup.find_all('a', attrs={'data-test': 'paginationLink'})
    last_page = a[9].text
    print(last_page)
    # ---------------------------------------------------------------
    # we use the current soup for only the first round of the loop
    # loops through all pages
    for i in range(1, int(last_page)):
        mian_url = 'https://www.truecar.com/used-cars-for-sale/listings/?buyOnline=true'
        url = mian_url + f'&page={i}'
        response = requests.get(url)
        print(f'------ THIS IS THE RESPONSE OF THE NEXT PAGE: {response} -------\n')
        soup = BeautifulSoup(response.text, 'html.parser')

        # find all divisions with {'data-test': 'cardContent'} containing 1 Car card
        div_tags = soup.find_all('div', attrs={'data-test': 'cardContent'})
        # print(type(div_tags), div_tags)

        # make a list of Cars - each item is a list of data of 1 Car
        cars = []

        # function to delete comma from the data
        def delete_comma(stm):
            return re.sub(',', '', stm)

        # for each main division
        for div in div_tags:
            car_info = []

            # find the data with this attr - delete the comma - add it to the car info
            car_name = delete_comma(div.findChild(attrs={'class': 'truncate'}).text)
            car_info.append(car_name)

            car_model = delete_comma(div.findChild(attrs={'class': 'vehicle-card-year text-xs'}).text)
            car_info.append(car_model)

            car_mile = delete_comma(div.findChild(attrs={'data-test': 'vehicleMileage'}).text)
            # grab the numbers part of the miles
            car_mile = re.findall(r'(\d*) miles', car_mile)
            car_info.append(car_mile[0])

            car_city = delete_comma(div.findChild(attrs={'data-test': 'vehicleCardLocation'}).text)
            car_info.append(car_city)

            car_price = delete_comma(div.findChild(attrs={'data-test': 'vehicleCardPricingBlockPrice'}).text)
            # grab the price number
            car_price = re.findall(r'\$(\d*$)', car_price)
            car_info.append(car_price[0])

            cars.append(car_info)

        '''for car in cars:
            print(f'\nCAR INFO: {car}')
            for i in range(0, 5):
                print(car[i])'''
        # --------------------------------------------------------

        for car in cars:
            my_cursor.execute('INSERT INTO truecar.cars (name, model, miles, city, price) VALUES (%s, %s, %s, %s, %s)',
                              (car[0], car[1], car[2], car[3], car[4]))
            cnx.commit()

        my_cursor.execute('SELECT * FROM cars')
        cnx.commit()
        data = my_cursor.fetchall()
        print(f'All Rows from The First Page until The {i} Page Number:\n')
        for row in data:
            print(f'{row}\n')
        print('******** END OF THIS PAGE  ********')

        """# the soup must change at the end of the loop, because we have the first page at the top, and we need it
        # change the url and get data from each page of the website
        mian_url = 'https://www.truecar.com/used-cars-for-sale/listings/?buyOnline=true'
        url = mian_url + f'&page={i}'
        response = requests.get(url)
        print(f'------ THIS IS THE RESPONSE OF THE NEXT PAGE: {response} -------\n')
        soup = BeautifulSoup(response.text, 'html.parser')"""

# ----------------------------------------------------------------------------------------------------------------------

except connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with Username or Password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cnx.close()

# first make the table, then alter with primary key, then insert data
# finds the number of the last page and loops through
# we made the DB not to accept repetitive data using: UNIQUE (name, model, miles, city, price)
# do not need a csv here

# not using PK: my_cursor.execute("ALTER TABLE cars ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")
