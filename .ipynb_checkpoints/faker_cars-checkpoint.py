#!/usr/bin/env python
# coding: utf-8

# ### Fake Vehicle Sales Generator
# This project intends to create random sales data for vehicles sold in the Philippines. The Faker package will be used to generate fake values. The fake values will be "adjusted" for the Philippine setting through the use of localized providers in Faker and the creation of lists representing vehicles and banking institutions in the country.
# 
# Project References:
# 
# Faker documentation: https://faker.readthedocs.io/en/master/
# 
# Loading Data from Python to Postgres: https://hakibenita.com/fast-load-data-python-postgresql
# 
# Purpose of "seek" in loading data from Python to Postgres: https://stackoverflow.com/questions/55181331/bulk-insert-using-postgresql-copy-from-psycopg2-and-stringio
# 
# Use of copy_expert instead of copy_from:
# https://github.com/psycopg/psycopg2/issues/1294
# 
# Postgres COPY syntax:
# https://www.postgresql.org/docs/current/sql-copy.html

# Import necessary Python packages

# This package will be used to open the .csv file containing vehicle data.
from csv import reader

# This package will create a Faker instance to generate random values.
from faker import Faker

# These packages will help create customized random values.
from faker.providers import BaseProvider, DynamicProvider

# These packages will connect this Python script to an existing Postgres database.
from psycopg2 import connect, sql

# This package will help customize the output to emit null values with Faker data.
import random

# This will create a string file that will load the Faker values to a Postgres database.
from io import StringIO

# Load the .csv file containing vehicle data that will be used to generate sales data.
# Data source: https://www.carguide.ph/p/philippine-car-price-guide-2016_18.html
# Data source extracted on 23 June 2023. Data was extracted and modified manually.
with open('./reference-files/vehicle-models.csv') as file:
    read_file = reader(file)
    cars = list(read_file)

# Extract the details of the vehicles along with the price. Load the extracted data in a list.
cars_sum = []
for list in cars:
    cars_sum.append(list[2] + ' ' + list[3])

# Create a list of banks in the Philippines with different namings to mimic real data inputs.
bank_list = ["BDO", "Banco de Oro",
             "MB", "Metrobank",
             "BPI", "Bank of the Philippine Islands",
             "LBP", "Land Bank of the Philippines", "Land Bank",
             "DBP", "Development Bank of the Philippines", "Development Bank",
             "PNB", "Philippine National Bank", 
             "RCBC", "Rizal Commercial Banking Corporation",
             "UBP", "Union Bank of the Philippines",
             "Chinabank", 
             "AUB", "Asia United Bank", "Asia United",
             "In-house"]

# Create a list of payment terms for the vehicles purchased. Values will be in both months and years.
payment_terms = ["12", "24", "36", "48", "60", "1", "2", "3", "4", "5", "6"]

# Create a list of vehicle colors with some values containing wrong spelling.
car_colors = ["White", "white",
              "Black", "black", "blk",
              "Gray", "gray", "Grey", "gray",
              "Silver", "silver",
              "Red", "red",
              "Green", "green",
              "Blue", "blue", "blu",
              "Orange", "orange",
              "Yellow", "yellow", "ylw",
              "Teal", "Sky Blue", "Skyblue", "skyblue"]

# Create a Faker instance with some outputs resembling Philippines-based data.
f = Faker(['en_PH'])

# Create a Faker provider to emit random values based from the cars_sum list.
car_sold = DynamicProvider(
    provider_name='car_sold',
    elements=cars_sum
)

# Add the provider to Faker.
f.add_provider(car_sold)

# Create a Faker provider to emit random bank names based from bank_list.
bank_provider = DynamicProvider(
    provider_name='bank',
    elements=bank_list
)

# Add the provider to Faker.
f.add_provider(bank_provider)

# Create a Faker provider to emit random payment periods based from payment_terms list.
payment_terms_provider = DynamicProvider(
    provider_name='terms',
    elements=payment_terms
)

# Add the provider to Faker.
f.add_provider(payment_terms_provider)

# Create a Faker provider to emit random vehicle colors based from cars_color list.
car_colors_provider = DynamicProvider(
    provider_name='car_color',
    elements=car_colors
)

