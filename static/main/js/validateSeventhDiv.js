setInterval(() => {
    if (is_clicked) console.log("clicked");
}, 500);

function validate_preference_div() {
    is_valid = false;
    lower_age_valid = false;
    upper_age_valid = false;
    language_valid = false;
    residence_valid = false;
    education_valid = false;
    employment_valid = false;
    lower_salary_valid = false;
    upper_salary_valid = false;

    lower_age = document.forms["matrimony-form"]["lower_age"].value;
    upper_age = document.forms["matrimony-form"]["upper_age"].value;

    language = document.forms["matrimony-form"]["language"].value;
    residence = document.forms["matrimony-form"]["place_of_residence"].value;
    education = document.forms["matrimony-form"]["education"].value;
    employment = document.forms["matrimony-form"]["employment"].value;
    lower_salary = document.forms["matrimony-form"]["salary_lower"].value;
    upper_salary = document.forms["matrimony-form"]["salary_upper"].value;

    if (lower_age === "") {
        x = document.getElementById("lower_age_bound_error");
        x.innerHTML = "<li><small>Lower Age Bound is required</small></li>";
    } else {
        x = document.getElementById("lower_age_bound_error");
        if (
            parseInt(lower_age) > parseInt(upper_age) ||
            parseInt(lower_age) < 18
        ) {
            x.innerHTML = "<li><small>Invalid value</small></li>";
        } else {
            x.innerHTML = "";
            lower_age_valid = true;
        }
    }

    if (upper_age === "") {
        x = document.getElementById("upper_age_bound_error");
        x.innerHTML = "<li><small>Upper Age Bound is required</small></li>";
    } else {
        x = document.getElementById("upper_age_bound_error");
        if (
            parseInt(upper_age) < parseInt(lower_age) ||
            parseInt(upper_age) < 18
        ) {
            x.innerHTML = "<li><small>Invalid value</small></li>";
        } else {
            x.innerHTML = "";
            upper_age_valid = true;
        }
    }

    if (residence === "") {
        x = document.getElementById("place_of_residence_error");
        x.innerHTML = "<li><small>Place of residence is required</small></li>";
    } else {
        x = document.getElementById("place_of_residence_error");
        x.innerHTML = "";
        residence_valid = true;
    }

    if (language === "") {
        x = document.getElementById("language_error");
        x.innerHTML = "<li><small>Language is required</small></li>";
    } else {
        x = document.getElementById("language_error");
        x.innerHTML = "";
        language_valid = true;
    }

    if (education === "") {
        x = document.getElementById("education_error");
        x.innerHTML = "<li><small>Education is required</small></li>";
    } else {
        x = document.getElementById("education_error");
        x.innerHTML = "";
        education_valid = true;
    }

    if (employment === "") {
        x = document.getElementById("employment_error");
        x.innerHTML = "<li><small>Occupation is required</small></li>";
    } else {
        x = document.getElementById("employment_error");
        x.innerHTML = "";
        employment_valid = true;
    }

    if (lower_salary === "") {
        x = document.getElementById("salary_lower_error");
        x.innerHTML = "<li><small>Lower Salary Bound is required</small></li>";
    } else {
        x = document.getElementById("salary_lower_error");
        if (lower_salary < 0)
            x.innerHTML =
                "<li><small>Lower Salary Bound should be > 0</small></li>";
        else {
            x.innerHTML = "";
            lower_salary_valid = true;
        }
    }

    if (upper_salary === "") {
        x = document.getElementById("salary_upper_error");
        x.innerHTML = "<li><small>Upper Salary Bound is required</small></li>";
    } else {
        x = document.getElementById("salary_upper_error");
        console.log("else");
        console.log(upper_salary < lower_salary);
        if (parseInt(upper_salary) < parseInt(lower_salary)) {
            x.innerHTML =
                "<li><small>Upper Salary Bound should be >= Lower Salary Bound</small></li>";
        } else {
            x.innerHTML = "";
            upper_salary_valid = true;
        }
    }

    if (
        lower_age_valid &&
        upper_age_valid &&
        language_valid &&
        residence_valid &&
        education_valid &&
        employment_valid &&
        lower_salary_valid &&
        upper_salary_valid
    )
        is_valid = true;

    return true;
}
