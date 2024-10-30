# Solution

My solution is implemented using flask

## Components needed

- [x] Handle file that gets updated
- [x] Implement a way to keep track of "yesterdays" price for each stock
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

- Install packages from `requirements.txt` (Only flask and its dependencies are required)
  - The notebook requires IPython (not included in requirements.txt)

- Run flask application via `flask --app Solution.py run` or `python Solution.py`

### Updating files

To ensure my solution can handle updating files I implemented a solution where data from `Data.csv` or `ExtendedData.csv` gets written to either `tmpData.csv` or `tmpExtendedData.csv` one line at a time. Using this the solution can be tested and it can be verified that the behavior is as expected at all stages.

- To write one line run `curl -X POST http://127.0.0.1:5000/update/<name>` where \<name> is either `orig` for the original dataset or `ext` for the extended dataset
  - `curl -X POST http://127.0.0.1:5000/update` is equal to `curl -X POST http://127.0.0.1:5000/update/orig`

- To write multiple lines at once run `curl -X POST http://127.0.0.1:5000/update_<NN>/<name>` where \<name> is either `orig` for the original dataset or `ext` for the extended dataset and \<NN> are the number of lines you want to write, e.g. 5.
  - `curl -X POST http://127.0.0.1:5000/update_<XX>` is equal to `curl -X POST http://127.0.0.1:5000/update_<XX>/orig`

- To write the remaining lines run `curl -X POST http://127.0.0.1:5000/updateAll/<name>` where \<name> is either `orig` for the original dataset or `ext` for the extended dataset
  - `curl -X POST http://127.0.0.1:5000/updateAll` is equal to `curl -X POST http://127.0.0.1:5000/updateAll/orig`

### Winners

 View the winners at `http://127.0.0.1:5000/winners/<filename>` where \<filename> are one of the files (do not include `.csv` in the url):

```text
Data
extendedData
testData
tmpData
tmpExtendedData
```

E.g. `http://127.0.0.1:5000/winners/extendedData` shows the winners for the data in extendedData.csv

`http://127.0.0.1:5000/winners` is equal to `http://127.0.0.1:5000/winners/Data`

### Viewing the data

You can also view the full datasets from the files using the same syntax described above for winners but replace `winners` with `data` in the url.

## Comments

- By writing to a separate file, `tmpData.csv` or `tmpExtendedData.csv`, one line at a time, i.e. gets updated continuously, I can verify that my solution supports files that get updated
