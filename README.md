# Solution

My solution will be implemented using flask

## Components needed

- [x] Handle file that gets updated
- [x] Implement a way to keep track of "yesterdays" price for each share
- [x] Sort according to percentage
- [x] Return "Winner" JSON structure
- [x] Only include stocks updated today in winners OR ~~if new date detected, set all percentages to 0~~
- [x] Manually extend dataset ~~Generate more data (Optional)~~

&rarr;

- [x] Combine components into `Solution.py`

## Files

`Solution.py` The file with my implemented solution

`Testing.py` File to build different components and test them using flask before moving to `Solution.py`

`Testing.ipynb` Notebook where I could develop components without using flask

`Data.csv` Data provided in task

`extendedData.csv` Extends provided dataset, adds another stock and two more dates

`testData.csv` Subset of original dataset, used to verify behavior if less than three stocks updated

`requirements.txt` Python environment

## How to run

- Install packages from requirements.txt (Only flask and its dependencies are required)
  - The notebook requires IPython (not included in requirements.txt)

- Run flask application via flask --app Solution.py run or python Solution.py

- To advance one line run curl -X POST http://127.0.0.1:5000/update to advance all lines run curl -X POST http://127.0.0.1:5000/updateAll

- View the result at http://127.0.0.1:5000/winners



## Comments

- By writing to a separate file, tmpData.csv, one line at a time, i.e. tmpData gets updated continuously, I can verify that my solution can handle this