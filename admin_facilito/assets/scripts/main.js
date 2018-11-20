
let form = document.querySelector("#search-user-form") 

form.addEventListener('submit', function(evt) {
    evt.preventDefault()

    action = form.action
    username =  document.querySelector("#username").value

    axios.get(`${action}?username=${username}`)
    .then(function (response) {
        let html = ""
        let link = window.location.pathname + "add/"
        
        response.data.forEach(el => {
                user = el.fields
                let href = link + user.username + "/"
                html += `<li> ${user.username} <a href="${href}">Agregar</a></li>`
        })

        document.querySelector("#results").innerHTML = html
    })
    .catch(function (error) {
        console.log(error)
    })
})

