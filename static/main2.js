var monthNeedle = 1

function moveForward1Month() {
  const queryStr1 = 'month ' + '_' + monthNeedle + ' day'
  const currentMonthDates = document.getElementsByClassName(queryStr1)
  for (let el of currentMonthDates) {
    el.style.display = 'none'
  }
  
  monthNeedle += 1;
  const queryStr2 = 'month ' + '_' + monthNeedle + ' day'
  const nextMonthDates = document.getElementsByClassName(queryStr2)
  for (let el of nextMonthDates) {
    el.style.display = 'block'
  }
}