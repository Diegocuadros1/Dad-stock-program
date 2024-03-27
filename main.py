import os
import datetime

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

      previous_date = 0

      for line in file:
        
        #splitting each new line into an array
        line = line.split()

        date = convert_to_date(line[1])

        #setting previous date to the previous line
        try:
          previous_date = convert_to_date(previous_line[1])
        except:
          previous_date = 0

        #if the line reaches an ending date, then while the starting date isnt found, append a new array to the date range array
        if date == ending_date:
          print("ending date found", ending_date)
          date_range.insert(0, line)
          date_found = True
          continue

        elif date < ending_date and date_found == False:
          ending_date = previous_date
          print("ending date found", ending_date)
          date_range.insert(0, previous_line)
          date_found = True
          continue

        if date == starting_date and date_found:
          print("Starting date found", starting_date)
          date_range.insert(0, line)
          return(date_range)
        
        if date < starting_date and date_found:
          starting_date = previous_date 
          print("Starting date found", starting_date)
          date_range.insert(0, previous_line)
          return(date_range)
  
        elif date_found:
          date_range.insert(0, line)
        
        previous_line = line
      
        
      if date_range:
        print("starting date not found", starting_date)
        return
        
      else:
        print("ending date was not found", ending_date)
        return
  else:
    print("The file you have inputed doesn't exist")



def alert(low, high, date_range):

  #setting high and low for starting date_range
  high_price = high * float(date_range[0][2])
  low_price = low * float(date_range[0][2])

  start_date = convert_to_date(date_range[0][1])


  for i in range(len(date_range) - 1):

    print(date_range[i][2])

    days_passed = convert_to_date(date_range[i][1]) - start_date

    if float(date_range[i][3]) >= high_price:
      print("HIGH ALERT REACHED: ", date_range[i][0], date_range[i][1])
      print("DAYS PASSED: ", days_passed.days)
      print("Start Date: ", start_date)
      print("Curr High: ", date_range[i][3])
      print("Number of days to alert: ", days_passed)


      #resetting start date & high and low price
      start_date = convert_to_date(date_range[i][1])
      high_price = high * float(date_range[i][2])
      low_price = low * float(date_range[i][2])

    if float(date_range[i][4]) <= low_price:
      print("Low ALERT REACHED: ", date_range[i][0], date_range[i][1])
      print("DAYS PASSED: ", days_passed.days)
      print("Start Date: ", start_date)
      print("Curr Low: ", date_range[i][4])
      print("Number of days to alert: ", days_passed)

      #resetting start date & high and low price
      start_date = convert_to_date(date_range[i][1])
      high_price = high * float(date_range[i][2])
      low_price = low * float(date_range[i][2])

    if days_passed.days >= 30:
      print("30 Days Reached: ", date_range[i][0], date_range[i][1])
      print("===============================================================================================================================")
      print("Start Date: ", start_date)


      start_date = convert_to_date(date_range[i][1])
      high_price = high * float(date_range[i][2])
      low_price = low * float(date_range[i][2])



  print("End Date Reached: ", date_range[len(date_range) - 1][0], date_range[len(date_range) - 1][1])

  print("Initial Start Date: ", date_range[0][0], date_range[0][1])

  return

#function to convert all date strings into datetime.date objects
def convert_to_date(date_str):
  format = '%m-%d-%Y'
  try:
    return datetime.datetime.strptime(date_str.strip(), format).date()
  except:
    print("Date was not in the proper format")
    return None


#input data
stock = input("stock: ")

starting_date = convert_to_date(input("pick a starting date (MM-DD-YYYY)"))
ending_date = convert_to_date(input("pick an ending date (MM-DD-YYYY)"))

drop_percent = int(input("Pick your drop percent: "))
rise_percent = int(input("Pick your rise percent: "))


low = ((100 - drop_percent) * 0.01)
high = ((100 + rise_percent) * 0.01) 

#getting the date range
date_range = find_date_range(stock, starting_date, ending_date)

#doing the alerts
alert(low, high, date_range)
