import csv
from flask import jsonify, Flask
from datetime import datetime

app = Flask(__name__)
app.json.sort_keys = False

class CSVWriter():
    # Class that used to write data from one csv file to another, one line at a time
    # Used to test that my solution can handle a file that gets updated
    def __init__(self, source, destination):
        self.i = 0
        self.source = source
        self.destination = destination
        with open(self.source, mode='r', newline='') as src, open(self.destination, mode='w', newline='') as dest:
            reader = csv.DictReader(src)
            csv.DictWriter(dest, fieldnames=reader.fieldnames).writeheader()

    def writeLine(self):
        lineWritten = 0
        with open(self.source, mode='r', newline='') as src, open(self.destination, mode='a', newline='') as dest:
            reader = csv.DictReader(src)
            writer = csv.DictWriter(dest, fieldnames=reader.fieldnames)
            for index, row in enumerate(reader):
                if index==self.i:
                    writer.writerow(row)
                    lineWritten = 1
        self.i = self.i+1
        if lineWritten:
            return "Data updated successfully", lineWritten
        else:
            return "Reached end of source file", lineWritten
        
class Stock():
    # The Stock class keeps track of a stock, convenient way of managing when a 
    # stock is updated
    def __init__(self, name, latest, last_updated):
        self.name = name
        self.closing_value = None
        self.latest = latest
        self.last_updated = last_updated
        self.percent = 0

    def __str__(self): # Simple 'print' function for easy debugging
        return f'Stock: [name: {self.name}, closing_value: {self.closing_value}, latest: {self.latest},\n last_updated: {self.last_updated}, percent: {self.percent:.2f}]'

    def calc_percent(self):
        if self.closing_value is None:
            self.percent = 0
        else:
            self.percent = round(self.latest/self.closing_value*100-100,2)       
    
    def to_dict(self, *args):
        # Function that returns only the specified attributes of the stock as a dict
        # Useful to construct the winners JSON structure
        return {key: getattr(self, key, None) for key in args}

def get_filedata(source):
    # Reads a csv file, returns all data within the file and a list of stocks
    data = []
    stocks = []
    with open(source, mode="r") as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            datetime_obj = datetime.strptime(row['Date'], "%Y-%m-%d %H:%M:%S")
            new_stock = 1 # Track if new stock, if yes add it to stocks
            for stock in stocks:
                if row['Kod'] == stock.name:
                    if datetime_obj.date()>stock.last_updated:
                        # If first occurence for this stock on this date, 
                        # update closing_value and when the stock was last updated
                        stock.closing_value = stock.latest
                        stock.last_updated = datetime_obj.date()
                    stock.latest = int(row['Kurs'])
                    stock.calc_percent()
                    new_stock = 0
                    break 
            if new_stock:
                stocks.append(Stock(name=row['Kod'], latest=int(row['Kurs']), last_updated=datetime_obj.date()))
            data.append(row)
    return stocks, data

def get_updated_stocks(stocks):
    # Returns the stocks that were updated 'today'
    stocks_datesorted = sorted(stocks, key=lambda x: x.last_updated, reverse=True)
    updated_stocks = [stocks_datesorted[0]]
    for stock in stocks_datesorted[1:]:
        if stocks_datesorted[0].last_updated == stock.last_updated:
            updated_stocks.append(stock)
        else:
            break # Since stocks are sorted according to date, if one is not updated the remaining stocks will not be either.
    return updated_stocks

csvwriter = CSVWriter('Data.csv', 'tmpData.csv')
csvwriterExtended = CSVWriter('extendedData.csv', 'tmpExtendedData.csv')

starting_point = 12 # Use this to advance the starting_point, =12 writes the entries from the first date to tmpData
for i in range(starting_point):
    csvwriter.writeLine()
    csvwriterExtended.writeLine()

# View the data in a specific file
@app.route('/data/<filename>', methods=['GET'])
def get_data_fname(filename):
    _, data = get_filedata(f'{filename}.csv')
    return jsonify({'data': data})

# Default behavior of data, get data from Data.csv
@app.route('/data', methods=['GET'])
def get_data():
    return get_data_fname("Data")

# Write one line from source to destination file
@app.route('/update/<name>', methods=['POST'])
def update_data_name(name):
    return update_multiple_name(name, 1)

# Default behavior of update, write one line to tmpData.csv
@app.route('/update', methods=['POST'])
def update_data():
    return update_multiple_name("orig", 1)

# Write multiple lines at once
@app.route('/update_<num>/<name>', methods=['POST'])
def update_multiple_name(name, num):
    counter = 0
    for i in range(int(num)):
        if name=="orig":
            message, written = csvwriter.writeLine()
            destfile = csvwriter.destination
        elif name=="ext":
            message, written = csvwriterExtended.writeLine()
            destfile = csvwriterExtended.destination
        if not written:
            break
        counter += 1
    return jsonify({"message": message, "lines": f'{counter} lines written', "file": destfile}), 200

# Default behavior of update_num, write <num> lines to tmpData.csv
@app.route('/update_<num>', methods=['POST'])
def update_multiple(num):
    return update_multiple_name("orig", num)

# Write rest of lines of source file to destination file
@app.route('/updateAll/<name>', methods=['POST'])
def update_data_all_name(name):
    written = 1
    while written:
        if name=="orig":
            _, written = csvwriter.writeLine()
        elif name=="ext":
            _, written = csvwriterExtended.writeLine()
    return jsonify({'message': f'{name}: All lines written'}), 200

# Default behavior of updateAll, write all lines to tmpData.csv
@app.route('/updateAll', methods=['POST'])
def update_data_all():
    return update_data_all_name("orig")

# Get winners of the latest date
@app.route('/winners/<filename>', methods=['GET'])
def get_winners_fname(filename):
    stocks, _ = get_filedata(f'{filename}.csv')
    sorted_stocks = sorted(get_updated_stocks(stocks), key=lambda x: x.percent, reverse=True)
    winners = []
    number_of_winners = 3
    for ind, win in enumerate(sorted_stocks[:number_of_winners]):
        tmp_dict = {}
        tmp_dict['rank'] = ind+1
        tmp_dict.update(win.to_dict("name", "latest", "percent"))
        winners.append(tmp_dict)
    return jsonify({'winners': winners})

# Default behavior of winners, get winners from original dataset
@app.route('/winners', methods=['GET'])
def get_winners():
    return get_winners_fname("Data")

if __name__ == '__main__':
    app.run(debug=True)