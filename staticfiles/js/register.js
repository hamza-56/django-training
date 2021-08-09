function validateUsername(value) {
    return /^(?=[a-zA-Z0-9._]{8,150}$)(?!.*[_.]{2})[^_.].*[^_.]$/.test(value);
};

function validatePassword(value) {
    return /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,20}$/.test(value);
}

function validateRegisterForm() {
    var form = document.getElementById('id_register_form'),
        username = form.querySelector('#id_username'),
        password1 = form.querySelector('#id_password1'),
        password2 = form.querySelector('#id_password2');

    form.addEventListener('submit', function (e) {
        console.log(validateUsername(username.value));
        if (!(validateUsername(username.value))) {
            window.alert('Please choose a suitable username')
            e.preventDefault();
            return;
        }

        if (!(validatePassword(password1.value))) {
            window.alert('Please choose a strong password')
            e.preventDefault();
            return;
        }

        if (password1.value != password2.value) {
            window.alert('Passwords donot match')
            e.preventDefault();
            return;
        }

    })
}

validateRegisterForm();
