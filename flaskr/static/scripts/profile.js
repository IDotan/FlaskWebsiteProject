function validateForm() {
    if (document.getElementById('pswError').hidden == false){            
        return false;
    }
}

const psw_input = document.getElementById('new_psw');
const psw_error = document.getElementById('pswError');
psw_input.addEventListener('focusout', function (event) {
    var userCheck = isOkPass(psw_input.value);
    if (userCheck.result == false) {
        //show the error
        psw_error.innerText = userCheck.error;
        psw_error.hidden = false;
    }
    else {
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
