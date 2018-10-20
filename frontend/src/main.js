var submitButton = document.getElementById('submit-button');

submitButton.addEventListener('click', () => {
    var form = new FormData(document.getElementById("rawInput"));
    window.setInterval(()=>console.log(form), 1000);
    var token = prompt("token", "");
    if (token == '') {
        alert('Enter a token!')
    }
    var houseData = {}
    houseData.Token = token;
    houseData.Suburb = document.getElementById('suburb').value;
    houseData.Rooms = document.getElementById('bedrooms').value;
    houseData.Type = document.getElementById('type').value;
    houseData.Distance = document.getElementById('distance').value;
    houseData.Car = document.getElementById('cars').value;
    houseData.Building_Area = document.getElementById('area').value;
    houseData.Year = document.getElementById('buildingAge').value;
    console.log(houseData)
    getPrice(houseData)
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
    }).catch(error => console.error('Error:', error))
    .then(res => res.json())
    .then(response => {
          console.log(response)
            var housePrice = document.getElementById('price')
            if(response.price) housePrice.innerText = response.price
            else {
                $('#invalidResult').toggleClass('d-none')
                $('#result').toggleClass('d-none')
            }
        console.log('Success:', JSON.stringify(response))
    })
    
}

//>> Alan Code

