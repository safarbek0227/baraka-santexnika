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
        console.log(icon)
        console.log(weather[0])
        document.querySelector('.wheather-img').src = icon

    })
    .catch(() => {
        msg.textContent = "Please search for a valid city 😩";
    });