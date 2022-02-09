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
  } else {
    console.log('Changing radar to loop');
    currentRadar.dataset.state = "loop";
    currentRadar.src = radar_loop;
    radarId.innerHTML = radar_code + " Radar Loop";
  }

  setRadarTimer();
}

function refresh_status_checks() {
  console.log("Refreshing status checks");
  servicesTotal = 0;
  servicesHealthy = 0;
  servicesUnhealthy = 0;
  status_checks = document.querySelectorAll('[data-statuscheck="True"]').forEach(status_check => {
    status_check.classList.add("service-health")
    if ('statusservice' in status_check.dataset && status_check.dataset.statuscheck === 'True') {
      var url = '/serviceStatus/' + status_check.dataset.statusservice;

      console.log('Status check for:', status_check.dataset.statusservice, url);

      fetch(url, { method: 'GET' })
        .then(Result => Result.json())
        .then(status_check => {
          var statusEl = document.getElementById('footer-text');
          console.log('Status check result:', status_check);
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

          const date = new Date();
          const datetime = date.getFullYear() + '-' + String(date.getMonth()).padStart(2, "0") + '-' + String(date.getDate()).padStart(2, "0") + ' ' + date.getHours() + ':' + date.getMinutes(); // "20211124"
          statusEl.innerHTML = servicesTotal + ' services (' + servicesHealthy + ' Up, ' + servicesUnhealthy + ' down) - Updated: ' + datetime;
        })
    }
  })

  setServiceStatusTimer();
}

function ready(fn) {
  if (document.readyState !== 'loading'){
    fn();
  } else {
    document.addEventListener('DOMContentLoaded', fn);
  }
}

function setRadarTimer() {
  setTimeout(function() {
    refresh_radar();
  }, radarTimer); // Refresh radar every 5 minutes
  console.log('Created radar refresh trigger');
}

function setServiceStatusTimer() {
  setTimeout(function() {
    refresh_status_checks();
  }, serviceTimer); // Refresh status checks every 5 minutes
  console.log('Created status check refresh trigger');
}

ready(function () {
  darkmodeTender();

  if (document.body.classList.contains('dark-mode')) {
    console.log('Dark mode on');
    document.getElementById('control-darkmode').setAttribute("checked", "true");
  }

  setRadarTimer();
  refresh_status_checks();
});
