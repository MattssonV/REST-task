import csv
from flask import jsonify, Flask
from datetime import datetime

app = Flask(__name__)
app.json.sort_keys = False
#app.config['JSON_SORT_KEYS'] = False

class CSVWriter():
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
            return {"message": "Data updated successfully"}, lineWritten
        else:
            return {"message": "Reached end of source file"}, lineWritten
        
class Stock():
    def __init__(self, name, latest, last_updated):
        self.name = name
        #self.closing_value = 1E6 # Initialize a large number, ensures initial percent is more or less 0 and avoids division by zero
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
        return {key: getattr(self, key, None) for key in args}
    
def round_floats(data, decimal_places=2):
    for key, value in data.items():
        if isinstance(value, float):
            data[key] = round(value, decimal_places)
    return data

def generate_data():
    return 0

def get_filedata(source):
    data = []
    stocks = []
    with open(source, mode="r") as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            # Add check for the stocks here, if new kod add to 'stocks', otherwise update that stock
            datetime_obj = datetime.strptime(row['Date'], "%Y-%m-%d %H:%M:%S")
            #row['twice'] = 2*int(row['Kurs'])
            #row['Day'] = datetime_obj.day
            new_stock = 1 # Track if new stock, if yes add it to stocks
            for stock in stocks:
                if row['Kod'] == stock.name:
                    if datetime_obj.date()>stock.last_updated:
                        stock.closing_value = stock.latest
                        stock.last_updated = datetime_obj.date()
                    stock.latest = int(row['Kurs'])
                    stock.calc_percent()
                    new_stock = 0
                    print(f"Updated {stock.name} value to {stock.latest}")
                    break
            if new_stock:
                stocks.append(Stock(name=row['Kod'], latest=int(row['Kurs']), last_updated=datetime_obj.date()))
            data.append(row)
    return stocks, data

def get_updated_stocks(stocks):
    stocks_datesorted = sorted(stocks, key=lambda x: x.last_updated, reverse=True)
    updated_stocks = [stocks_datesorted[0]]
    for stock in stocks_datesorted[1:]:
        if stocks_datesorted[0].last_updated == stock.last_updated:
            updated_stocks.append(stock)
        else:
            break # Since stocks are sorted according to date, if one is not updated the remaining stocks will not be either.
    return updated_stocks

csvwriter = CSVWriter('Data.csv', 'tmpData.csv')
starting_point = 12 # Use this to advance the starting_point, =12 writes the entries from the first date to tmpData
for i in range(starting_point):
    csvwriter.writeLine()

@app.route('/data2', methods=['GET'])
def get_tmpdata():
    # Use the instance to get the updated data
    _, data = get_filedata('tmpData.csv')
    return jsonify({'data': data})

@app.route('/update', methods=['POST'])
def update_data():
    message, _ = csvwriter.writeLine()
    return jsonify(message), 200

@app.route('/updateAll', methods=['POST'])
def update_data_all():
    written = 1
    while written:
        _, written = csvwriter.writeLine()
    return jsonify({'message': 'All lines written'}), 200

#def get_winners(stocks, number_of_winners=3):
#def get_winners(number_of_winners=3):
@app.route('/winners', methods=['GET'])
def get_winners():
    stocks, _ = get_filedata('tmpData.csv')
    sorted_stocks = sorted(get_updated_stocks(stocks), key=lambda x: x.percent, reverse=True)
    winners = []
    number_of_winners = 3
    for ind, win in enumerate(sorted_stocks[:number_of_winners]):
        tmp_dict = {}
        tmp_dict['rank'] = ind+1
        tmp_dict.update(win.to_dict("name", "latest", "percent"))
        winners.append(tmp_dict)
    return jsonify({'winners': winners})

"""
def get_winners(stocks, number_of_winners=5):    
    sorted_stocks = sorted(get_updated_stocks(stocks), key=lambda x: x.percent, reverse=True)
    winners = []
    for ind, win in enumerate(sorted_stocks[:number_of_winners]):
        tmp_dict = {}
        tmp_dict['rank'] = ind+1
        tmp_dict.update(win.to_dict("name", "latest", "percent"))
        winners.append(tmp_dict)
    return winners
"""
data = []
with open("Data.csv", mode="r") as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        datetime_obj = datetime.strptime(row['Date'], "%Y-%m-%d %H:%M:%S")
        row['twice'] = 2*int(row['Kurs'])
        row['Day'] = datetime_obj.day
        data.append(row)

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data)

"""
def get_winners():
    stocks, _ = get_filedata('tmpData.csv')
    sorted_stocks = sorted(stocks, key=lambda x: x.percent, reverse=True)
    winners = []
    number_of_winners = 3
    for ind, win in enumerate(sorted_stocks[:number_of_winners]):
        tmp_dict = {}
        tmp_dict['rank'] = ind+1
        tmp_dict.update(win.to_dict("name", "latest", "percent"))
        winners.append(tmp_dict)
    return jsonify({'winners': winners})
"""
"""
@app.route('/fullData', methods=['GET'])
def get_data():
    _, data = get_filedata('Data.csv')
    return jsonify(data)
"""
"""
    stocks, _ = get_filedata('Data.csv')
    sorted_stocks = sorted(get_updated_stocks(stocks), key=lambda x: x.percent, reverse=True)
    winners = []
    number_of_winners = 3
    for ind, win in enumerate(sorted_stocks[:number_of_winners]):
        tmp_dict = {}
        tmp_dict['rank'] = ind+1
        tmp_dict.update(win.to_dict("name", "latest", "percent"))
        winners.append(tmp_dict)
    return jsonify({'winners': winners})
"""

"""
if name=="orig":
    message, _ = csvwriter.writeLine()
elif name=="ext":
    message, _ = csvwriterExtended.writeLine()
return jsonify(message), 200
"""

if __name__ == '__main__':
    app.run(debug=True)

#print(data)
#print(jsonify(data))