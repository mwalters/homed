/*!
* Start Bootstrap - Bare v5.0.7 (https://startbootstrap.com/template/bare)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-bare/blob/master/LICENSE)
*/

var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
})

var [servicesTotal, servicesHealthy, servicesUnhealthy] = [0,0,0];
var radarTimer = 5 * 60 * 1000; // 5 Minutes
var serviceTimer = 5 * 60 * 1000; // 5 Minutes

function darkmodeTender() {
  chk = document.getElementById('control-darkmode');
  chk.addEventListener('click', function() {
    if (this.checked) {
      document.body.classList.remove("light-mode");
      document.body.classList.add("dark-mode");
      console.log(hdate(), 'Dark mode toggled on');
    } else {
      document.body.classList.remove("dark-mode");
      document.body.classList.add("light-mode");
      console.log(hdate(), 'Dark mode toggled off');
    }
  });
}

function refresh_weather() {
  var currentRadar = document.getElementById('currentRadar');

  console.log(hdate(), 'Refreshing radar loop')
  currentRadar.src = 'https://radar.weather.gov/ridge/lite/K' + currentRadar.dataset.radar + '_loop.gif?' + new Date().getTime();
  setRadarTimer();
  fetch('/homedweather', { method: 'GET' })
    .then(Result => Result.json())
    .then(weather => {
      console.log(hdate(), 'Updating current temp and feels-like temp', weather);
      document.getElementById('current_temp').innerHTML = Math.round(weather.current_conditions.main.temp);
      document.getElementById('current_feelslike').innerHTML = Math.round(weather.current_conditions.main.feels_like);
    })
}

function refresh_status_checks() {
  console.log(hdate(), "Refreshing status checks");
  servicesTotal = 0;
  servicesHealthy = 0;
  servicesUnhealthy = 0;
  status_checks = document.querySelectorAll('[data-statuscheck="True"]').forEach(status_check => {
    status_check.classList.add("service-health")
    if ('statusservice' in status_check.dataset && status_check.dataset.statuscheck === 'True') {
      var url = '/serviceStatus/' + status_check.dataset.statusservice;

      console.log(hdate(), 'Status check for:', status_check.dataset.statusservice, url);

      fetch(url, { method: 'GET' })
        .then(Result => Result.json())
        .then(status_check => {
          var statusEl = document.getElementById('footer-text');
          console.log(hdate(), 'Status check result:', status_check);
          el = document.querySelectorAll('[data-statusservice="' + status_check.service + '"]').forEach(service_el => {
            servicesTotal++;
            if (status_check.status_code == 200) {
              servicesHealthy++;
              service_el.classList.add("service-healthy")
            } else {
              servicesUnhealthy++;
              service_el.classList.add("service-unhealthy")
            }
          })

          statusEl.innerHTML = servicesTotal + ' services (' + servicesHealthy + ' Up, ' + servicesUnhealthy + ' down) - Updated: ' + hdate();
        })
    }
  })

  setServiceStatusTimer();
}

function hdate() {
  return new Date().toLocaleDateString(navigator.languages[0], {
    day: 'numeric',
    month: 'numeric',
    year: 'numeric',
    hour12: false,
    hour: 'numeric',
    minute: '2-digit',
    second: '2-digit',
  })
}

function setRadarTimer() {
  setTimeout(function() {
    refresh_weather();
  }, radarTimer); // Refresh radar every 5 minutes
  console.log(hdate(), 'Created radar refresh trigger');
}

function setServiceStatusTimer() {
  setTimeout(function() {
    refresh_status_checks();
  }, serviceTimer); // Refresh status checks every 5 minutes
  console.log(hdate(), 'Created status check refresh trigger');
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
    console.log(hdate(), 'Dark mode on');
    document.getElementById('control-darkmode').setAttribute("checked", "true");
  }

  setRadarTimer();
  refresh_status_checks();
});
