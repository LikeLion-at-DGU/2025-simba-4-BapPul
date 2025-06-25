let userId = document.getElementById('user-id');
let userPw = document.getElementById('user-pw');
let userPwcheck = document.getElementById('user-pwCheck');
let userName = document.getElementById('user-nickname');
let userSchool = document.getElementById('user-school');

const button = document.getElementById("signupBtn");

function checkId(value) {
    return /[A-Za-z]/.test(value) &&
        /[0-9]/.test(value) &&
        /^[A-Za-z0-9]+$/.test(value);
}
function checkPw(value) {
    return value.length >= 8 &&
        /[A-Za-z]/.test(value) &&
        /[0-9]/.test(value) &&
        /^[A-Za-z0-9]+$/.test(value);
}

function isMatch(password1, password2) {
    return password1 === password2;
}

function checkName(value) {
    return /^[가-힣]{1,6}$/.test(value);
}

function validateForm() {
    const idValid = checkId(userId.value);
    const pwValid = checkPw(userPw.value);
    const pwSame = isMatch(userPw.value, userPwcheck.value);
    const nameValid = checkName(userName.value);
    const schoolFilled = userSchool.value.trim() !== '';

    const allValid = idValid && pwValid && pwSame && nameValid && schoolFilled;

    if (allValid) {
        button.disabled = false;
        button.style.backgroundColor = '#FF4C4F'; // 핑크색
        button.style.color = 'white';
        button.style.cursor = 'pointer';
    } else {
        button.disabled = true;
        button.style.backgroundColor = 'gray';
        button.style.color = 'white';
        button.style.cursor = 'not-allowed';
    }

    console.log({
        idValid,
        pwValid,
        pwSame,
        nameValid,
        schoolFilled
    });
    
}

[userId, userPw, userPwcheck, userName, userSchool].forEach(el => {
    el.addEventListener('input', validateForm);
});