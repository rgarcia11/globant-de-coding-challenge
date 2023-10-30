This is the solution proposed for Globant's Data Engineering challenge by candidate Rogelio Garcia. Hope you enjoy the result!

# Challenge
Welcome to Globant’s Data Engineering coding challenge!

You will find several different sections in here. Mind that:

- You can choose which sections to solve based on your experience and available time
- if you don’t know how to solve a section, you can proceed with the following one
- You can use whichever language, libraries, and frameworks that you want.
- The usage of cloud services is allowed, you can choose whichever cloud provider that
you want
- Try to always apply best practices and develop a scalable solution.
- We recommend you to solve everything
- If you don’t have time to solve any sections, try to think the toolstack you would like to
use and the resulting architecture, and why.
- Every complement you might want to add is highly welcome!
- In case you have a personal github repository to share with the interviewer, please do!


## Section 1: API
In the context of a DB migration with 3 different tables (departments, jobs, employees) , create
a local REST API that must:
1. Receive historical data from CSV files
2. Upload these files to the new DB
3. Be able to insert batch transactions (1 up to 1000 rows) with one request

You need to publish your code in GitHub. It will be taken into account if frequent updates are
made to the repository that allow analyzing the development process. Ideally, create a
markdown file for the Readme.md

### Clarifications
- You decide the origin where the CSV files are located.
- You decide the destination database type, but it must be a SQL database.
- The CSV file is comma separated.

## Section 2: SQL
You need to explore the data that was inserted in the previous section. The stakeholders ask
for some specific metrics they need. You should create an end-point for each requirement.

### Requirements

- Number of employees hired for each job and department in 2021 divided by quarter. The
table must be ordered alphabetically by department and job.

#### Output example:

department | job | Q1 | Q2 | Q3 | Q4
--- | --- | --- | --- | --- | ---
Staff | Recruiter | 3 | 0 | 7 | 11
Staff | Manager | 2 | 1 | 0 | 2
Supply | Chain Manager | 0 | 1 | 3 | 0

- List of ids, name and number of employees hired of each department that hired more
employees than the mean of employees hired in 2021 for all the departments, ordered
by the number of employees hired (descending).

#### Output example:

id | department | hired
--- | --- | ---
7 | Staff | 45
9 | Supply Chain | 12

## Bonus Track! Cloud, Testing & Containers
Add the following to your solution to make it more robust:
- Host your architecture in any public cloud (using the services you consider more
adequate)
- Add automated tests to the API
    - You can use whichever library that you want
    - Different tests types, if necessary, are welcome
- Containerize your application
    - Create a Dockerfile to deploy the package

# Solution
The solution was built using Flask and PostgreSQL. It was built locally at first, adding tests for each endpoints as well. It was then dockerized and launched at Cloud SQL (PostgreSQL instance) for the database, and Cloud Run for the dockerized Flask App. Users can interact with the app's front end. It was developed in Flutter and hosted in firebase. The public URL is: https://globant-challenge-web.web.app/.

### Endpoints
The endpoints cover the entire CRUD for the app, the two analytics requirements and loading a CSV file for each table.

#### List of endpoints
##### Departments
**POST** `/departments/upload` uploads a CSV file to the database. It receives three values in the form-data: `csv_file` (the CSV file to upload), `csv_header_row` (whether or not there's a header row to ignore) and `batch_size` (the number of lines that will be inserted per insert batch).
**POST** `/department` creates a department. It receives a JSON file as part of the body with the department into:
```json
{
    "department": "test1"
}
```
This endpont returns the created object.
**GET** `/department` gets a single department. It receives the department's ID in the query parameters (`/department?id=15`).
**GET** `/departments` gets all departments.
**PUT** `/department` edit a department. It receives both the department's ID in the query parameters and the updated object in the body. It returns the updated object.
**DELETE** `/department` delete a department. It receives the department's ID as a query parameter. It returns the deleted object.
**DELETE** `/departments` deletes all departments.
**GET** `/departments/over_hiring_mean` receives the year as a query parameter.

##### Employees
**POST** `/employees/upload` uploads a CSV file to the database. It receives three values in the form-data: `csv_file` (the CSV file to upload), `csv_header_row` (whether or not there's a header row to ignore) and `batch_size` (the number of lines that will be inserted per insert batch).
**POST** `/employee` creates an employee. It receives a JSON file as part of the body with the employee into:
```json
{
        "datetime": "Fri, 15 Jan 2021 00:00:00 GMT",
        "department_id": 3,
        "job_id": 1,
        "name": "test employee"
}
```
This endpont returns the created object.
**GET** `/employee` gets a single employee. It receives the employee's ID in the query parameters (`/department?id=15`).
**GET** `/employees` gets all employees.
**PUT** `/employee` edit a employee. It receives both the employee's ID in the query parameters and the updated object in the body. It returns the updated object.
**DELETE** `/employee` delete an employee. It receives the employee's ID as a query parameter. It returns the deleted object.
**DELETE** `/employees` deletes all employees.
**GET** `/employees/hired_by_quarter` receives the year as a query parameter.


##### Jobs
**POST** `/jobs/upload` uploads a CSV file to the database. It receives three values in the form-data: `csv_file` (the CSV file to upload), `csv_header_row` (whether or not there's a header row to ignore) and `batch_size` (the number of lines that will be inserted per insert batch).
**POST** `/job` creates a job. It receives a JSON file as part of the body with the job into:
```json
{
        "job": "test job",
}
```
This endpont returns the created object.
**GET** `/job` gets a single job. It receives the job's ID in the query parameters (`/department?id=15`).
**GET** `/jobs` gets all jobs.
**PUT** `/job` edit a job. It receives both the job's ID in the query parameters and the updated object in the body. It returns the updated object.
**DELETE** `/job` delete a job. It receives the job's ID as a query parameter. It returns the deleted object.
**DELETE** `/jobs` deletes all jobs.

### Website
The website is a Flutter project. It attempts to "copy" Globant's website in two sections: the Landing and the "open positions" section, as shown below. On top the Globant website and below, the challenge website. On the "START REINVENTING" interaction, the user can type in their name, job and department of their dreams and they are promtly "hired" — added to the database.
<img width="1766" alt="image" src="https://github.com/rgarcia11/globant-de-coding-challenge/assets/20799682/688bfd4a-a59a-4b6c-b37c-c1d085c6c638"> 
<img width="1770" alt="image" src="https://github.com/rgarcia11/globant-de-coding-challenge/assets/20799682/df224c22-14f7-4526-954b-fb65461f8d23">
<img width="1774" alt="image" src="https://github.com/rgarcia11/globant-de-coding-challenge/assets/20799682/f4e0cbab-1697-4360-a397-bd62a51f5602">
<img width="1789" alt="image" src="https://github.com/rgarcia11/globant-de-coding-challenge/assets/20799682/891e0fa0-668c-4fc5-aec8-f573551275e2">



