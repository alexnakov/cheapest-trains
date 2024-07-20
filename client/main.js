const monthsArray = ["January","February","March","April","May","June","July","August","September","October","November","December"];

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

const now = new Date()

console.log("Now is " + now.toDateString())

const currentMonth = now.getMonth() //  Month of the year 0 - 11

now.setDate(1) // Set the day the 1st of the month

const dayOfTheWeek1st = now.getDay() //  Day of the week 0 - 6 [Sunday 0, Monday 1]

if (dayOfTheWeek1st - 1 != 0) { // i.e if its NOT monday
    now.setDate(now.getDate() - (dayOfTheWeek1st - 1))
}

const allTDtagsTop = document.querySelectorAll(`td>div.date`)

for (let i=0; i<allTDtagsTop.length; i++) {
  let strDate = formatDate(now)
  allTDtagsTop[i].textContent = strDate
  now.setDate(now.getDate() + 1)
}

