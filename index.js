const fs = require('fs');
const readline = require('readline');
const path = require("path");
const moment = require('moment');
const prompt = require('prompt-sync')();

//Converting to date using moment.js
const convertToDate = (date) => {
  const format = 'MM-DD-YYYY';
  const formatedDate = moment(date.trim(), format, true);

  if (!formatedDate.isValid()) {
    console.error("Date as not in proper format");
    return null;
  }

  return formatedDate;
};

//Finding date range in stock profile
const findDateRange = async (stock, startingDate, endingDate) => {
  const filePath = path.join("./stocks", `${stock}.txt`);

  if (fs.existsSync(filePath)) {
    console.log("File Found!!");

    const fileStream = fs.createReadStream(filePath);
    const rl = readline.createInterface({
      input: fileStream,
      crlfDelay: Infinity
    });

    //variables to hold processing state
    let dateRange = []
    let dateFound = false
    let previousLine = null

    let lineCount = 0

    //for every line in the text file
    for await (const line of rl) {

      //Skipping the first two lines
      lineCount++;
      if (lineCount <= 2) continue;

      //splitting the lines into an array
      let lineParts = line.split(/\s+/);
      let date = convertToDate(lineParts[1]);

      if (previousLine) {
        previousDate = convertToDate(previousLine[1])
      }
      
      //if the line reaches an ending date, then while the starting date isnt found, 
      //append a new array to the date range array
      if (date.isSame(endingDate)) {
        console.log("ending date found", endingDate.format("MM/DD/YYYY"))
        dateRange.unshift(lineParts)
        dateFound = true
        continue
      }

      else if (date.isBefore(endingDate) && dateFound == false) {
        endingDate = previousDate
        console.log("ending date found", endingDate.format("MM/DD/YYYY"))
        dateRange.unshift(previousLine)
        dateFound = true
        continue
      }


      //if the line reaches an ending date, then while the starting date isnt found, 
      //append a new array to the date range array
      if (date.isSame(startingDate) && dateFound) {
        console.log("Starting date found", startingDate.format("MM/DD/YYYY"))
        dateRange.unshift(lineParts)
        return(dateRange)
      }

      if (date.isBefore(startingDate) && dateFound) {
        startingDate = previousDate
        console.log("Starting Date found", startingDate.format("MM/DD/YYYY"))
        dateRange.unshift(previousLine)
        return(dateRange)
      }

      else if (dateFound) {
        dateRange.unshift(lineParts)
      }

      previousLine = lineParts
    }

    //error handling
    if (dateRange) {
      console.log("ERROR: Starting date not found", startingDate)
      return
    }

    else {
      console.log("ERROR: Ending date not found", endingDate)
      return
    }
  }

  else {
    console.log("The file you have inputed doesn't exist")
  }
}

//Alerting dates
const alert = (low, high, dateRange) => {
  //setting high and low for starting date range
  highPrice = high * parseFloat(dateRange[0][2])
  lowPrice = low * parseFloat(dateRange[0][2])

  startDate = convertToDate(dateRange[0][1])

  for (let i = 0; i < dateRange.length - 1; i++) {
    console.log(dateRange[i][2]) //, "HIGH: ", highPrice, "LOW: ", lowPrice

    daysPassed = convertToDate(dateRange[i][1]).diff(startDate, "days");

    if (parseFloat(dateRange[i][3]) >= highPrice) {
      console.log("High Alert Reached: ", dateRange[i][0], dateRange[i][1]);
      console.log("Days Passed: ", daysPassed);
      console.log("Start Date: ", startDate.format("MM/DD/YYYY"));
      console.log("Current High: ", dateRange[i][3]);

      //resetting start date & high and low price
      startDate = convertToDate(dateRange[i][1])
      highPrice = high * parseFloat(dateRange[i + 1][2])
      lowPrice = low * parseFloat(dateRange[i+ 1][2])
    }

    if (parseFloat(dateRange[i][4]) <= lowPrice) {
      console.log("Low Alert Reached: ", dateRange[i][0], dateRange[i][1])
      console.log("Days Passed: ", daysPassed)
      console.log("Start Date: ", startDate.format("MM/DD/YYYY"))
      console.log("Current Low: ", dateRange[i][4])
      
      //resetting start date & high and low price
      startDate = convertToDate(dateRange[i][1])
      highPrice = high * parseFloat(dateRange[i + 1][2])
      lowPrice = low * parseFloat(dateRange[i + 1][2])
    }

    if (daysPassed >= 30) {
      console.log("30 Days Reached!: ", dateRange[i][0], dateRange[i][1])
      console.log("===============")
      console.log("Start Date: ", startDate.format("MM/DD/YYYY"))

      //resetting start date & high and low price
      startDate = convertToDate(dateRange[i][1])
      highPrice = high * parseFloat(dateRange[i + 1][2])
      lowPrice = low * parseFloat(dateRange[i + 1][2])
    }
  }

  console.log("End Date Reached: ", dateRange[dateRange.length - 1][0], dateRange[dateRange.length - 1][1])

  console.log("Initial Start Date: ", dateRange[0][0], dateRange[0][1])

  return
}



// Assuming async handling
(async () => {
  const stock = prompt("Stock: ");
  const startingDate = convertToDate(prompt('Pick a starting date (MM-DD-YYYY): '));
  const endingDate = convertToDate(prompt('Pick and ending date (MM-DD-YYYY): '));
  const dropPercent = parseFloat(prompt("Pick you drop percent: "));
  const risePercent = parseFloat(prompt("Pick your rise percent: "));

  const low = ((100 - dropPercent) * 0.01);
  const high = ((100 + risePercent) * 0.01);

  const dateRange = await findDateRange(stock, startingDate, endingDate);
  alert(low, high, dateRange);
  
})();