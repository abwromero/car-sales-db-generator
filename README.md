Mock Sales Database with AWS, Terraform, Docker, Faker, JupyterLab, and Postgres

I. Introduction

This project intends to create a mock sales database in AWS RDS with the use of Faker and Postgres. The fake data generated intends to represent total car sales in the Philippines for a given period. That said, selected columns for this database intends to mimic values similar or the same with ones from the Philippines. These are details such as vehicles, provinces, cities, street addresses, companies, banks, mobile numbers, etc. This makes the data generated as close to real values as possible. TAKE NOTE THAT THIS PROJECT WILL INCUR COSTS THROUGH THE USE OF AWS.

II. Pre-requisites
* Ensure Docker and Docker Compose are installed
* AWS Access Key and Secret Access Key

III. Installation
* Clone the Git repository for this project
* Set the working directory inside the cloned folder
* Run the following command:
    * “docker compose up”

IV. Implementation of AWS applications with Terraform

AWS applications need to be setup, specifically a mock RDS Postgres database in AWS. The main ETL application (write-up to be followed by this one) will extract the data from this external RDS database and load it inside the RDS database inside the application's VPC.

NOTE: IT IS ALSO IMPORTANT TO NOTE THAT THE IMPLEMENTATION OF THIS PROJECT IN AWS WILL INCUR COSTS. IF YOU PROCEED TO INITIALIZE THIS PROJECT IN AWS, ENSURE TO STOP AND REMOVE ALL RESOURCES AFTER.


* To communicate the creation of resources in AWS, Terraform will be used to create the infrastructure. Here are the steps to setup your Terraform account:
    * Sign up for Terraform Cloud
    * Create your organization and workspace
    * Select your workspace and go to "General"
    * Under the "Execution Mode", select "Local" and then "Save Settings". Choosing this setting will prevent any errors when using Terraform in this project.
    * After choosing the "Execution Mode", click your username on the top left of the page.
    * Go to Settings -> Variable Sets -> Create Variable Set
    * For the Variable Set Scope, choose "Apply to Specific Projects and Workspaces"
    * Ensure that the workspace you created should be included in the "Apply to workspaces" dropdown.
    * For the first key, select "Environment variable" and type "AWS_ACCESS_KEY_ID" for the key. The value should be your AWS Access Key ID. Check the "Sensitive" box. Click "Add Variable".
    * For the second key, select "Environment variable" and type "AWS_SECRET_ACCESS_KEY" for the key. The value should be your AWS Secret Access Key. Check the "Sensitive" box. Click "Add Variable".
    * After adding the two variables, click "Save Variable Set"
    * Go back to the local working directory. Input your organization and workspace in the cloud block inside the terraform block located on the main Terraform file (terraform/main/main.tf).
    * In the Terminal, change the present working directory to terraform/main.
    * Run the following command:
        * "terraform init"
    * After the initialization, run the command:
        * "terraform plan"
    * Run this command after running the second Terraform command:
        * "terraform apply -auto-approve"
    * There should be a confirmation after that the AWS environment has been created.
    * NOTE on the Usage of Terraform Cloud: The number of services initialized on AWS through Terraform Cloud should be within the Terraform free tier, but there will still be costs from the side of AWS. Also, the use of Terraform Cloud protects any sensitive data since the backend and state are not stored locally. Storing these locally can expose your AWS credentials.

V. Notes About Docker Volumes
It can be seen from the Docker Compose file that there are volumes that are connected to folders from the host computer. Here is a brief explanation of bind mounts:

* Bind Mounts
    * These are volumes connected to folders in the host computer. These are accessible to both the host computer and the Docker environment.

For the sake of simplicity, bind mounts are helpful when scripts are developed, such as ones for SQL and Python. Modified scripts are instantly reflected inside Docker during development. Moreover, this is easier for developers to test their scripts. On the other hand, if the data does not have to be accessed from the outside the Docker environment, such as database volumes or logs, it is better to assign these to Named Volumes.

It is important to point out that during production, all scripts required by the applications should be built inside the image. This ensures and respects the essence of containerization as all required scripts will always be with the application wherever it is run. The applications are guaranteed to run no matter which host computer these Docker images are running on.

VI. Access to the Applications
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

* RDS Postgres through pgAdmin
    * http://localhost:5030
    * Login with the following details:
        * Username/Email: faker@faker.com
        * Password: password
    * Go to Secrets Manager in AWS and find the username and password generated for your RDS database.
        * NOTE: You can see the username of the database on the Configuration Tab of your RDS database.
        * To connect pgAdmin to Postgres, click “Add New Server” in Quick Links. Enter the following:
            * In the General tab:
                * Name: RDS_DB_NAME
            * In the Connection tab:
                * Host name/address: RDS_ENDPOINT
                * Port: 5432
                * Maintenance database: postgres
                * Username: RDS_USERNAME
                * Password: RDS_PASSWORD


VII. Running the Python script and viewing the results
* Inside JupyterLab, do the following:
    * On the left side, click “faker_cars.ipynb”.
    * On the sixth cell of "faker_cars.ipynb", input the database name, username, RDS endpoint, and password of the RDS Database and save the file.
    * Restart the kernel and run the entire script.
    * At this point, the results should have been sent to RDS
* Go to the pgAdmin page:
    * Go to the RDS database
    * Find and click the “raw” schema
    * Look for the table “raw_values” and inspect the data
        * If the Python script was not modified, there should be 50,000 rows values generated with fake values.

VIII. Shutting Down the Containers
* If you want to shut down all of the containers in the Docker Compose file, you can run the following command:
    * “docker compose down”

XI. Stop and remove AWS infrastructure on Terraform
* IMPORTANT: Stop all of the services on AWS to prevent any additional costs. To shutdown the AWS services started through Terraform, run the following command:
    * "terraform destroy -auto-approve"
* Ensure that the process reaches completion and without errors. 

XI. Final Notes
* If there are errors or areas this project can improve on, please let me know.

X. References

Faker documentation:
https://faker.readthedocs.io/en/master/

Loading Data from Python to Postgres:
https://hakibenita.com/fast-load-data-python-postgresql 

Purpose of "seek" in loading data from Python to Postgres:
https://stackoverflow.com/questions/55181331/bulk-insert-using-postgresql-copy-from-psycopg2-and-stringio

Use of copy_expert instead of copy_from:
https://github.com/psycopg/psycopg2/issues/1294

Postgres COPY syntax:
https://www.postgresql.org/docs/current/sql-copy.html

List of vehicles source (vehicle data copied and processed manually):
https://www.carguide.ph/p/philippine-car-price-guide-2016_18.html

DevOps Bootcamp: Terraform by Andrei Neagoie and Andrei Dumitrescu:
https://www.udemy.com/course/devops-bootcamp-terraform-certification/