const monthsArray = ["January","February","March","April","May","June","July","August","September","October","November","December"];
const now = new Date() // Date obj upon loading the page

// This varible will be my 'state'
var currentMonthAndYear = [now.getMonth(), now.getFullYear()]

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

function set1stMonthOnCalendar(nowDate) {
  /*
  Params: Initial Date object upon loading the page.
  */

  nowDate.setDate(1) // Set the day the 1st of the month

  const dayOfTheWeek1st = nowDate.getDay() //  Day of the week 0 - 6 [Sunday 0, Monday 1]

  if (dayOfTheWeek1st - 1 != 0) { // i.e if its NOT monday
    nowDate.setDate(nowDate.getDate() - (dayOfTheWeek1st - 1))
  }

  const allTDtagsTop = document.querySelectorAll(`td>div.date`)
  const todaysDate = new Date()

  for (let i=0; i<allTDtagsTop.length; i++) {
    let strDate = formatDate(nowDate)
    allTDtagsTop[i].textContent = strDate

    // If the current date is today, the background is painted
    // aqua to show that.
    if (isSameDate(todaysDate, nowDate)) {
      allTDtagsTop[i].style.backgroundColor = `aqua`;
    }
    nowDate.setDate(nowDate.getDate() + 1)
  }
}

window.onload = set1stMonthOnCalendar(now)

// BUTTONS functions

function forwardMonthBtn() {
  const calendarTableCurrentMonth = document.getElementById(`current-month`).textContent
  
  const monthIndex = monthsArray.indexOf(calendarTableCurrentMonth)
  const dateObj1MonthAheadOn1st = new Date(2024,monthIndex+1,1)

  console.log(monthIndex)
  console.log(dateObj1MonthAheadOn1st)
}

forwardMonthBtn()




