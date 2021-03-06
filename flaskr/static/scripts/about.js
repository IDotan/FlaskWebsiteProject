function switchTab(tab) {
    if (tab == 'site') {
        document.getElementsByClassName('tab-content')[0].style.backgroundColor = 'rgba(193, 193, 193, 0.7)';
        document.getElementsByClassName('site-about')[0].classList.add('active');
        document.getElementsByClassName('dev-about')[0].classList.remove('active');
        document.getElementsByClassName('content-site')[0].hidden = false;
        document.getElementsByClassName('content-dev')[0].hidden = true;
        document.getElementsByClassName('content-dev')[0].style.display = "none"
    } else {
        document.getElementsByClassName('tab-content')[0].style.backgroundColor = 'rgba(76, 152, 175, 0.7)';
        document.getElementsByClassName('site-about')[0].classList.remove('active');
        document.getElementsByClassName('dev-about')[0].classList.add('active');
        document.getElementsByClassName('content-site')[0].hidden = true;
        document.getElementsByClassName('content-dev')[0].hidden = false;
        document.getElementsByClassName('content-dev')[0].style.display = "grid"
    }
}

window.onload = function() {
    if (String(location).includes("site")) {
        document.getElementsByClassName('site-about')[0].click();
    }
    if (String(location).includes("dev")) {
        document.getElementsByClassName('dev-about')[0].click();
    }
    var linkedAlert = setInterval(function() {
        if (document.getElementsByClassName('LI-view-profile').length != 0) {
            document.getElementsByClassName('linkedin-script-alert')[0].remove();
            clearInterval(linkedAlert);
        }
    }, 1000);
    setTimeout(function() { clearInterval(linkedAlert); }, 5000);
}