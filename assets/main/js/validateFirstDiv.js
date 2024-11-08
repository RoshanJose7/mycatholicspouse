setInterval(function (){
    if (is_clicked)
    validate_first_div();
}, 500);

is_clicked = false;

function validate_first_div() {
    is_valid = false;
    first_name_valid = false;
    last_name_valid = false;
    email_valid = false;
    phone_valid = false;
    mt_valid = false;
    addr_l1_valid = false;
    ct_valid = false;
    state_valid = false;
    zip_valid = false;

    first_name = document.forms["matrimony-form"]["first_name"].value;
    last_name = document.forms["matrimony-form"]["last_name"].value;
    email = document.forms["matrimony-form"]["email"].value;
    phone_no = document.forms["matrimony-form"]["phone_number"].value;
    mt = document.forms["matrimony-form"]["mother_tongue"].value;
    addr_l1 = document.forms["matrimony-form"]["addr_1"].value;
    ct = document.forms["matrimony-form"]["city"].value;
    state = document.forms["matrimony-form"]["state"].value;
    zip = document.forms["matrimony-form"]["pin_code"].value;

    if (first_name === ""){
        x = document.getElementById('first_name_error');
        x.innerHTML = '<li><small>First Name is required</small></li>';
    } else {
        x = document.getElementById('first_name_error');
        x.innerHTML = '';
        first_name_valid = true;
    }

    if (last_name === ""){
        x = document.getElementById('last_name_error')
        x.innerHTML = '<li><small>Last Name is required</small></li>';
    } else {
        x = document.getElementById('last_name_error')
        x.innerHTML = '';
        last_name_valid = true;
    }

    if (email === ""){
        x = document.getElementById('email_error');
        x.innerHTML = '<li><small>Email is required</small></li>';
    } else {
        x = document.getElementById('email_error');
        x.innerHTML = '';
        var mailformat = /^(?:[\w\!\#\$\%\&\'\*\+\-\/\=\?\^\`\{\|\}\~]+\.)*[\w\!\#\$\%\&\'\*\+\-\/\=\?\^\`\{\|\}\~]+@(?:(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-](?!\.)){0,61}[a-zA-Z0-9]?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9\-](?!$)){0,61}[a-zA-Z0-9]?)|(?:\[(?:(?:[01]?\d{1,2}|2[0-4]\d|25[0-5])\.){3}(?:[01]?\d{1,2}|2[0-4]\d|25[0-5])\]))$/;
        if(!email.match(mailformat)){
            x.innerHTML = '<li><small>Invalid Email</small></li>';
        }
        else {
            x.innerHTML = '';
            email_valid = true;
        }
    }

    if (phone_no === ""){
        x = document.getElementById('phone_error');
        x.innerHTML = '<li><small>Phone Number is required</small></li>';
    }
    else {
        x = document.getElementById('phone_error');
        if(!phone_no.match(/^\d{10}$/)){
            x.innerHTML = '<li><small>Invalid Phone Number</small></li>';
        }
        else {
            x.innerHTML = '';
            phone_valid = true;
        }
    }

    if(mt === "") {
        x = document.getElementById('mt_error');
        x.innerHTML = '<li><small>Mother Tongue is required</small></li>';
    }
    else {
        x = document.getElementById('mt_error');
        x.innerHTML = '';
        mt_valid = true;
    }

    if(addr_l1 === "") {
        x = document.getElementById('addr_l1_error');
        x.innerHTML = '<li><small>Address Line #1 is required</small></li>';
    }
    else {
        x = document.getElementById('addr_l1_error');
        x.innerHTML = '';
        addr_l1_valid = true;
    }

    if(ct === "") {
        x = document.getElementById('ct_error');
        x.innerHTML = '<li><small>City is required</small></li>';
    }
    else {
        x = document.getElementById('ct_error');
        x.innerHTML = '';
        ct_valid = true;
    }

    if(state === "Select State"){
        x = document.getElementById('state_error');
        x.innerHTML = '<li><small>State is required</small></li>';
    }
    else {
        x = document.getElementById('state_error');
        x.innerHTML = '';
        state_valid = true;
    }

    if(zip === "") {
        x = document.getElementById('zip_error');
        x.innerHTML = '<li><small>Pin Code is required</small></li>';
    }
    else {
        x = document.getElementById('zip_error');
        x.innerHTML = '';
        zip_valid = true;
    }

    if(first_name_valid && last_name_valid && email_valid && phone_valid && mt_valid && addr_l1_valid && state_valid)
        is_valid = true;

    return is_valid;
}