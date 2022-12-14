function getTodos() {
    text = event.target.parentElement.querySelector('input').value
    console.log(text)
    if (text != '') {
        editTodo(text, 'add')
        text = ''
    }
}
function updated(id) {
    editTodo(id, 'update')
}
function editTodo(todo, condition) {
    if (window.XMLHttpRequest) {
        var xhttp = new XMLHttpRequest();
    } else {  // code for IE6, IE5
        var xhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4 && xhttp.status === 200) {
            var data = JSON.parse(this.responseText);
            location.reload()

        }
    }

    var url = "/GetTodos/"
    xhttp.open("GET", url + `?data=${todo}&event=${condition}`, true);
    xhttp.send();
}

linkers = document.querySelectorAll('.list > li > a')
for (let i = 0; i < linkers.length; i++) {
    if (linkers[i].pathname == window.location.pathname) {
        linkers[i].parentElement.classList.add('active')
    }
    else {
        linkers[i].parentElement.classList.remove('active')
    }
}

function dropdown() {
    document.querySelector('.focus-item').classList.toggle('active')
}

/*SEARCH BY USING A CITY NAME (e.g. athens) OR A COMMA-SEPARATED CITY NAME ALONG WITH THE COUNTRY CODE (e.g. athens,gr)*/
const form = document.querySelector(".top-banner form");
const input = document.querySelector(".top-banner input");
const msg = document.querySelector(".top-banner .msg");
const list = document.querySelector(".ajax-section .cities");
/*SUBSCRIBE HERE FOR API KEY: https://home.openweathermap.org/users/sign_up*/
const apiKey = "4d8fb5b93d4af21d66a2948710284366";

//ajax here
const url = `https://api.openweathermap.org/data/2.5/weather?q=Andijon&appid=${apiKey}&units=metric`;

fetch(url)
    .then(response => response.json())
    .then(data => {
        const { main, name, sys, weather } = data;
        console.log(main.temp)
        document.querySelector('.degres').innerText = main.temp
        const icon = `https://s3-us-west-2.amazonaws.com/s.cdpn.io/162656/${weather[0]["icon"]
            }.svg`;
        document.querySelector('.wheather-img').src = icon

    })
    .catch(() => {
        msg.textContent = "Please search for a valid city ????";
    });





function PrintElem(elem) {
    var mywindow = window.open('', 'PRINT', 'height=400,width=600');

    mywindow.document.write('<html><head><title>' + document.title + '</title>');
    mywindow.document.write('</head><body >');
    mywindow.document.write('<br><br>')
    mywindow.document.write('<h1>' + 'Baraka santexnika' + '</h1>');
    mywindow.document.write('<h4>Tel: +998972361677</h4>');
    mywindow.document.write('</body></html>');

    mywindow.document.close(); // necessary for IE >= 10
    mywindow.focus(); // necessary for IE >= 10*/

    mywindow.print();
    mywindow.close();

    return true;
}