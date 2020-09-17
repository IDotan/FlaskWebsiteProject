function isOkMail() {
    const mail = document.getElementsByClassName('input-field')[0].value
    if (mail.length == 0)
        return false
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if (mail.match(mailformat)) {
        return true
    }
    return false
}