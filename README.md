# Truecar
### The Truecar Project aims to scrape data from the Truecar website -https://www.truecar.com/used-cars-for-sale/listings/?buyOnline=true- (via Beautiful Soup), where cars are on sale online, and then extract desired data in order to use through 2 objectives: 
### 1) Save specific data about cars (Name, Model, Mile, City and Price) on MySQL Database, more importantly data must not be repeatitive.
### 2) In the second version of the project, this data will be saved in a CSV file in order to train a Machine Learning model and use it for predicting a car's Price by inserting the other four piece of information.

#### Description:
Code is written in Python using PyCharm, and in this Application there are various libraries that I used...
1. requests: to make a HTTP Request with the website address
2. BeautifulSoup from bs4: to read and fetch the data I requested 
3. connector from mysql: to connect to the MySQL Database
4. errorcode from mysql.connector: to handle the errors of the database connection and user identification
5. re: to use regex for manipulating the data that is fetched from the website
6. csv: to work with the csv file that I mentioned earlier
7. tree from sklearn

#### Installation instructions:
1. To use python I have tried coding with PyCharm which has been easy and straightforward. Here is the link to download and install: https://www.jetbrains.com/pycharm/download/?section=windows / https://www.jetbrains.com/help/pycharm/installation-guide.html#snap
2. In order to use the libraries just import them as I did in the code.

#### Errors and Problems:
1. In the ML part, when I insert the entry data and Enter for the output, I guess there is a problem with how the data is saved in the csv file.
