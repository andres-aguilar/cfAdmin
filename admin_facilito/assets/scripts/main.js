
let form = document.querySelector("#search-user-form") 

form.addEventListener('submit', function(evt) {
    evt.preventDefault()

    action = form.action
    username =  document.querySelector("#username").value

    axios.get(`${action}?username=${username}`)
    .then(function (response) {
        console.log(response)
    })
    .catch(function (error) {
        console.log(error)
    })
})

