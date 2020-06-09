### Freshdesk example data generation

- Uses Python to generate ticket information, leveraging Faker Library, and Pandas (of course).
- Stores data first as JSON
- Takes Json and puts into SQLite Database
- Then using SQL Queries, Checks for 
    - Time spent Open - So the current time minus the ticket open time; if it has been closed, final ticket time minus original time (Excluding this for speed).
    - Time spent Waiting on Customer - Ticket of waiting on customers current time minus ticket open time.
    - Time spent waiting for response (Pending Status) -
    - Time till resolution - time to solved.
    - Time to first response (First time to first ticket time).

The notebook steps through each part of this process, aside from the SQL, which is using simple filtering that with more time spent would expand in complexity and scope.

## Scripting.
To run these scripts in a bash file, simple write the scripts as normal (i.e., python3 generator.sqlite.py; SQLite.sql;).
 
 """The majority of the program is run through the python script listed, the SQL is an easy next step."""

 """ The SQL scripts require more time input to get perfect, but is a good demonstration of how one would analyse this dataset"""

 #### I tend to use Python for data analysis where possible as i'm very proficient with it.