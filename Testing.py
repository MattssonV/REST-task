import csv
from flask import jsonify, Flask
from datetime import datetime

app = Flask(__name__)

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
            return {"message": "Data updated successfully"}
        else:
            return {"message": "Reached end of source file"}
        
class Stock():
    def __init__(self, key):
        self.key = key
        self.yesterday_max = 1E6 # Initialize a large number, ensures initial percentage is more or less 0 and avoids division by zero
        self.todays_max = 0
        self.updated_today = 0
        self.percentage = self.todays_max/self.yesterday_max*100


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
            row['twice'] = 2*int(row['Kurs'])
            row['Day'] = datetime_obj.day
            data.append(row)
        #headers = next(reader)  # Skip headers if needed
    return data

data = []
with open("Data.csv", mode="r") as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        datetime_obj = datetime.strptime(row['Date'], "%Y-%m-%d %H:%M:%S")
        row['twice'] = 2*int(row['Kurs'])
        row['Day'] = datetime_obj.day
        data.append(row)
    #headers = next(reader)  # Skip headers if needed

@app.route('/data', methods=['GET'])
def get_data():
    # Use the instance to get the updated data
    return jsonify(data)

csvwriter = CSVWriter('Data.csv', 'tmpData.csv')

@app.route('/data2', methods=['GET'])
def get_tmpdata():
    # Use the instance to get the updated data
    return jsonify({'data':get_filedata('tmpData.csv')})

@app.route('/update', methods=['POST'])
def update_data():
    return jsonify(csvwriter.writeLine()), 200

if __name__ == '__main__':
    app.run(debug=True)

#print(data)
#print(jsonify(data))