setInterval(function(){
    if (is_clicked)
        validate_family_div();
},500);



function validate_family_div(){
    is_valid = false;
    fathers_name_valid = false;
    mothers_name_valid = false;
    siblings_valid = false;
    brothers_valid = false;
    sisters_valid = false;
    family_members_valid = false;
    
    mothers_name = document.forms["matrimony-form"]["mothers_name"].value;
    fathers_name = document.forms["matrimony-form"]["fathers_name"].value; 
    siblings = document.forms["matrimony-form"]["siblings"].value;
    brothers = document.forms["matrimony-form"]["brothers"].value;
    sisters = document.forms["matrimony-form"]["sisters"].value;
    family_members = document.forms["matrimony-form"]["family_members"].value;
   
    if (mothers_name === ""){
        x = document.getElementById('mothers_name_error');
        x.innerHTML = '<li><small>Mother\'s Name is required</small></li>';
    } else {
        x = document.getElementById('mothers_name_error');
        x.innerHTML = '';
        mothers_name_valid = true;
    }

    if (fathers_name === ""){
        x = document.getElementById('fathers_name_error');
        x.innerHTML = '<li><small>Father\'s Name is required</small></li>';
    } else {
        x = document.getElementById('fathers_name_error');
        x.innerHTML = '';
        fathers_name_valid = true;
    }

    if (siblings === ""){
        x = document.getElementById('siblings_error');
        x.innerHTML = '<li><small>Number of Siblings is required</small></li>';
    } else {
        x = document.getElementById('siblings_error');
        x.innerHTML = '';
        siblings_valid = true;
    }

    if (brothers === ""){
        x = document.getElementById('brothers_error');
        x.innerHTML = '<li><small>Number of brothers is required</small></li>';
    } else {
        x = document.getElementById('brothers_error');
        x.innerHTML = '';
        brothers_valid = true;
    }

    if (sisters === ""){
        x = document.getElementById('sisters_error');
        x.innerHTML = '<li><small>Number of sisters is required</small></li>';
    } else {
        x = document.getElementById('sisters_error');
        x.innerHTML = '';
        sisters_valid = true;
    }

    if (family_members === ""){
        x = document.getElementById('family_members_error');
        x.innerHTML = '<li><small>Number of family members residing at your Residence is required</small></li>';
    } else {
        x = document.getElementById('family_members_error');
        x.innerHTML = '';
        family_members_valid = true;
    }



    if(fathers_name_valid && mothers_name_valid && siblings_valid && brothers_valid && sisters_valid && family_members_valid )
        is_valid = true;

    
    return is_valid;
}        