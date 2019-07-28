**Have a question or suggestion?**
Contact me on [Linkedin](https://www.linkedin.com/in/fernandosmbrito), or open a pull request on this project.

**Programming assignment for the [Udacity Data Engineering Nanodegree](https://www.udacity.com/course/data-engineer-nanodegree--nd027) program.**

---

# Project 1: Data Modeling with Postgres

> In this project, you’ll model user activity data for a music streaming app called Sparkify. You’ll create a relational database and ETL pipeline designed to optimize queries for understanding what songs users are listening to. In PostgreSQL you will also define Fact and Dimension tables and insert data into your new tables.

## Features 
### Requested in the assignment

* Python ETL scripts to load JSON files into a PostgreSQL database
* Dimensional data modeling


### Implemented by my own

* E-R diagram: using online tool (https://dbdiagram.io/d/)
* Timing functions: Python function annotations allows easy benchmarking
* Bash script: allows log saving and automate execution of multiple scripts
* Extra Jupyter notebook with visualizations: allows data exploration
* Python dependencies file: allows easy installation


### Limitations and nice to haves
* Incremental load: currently, on each execution, the entire database is dropped and all input files are processed. In a real world scenario, incremental load could be considered
* Metadata table: to achieve the above and have better visibility on how the ETL is performing, a metadata table could be created
* Load join result in memory: the ETL script has a step where songs must be located (by a SQL query) for each event. In a real world scenario, depending on the size of the songs table, it could be loaded once in memory and used for quick look-up
* Optimize storage/fields: for the scope of this assignment, not much consideration has been given on the data types used on the Postgres schema


## Technology Stack
* [Python](https://www.python.org/)
* [pandas](https://pandas.pydata.org/)
* [Jupyter notebook](https://jupyter.org/)
* [Plotly charts for Python](https://plot.ly/python/)
* [PostgreSQL](https://www.postgresql.org/)

## Instructions

### Installation

Install all necessary modules to run the current project:

```bash
$ git clone https://github.com/fernandobrito/data-engineering-udacity
$ cd data-engineering-udacity
$ pip3 install -r requirements.txt
```

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

* `create_tables.py`: script to create and drop tables and database
* `etl.py`: main ETL script to process raw input files and insert them on the database
* `run_all.sh`: convenience shell script to run both scripts above
* `sql_queries.py`: SQL queries used by the other scripts

* `utils/`: helper functions
* `notebooks/`: Jupyter notebooks for exploring the data interactively
* `logs/`: log of the ETL script executions
* `docs/`: E-R diagram and images used on this README
* `data/`: raw input data provided by the assignment

## Comments to the reviewer

* Since there were no requirements about this, I decided to round the duration (both in the `songs` table and in the ETL when processing the `length` attribute in the `log events`) to the second
* Out of the 7.400 log events, I could only find the song and artist in the database (data coming from `song_data`) for 1 event. First I through my SQL query was wrong, but I guess there are almost no matches since we only have a subset of the artists and songs in `song_data`
* I tried using the `COPY` command to do a bulk insert, but it doesn't support `ON CONFLICT`. One option would be to create a temporary table on the database and then use it to upsert rows into my main table, but I ran out of time for this assignment

## Data model

![](docs/erd.png?raw=true)

## Graphs

I have created an extra Jupyter notebook to plot some graphs (using Plotly) for this dataset.

![](docs/viz1-plan.png?raw=true)

![](docs/viz2-gender.png?raw=true)

![](docs/viz3-found.png?raw=true)

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
