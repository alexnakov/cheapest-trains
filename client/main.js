const monthsArray = ["January","February","March","April","May","June","July","August","September","October","November","December"];
const now = new Date() // Date obj upon loading the page
var currentMonthAndYear = [now.getMonth(), now.getFullYear()] // State: month and year

function formatDate(date) {
    // Extract the day, month, and year from the date object
    let day = date.getDate();
    let month = date.getMonth() + 1; // Months are zero-based
    let year = date.getFullYear();
  
    // Add leading zeros if necessary
    day = day < 10 ? '0' + day : day;
    month = month < 10 ? '0' + month : month;
    year = year % 100; // Get the last two digits of the year
    year = year < 10 ? '0' + year : year;
  
    // Construct the formatted date string
    return day + '/' + month + '/' + year;
}

function isSameDate(date1, date2) {
  return date1.getFullYear() === date2.getFullYear() &&
         date1.getMonth() === date2.getMonth() &&
         date1.getDate() === date2.getDate();
}

function setMonthText(monthString) {
  const monthEl = document.getElementById(`current-month`)
  monthEl.textContent = monthString
}

function setCalendarTable(monthAndYear) {
  /*
    Params: monthAndYear (Array length 2)
    Whatever month and year is passed, a 5x7 calendar 
    is created in the table in index.html
  */

  const dateObjPassed = new Date(monthAndYear[1], monthAndYear[0], 1)
  const dayOfTheWeek1st = dateObjPassed.getDay() // Monday, Tues, Wed etc... as 0 - 6 incl

  if (dayOfTheWeek1st - 1 != 0) { // i.e if its NOT monday
    dateObjPassed.setDate(nowDate.getDate() - (dayOfTheWeek1st - 1))
  }

  const todaysDate = new Date()
  const allTDtagsTop = document.querySelectorAll(`td>div.date`)

  for (let i=0; i<allTDtagsTop.length; i++) {
    let strDate = formatDate(dateObjPassed)
    allTDtagsTop[i].textContent = strDate

    // If the current date is today, the background is painted
    // aqua to show that.
    if (isSameDate(todaysDate, dateObjPassed)) {
      allTDtagsTop[i].style.backgroundColor = `aqua`;
    }
    dateObjPassed.setDate(dateObjPassed.getDate() + 1)
  }
}

function nextMonthOn1st(monthAndYear) {
  /*
    Params: monthAndYear (Array length 2)
    Returns: Date() obj which is the next month on the 1st
  */

  let date1 = new Date(monthAndYear[1], monthAndYear[0], 1) // 1st of that month
  date1.setDate(date1.getMonth() + 1)
  console.log(date1)
}

window.onload = setCalendarTable(currentMonthAndYear)

// BUTTONS functions

function forwardMonthBtn() {
  const calendarTableCurrentMonth = document.getElementById(`current-month`).textContent
  
  const monthIndex = monthsArray.indexOf(calendarTableCurrentMonth)
  const dateObj1MonthAheadOn1st = new Date(2024,monthIndex+1,1)
}

forwardMonthBtn()




