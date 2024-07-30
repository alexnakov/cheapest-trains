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

  if (monthNeedle != 0) {
    const backBtn = document.getElementById('prev-month-btn')
    backBtn.removeAttribute('disabled')
  }

  if (monthNeedle != 1) {
    const forwardBtn = document.getElementById('next-month-btn')
    forwardBtn.setAttribute('disabled','true')
  }
}

function moveBack1Month() {
  const queryStr1 = 'month ' + '_' + monthNeedle + ' day'
  const currentMonthDates = document.getElementsByClassName(queryStr1)
  for (let el of currentMonthDates) {
    el.style.display = 'none'
  }
  
  monthNeedle -= 1;
  const queryStr2 = 'month ' + '_' + monthNeedle + ' day'
  const nextMonthDates = document.getElementsByClassName(queryStr2)
  for (let el of nextMonthDates) {
    el.style.display = 'block'
  }

  if (monthNeedle == 1) {
    const backBtn = document.getElementById('prev-month-btn')
    backBtn.setAttribute('disabled','true')
  }

  if (monthNeedle != 2) {
    const forwardBtn = document.getElementById('next-month-btn')
    forwardBtn.removeAttribute('disabled')
  }
}
