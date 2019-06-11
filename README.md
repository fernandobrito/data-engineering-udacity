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
* Timing functions: to allow benchmarking
* Bash script: to allow log saving and automate execuation of multiple scripts
* Extra Jupyter notebook with visualizations
* Python dependencies file

Test time with load (1s for songs, 11.5s for events)


### Limitations and nice to haves
* Incremental load: currently, on each execution, the entire database is dropped and all input files are processed. In a real world scenario, incremental load could be considered
* Metadata table: to achieve the above and have better visibility on how the ETL is performing, a metadata table could be created
* Load join result in memory: the ETL script has a step where songs must be located (by a SQL query) for each event. In a real world scenario, depending on the size of the songs table, it could be loaded once in memory and used for quick look-up
* Optimize storage/fields: for the scope of this assignment, not much consideration has been given on the data types used on the Postgres schema


## Technology Stack
* Python 3
* Pandas
* Jupyter notebooks
* Plotly charts
* Postgres

## Instructions

### Installation

Install all necessary modules to run the current project:

```bash
$ git clone https://github.com/fernandobrito/reactnd-project-flashcards
$ cd reactnd-project-flashcards/
$ pip3 install
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

Do both and save output on the `logs/` folder:

```bash
$ { python3 create_tables.py; python3 etl.py; } 2>&1 | tee -a "logs/$(date +"%Y-%m-%d-%H:%M:%S").txt"
```

## Comments to the reviewer

Duration

## Graphs

I have created an extra Jupyter notebook to plot some graphs (using Plotly) for this dataset.

![](doc/viz1-plan.png?raw=true)

![Image of Yaktocat](doc/viz2-gender.png?raw=true)

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