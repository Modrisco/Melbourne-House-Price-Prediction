var submitButton = document.getElementById('submit-button');

submitButton.addEventListener('click', () => {
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
    }).then(res => res.json())
      .then(response => {
          console.log(response)
            var housePrice = document.getElementById('price')
            housePrice.innerHTML = '$' + response.price
        console.log('Success:', JSON.stringify(response))
    })
    .catch(error => console.error('Error:', error))
}
