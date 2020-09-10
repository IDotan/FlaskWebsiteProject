function validateForm() {
    if ((document.getElementById('usernameError').hidden == false) || (document.getElementById('pswError').hidden == false) || (document.getElementById('emailError').hidden == false)) {
        return false;
    }
}

const user_input = document.getElementById('Username');
const user_error = document.getElementById('usernameError');
user_input.addEventListener('focusout', function(event) {
    var userCheck = isOkUser(user_input.value);
    if (userCheck.result == false) {
        //show the error
        user_error.innerText = userCheck.error;
        user_error.hidden = false;
    } else {
        $.post(userIDAvailableLink, {
            usernameCheck: user_input.value
        }, function(data) {
            if (data.valid == 'no') {
                user_error.innerText = "Username already in use";
                user_error.hidden = false;
            } else {
                user_error.innerText = "";
                user_error.hidden = true;
            }
        })
    }
});

function isOkUser(u) {
    var anUpperCase = /[A-Z]/;
    var aLowerCase = /[a-z]/;
    var aNumber = /[0-9]/;
    var obj = {}
    obj.result = true;
    if (u.length < 5) {
        obj.result = false;
        obj.error = "Must be longer then 5";
        return obj;
    }
    var invaliedChar = 0;
    for (var i = 0; i < u.length; i++) {
        if (anUpperCase.test(u[i]) == false && aLowerCase.test(u[i]) == false && aNumber.test(u[i]) == false) {
            invaliedChar++;
        }
    }
    if (invaliedChar != 0) {
        obj.result = false;
        obj.error = "Can only use english characters and numbers";
        return obj;
    }
    return obj;
}

const psw_input = document.getElementById('psw');
const psw_error = document.getElementById('pswError');
psw_input.addEventListener('keyup', function(event) {
    var userCheck = isOkPass(psw_input.value);
    if (userCheck.result == false) {
        //show the error
        psw_error.innerText = userCheck.error;
        psw_error.hidden = false;
    } else {
        psw_error.innerText = "";
        psw_error.hidden = true;
    }
});

function isOkPass(p) {
    var anUpperCase = /[A-Z]/;
    var aLowerCase = /[a-z]/;
    var aNumber = /[0-9]/;
    var aSpecial = /[!|@|#|$|%|^|&|*|(|)|-|_]/;
    var obj = {};
    obj.result = true;

    if (p.length < 8) {
        obj.result = false;
        obj.error = "Not long enough!"
        return obj;
    }

    var numUpper = 0;
    var numLower = 0;
    var numNums = 0;
    var numSpecials = 0;
    for (var i = 0; i < p.length; i++) {
        if (anUpperCase.test(p[i]))
            numUpper++;
        else if (aLowerCase.test(p[i]))
            numLower++;
        else if (aNumber.test(p[i]))
            numNums++;
        else if (aSpecial.test(p[i]))
            numSpecials++;
    }

    if (numUpper < 1 || numLower < 1 || numNums < 1 || numSpecials < 1) {
        obj.result = false;
        obj.error = "Password must include at lest one capetal, lower, number and a symbol";
        return obj;
    }
    return obj;
}
const mail_input = document.getElementById('email');
const mail_error = document.getElementById('emailError');
mail_input.addEventListener('focusout', function(event) {
    var mailCheck = isOkMail(mail_input.value);
    if (mailCheck == false) {
        //show the error
        mail_error.innerText = "Not a valid E-mail";
        mail_error.hidden = false;
    } else {
        $.post(emailAvailableLink, {
            emailCheck: mail_input.value
        }, function(data) {
            if (data.valid == "no") {
                mail_error.innerText = "E-mail already in use";
                mail_error.hidden = false;
            } else {
                mail_error.innerText = "";
                mail_error.hidden = true;
            }
        })
    }
});

function isOkMail(m) {
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if (m.match(mailformat)) {
        return true
    }
    return false
}