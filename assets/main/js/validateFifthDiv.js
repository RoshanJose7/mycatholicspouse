setInterval(function (){
    if (is_clicked)
    {
        validate_widowed_div();
    }
}, 500);

function validate_widowed_div() {
    is_valid = false;
    former_spouse_valid = false;
    marriage_date_valid = false;
    death_date_valid = false;
    children_valid = false;
    sons_valid = false;
    daughters_valid = false;
    
    former_spouse = document.forms["matrimony-form"]["former_spouse_name_2"].value;
    marriage_date = document.forms["matrimony-form"]["marriage_date_2"].value;
    death_date = document.forms["matrimony-form"]["date_of_death"].value;
    children = document.forms["matrimony-form"]["no_of_children_2"].value;
    sons = document.forms["matrimony-form"]["no_of_sons_2"].value;
    daughters = document.forms["matrimony-form"]["no_of_daughters_2"].value;
   

    if (former_spouse === ""){
        x = document.getElementById('former_spouse_name_error');
        x.innerHTML = '<li><small>Former Spouse name is required</small></li>';
    } else {
        x = document.getElementById('former_spouse_name_error');
        x.innerHTML = '';
        former_spouse_valid = true;
    }

    if (marriage_date === ""){
        x = document.getElementById('marriage_date_error');
        x.innerHTML = '<li><small>Marriage date is required</small></li>';
    } else {
        x = document.getElementById('marriage_date_error');
        x.innerHTML = '';
        marriage_date_valid = true;
    }

    if (death_date === ""){
        x = document.getElementById('death_date_error');
        x.innerHTML = '<li><small>Death date is required</small></li>';
    } else {
        x = document.getElementById('death_date_error');
        x.innerHTML = '';
        death_date_valid = true;
    }

    if (children === ""){
        x = document.getElementById('children_error');
        x.innerHTML = '<li><small>Number of children from previous marriage is required</small></li>';
    } else {
        x = document.getElementById('children_error');
        x.innerHTML = '';
        children_valid = true;
    }

    if (sons === ""){
        x = document.getElementById('sons_error');
        x.innerHTML = '<li><small>Number of sons from previous marriage is required</small></li>';
    } else {
        x = document.getElementById('sons_error');
        x.innerHTML = '';
        sons_valid = true;
    }

    if (daughters === ""){
        x = document.getElementById('daughters_error');
        x.innerHTML = '<li><small>Number of daughters from previous marriage is required</small></li>';
    } else {
        x = document.getElementById('daughters_error');
        x.innerHTML = '';
        daughters_valid = true;
    }

    if(former_spouse_valid && marriage_date_valid && death_date_valid && children_valid && sons_valid && daughters_valid)
        is_valid = true;

    return is_valid;
}