var ready = (callback) => {
    if (document.readyState != "loading") callback();
    else document.addEventListener("DOMContentLoaded", callback);
}
ready(() => {
    document.querySelector(".header").style.height = window.innerHeight + "px";
})

function show_image(src, width, height, alt,where) {
    var img = document.createElement("img");
    img.src = src;
    // img.width = width;
    // img.height = height;
    img.alt = alt;
    img.className= "img-fluid"
    
    // This next line will just add it to the <body> tag
    document.getElementById(where).appendChild(img);
}

$(document).ready(function(){
    var jsonViewer = new JSONViewer();
    $('#researcher-show-list').click(function(){
        var url = "http://127.0.0.1:5000/demo/datasets";
        
        fetch(url,{
            method: "GET",
            mode: "cors"
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error(response.error)
            }
            return response.json();
        })
        .then(data => {
            var ul = document.getElementById("researcher-list");
            ul.replaceChildren();
            data.forEach(element => {
                var li = document.createElement("li");
                li.className = "researcher-list-li";
                li.appendChild(document.createTextNode(element));
                ul.appendChild(li); 
            });
            
        })
        .catch(function(error) {
            document.getElementById('messages').value = error;
        });
    })
    $('#researcher-show-sample-image').click(function(){
        var url = "http://127.0.0.1:5000/demo/datasets/demo-dataset/datastores/datastore-ds-raw/sample-image";
        fetch(url,{
            method: "GET",
            mode: "cors"
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error(response.error)
            }
        })
        .then(data => {
            document.getElementById("researcher-sample-image").style.display = "block";
            document.getElementById("json_sample_image_tags").style.display = "none";
            document.getElementById("researcher-sample-image").replaceChildren();
            show_image(url,281,213,data,"researcher-sample-image");
        })
        .catch(function(error) {
            alert(error);
        });
        
    })
    $('#researcher-sample-image-show-tags').click(function(){
        var url = "http://127.0.0.1:5000/demo/datasets/demo-dataset/datastores/datastore-ds-raw/sample-image?onlytags=true";
        fetch(url,{
            method: "GET",
            mode: "cors"
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error(response.error)
            }
            response.text().then(function(result){
                document.getElementById("researcher-sample-image").style.display = "none";
                document.getElementById("json_sample_image_tags").style.display = "block";
                var div = document.getElementById("json_sample_image_tags");
                div.replaceChildren();
                div.appendChild(jsonViewer.getContainer());
                maxLvl = 7;
                colAt = 7;
                jsonViewer.showJSON(JSON.parse(result), maxLvl, colAt); 
            })
        })
        .catch(function(error) {
            alert(error);
        });
    })
    $('#researcher-show-deid-image').click(function(){
        var url = "http://127.0.0.1:5000/demo/datasets/demo-dataset/datastores/datastore-ds-raw/sample-image/deid";
        fetch(url,{
            method: "GET",
            mode: "cors"
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error(response.error)
            }
        })
        .then(data => {
            document.getElementById("researcher-sample-image-deid").style.display = "block";
            document.getElementById("json_sample_deid_image_tags").style.display = "none";
            document.getElementById("researcher-sample-image-deid").replaceChildren();
            show_image(url,281,213,data,"researcher-sample-image-deid");
        })
        .catch(function(error) {
            alert(error);
        });
    })
    $('#researcher-show-deid-image-tags').click(function(){
        var url = "http://127.0.0.1:5000/demo/datasets/demo-dataset/datastores/datastore-ds-raw/sample-image/deid?onlytags=true";
        fetch(url,{
            method: "GET",
            mode: "cors"
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error(response.error)
            }
            response.text().then(function(result){
                document.getElementById("researcher-sample-image-deid").style.display = "none";
                document.getElementById("json_sample_deid_image_tags").style.display = "block";
                var div = document.getElementById("json_sample_deid_image_tags");
                div.replaceChildren();
                div.appendChild(jsonViewer.getContainer());
                maxLvl = 7;
                colAt = 7;
                jsonViewer.showJSON(JSON.parse(result), maxLvl, colAt); 
            })
        })
        .catch(function(error) {
            alert(error);
        });
    })

    $('#patient-list-mappings').click(function(){
        var url = "http://127.0.0.1:5000/demo/consents/demo-dataset/datastores/consent-ds/usermappings";
        fetch(url,{
            method: "GET",
            mode: "cors"
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error(response.error)
            }
            response.text().then(function(result){
                document.getElementById("json_patient_tags").style.display = "block";
                var div = document.getElementById("json_patient_tags");
                div.replaceChildren();
                div.appendChild(jsonViewer.getContainer());
                maxLvl = 7;
                colAt = 7;
                jsonViewer.showJSON(JSON.parse(result), maxLvl, colAt); 
            })
        })
        .catch(function(error) {
            alert(error);
        });
    })

    $('#patient-list-consent').click(function(){
        var url = "http://127.0.0.1:5000/demo/consents/demo-dataset";
        fetch(url,{
            method: "GET",
            mode: "cors"
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error(response.error)
            }
            response.text().then(function(result){
                document.getElementById("json_patient_tags").style.display = "block";
                var div = document.getElementById("json_patient_tags");
                div.replaceChildren();
                div.appendChild(jsonViewer.getContainer());
                maxLvl = 7;
                colAt = 7;
                jsonViewer.showJSON(JSON.parse(result), maxLvl, colAt); 
            })
        })
        .catch(function(error) {
            alert(error);
        });
    })

    $('#doctor-request-consent').click(function(){
        var url = "http://127.0.0.1:5000/demo/consents/demo-dataset/datastores/consent-ds/create";
        fetch(url,{
            method: "GET",
            mode: "cors"
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error(response.error)
            }
            response.text().then(function(result){
                document.getElementById("json_doctor_tags").style.display = "block";
                var div = document.getElementById("json_doctor_tags");
                div.replaceChildren();
                div.appendChild(jsonViewer.getContainer());
                maxLvl = 7;
                colAt = 7;
                jsonViewer.showJSON(JSON.parse(result), maxLvl, colAt); 
            })
        })
        .catch(function(error) {
            alert(error);
        });
    })

    $('#patient-grant-consent').click(function(){
        var url = "http://127.0.0.1:5000/demo/consents/demo-dataset/datastores/consent-ds/consents/activate";
        fetch(url,{
            method: "GET",
            mode: "cors"
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error(response.error)
            }
            response.text().then(function(result){
                document.getElementById("json_patient_tags").style.display = "block";
                var div = document.getElementById("json_patient_tags");
                div.replaceChildren();
                div.appendChild(jsonViewer.getContainer());
                maxLvl = 7;
                colAt = 7;
                jsonViewer.showJSON(JSON.parse(result), maxLvl, colAt); 
            })
        })
        .catch(function(error) {
            alert(error);
        });
    })

    $("#nlp-retrieve").click(function(){
        var file = document.getElementById("customFile").files[0];
        var url = "http://127.0.0.1:5000//demo/nlp";

        var data = new FormData()
        data.append('file',file)
        fetch(url,{
            method: "POST",
            mode: "cors",
            body: data
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error(response.error)
            }
            response.text().then(function(result){
                document.getElementById("json_nlp_tags").style.display = "block";
                var div = document.getElementById("json_nlp_tags");
                div.replaceChildren();
                div.appendChild(jsonViewer.getContainer());
                maxLvl = 7;
                colAt = 7;
                jsonViewer.showJSON(JSON.parse(result), maxLvl, colAt); 
            })
        })
        .catch(function(error) {
            alert(error);
        });




    })
})