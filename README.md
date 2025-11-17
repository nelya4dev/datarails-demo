# 🛠️ Senior Software Engineer Home Assignment: Data Ingestion and Transformation Service

## Objective
Design, implement, and deploy a full-stack service for ingesting structured data from a multi-sheet Excel file, transforming it based on external configuration, validating/cleaning it, and persisting the results to a PostgreSQL database.
**Feel free to use AI tools**

## Stack Requirements
* **Backend:** **Django** or **FastAPI** 
* **Database:** **PostgreSQL**
* **Data Processing:** Python
* **Frontend:** **React**
* **Bonus:** Docker/ K8s

## Task Breakdown

### 1. Data Sources
The required input files are located in the respective directories:
* **Input Excel (`data/input.xlsx`):** Contains two sheets: `Employees` and `Projects`.
* **Configuration CSV (`config/config.csv`):** Defines the transformations, mappings, and calculations to be applied.

### 2. Backend Implementation (Data Pipeline)
The backend must orchestrate the data flow and handle error cases gracefully.

#### Database Schema
Design and implement a PostgreSQL schema (e.g., using ORMs) to store the **transformed and cleaned** `Employees` data.

#### API Endpoints
Implement the following REST endpoints:
* `POST /api/upload`: Accepts the multi-sheet Excel file. This must **trigger an asynchronous job** and returns the job Id.
* `GET /api/status/{job_id}`: Returns the status (**Pending, Processing, Completed, Failed**) and any associated error messages for the job.
* `GET /api/employees`: Returns a paginated list of the transformed and saved employee data.


#### Transformation Pipeline Logic
The asynchronous task must implement the following steps:
1.  **Load Configuration:** Read transformation rules from `config/config.csv`.
2.  **Read Excel:** Read both the `Employees` and `Projects` sheets.
3.  **Validate & Clean:**
    * **Validate required fields** (`employee_id`, `project_id`, `salary`).
    * **Validate data types** (e.g., salary/budget must be numeric).
    * If a row contains critical errors (e.g., missing ID, non-numeric in a calculation field), **log the error and skip only that row**. The rest of the file must continue processing.
4.  **Transform:** Apply the rules defined in `config/config.csv`.
5.  **Persist:** Save only the **valid and transformed** data into PostgreSQL, ensuring transaction integrity.

### 3. Frontend Implementation (React)
The React application must provide:
* An interface to upload the `input.xlsx` file via the `POST /api/upload` endpoint.
* A mechanism to track the job status by polling `/api/status/{job_id}`.
* A clean, structured table view to display the final persisted `Employees` data upon job completion.

## Deliverables & Evaluation

The submission should include:
1.  A link to the Git repository with all source code.
2.  Clear instructions on how to set up and run the service (including running the database and frontend/backend services).