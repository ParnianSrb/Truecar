## A Project to fetch unrepeated data from a Website and save the desired parts in a Database, finally use this stored data for Machine Learning purposes.
#### Working with the cars being on sale online with various features from Truecar website: 
#### https://www.truecar.com/used-cars-for-sale/listings/?buyOnline=true

#### Due to learning and practicing objectives I have used two files for testing, namely "practice-csv.py" and "practice2.py", which may seem useless for readers.
#### The "project_1.3.py" file does not include the Machine Learning part, whereas "project_2.0.py" file does include ML, and it is also the final version.

### Description
1. The goal is to fetch the data of each car on sale, which are Name, Model, Miles(traveled distance), City and Price.
2. The fetching process is done using "BeautifulSoup" from "bs4" library. I sent a request, used the text option of the response -using html parser- and took relevant divisions of the HTML code to find all of the data that is needed with desired attributes of that content.
3. This data should not be repeated, in that I have used the combination of all the five fields (name, model, miles, city, price) as a Unique Parameter in the structure of the Database.
4. Each time this code is run, it should add the data to the Database only if it is new.
5. I have stored data in a MySQL Database named "truecar", which owns only one table named "cars" -using MySQL Python Connector.
6. To handle Database connection errors I have used the try/except method, catching all errors by "errorcode" from "mysql.connector" library.
7. In order to use the data later for training a Machine Learning model -using Decision Tree Classifier-, I have fetched the data from the "truecar" Database and saved them in a CSV file using "csv" library.
8. Then, there is the "machine_learning()" function, which takes the CSV file as well as the string that is the user's input and converts this input string to a readable format for itself (I have used Regex for this part and imported "re" librray at the top of the code) and then predicts the "Price" of that specific car by using Name, Model, Miles and City.
