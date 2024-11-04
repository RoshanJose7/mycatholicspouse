and_output = (x) => x.reduce((acc, i) => (acc && i), true);

required = (x) => ((x.value === "") ? false : true);

setInterval(function () {
    if (is_clicked){
        validate_third_div();
    }
}, 500);

function validate_third_div() {
    inps = document.getElementById("2").getElementsByTagName("input");
    inps = [...inps];
    inps.shift();
    new_inps = []
    for(var i = 0; i < inps.length; i++){
        if(inps[i]["className"] !== "form-check-input")
            new_inps.push(inps[i])
    }
    req_list = new_inps.map((inp) => required(inp));

    for(var i = 0; i < new_inps.length; i++) {
        try {
            var obj = new_inps[i].parentElement.children[2];
            obj.innerHTML = req_list[i] ? "" : "<li><small>This is required</small></li>";
        } catch (e) {
            req_list[i] = true;
            continue;
        }
    }
    let disability_not_given = true;
    let disability_type = document.getElementById("id_disability_type").value;
    let x = document.getElementById("id_error_disability");
    if(document.forms["matrimony-form"]["Disability"].value === "Yes" && disability_type == ""){
        disability_not_given = false;
        x.innerHTML = "<li><small>This is required</small></li>";
    } else {
        x.innerHTML = "";
    }
    return and_output(req_list.slice(0, 12)) && disability_not_given;
}