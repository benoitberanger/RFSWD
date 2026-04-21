# RFSWD
Python script to parse and print the CSV files for RF Safety Watchod.  
Only the MaRS is quiped with Python, not the Host.  
Same for Temerature sensors

# Setup
Place the [parse_csv_RFSWD.py](parse_csv_RFSWD.py) file `%MriCustomer%\bin` (on the Host)  
Do the same for [parse_PerCoilTemp.py](parse_PerCoilTemp.py)

# Run
  ```bash
  python3 /opt/medcom/MriCustomer/bin/parse_csv_RFSWD.py
  ```
  ```bash
  python3 /opt/medcom/MriCustomer/bin/parse_PerCoilTemp.py
  ```

# Python verion
- XA60: `3.9.2`
