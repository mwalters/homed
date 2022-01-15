/*!
* Start Bootstrap - Bare v5.0.7 (https://startbootstrap.com/template/bare)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-bare/blob/master/LICENSE)
*/

var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
})

function darkmodeTender() {
  chk = document.getElementById('control-darkmode');
  chk.addEventListener('click', function() {
    if (this.checked) {
      document.body.classList.remove("light-mode");
      document.body.classList.add("dark-mode");
      console.log('Dark mode toggled on')
    } else {
      document.body.classList.remove("dark-mode");
      document.body.classList.add("light-mode");
      console.log('Dark mode toggled off')
    }
  });
}


function ready(fn) {
  if (document.readyState !== 'loading'){
    fn();
  } else {
    document.addEventListener('DOMContentLoaded', fn);
  }
}

ready(function () {
  darkmodeTender();

  if (document.body.classList.contains('dark-mode')) {
    console.log('Dark mode on')
    document.getElementById('control-darkmode').setAttribute("checked", "true");
  }
});
