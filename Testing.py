import csv

with open("Data.csv", mode="r") as file:
    reader = csv.reader(file)
    headers = next(reader)  # Skip headers if needed

    for row in reader:
        # Process each row
        print(row)
        #pass