import os

#input data
stock = input("stock: ")

starting_date = input("pick a starting date (MM-DD-YYYY)")
ending_date = input("pick an ending date (MM-DD-YYYY)")

drop_percent = int(input("Pick your drop percent: "))
rise_percent = int(input("Pick your rise percent: "))

#function for finding date range
def find_date_range(stock, starting_date, ending_date):

  file_path = f'./stocks/{stock}.txt'

  #if file exists, open the file
  if os.path.exists(file_path):
    print("File Found")

    with open(file_path, 'r') as file:

      #skips the first two lines
      file.readline()
      file.readline()
      
      #initiating date range array
      date_range = []

      #initiating date range boolean
      date_found = False

      for line in file:
        
        #splitting each new line into an array
        line = line.split() 

        #if the line reaches an ending date, then while the starting date isnt found, append a new array to the date range array
        if line[1] == ending_date:
          print("ending date found", ending_date)
          date_range.insert(0, line)
          date_found = True
          continue

        elif line[1] == starting_date and date_found:
          print("Starting date found")
          date_range.insert(0, line)
          return(date_range)
  
        elif date_found:
          date_range.insert(0, line)
        
        
        
      if date_range:
        print("starting date not found", starting_date)
        
      else:
        print("ending date was not found", ending_date)
  else:
    print("The file you have inputed doesn't exist")






def alert(low, high, date_range):

  #setting high and low for starting date_range
  high_price = high * float(date_range[0][2])
  low_price = low * float(date_range[0][2])

  days_passed = 0

  start_date = date_range[0][1]


  for i in range(len(date_range) - 1):

    print(date_range[i][2])

    if float(date_range[i][3]) >= high_price:
      print("HIGH ALERT REACHED: ", date_range[i][0], date_range[i][1])
      print("DAYS PASSED: ", days_passed)
      print("Start Date: ", start_date)
      print("Curr High: ", date_range[i][3])

      #resetting start date & high and low price
      start_date = date_range[i][1]
      high_price = high * float(date_range[i][2])
      low_price = low * float(date_range[i][2])

    if float(date_range[i][4]) <= low_price:
      print("Low ALERT REACHED: ", date_range[i][0], date_range[i][1])
      print("DAYS PASSED: ", days_passed)
      print("Start Date: ", start_date)
      print("Curr Low: ", date_range[i][4])

      #resetting start date & high and low price
      start_date = date_range[i][1]
      high_price = high * float(date_range[i][2])
      low_price = low * float(date_range[i][2])


    days_passed += 1

  print("End Date Reached: ", date_range[len(date_range) - 1][0], date_range[len(date_range) - 1][1])

  print("Start Date: ", date_range[0][0], date_range[0][1])

  return



low = ((100 - drop_percent) * 0.01)
high = ((100 + rise_percent) * 0.01) 

#getting the date range
date_range = find_date_range(stock, starting_date, ending_date)

#doing the alerts
alert(low, high, date_range)
