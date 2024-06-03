# IR Project

## Description
A search engine that can be applied to two data sets (Clinical Trials) and (COVID) with UI using Flutter platform.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)


## Installation
1. Clone the repo:
    ```sh
    git clone https://github.com/Hanifa711/project
    ```
2. Install dependencies:
    ```sh
    pip install nltk fastapi uvicorn spellchecker pickle sklearn requests beautifulsoup4 gensim matplotlib
    ```
3. Be careful with this library(uninstall it first):
   ```sh
    pip install scipy==1.12.0
    ```

## Usage
To run the project, follow these steps:
1. Command to start the project:
    ```sh
    uvicorn endpoints:app
    ```
2. Access the project at:
    ```sh
    http://localhost:8000
    ```
3. Run the flutter project for easier experience(check the Flutter brunch).
    
## Features:

1. Suggest and correct querries.
2. Retrieve the top 10 relevant results if there are any.
3. Web Crawking.
4. Data Clustering.
