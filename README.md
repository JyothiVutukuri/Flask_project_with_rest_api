# Flask Project with Restful API

Author: Vishnu Jyothi Vutukuri

## Project Overview

This project is a Flask project with a Restful API, using SQLAlchemy to connect to a SQLite database for gathering data from crawled websites.

## Table of Contents

- [Getting Started](#getting-started)
  - [Cloning the Project](#cloning-the-project)
  - [Prerequisites](#prerequisites---setting-up-a-virtual-environment)
  - [Installation](#installation---installing-requirements)
- [Grab Data](#grab-data)
- [Usage](#Usage---running-the-project)
- [Rest APIs](#rest-apis)

## Getting Started

### Cloning the Project
Follow these steps to clone this "Flask" project repository to your local machine:

```bash
# Open a terminal or command prompt.
cd /path/to/your/desired/directory  # Replace with your desired location.

git clone https://github.com/JyothiVutukuri/flask_project_with_rest_api.git

cd flask-project_with_rest_api
```
Now you have successfully cloned the project to your local machine and are ready to work on it.

### Prerequisites - Setting Up a Virtual Environment

To ensure a clean and isolated environment for your project, we recommend using a virtual environment. Follow these steps to create a virtual environment and install the project's requirements:

- Open a terminal or command prompt.
- Navigate to the root directory of the project where the "requirements.lock"` file is located:

   ```bash
   cd /path/to/project_with_rest_api
   ```
   
Create a virtual environment using the Python interpreter:
    
    python3 -m venv venv
This command will create a new directory named venv in your project directory, which will contain the isolated Python environment.

Activate the virtual environment:

On macOS and Linux:

    source venv/bin/activate

On Windows:

    venv\Scripts\activate

After activation, your terminal prompt should change to indicate that you are now working within the virtual environment.

## Installation - Installing Requirements

Install the project's requirements using pip:

    pip install -r requirements.lock
This command will install all the necessary Python packages and dependencies specified in the requirements.lock file.

Note: It's a good practice to activate the virtual environment every time you work on the project. When you're done working on the project, you can deactivate the virtual environment with the deactivate command.

    deactivate

## Grab data
This project also creates the SQlite database by grabbing the data from the crawled websites. To grab the data from the crawled websites, run the following command:

### Create database by:

    flask db upgrade

#### Add sites by:

    python add_sites_info.py

Note: Takes a while(around 5 to 30 minutes) to grab and save the data from the crawled websites.

### Add `ZIENGS` website crawled data by:

    python grab_and_save_data_from_ziengs_site.py <ziengs_crawl_input_file_path>

### Add `OMODA` website crawled data by:

    python grab_and_save_data_from_omoda_site.py <omoda_crawl_input_file_path>


### Add `OMODA` website crawled data by:

    python grab_and_save_data_from_zalando_site.py <grab_and_save_data_from_zalando_site>



## Usage - Running the Project
To run the project, run the following command:

    Flask run

You can access the project via http://127.0.0.1:5000, which opens the home page of the project.


## Rest APIs
`Note: All api endpoints are paginated with default(20 items)/custom_limit per page. To get the next page, use the  next_url available in the response.`

The following REST API endpoints are available for interacting with the project's data:
    
Indexed sites --> http://127.0.0.1:5000/api/sites
    
Purpose: This endpoint provides access to information about different sites or competitors.

Indexed brands --> http://127.0.0.1:5000/api/brands

Purpose: This endpoint allows users to retrieve information about brands within the Dutch shoe retail market.
    
Indexed product categories --> http://127.0.0.1:5000/api/categories

Purpose: This endpoint provides data related to product categories.
    
Indexed product types --> http://127.0.0.1:5000/api/product_types

Purpose: This endpoint offers information about different types of products.
    
Brand related products --> http://127.0.0.1:5000/api/brand/1/products `Note: Replace 1 with the brand_id of your choice.` 

Purpose: This endpoint allows users to retrieve products associated with a specific brand using the brand_id parameter.

Product detail --> http://127.0.0.1:5000/api/product/1  `Note: Replace 1 with the product_id of your choice.` 

Purpose: This endpoint provides detailed information about a specific product identified by the product_id parameter.