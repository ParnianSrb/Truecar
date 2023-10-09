import requests
from bs4 import BeautifulSoup
from mysql import connector
from mysql.connector import errorcode
import re

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

    my_cursor = cnx.cursor()

    # my_cursor.execute('CREATE DATABASE IF NOT EXISTS truecar ')
    '''my_cursor.execute('CREATE TABLE IF NOT EXISTS cars (name VARCHAR(100) NOT NULL,'
                      'model SMALLINT NOT NULL,'
                      'miles FLOAT NOT NULL,'
                      'city VARCHAR(50) NOT NULL,'
                      'price FLOAT NOT NULL)')'''
# ----------------------------------------------------------------------------------------------------------------------

    response = requests.get('https://www.truecar.com/used-cars-for-sale/listings/?buyOnline=true')
    print(response)

    soup = BeautifulSoup(response.text, 'html.parser')

    # find all divisions with {'data-test': 'cardContent'} containing 1 Car card
    div_tags = soup.find_all('div', attrs={'data-test': 'cardContent'})
    # print(type(div_tags), div_tags)

    # make a list of Cars - each item is a list of data of 1 car
    cars_list = []

    # function to delete comma from the data
    def delete_comma(stm):
        return re.sub(',', '', stm)

    index = 0
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

        cars_list.append(car_info)

    '''for car in cars:
        print(f'\nCAR INFO: {car}')
        for i in range(0, 5):
            print(car[i])'''
# ----------------------------------------------------------------------------------------------------------------------

    for car in cars_list:
        my_cursor.execute('INSERT INTO truecar.cars (name, model, miles, city, price) VALUES (%s, %s, %s, %s, %s)',
                          (car[0], car[1], car[2], car[3], car[4]))
        cnx.commit()

    my_cursor.execute('SELECT * FROM cars')
    data = my_cursor.fetchall()
    for row in data:
        print(f'{row}\n')

# -------------------------------------------------
    # Create csv file
    f = open('cars' + '.csv', 'w')

    for row in data:
        f.write(','.join(str(r) for r in data) + '\n')

    f.close()
    print(str(len(data)) + ' rows written successfully to ' + f.name)


# ----------------------------------------------------------------------------------------------------------------------

except connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with Username or Password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cnx.commit()
    cnx.close()

# first make the table, then alter with primary key, then insert data

# the same as version project_1.1 with the change of the rows in the try statement and the bs

# not using PK: my_cursor.execute("ALTER TABLE cars ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")


