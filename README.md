# Compare DataFrames From The Command Line

This application loads tabular data from file into pandas dataframes and compares them for differences. This is usefull if you want to check for data consistency after dumping data from a DB or running an ETL pipeline.

Simply pass the names of / path to  2 CSV-files as arguments. (ABS or REL ?)

There are checks for an identical structure but if row count differs while the indices are overlapping the matching subselection is compared.

## WIP - Up next

- [ ] Check if abs or rel paths makes more sense
- [ ] Add more tests
- [ ] Add XLSX support
- [ ] Add an extra argument to enable dropping certain columns
- [ ] The try-execpt block is a workaround so that i can import the functions into other modules ... -> see medium blogpost for that, maybe
