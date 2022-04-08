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
    $('#researcher-show-list').click(function(){
        var url = "http://127.0.0.1:5000/demo";
        
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
                li.appendChild(document.createTextNode(element));
                ul.appendChild(li); 
            });
            
        })
        .catch(function(error) {
            document.getElementById('messages').value = error;
        });
    })
    $('#researcher-show-sample-image').click(function(){
        var url = "http://127.0.0.1:5000/demo/demo-dataset/datastores/datastore-ds-raw/sample-image";
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
            console.log(data);
            show_image(url,281,213,data,"researcher-sample-image");
        })
        .catch(function(error) {
            alert(error);
        });
    })
    $('#researcher-show-deid-image').click(function(){
        var url = "http://127.0.0.1:5000/demo/demo-dataset/datastores/datastore-ds-raw/sample-image/deid";
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
            console.log(data);
            show_image(url,281,213,data,"researcher-sample-image-deid");
        })
        .catch(function(error) {
            alert(error);
        });
    })
})