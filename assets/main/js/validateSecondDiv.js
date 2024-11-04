objs = document.getElementById("1").getElementsByClassName('form-group');
certs = [...document.getElementById("cert").children];
objs = [...objs];
objs.shift();

s = [...document.getElementsByName("Education Level")];
s.map((s) => s.addEventListener("change", function (){
    clear_state();
    validate_second_div();
}));


function isNumeric(n) {
    return !isNaN(parseFloat(n)) && isFinite(n);
}

function clear_state(){
    for(var i=0; i<objs.length; i++){
        document.getElementById(objs[i]['children'][2].id).innerHTML = "";
    }
    for(var i=0; i<certs.length; i++){
        document.getElementById(certs[i]['children'][2].id).innerHTML = "";
    }
}

setInterval(function(){
    clear_state();
    validate_second_div();
},500);

function input_valid(start, end) {
    const temp_valid = objs.slice(start, end).map(
        (obj) => {
        inp = obj['children'][1];
        if(inp.value === "")
            return false;
        else if(inp.type === "number"){
            if(!isNumeric(inp.value)) {
                return false;
            }
            else {
                if(parseFloat(inp.value) > 100.0)
                    return false;
                return true;
            }
        }
        return true;
    });
    return temp_valid;
}

function upload_valid(start, end){
    const temp_valid = certs.slice(start, end).map(
        (cert) => {
            inp = cert['children'][0];
            if(inp.value){
                return true;
            } else {
                return false;
            }
        });
    return temp_valid;
};

function set_errors(start, end, x, y) {
    temp = objs.slice(start, end);
    for(var i=0; i<x.length; i++){
        document.getElementById(temp[i]['children'][2].id).innerHTML = !x[i]?"<li><small>Invalid Entry</small></li>":"";
    }
    temp = certs;
    for(var i=0; i<y.length; i++){
        document.getElementById(temp[i]['children'][2].id).innerHTML = !y[i]?"<li><small>Required</small></li>":"";
    }
}

and_output = (x) => x.reduce((acc, i) => (acc && i), true);

function validate_second_div() {
    is_valid = true;
    level = document.forms["matrimony-form"]["Education Level"].value;
    if(level === 'Less Than 10th'){
        return is_valid;
    }
    else if(level === '10th'){
        var x = input_valid(0, 2);
        var y = upload_valid(0, 1);
        set_errors(0, 2, x, y);
        return is_valid && and_output(x) && and_output(y);
    }
    if(level === '12th'){
        var x = input_valid(0, 4);
        var y = upload_valid(0, 1);
        set_errors(0, 4, x, y);
        return is_valid && and_output(x) && and_output(y);
    }
    if(level === 'Graduate'){
        var x = input_valid(0, 6);
        var y = upload_valid(0, 1);
        set_errors(0, 6, x, y);
        return is_valid && and_output(x) && and_output(y);
    }
    if(level === 'Post Graduate'){
        var x =  input_valid(0, 8);
        var y = upload_valid(0, 1);
        set_errors(0, 8, x, y);
        return is_valid && and_output(x) && and_output(y);
    }
    if(level === 'Other'){
        var x = input_valid(8, 11);
        var y = upload_valid(0, 1);
        set_errors(8, 11, x, y);
        return is_valid && and_output(x) && and_output(y);
    }
}
