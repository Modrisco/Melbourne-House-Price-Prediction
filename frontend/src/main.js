var clickButton = document.getElementById('submit')
clickButton.addEventListener('click', () => {
    var token = prompt("token", "");
    if (token == '') {
        alert('Enter a token!')
    }
    var data = {}
    data.Token = token;
    data.Suburb = document.getElementsByTagName('input')[0].value;
    data.Rooms = document.getElementsByTagName('input')[1].value;
    data.Type = document.getElementsByTagName('input')[2].value;
    data.Distance = document.getElementsByTagName('input')[3].value;
    data.Car = document.getElementsByTagName('input')[4].value;
    data.Building_Area = document.getElementsByTagName('input')[5].value;
    data.Year = document.getElementsByTagName('input')[6].value;
    console.log(data)
    getPrice(data)
})

function getPrice(data) {
    var url = 'http://127.0.0.1:5000/house/data';

    fetch(url, {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        mode: "cors", // no-cors, cors, *same-origin
        body: JSON.stringify(data), // data can be `string` or {object}!
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, same-origin, *omit
        headers: {
            "Content-Type": "application/json; charset=utf-8",
            // "Content-Type": "application/x-www-form-urlencoded",
        },
        redirect: "follow", // manual, *follow, error
        // referrer: "no-referrer", // no-referrer, *client
    }).then(res => res.json())
.then(response => {
        var price = document.getElementById('price')
        price.innerHTML = 'Price: ' + response.price
    console.log('Success:', JSON.stringify(response))
})
.catch(error => console.error('Error:', error));
}