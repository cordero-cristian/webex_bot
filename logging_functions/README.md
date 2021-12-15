# Logging Functions

The Logging Functions contain 3 main files
<div>
<h3>
- __init__.py<br>
- logging.py<br> 
- logging.ini
</h3>
</div>
<br>
<h4> __init__.py </h4>
This file identifies and loads the logging.ini config file
<br>
<br>
<h4>logging.py</h4>
This file give the logger the correct name and standardizes a way to log each level of sys-log
<br>
<br>
<h4>logging.ini</h4>
This file contains the configuration for each logger. 
two loggers are currently defined, a file logger and a logger that writes to the terminal 