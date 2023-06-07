document.querySelector('form').addEventListener('submit', function(event) {
    var password = document.querySelector('#password').value;
    var passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
    var passwordMessage = document.querySelector('#password-message');

    if (!passwordRegex.test(password)) {
        event.preventDefault();
        document.querySelector('#password').style.borderColor = 'red';
        passwordMessage.style.display = 'block';
    } else {
        document.querySelector('#password').style.borderColor = '';
        passwordMessage.style.display = 'none';
    }
});