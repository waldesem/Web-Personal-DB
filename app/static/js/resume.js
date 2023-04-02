'use strict'

//создать анкету и добавить данные
function createResume () {
    const mainHead = document.createElement('h4');
    mainHead.innerHTML = "Создать анкету";
    document.getElementById('appHeaders').innerHTML = mainHead.outerHTML;
    const divResume = document.createElement('div');
    
    // создаем форму для загрузки данных через файл
    const formUpload = document.createElement('form');
    formUpload.setAttribute("id", "formFile");
    formUpload.setAttribute("class", "mb-3");
    formUpload.setAttribute("method", "post");
    formUpload.setAttribute("role", "form");
    const lblUpload = document.createElement('label');
    lblUpload.setAttribute("for", "formFile");
    lblUpload.setAttribute("class", "form-label");
    lblUpload.innerHTML = "Загрузка файла Excel (xlsx, xlm)";
    formUpload.appendChild(lblUpload);
    const inputUpload = document.createElement('input');
    inputUpload.setAttribute("class", "form-control");
    inputUpload.setAttribute("type", "file");
    inputUpload.setAttribute("id", "formFile");
    formUpload.appendChild(inputUpload);
    const btnUpload = document.createElement('button');
    btnUpload.setAttribute("class", "btn btn-primary btn");
    btnUpload.setAttribute("type", "submit");
    btnUpload.setAttribute("id", "submitFile");
    btnUpload.innerHTML = "Загрузить";
    formUpload.appendChild(btnUpload);

    // создаем форму для ручного ввода данных анкеты
    divResume.appendChild(formUpload);
    divResume.appendChild(formResume);
    document.getElementById('appContent').innerHTML = divResume.outerHTML;
    // прослушиваем событие от нажатии кнопки на форме загрузки файла
    document.getElementById("formFile").addEventListener("click", function (){
        let form = document.getElementById("formMultiform");
        let formData = new FormData(form);
        let csrf_token = document.getElementById("csrf_token").value
        formData.append("csrf_token", csrf_token)
        fetch('/upload', {
            method: "post",
            body: formData
            })
            .then(response => response.json())
            .then(response => {
                let resp = response["data"];
                let candId = JSON.parse(resp['data']);
                let message = JSON.parse(resp['message']);
                divAlert = createMessage ("alert alert-primary", message)
                document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
                createProfile(candId)
            });
        });

    // прослушиваем событие от нажатии кнопки на форме загрузки данных
    document.getElementById("submitMultiform").addEventListener("click", function (){
        let form = document.getElementById("formMultiform");
        let formData = new FormData(form);
        let csrf_token = document.getElementById("csrf_token").value
        formData.append("csrf_token", csrf_token)
        fetch('/resume', {
            method: "post",
            body: formData
            })
            .then(response => response.json())
            .then(response => {
                let resp = response["data"];
                let candId = JSON.parse(resp['data']);
                let message = JSON.parse(resp['message']);
                divAlert = createMessage ("alert alert-primary", message)
                document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
                createProfile(candId)
            });
        });
    }
