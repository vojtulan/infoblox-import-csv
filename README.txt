Put CSV files (with bad ip format) to the "csv" directory.
After that just run "python3 magic.py"
Script will read all csv files that are in "csv" directory and import them into newly created csv file for infoblox import. It will create csv file
named "corrected.csv" which incudes corrected ip addreses from the csv directory.
Your EXCEL file with imported IP and mac addresses will be generated in scripts root directory - infobloxImport.csv