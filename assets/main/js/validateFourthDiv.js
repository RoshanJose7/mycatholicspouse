setInterval(function (){
    if (is_clicked)
    {
        validate_fourth_div();
    }
}, 500);

function validate_fourth_div() {
    is_valid = false;
    frm_spouse_valid = false;
    marre_date_valid = false;
    div_date_valid = false;
    m_a_date_valid = false;
    chldrn_valid = false;
    sns_valid = false;
    dghtrs_valid = false;
    

    frm_spouse = document.forms["matrimony-form"]["former_spouse_name_1"].value;
    marre_date = document.forms["matrimony-form"]["marriage_date_1"].value;
    div_date = document.forms["matrimony-form"]["divorce_date"].value;
    m_a_date = document.forms["matrimony-form"]["marriage_annulment_date"].value;
    chldrn = document.forms["matrimony-form"]["no_of_children_1"].value;
    sns = document.forms["matrimony-form"]["no_of_sons_1"].value;
    dghtrs = document.forms["matrimony-form"]["no_of_daughters_1"].value;
   

    if (frm_spouse === ""){
        x = document.getElementById('former_spouse_name_error1');
        x.innerHTML = '<li><small>Former Spouse name is required</small></li>';
    } else {
        x = document.getElementById('former_spouse_name_error1');
        x.innerHTML = '';
        frm_spouse_valid = true;
    }

    if (marre_date === ""){
        x = document.getElementById('marriage_date_error1');
        x.innerHTML = '<li><small>Marriage date is required</small></li>';
    } else {
        console.log('hi');
        x = document.getElementById('marriage_date_error1');
        x.innerHTML = '';
        marre_date_valid = true;
    }

    if (m_a_date === ""){
        x = document.getElementById('marriage_annulment_date_error1');
        x.innerHTML = '<li><small>Marriage Annulment date is required</small></li>';
    } else {
        console.log('hi');
        x = document.getElementById('marriage_annulment_date_error1');
        x.innerHTML = '';
        m_a_date_valid = true;
    }

    if (div_date === ""){
        x = document.getElementById('divorce_date_error1');
        x.innerHTML = '<li><small>Divorce date is required</small></li>';
    } else {
        x = document.getElementById('divorce_date_error1');
        x.innerHTML = '';
        div_date_valid = true;
    }

    if (chldrn === ""){
        x = document.getElementById('children_error1');
        x.innerHTML = '<li><small>Number of children from previous marriage is required</small></li>';
    } else {
        x = document.getElementById('children_error1');
        x.innerHTML = '';
        chldrn_valid = true;
    }

    if (sns === ""){
        x = document.getElementById('sons_error1');
        x.innerHTML = '<li><small>Number of sons from previous marriage is required</small></li>';
    } else {
        x = document.getElementById('sons_error1');
        x.innerHTML = '';
        sns_valid = true;
    }

    if (dghtrs === ""){
        x = document.getElementById('daughters_error1');
        x.innerHTML = '<li><small>Number of daughters from previous marriage is required</small></li>';
    } else {
        x = document.getElementById('daughters_error1');
        x.innerHTML = '';
        dghtrs_valid = true;
    }

    if(frm_spouse_valid && marre_date_valid && div_date_valid && chldrn_valid && m_a_date && sns_valid && dghtrs_valid )
        is_valid = true;

    
    return is_valid;
}       