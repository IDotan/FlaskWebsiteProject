function switchTab(tab) {
    if (tab == 'site') {
        document.getElementsByClassName('tab-content')[0].style.backgroundColor = 'rgba(193, 193, 193, 0.7)';
        document.getElementsByClassName('site-about')[0].classList.add('active')
        document.getElementsByClassName('dev-about')[0].classList.remove('active')
    } else {
        document.getElementsByClassName('tab-content')[0].style.backgroundColor = 'rgba(76, 152, 175, 0.7)';
        document.getElementsByClassName('site-about')[0].classList.remove('active')
        document.getElementsByClassName('dev-about')[0].classList.add('active')
    }
}

window.onload = function() {
    if (String(location).includes("site")) {
        document.getElementsByClassName('site-about')[0].click();
    }
    if (String(location).includes("dev")) {
        document.getElementsByClassName('dev-about')[0].click();
    }
}