# Add the provider to Faker.
f.add_provider(car_colors_provider)

# Create a Faker provider to generate random driver's license numbers.
class LicenseProvider(BaseProvider):
    def license_number(self):
        return f.bothify(text="?##-##-######", letters="ABCDEFGHIJKLMNOP")

# Add the provider to Faker.
f.add_provider(LicenseProvider)

# Connect to the Postgres database with the following data.
# Login credentials were based on the data entered in the docker-compose file for Postgres.
# The "connect" function comes from the psycopg2 package.
conn = connect(
    dbname='faker',
    user='faker',
    host='faker-db',
    password='faker'
)

# Connect to the database by creating a cursor from the connection.
cursor = conn.cursor()

# Create 500,000 rows of random data that will mimic car sales.
target_values=500000

# Set the null values per column at 5 percent.
percentage_of_null_values=0.05

# Create a list that will show the distribution of non-null and null values per column.
weight_vs_null_values = [1-percentage_of_null_values,percentage_of_null_values]

# Create an instance of StringIO for the .csv file that will be loaded in the database.
raw_data_csv_file = StringIO()

# Create a for-loop with the set target_values to generate a .csv file with 5,000 entries.
for row in range(target_values):
    name = random.choices([f.name(), "null"], weights=weight_vs_null_values)[0]
    license = random.choices([f.license_number(), "null"], weights=weight_vs_null_values)[0]    
    num = random.choices([f.mobile_number(), "null"], weights=weight_vs_null_values)[0]
    email = random.choices([f.ascii_free_email(), "null"], weights=[1-percentage_of_null_values,percentage_of_null_values])[0]
    company = random.choices([f.company(), "null"], weights=[1-percentage_of_null_values,percentage_of_null_values])[0]
    street = random.choices([f.street_address(), "null"], weights=[1-percentage_of_null_values,percentage_of_null_values])[0]
    city = random.choices([f.province_lgu(), "null"], weights=[1-percentage_of_null_values,percentage_of_null_values])[0]
    province = random.choices([f.province(), "null"], weights=[1-percentage_of_null_values,percentage_of_null_values])[0]
    date = random.choices([f.date_this_year(), "null"], weights=[1-percentage_of_null_values,percentage_of_null_values])[0]
    bank = random.choices([f.bank(), "null"], weights=[1-percentage_of_null_values,percentage_of_null_values])[0]

    # Since terms is a SMALLINT data type, a null value represented by the value 999 will be inserted instead.
    terms = random.choices([f.terms(), "999"], weights=[1-percentage_of_null_values,percentage_of_null_values])[0]
    
    car = random.choices([f.car_sold(), "null"], weights=[1-percentage_of_null_values,percentage_of_null_values])[0]
    color = random.choices([f.car_color(), "null"], weights=[1-percentage_of_null_values,percentage_of_null_values])[0]
    plate_num = random.choices([f.automobile_license_plate(), "null"], weights=[1-percentage_of_null_values,percentage_of_null_values])[0]

# Create a string with the values above delimited by the pipe symbol (|).
# A line break will also be included at the end of the line to create another line for the next generated value.
    raw_data_csv_file.write("|".join((name,
                                      license,
                                      num,
                                      email,
                                      company,
                                      street,
                                      city,
                                      province,
                                      str(date),
                                      bank,
                                      terms,
                                      car,
                                      color,
                                      plate_num)) + '\n')

# Move the cursor of the StringIO file at the beginning for the values to load properly on the Postgres database.
raw_data_csv_file.seek(0)

# Copy the generated data to the Postgres database.
cursor.copy_expert(sql="""
                        COPY raw.raw_values(name,
                                            license,
                                            num,
                                            email,
                                            company,
                                            street,
                                            city,
                                            province,
                                            date,
                                            bank,
                                            terms,
                                            car,
                                            color,
                                            plate)
                        FROM STDIN
                        WITH
                        (FORMAT CSV,
                        DELIMITER '|')
                        """, file=raw_data_csv_file)

# Commit the actions inside the database.
conn.commit()

# Close the connection to Postgres.
conn.close()

# Close the StringIO instance.
raw_data_csv_file.close()

