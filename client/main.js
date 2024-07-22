const monthsArray = ["January","February","March","April","May","June","July","August","September","October","November","December"];
var selectedMonth = new Date() // Date obj upon loading the page
var monthNeedle = 0 // Used to not allow previous than current month movement.

// UTILITIES FUNCTIONS

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

// GETTERS AND SETTERS

function moveMonth(numberOfMonths) {
  selectedMonth.setDate(1)
  selectedMonth.setMonth(selectedMonth.getMonth() + numberOfMonths)
  monthNeedle += numberOfMonths
}

// UI UPDATE FUNCTIONS

function setMonthText(monthString) {
  const monthEl = document.getElementById(`current-month`)
  monthEl.textContent = monthString
}

function setCalendarTable(date) {
  /*
    Params: Date object.
    Whatever month and year is passed, a 5x7 calendar 
    is created in the table in index.html
  */

  const dateObjPassed = new Date(date.getFullYear(), date.getMonth(),1)
  const dayOfTheWeek1st = dateObjPassed.getDay() // Monday, Tues, Wed etc... as 0 - 6 incl

  if (dayOfTheWeek1st - 1 > 0) { // i.e if its NOT monday
    dateObjPassed.setDate(dateObjPassed.getDate() - (dayOfTheWeek1st - 1))
  } else if (dayOfTheWeek1st - 1 < 0) {
    dateObjPassed.setDate(dateObjPassed.getDate() + (dayOfTheWeek1st - 1))
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
    } else if (dateObjPassed.getDate() == 1 && dateObjPassed.getMonth() == date.getMonth()) {
      allTDtagsTop[i].style.backgroundColor = `orange`;
    }

    dateObjPassed.setDate(dateObjPassed.getDate() + 1)
  }
}

function clearSpecialDays() {
  const allTDtagsTop = document.querySelectorAll(`td>div.date`)
  for (let tag of allTDtagsTop) {
    tag.style.backgroundColor = 'red'
  }
}

// BUTTONS

const nextMonthBtn = document.getElementById(`next-month-btn`)
const prevMonthBtn = document.getElementById(`prev-month-btn`)

function nextMonth() {
  moveMonth(1)
  clearSpecialDays() // This must be before the next line
  setCalendarTable(selectedMonth)
  setMonthText(monthsArray[selectedMonth.getMonth()])

  if (monthNeedle == 3) {
    nextMonthBtn.setAttribute('disabled','true')
  }
  prevMonthBtn.disabled = false
}

function prevMonth() {
  moveMonth(-1)
  clearSpecialDays() // This must be before the next line
  setCalendarTable(selectedMonth)
  setMonthText(monthsArray[selectedMonth.getMonth()])

  prevMonthBtn.disabled = true ? monthNeedle == 0 : false;
  nextMonthBtn.disabled = false
}

// IF NAME == MAIN

window.onload = setCalendarTable(selectedMonth)




