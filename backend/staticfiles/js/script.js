function getTodos(){
    text = event.target.parentElement.querySelector('input').value
    console.log(text)
    if (text != ''){
        editTodo(text, 'add')
        text=''
    }
}
function updated(id){
    console.log(id)
    editTodo(id, 'update')
}
function editTodo(todo, condition){
    if (window.XMLHttpRequest) {
        var xhttp = new XMLHttpRequest();
    } else {  // code for IE6, IE5
        var xhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4 && xhttp.status === 200) {
            var data = JSON.parse(this.responseText);
            console.log(data)
            location.reload()

        }
    }
    
    var url = "/GetTodos/"
    xhttp.open("GET", url + `?data=${todo}&event=${condition}`, true);
    xhttp.send();
}

linkers = document.querySelectorAll('.list > li > a')
for(let i = 0; i < linkers.length; i++){
    if(linkers[i].pathname == window.location.pathname){
        linkers[i].parentElement.classList.add('active')
    }
    else{
        linkers[i].parentElement.classList.remove('active')
    }
}

function dropdown(){
    document.querySelector('.focus-item').classList.toggle('active')
}