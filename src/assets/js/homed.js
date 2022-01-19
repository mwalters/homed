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
      console.log('Dark mode toggled on');
    } else {
      document.body.classList.remove("dark-mode");
      document.body.classList.add("light-mode");
      console.log('Dark mode toggled off');
    }
  });
}

function refresh_radar() {
  currentRadar = document.getElementById('currentRadar');
  radarId = document.getElementById('radarId');
  radar_code = currentRadar.dataset.radar;
  radar_static = 'https://radar.weather.gov/ridge/lite/K' + radar_code + '_9.gif';
  radar_loop = 'https://radar.weather.gov/ridge/lite/K' + radar_code + '_loop.gif?' + new Date().getTime();

  if (currentRadar.dataset.state == "loop") {
    console.log('Changing radar to static');
    currentRadar.src = radar_static;
    currentRadar.dataset.state = "static"
    radarId.innerHTML = radar_code + " Radar (loop is loading)"
    console.log('Waiting 5 seconds before loading loop again')
    setTimeout(function() { refresh_radar(); }, 5000);
  } else {
    console.log('Changing radar to loop');
    currentRadar.dataset.state = "loop"
    currentRadar.src = radar_loop;
    radarId.innerHTML = radar_code + " Radar Loop"
  }

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
  setTimeout(function() {
    refresh_radar();
  }, 900000); // Refresh radar every 15 minutes 900000
  console.log('Created radar refresh trigger');

  if (document.body.classList.contains('dark-mode')) {
    console.log('Dark mode on');
    document.getElementById('control-darkmode').setAttribute("checked", "true");
  }
});
