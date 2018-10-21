let userInfo = {}

var submitButton = document.getElementById('submit-button');
// var loginButton = document.getElementById('login-button');

submitButton.addEventListener('click', () => {
    if(!userInfo.token){
        $('#notLogin').collapse('show')
        return
    }
    var houseData = {}
    houseData.Token = userInfo.token;
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

// loginButton.addEventListener('click', () => {
//     let un = document.getElementById('username').value
//     let up = document.getElementById('password').value
//     let userJSON = {
//         'username': un,
//         'password': up
//     }
// })

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
        userInfo.token = resp.token
        userInfo.username = resp.username
        userInfo.name = resp.name
        $('#notLogin').collapse('hide')
        $('#login_modal').modal('hide')
        $('#userSetting').removeClass('d-none')
        $('#login-modal-button').addClass('d-none')
    })
    .catch(err=>{
        // if(err === 0) $()
    })
})

$('#login_modal').on('hidden.bs.modal', ()=>{
    $('#invalidLogin').addClass('d-none')
    $('#usernameInput').prop('value','')
    $('#passwordInput').prop('value','')
})

$('#userProfile').on('shown.bs.modal', function () {
    $('#profile_username').text(userInfo.username || '')
    $('#profile_name').text(userInfo.name || '')
    $('#profile_token').text(userInfo.token || '')
})


$('#signOut').click(()=>{
    userInfo = {}
    $('#userSetting').addClass('d-none')
    $('#login-modal-button').removeClass('d-none')
})

$('#originalPwdBtn').click(()=>{
    userInfo.pwdRequestOri = $('#originalPwdInput').val()
    $('#originalPwdBtn').addClass('d-none')
    $('#originalPwdInput').addClass('d-none')
    $('#updatePwdBtn').removeClass('d-none')
    $('#updatePwdInput').removeClass('d-none')
})

$('#updatePwdBtn').click(()=>{
    $('#updatePwdBtn').addClass('d-none')
    $('#updatePwdInput').addClass('d-none')
    let url = "http://127.0.0.1:5000/auth/update"
    let request = {
        username: userInfo.username,
        password: userInfo.pwdRequestOri,
        new_password: $('#updatePwdInput').val()
    }
    console.log('request',request)
    fetch(url,{
            method:"PUT",
            body:JSON.stringify(request),
            header:{
                "Content-Type": "application/json"
            }
        }
    ).then(res=>{
        console.log(res)
        if(res.status !== 200) $('#failUpdatePwd').removeClass('d-none')
        else{
            $('#sucessUpdatePwd').removeClass('d-none')
        }
    }).catch(err=>consoel.log(err))
})

$('#failUpdatePwd').click(()=>{
    $('#failUpdatePwd').addClass('d-none')
    $('#originalPwdBtn').removeClass('d-none')
    $('#originalPwdInput').removeClass('d-none')
})

$('#sucessUpdatePwd').click(()=>{
    $('#sucessUpdatePwd').addClass('d-none')
    $('#originalPwdBtn').removeClass('d-none')
    $('#originalPwdInput').removeClass('d-none')
})

$('#copyToken').click(()=>{
    let temp = $("<input>")
    temp.val($('#profile_token').text()).select()
    document.execCommand("copy")
    temp.remove()
})

$(function () {
    $('[data-toggle="popover"]').popover()
})

// $('#clipboardPopover').popover('show')