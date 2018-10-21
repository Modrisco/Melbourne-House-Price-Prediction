userToken = ""

var submitButton = document.getElementById('submit-button');

submitButton.addEventListener('click', () => {
    if(!userToken){
        $('#notLogin').collapse('show')
        console.log('please login')
        return
    }
    var houseData = {}
    houseData.Token = userToken;
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
    })
    .then(res => res.json())
    .then(response => {
          console.log(response)
            var housePrice = document.getElementById('price')
            if(response.price){
                housePrice.innerText = response.price
                if(!$('#invalidResult').hasClass('d-none')) $('#invalidResult').addClass('d-none')
                $('#result').removeClass('d-none')
            }
            else {
                if(!$('#result').hasClass('d-none')) $('#result').addClass('d-none')
                $('#invalidResult').removeClass('d-none')
            }
        console.log('Success:', JSON.stringify(response))
    })
    .catch(error => console.error('Error:', error))
    
}

console.log('user')
$('#loginSubmit').click(()=>{
    let url = 'http://127.0.0.1:5000/auth/login'
    let data = {
        username: $('#usernameInput').val(),
        password: $('#passwordInput').val()
    }
    fetch(url,{
        method:'POST',
        body:JSON.stringify(data),
        headers:{
            "Content-Type":"application/json"
        }
    })
    .then(res=>{
        if(res.status === 400 || res.status === 403) {
            $('#invalidLogin').removeClass('d-none')
            throw 0
        }
        return res.json()
    })
    .then(resp=>{
        console.log(resp.token)
        // regex = new new RegExp(';\s?')
        userToken = resp.token
        $('#notLogin').collapse('hide')
        $('#login_modal').modal('hide')
    })
    .catch(err=>{
        // if(err === 0) $()
    })
})

$('#login_modal').on('hidden.bs.modal', function (e) {
    $('#invalidLogin').addClass('d-none')
    $('#usernameInput').prop('value','')
    $('#passwordInput').prop('value','')
})