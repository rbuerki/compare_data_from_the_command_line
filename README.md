# Compare DataFrames From The Command Line

This is a tiny application to compare dataframes from the CLI. Simply pass the names of / path to  2 CSV-files as arguments. There are checks for an identical structure but if row count differs while the indices are overlapping the matching subselection is compared.

## WIP - Up next

- [ ] Add more tests
- [ ] Add read XLSX read
- [ ] Add an extra argument to enable dropping certain columns
- [ ] The try-execpt block is a workaround so that i can import the functions into other modules ... -> see medium blogpost for that, maybe
