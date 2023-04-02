'use strict'

//user authentification
function userLogin () {
    document.getElementById('appMessages').innerHTML = '';
    const loginHead = document.createElement('h4');
    loginHead.innerHTML = "Вход в систему";
    document.getElementById('appHeaders').innerHTML = loginHead.outerHTML;

    const formLogin = loginForm()
    document.getElementById('appContent').innerHTML = formLogin.outerHTML;

    document.getElementById("loginSubmit").addEventListener("click", function (){
        let form = document.getElementById("loginForm");
        let formData = new FormData(form);
        //let csrf_token = document.getElementById("csrf_token").value
        //formData.append("csrf_token", csrf_token)
        fetch('login', {
            method: "post",
            body: formData
            })
            .then(response => response.json())
            .then(response => {
                let data = response["data"];
                if (data['user'] == "None"){
                    let divAlert = createMessage ("alert alert-warning", "Неверный логин или пароль")
                    document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
                } else {
                    tablePage('/index/', 'alert alert-success', 'Новых анкет: ')        
                };
            });
        });
    }

//user logout
function userLogout(){
    fetch("/logout")
        .then(response => response.json());
        userLogin ()   
};
