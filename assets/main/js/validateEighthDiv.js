function clear_error(atchs){
    atchs.forEach((atch, index) => {
        atch.parentElement.children[2].innerHTML = "";
    })
}

setInterval(function () {
        if(is_clicked){
            validate_eighth_div();
        }
    }, 500);

function validate_eighth_div() {
    atchs = [...document.getElementById('7').getElementsByTagName("input")];
    atchs.shift();
    // atchs.splice(9, 2);
    new_atchs = [];
    for(var i = 0; i<atchs.length; i++){
        var x = atchs[i].id;
        if (x === "Civil Divorce Document") {
            if(document.getElementById("Divorced").checked)
            new_atchs.push(atchs[i]);
        }
        else if (x === "Marriage Annulment Document"){
            if(document.getElementById("Divorced").checked)
            new_atchs.push(atchs[i]);
        }
        else if (x === "Former Spouse Death Certificate"){
            if(document.getElementById("Widowed").checked)
                new_atchs.push(atchs[i]);
        }
        else if (x === "Disability Certificate"){
            if(document.forms["matrimony-form"]["Disability"].value === "Yes")
            new_atchs.push(atchs[i]);
        }
        else{
            new_atchs.push(atchs[i]);
        }
        // if(x === "Civil Divorce Document" && (!document.getElementById("Legal Divorce").checked || document.getElementById("Single").checked || document.getElementById("Widowed").checked || document.getElementById("Church Divorce").checked))
        //     continue;
        // else if(x === "Marriage Annulment Document" && (!document.getElementById("Church Divorce").checked || document.getElementById("Single").checked || document.getElementById("Widowed").checked || document.getElementById("Legal Divorce").checked))
        //     continue;
        // if (x === "Disability Certificate" && document.forms["matrimony-form"]["Disability"].value === "No")
        //     continue;
        // new_atchs.push(atchs[i]);
    }
    // console.log(atchs);
    req_list = new_atchs.map((atch) => required(atch));
    required_li = document.createElement("li");
    required_li.innerHTML = "<small>This is required</small>";
    size_li = document.createElement("li");
    size_li.innerHTML = "<small>File size exceeded size limit.</small>";
    ext_li = document.createElement("li");
    ext_li.innerHTML = "<small>Invalid File Format.</small>";
    clear_error(atchs);
    var not_error = true;
    new_atchs.forEach((atch, index) => {
        if ( !req_list[index] ){
            var required_li_new = required_li.cloneNode(true);
            atch.parentElement.children[2].appendChild(required_li_new);
        } else {
            if (!(atch.className == "custom-file-input doc") && !['jpg','png','bmp','jpeg'].includes(atch.files[0].name.split(".").pop())){
                var ext_li_new = ext_li.cloneNode(true);
                atch.parentElement.children[2].appendChild(ext_li_new);
                not_error = false;
            }
            if (parseInt(atch.files[0].size) > 2097155){
                var size_li_new = size_li.cloneNode(true);
                atch.parentElement.children[2].appendChild(size_li_new);
                not_error = false;
            }
        }
        // atch.parentElement.children[2].innerHTML = req_list[index] ? "" : "<li><small>This is required</small></li>";
    })
    return and_output(req_list) && not_error;
}