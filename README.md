# Compare DataFrames From The Command Line
(Small side project, June 2020)

This application loads tabular data from file into pandas dataframes and compares them for differences. This is usefull if you want to check for data consistency after dumping data from a DB or running an ETL pipeline.

Simply pass the names of / rel path to 2 CSV-files as arguments.

There are checks for an identical structure but if row count differs while the indices are overlapping the matching subselection is compared.

## WIP - Up next


- [ ] Clean up the TODOs
- [ ] The try-execpt block is a workaround so that i can import the functions into other modules ... -> see medium blogpost for that, maybe, but I think I solved it here
- [ ] Add XLSX support
- [ ] Add Licence
- [ ] ...


## Aknowledgements / Resources

This project was essentially a playground to experiment with test driven development and for working with a CLI. This resources got me started:

- [Article on Command Line Interfaces with Argparse](https://realpython.com/command-line-interfaces-python-argparse/) on RealPython
- [Article on Unit Testing With Pytest](https://realpython.com/pytest-python-testing/) also on RealPython