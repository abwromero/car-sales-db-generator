Mock Sales Database with Docker, Faker, JupyterLab, and Postgres

I. Introduction
This project intends to create a mock sales database with the use of Faker and Postgres. The fake data generated intends to represent total car sales in the Philippines for a given period. That said, selected columns for this database intends to mimic values similar or the same with ones from the Philippines. These are details such as vehicles, provinces, cities, street addresses, companies, banks, mobile numbers, etc. This makes the data generated as close to real values as possible.

II. Pre-requisites
* Ensure Docker and Docker Compose are installed

III. Installation
* Run the following command to create a volume for the Postgres database:
    * “docker volume create faker-volume”
* Run the following command to create a network for Postgres and JupyterLab:
    * “docker network create faker-network”
* Optional: In case you want to connect this as a mock source for another project in Docker, connect the Postgres database to another network. In my use case, this project serves as a mock source for another project of mine. The other network this project is connected to is called “de-network”. Please see the Docker Compose file for reference on how this was built.
* Clone the Git repository for this project
* Set the working directory inside the cloned folder
* Run the following command:
    * “docker-compose up”

IV. Notes About Docker Volumes
It can be seen from the Docker Compose file that there are volumes that are connected to folders from the host computer, while there are others that just have volume names. Here is a brief explanation of the two:
* Named Volumes
    * These are volumes that are located inside Docker and cannot be accessed outside the Docker environment.
* Bind Mounts
    * These are volumes connected to folders in the host computer. These are accessible to both the host computer and the Docker environment.

For the sake of simplicity, bind mounts are helpful when scripts are developed, such as ones for SQL and Python. Modified scripts are instantly reflected inside Docker during development. Moreover, this is easier for developers to test their scripts. On the other hand, if the data does not have to be accessed from the outside the Docker environment, such as database volumes or logs, it is better to assign these to Named Volumes.

It is important to point out that during production, all scripts required by the applications should be built inside the image. This ensures and respects the essence of containerization as all required scripts will always be with the application wherever it is run. The applications are guaranteed to run no matter which host computer these Docker images are running on.

V. Access to the Applications
* JupyterLab
    * http://localhost:8888
    * To get the token to access JupyterLab, do the following:
        * Run the following command and get the container ID of JupyterLab:
            * “docker ps”
        * Run the following command  with the container ID of JupyterLab:
            * “docker exec -it CONTAINER_ID /bin/bash”
        * After entering the command above, you will enter the bash environment for JupyterLab, run the following command:
            * “jupyter server list”
        * The output should give one service running. Copy the hash-looking token from the output and paste it in the token below the localhost:8888 landing page and assign your password.
* Postgres through pgAdmin
    * http://localhost:5040
    * Login with the following details:
        * Username/Email: faker@faker.com
        * Password: password
    * To connect pgAdmin to Postgres, click “Add New Server” in Quick Links. Enter the following:
        * In the General tab:
            * Name: faker
        * In the Connection tab:
            * Host name/address: faker-db
            * Port: 5432
            * Maintenance database: postgres
            * Username: faker
            * Password: faker

VI. Running the Python script and viewing the results
* Inside JupyterLab, do the following:
    * On the left side, click “faker_cars.ipynb”.
    * Restart the kernel and run the entire script.
    * At this point, the results should have been sent to Postgres
* Go to the pgAdmin page:
    * Go to the “faker” database
    * Find and click the “raw” schema
    * Look for the table “raw_values” and inspect the data
        * If the Python script was not modified, there should be 5000 rows values generated with fake values.

VII. Shutting Down the Containers
* If there are no applications that need to take the generated data in Postgres, you can turn off the containers with the following command:
    * “docker-compose down”
* If you want to delete the generated data inside Postgres while shutting down, you can run the following command:
    * “docker-compose down -v”

VIII. Final Notes
* If there are errors or areas this project can improve on, please let me know.

XI. References

Faker documentation: https://faker.readthedocs.io/en/master/

Loading Data from Python to Postgres: https://hakibenita.com/fast-load-data-python-postgresql 

Purpose of "seek" in loading data from Python to Postgres: https://stackoverflow.com/questions/55181331/bulk-insert-using-postgresql-copy-from-psycopg2-and-stringio

Use of copy_expert instead of copy_from:
https://github.com/psycopg/psycopg2/issues/1294

Postgres COPY syntax:
https://www.postgresql.org/docs/current/sql-copy.html

List of vehicles source (vehicle data copied and processed manually):
https://www.carguide.ph/p/philippine-car-price-guide-2016_18.html
