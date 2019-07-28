**Have a question or suggestion?**
Contact me on [Linkedin](https://www.linkedin.com/in/fernandosmbrito), or open a pull request on this project.

**Programming assignment for the [Udacity Data Engineering Nanodegree](https://www.udacity.com/course/data-engineer-nanodegree--nd027) program.**

---

# Project 3: Data Warehouse with Amazon Redshift

> In this project, you'll apply what you've learned on data warehouses and AWS to build an ETL pipeline for a database hosted on Redshift. To complete the project, you will need to load data from S3 to staging tables on Redshift and execute SQL statements that create the analytics tables from these staging tables.

## Features 
### Requested in the assignment

* Python ETL scripts to load CSV files from S3 into Redshift
* Dimensional data modeling


### Implemented by my own

* E-R diagram: using online tool (https://dbdiagram.io/d/)
* Timing functions: Python function annotations allows easy benchmarking
* Bash script: allows log saving and automate execution of multiple scripts
* Extra Jupyter notebook with visualizations: allows data exploration
* Infrastructure as code: extra Jupyter notebook to spin up a Redshift cluster on AWS
* Python dependencies file: allows easy installation


### Limitations and nice to haves
* Metadata table: to achieve the above and have better visibility on how the ETL is performing, a metadata table could be created
* Optimize storage/fields: for the scope of this assignment, not much consideration has been given on the data types used on the Redshift schema


## Technology Stack
* [Amazon Redshift](https://aws.amazon.com/redshift/)
* [Python](https://www.python.org/)
* [pandas](https://pandas.pydata.org/)
* [Jupyter notebook](https://jupyter.org/)
* [Plotly charts for Python](https://plot.ly/python/)


## Instructions

### Installation

Install all necessary modules to run the current project:

```bash
$ git clone https://github.com/fernandobrito/<replace>
$ cd <replace>
$ pip3 install -r requirements.txt
```

### Set up Redshift cluster

Fill AWS credentials and necessary configurations on `dwh.cfg`. Use `notebooks/manager_cluster.ipynb` to create and start a Redshift cluster.

### Execution

Reset database state (drop tables and database):

```bash
$ python3 create_tables.py
```

Run ETL:
```bash
$ python3 etl.py
```

Or do both and save output on the `logs/` folder:

```bash
$ sh run_all.sh
```

### Files and folders

* `dwh.cfg`: configuration file to create Redshift cluster and connect to it
* `create_tables.py`: script to create and drop tables and database
* `etl.py`: main ETL script to process raw input files and insert them on the database
* `run_all.sh`: convenience shell script to run both scripts above
* `sql_queries.py`: SQL queries used by the other scripts

* `utils/`: helper functions
* `notebooks/`: Jupyter notebooks for exploring the data interactively
* `logs/`: log of the ETL script executions
* `docs/`: E-R diagram and images used on this README

## Comments to the reviewer

* The staging tables have, on purpose, all columns as type `varchar`, since its purpose is to load the raw data with as little processsing as possible. Data types are then casted/converted by the ETL step

* To reduce data shuffling between the nodes in the cluster, all dimension tables have been created with a `DISTSTYLE ALL`

* The `songplays` and `time` tables have been sorted by time using `SORTKEY(start_time)`. Other tables have been sorted by their primary keys to speed up JOINs.

* Since there were no requirements about this, I decided to round the duration (both in the `songs` table and in the ETL when processing the `length` attribute in the `log events`) to the second

## Data model

### Staging tables
![](docs/erd-staging.png?raw=true)

### Dimensional modeling
![](docs/erd.png?raw=true)

## Graphs

I have created an extra Jupyter notebook to plot some graphs (using Plotly) for this dataset.

![](docs/viz1-plan.png?raw=true)

![](docs/viz2-gender.png?raw=true)

![](docs/viz3-found.png?raw=true)

![](docs/viz4-found.png?raw=true)

## References

%sql in jupyter notebooks
https://towardsdatascience.com/jupyter-magics-with-sql-921370099589



## Contributing

1. Fork it
2. Create your feature branch with specs (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request


## Contributors

* Fernando Brito ([fernandobrito](https://github.com/fernandobrito))


## License

This project is licensed under the MIT License. Check the `LICENSE` file.