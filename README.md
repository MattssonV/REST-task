# Solution

My solution will be implemented using flask

## Components needed

- [x] Handle file that gets updated
- [x] Implement a way to keep track of "yesterdays" price for each share
- [x] Sort according to percentage
- [x] Return "Winner" JSON structure
- [ ] If new date detected, set all percentages to 0 OR only include stocks updated today in winners
- [ ] Generate more data (Optional)

&rarr;

- [ ] Combine components into Solution.py

## How to run

- Install packages from requirements.txt (Only flask and its dependencies are required)

- Run flask application via flask --app Solution.py run or python Solution.py

- To advance one line run curl -X POST http://127.0.0.1:5000/update to advance all lines run curl -X POST http://127.0.0.1:5000/updateAll

- View the result at http://127.0.0.1:5000/winners

## Comments

- By writing to a separate file, tmpData.csv, one line at a time, i.e. tmpData gets updated continuously, I can verify that my solution can handle this