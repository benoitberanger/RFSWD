# RFSWD
Python script to parse and print the CSV files for RF Safety Watchod.  
Only the MaRS is quiped with Python, not the Host.  

# Setup
1. Place the [parse_csv_RFSWD.py](parse_csv_RFSWD.py) file `%MriCustomer%\bin` (on the Host)
2. Add an alias in the _.bashrc_ on the MaRS :
  ```bash
  alias check_RFSWD='python3 /opt/medcom/MriCustomer/bin/parse_csv_RFSWD.py'
  ```

# Run
On the MaRS, just run `check_RFSWD`

# Python verion
- XA60: `3.9.2`
