document.querySelector('form').addEventListener('submit', function (event) {
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


function formCaptcha() {
    var captchaId = "54cd0af70168ed6991797bf2a431c806";
    var product = "float";
    var gt = null;  
    
    initGeetest4({
        captchaId: captchaId,
        product: product,
    }, function (captchaObj) {
        gt = captchaObj;
        gt.appendTo("#captcha");

        gt.onSuccess(function (e) {
            var result = gt.getValidate();
            $('#lot_number').val(result.lot_number);
            $('#captcha_output').val(result.captcha_output);
            $('#pass_token').val(result.pass_token);
            $('#gen_time').val(result.gen_time);

            $('form').submit();
        });
    });

    $('#captchaModal').on('hidden.bs.modal', function (e) {
        if (gt) {
            gt.destroy();
        }
    });
    
    $('#reset_btn').click(function () {
        if (gt) {
            gt.reset();
        }
    });
}

