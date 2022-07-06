console.log("hi")

function getUser() {
     const input = document.getElementById("frontend_req").user_id.value;
     fetch(` https://reqres.in/api/users/${input}`)
        .then(response => response.json())
        .then( responseOBJECT => displayUser(responseOBJECT.data))
        .catch(
            err => console.log(err)
    );
}

function displayUser(data){
    const div = document.getElementById("place_holder_for_response")
    div.innerHTML=  `
                    <br>
                    <h3>${data?.first_name} ${data?.last_name}</h3>
                    <h4>${data?.email}</h4>
                    <img src="${data?.avatar}" alt="Profile Picture"/>
                `
}
