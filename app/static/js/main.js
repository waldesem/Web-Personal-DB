'use strict';
    
//проверка сессии пользователя, если не авторизован - редирект на страницу логина
fetch('/login')
.then(response => response.json())
.then(response => {
    let resp = response["data"];
    if (resp['user'] != "None") {
        mainPage('/index/main/')
    } else {
        userLogin()
    };
});

//implementation code for construct html elements
function constructHtmlElement(attrsArray) {
    let element = document.createElement(attrsArray[0]); //create element
    if (!Array.isArray(attrsArray[1])) {
        element.innerHTML = attrsArray[1]
    } else {
        for (let attr of attrsArray[1]) {
            element.setAttribute(attr[0], attr[1]);
            if (attrsArray.length > 2) element.innerHTML = attrsArray[2];
        };
    };
    return element
};

//constructor form from jinja template
function constructForm(jinjaForm, func, label) {
    let wrapper= document.createElement('div');
    wrapper.innerHTML= jinjaForm.trim();
    if (func || label){
        let submitBtn = constructHtmlElement(["button", [
           ["class", "btn btn-primary"],
           ["type", "submit"],
           ["onclick", func]
        ], label]);
        wrapper.appendChild(submitBtn);
    };
    return wrapper
};

//check user authentification and login
function userLogin() {
    const divAlert = constructHtmlElement(["div", [
        ["class", "alert alert-info"], 
        ["role", "alert"]
    ], "Авторизуйтесь чтобы продолжить работу"]);   //создаем сообщение
    document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
    //заголовок
    const loginHead = constructHtmlElement(["h5", "Вход в систему"]);
    document.getElementById('appHeaders').innerHTML = loginHead.outerHTML;
    //форма для ввода данных
    const divLogin = document.createElement('div');
    divLogin.appendChild(constructForm(formLogin));
    document.getElementById('appContent').innerHTML = divLogin.outerHTML;
    const hiddden = constructHtmlElement(["input", [
        ["class", "form-check-input"], ["type", "hidden"], ["value", ""], ["name", "remember"]
    ]]);
    const appendHidden = document.getElementById("loginFormId");
    appendHidden.appendChild(hiddden);
    //обработка нажатия кнопки Войти
    const form = document.getElementById("loginFormId")
    form.addEventListener('submit', function (event){
        const form = document.getElementById('loginFormId');
        const formData = new FormData(form);
        fetch('login', {
            method: "post",
            body: formData
        })
        .then(response => response.json())
        .then(response => {
        let resp = response["data"];
        if (resp['user'] == "None") {
            let divAlert = constructHtmlElement(["div", [
                ["class", "alert alert-warning"], 
                ["role", "alert"]
            ], "Неверный логин или пароль"]);
            document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
        } else {
            mainPage('/index/main/', 'alert alert-success', 'Новых анкет: ')
        };
        })
    });
};

//user logout
function userLogout() {
    fetch('logout')
        .then(response => response.json())
        .then(response =>{
            console.log(response["data"])
        });
    userLogin()
};

//upload page of candidates table (main and officer page) 
function mainPage(path, currentPage=0) {
    fetch(path + currentPage)
    .then(response => response.json())
    .then(data => {
        let resp = data["data"];
        const countPages = resp[1].pager;
        //оповещение и заголовок
        const divAlert = constructHtmlElement(["div", [
            ["class", 'alert alert-info'], 
            ["role", "alert"],
        ], `<a href="#" onclick=mainPage('/index/new/'); return false>Новых анкет: ${resp[1].items}</a>`]);
        document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
        if (path == '/index/main/' || path == '/index/new/') {
            const mainHead = constructHtmlElement(['h5', "Главная страница"]);
            document.getElementById('appHeaders').innerHTML = mainHead.outerHTML;
        } else {
            const mainHead = constructHtmlElement(['h5', "Cтраница пользователя"]);
            document.getElementById('appHeaders').innerHTML = mainHead.outerHTML;
        };
        //содержимое страницы
        const division = document.createElement('div');
        //форма расширенного поиска
        const divForm = document.createElement("div");
        division.appendChild(divForm)
        const searchResult = constructForm(formExtSearch);
        divForm.appendChild(searchResult)
        //таблица кандидатов либо результатов поиска
        const tableResult = constructHtmlElement(["div", [
            ["class", "py-5"], 
            ["id", "tableResult"]
        ]]);
        tableResult.appendChild(constrVertTable(resp[0]));
        tableResult.appendChild(createPager());
        division.appendChild(tableResult);
        document.getElementById('appContent').innerHTML = division.outerHTML;
        //обработка события кнопки на форме поиска
        const form = document.getElementById("searchExtFormId")
        form.addEventListener('submit', function (event){
            //const form = document.getElementById('loginFormId');
            searchItem('searchExtFormId', 'extsearch')
        });
        //update pages button state
        listPages(currentPage, countPages);     
        //click to the next page
        document.getElementById("nextPage").addEventListener("click", function () {
            if (countPages != 0) {
                mainPage(path, currentPage + 1)
            } else {
                mainPage(path, currentPage)
            };
        });
        //click to the previous page
        document.getElementById("previousPage").addEventListener("click", function () {
            if (currentPage != 0) {
                mainPage(path, currentPage - 1)
            } else {
                mainPage(path, currentPage)
            };
        });
    });
};

//functionality for fast and extended search
function searchItem(idForm, path, currentPage=0) {
    const form = document.getElementById(idForm);
    const formData = new FormData(form);
    fetch(`/search/${path}/${currentPage}`, {
        method: "post",
        body: formData
    })
    .then(response => response.json())
    .then(response => {
        let resp = response["data"];
        let countPages = resp[1]['pager'];
        //results of search
        document.getElementById('appMessages').innerHTML = "";
        const mainHead = constructHtmlElement(['h5', "Результат поиска"]);
        document.getElementById('appHeaders').innerHTML = mainHead.outerHTML;
        const division = document.createElement('div');
        let divTable = constrVertTable(resp[0]);
        division.appendChild(divTable);
        let divPager = createPager()
        division.appendChild(divPager);
        if (path != "extsearch"){
            document.getElementById('appContent').innerHTML = division.outerHTML;
        } else {
            document.getElementById('tableResult').innerHTML = division.outerHTML;
        }
        //update pages button state
        listPages(currentPage, countPages);
        //click to the next page
        document.getElementById("nextPage").addEventListener("click", function () {
            if (countPages != 0) {
                searchItem(idForm, path, currentPage + 1)
            } else {
                searchItem(idForm, path, currentPage)
            };
        });
        //click to the previous page
        document.getElementById("previousPage").addEventListener("click", function () {
            if (currentPage != 0) {
                searchItem(idForm, path, currentPage - 1)
            } else {
                searchItem(idForm, path, currentPage)
            };
        });
    });
};

//create pager element
function createPager() {
    const divPager = constructHtmlElement(["div", [
        ["class", "py-5"],
        ["id", "divPager"]
    ]]);
    const navPage = document.createElement('nav');
    divPager.appendChild(navPage);
    const pagerUl = constructHtmlElement(["ul", [
        ["class", "pagination justify-content-center"], 
        ["id", "pager"]
    ]]);
    navPage.appendChild(pagerUl);
    let idPagers = ["previousPage", "nextPage"];
    let namePagers = ["Предыдущая", "Следующая"];
    for (let i in namePagers) {
        const pageItem = constructHtmlElement(['li', [
            ["class", "page-item"], 
            ["id", idPagers[i]]
        ]]);
        pagerUl.appendChild(pageItem);
        const pageLink = constructHtmlElement(['a', [
            ["class", "page-link"], 
            ["href", "#"]
        ], namePagers[i]]);
        pageItem.appendChild(pageLink);
    };
    return divPager
};

//update pager state 
function listPages(currentPage, countPages) {
    let nextItem = document.getElementById('nextPage');
    let previousItem = document.getElementById('previousPage');
    if (currentPage == 0) {
        previousItem.setAttribute("class", "disabled")
    } else {
        if (previousItem.hasAttribute("class", "disabled")) {
            previousItem.removeAttribute("class", "disabled")
        };
    };
    if (countPages == 0) {
        nextItem.setAttribute("class", "disabled")
    } else {
        if (nextItem.hasAttribute("class", "disabled")) {
            nextItem.removeAttribute("class", "disabled")
        };
    };
}

//create table with candidates list
function constrVertTable(candidates) {
    const divTable = constructHtmlElement(["div", [
        ["id", "divTable"]
    ]]);
    const table = constructHtmlElement(["table", [
        ["class", "table table-hover table-responsive align-middle py-1"]
    ]]);
    divTable.appendChild(table);
    const thead = document.createElement('thead');
    table.appendChild(thead);
    const tbody = document.createElement('tbody');
    table.appendChild(tbody);
    let tr = document.createElement('tr');
    let tableHeader = [
        "#", "Регион", "Фамилия Имя Отчество", "Дата рождения", "Статус", "Дата"
    ];
    let tabbleAttrs = [
        ["width", "5%"], ["width", "15%"], ["width", "30%"], ["width", "15%"], ["width", "15%"], ["width", "15%"]
    ];
    for (let i = 0; i < tableHeader.length; i++) {
        let th = constructHtmlElement(['th', [
            tabbleAttrs[i]
        ], tableHeader[i]]);
        tr.appendChild(th);
        thead.appendChild(tr);
    };
    for (let candidate of candidates) {
        let tr = document.createElement('tr');
        tr.setAttribute("height", "50px");
        let items = [
            candidate['id'],  candidate['region'],  candidate['fullname'], 
            candidate['birthday'],  candidate['status'],  candidate['deadline']
        ];
        for (let val of items) {
            let td = document.createElement('td');
            if (val == candidate['fullname']) {
                let a = constructHtmlElement(
                    ["a", [
                        ["href", "#"], 
                        ["onclick", `openProfile(${candidate['id']})`]
                    ], val]);
                td.appendChild(a);
            } else {
                td.innerHTML = val
            };
            if (val == candidate['deadline'] || val == candidate['birthday']) {
                let date = new Date(Date.parse(val));
                td.innerHTML =  date.toLocaleDateString('ru-RU')
            };
            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    };
    return divTable
}

//открываем страницу для заполенения/загрузки анкеты
function createResume(candId=0) {
    document.getElementById('appMessages').innerHTML = "";
    const resumeHead = document.createElement('h5');
    resumeHead.innerHTML = "Создать анкету";
    document.getElementById('appHeaders').innerHTML = resumeHead.outerHTML;
    const divResume = constructHtmlElement(["div", [
        ["class", "py-1"]
    ]]);
    const divformUpload = document.createElement('div');
    divResume.appendChild(divformUpload);
    divformUpload.innerHTML = formUpload;
    const divformResume = document.createElement('div');
    divResume.appendChild(divformResume);
    divformResume.innerHTML = (constructForm(formResume)).outerHTML;
    if (candId != 0) {
        fetch("/profile/anketa/" + candId)
        .then(response => response.json())
        .then(data => {
        let resps = data[0][0];
        delete resps['id'];
        delete resps['region'];
        delete resps['status'];
        delete resps['deadline'];
        delete resps['request_id'];
        let resumeId = document.getElementById("resumeFormId");
        let tagName = resumeId.getElementsByTagName("input");
        for (let i = 0; i < tagName.length-1; i++){
            tagName[i].setAttribute("value", Object.values(resps)[i])
        };      
        });
    };
    document.getElementById('appContent').innerHTML = divResume.outerHTML;
    const form = document.getElementById("resumeFormId")
    form.addEventListener('submit', function (event){
        submitResume("resumeFormId", "/resume")
    });
};

function submitResume(formId, url){
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    fetch(url, {
        method: "post",
        body: formData
    })
    .then(response => response.json())
    .then(response => {
        let resp = response;
        let divAlert = constructHtmlElement(["div", [
            ["class", "alert alert-primary"], 
            ["role", "alert"]
        ], resp['message']]);
        document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
        openProfile(resp["cand_id"])
    });
};

//сброс статуса анкеты на UPDATE при необходимости
function updateStatus(candId) {
    fetch("/resume/update/" + candId)
    .then(response => response.json())
    .then(data => {
        let resp = data;
        openProfile(candId);
        let divAlert = constructHtmlElement(["div", [
            ["class", "alert alert-info"], 
            ["role", "alert"]
        ], resp['message']]);
        document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
    });
};

//send resume to the automatic check
function sendResume(candId) {
    fetch("/resume/send/" + candId)
    .then(response => response.json())
    .then(data => {
        let resp = data;
        let divAlert = constructHtmlElement(["div", [
            ["class", "alert alert-info"], 
            ["role", "alert"]
        ], resp['message']]);
        document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
        mainPage('/index/main/')
    });
};

//добавление данных в акету
function addToAnketa(candId){
    const profileHead = constructHtmlElement(["h5", "Добавить информацию в анкету"]);
    document.getElementById('appHeaders').innerHTML = profileHead.outerHTML;
    const divContent = constructHtmlElement(["div", [
        ["class", "py-1"],
    ]]);    
    //anketa
    const resumeSubNames = [
        'Должности', 'Документы', 'Адреса', 'Контакты', 'Работа', 'Связи'
    ]
    const anketaIds = [
        'staffId', 'docId', 'addressId', 'contactId', 'workId','relationId'
    ]
    const anketaForms = [
        constructForm(formStaff), constructForm(formDocument), constructForm(formAddress), 
        constructForm(formContact), constructForm(formWorkplace), constructForm(formRelation)
    ]
    for (let i = 0; i < resumeSubNames.length; i++) {
        const divCollapse = constructHtmlElement(["div", [
            ["class", "py-1"]
        ]]);
        const targetHeader = constructHtmlElement(["h6", resumeSubNames[i]]);
        divCollapse.appendChild(targetHeader);
        const divColl = constructHtmlElement(["form", [
            ["onsubmit", "return false"],
            ["id", `${anketaIds[i]}`]
        ]]);
        divCollapse.appendChild(divColl);
        divContent.appendChild(divCollapse);
    };
    document.getElementById("profileContentId").innerHTML = divContent.outerHTML;

    for (let i = 0; i < resumeSubNames.length; i++) {
        document.getElementById(`${anketaIds[i]}`).innerHTML = anketaForms[i].outerHTML;
        let addListener = document.getElementById(`${anketaIds[i]}`)
        addListener.addEventListener('submit', function (event){
            updateData(`${anketaIds[i]}`, `update/${anketaIds[i]}`, candId)
        });
    };
};

//open profile and anketa's page
function openProfile(candId) {
    const profileHead = constructHtmlElement(["h5", "Анкета кандидата/сотрудника"]);
    document.getElementById('appHeaders').innerHTML = profileHead.outerHTML;
    const divProfile = constructHtmlElement(["div", [
        ["class", "py-1"]
    ]]);
    const navBtnGroup = constructHtmlElement(["div", [
        ["class", "btn-group py-2 btn-hidden-print w-100"],
        ["data-bs-toggle", "button" ],
        ["role", "group"]
    ]]);
    divProfile.appendChild(navBtnGroup)
    const navBtnAnketa = constructHtmlElement(["button", [
        ["class", "btn btn-outline-primary"],
        ["type", "button"],
        ["onclick", `openProfile(${candId})`]
    ], "Анкета"]);
    navBtnGroup.appendChild(navBtnAnketa);
    const navBtnCheck = constructHtmlElement(["button", [
        ["class", "btn btn-outline-primary"],
        ["type", "button"],
        ["onclick", `openCheck(${candId})`]
    ], 'Проверка']);
    navBtnGroup.appendChild(navBtnCheck);
    const navBtnReg = constructHtmlElement(["button", [
        ["class", "btn btn-outline-primary"],
        ["type", "button"],
        ["onclick", `openRegistry(${candId})`]
    ], 'Согласование']);
    navBtnGroup.appendChild(navBtnReg);
    const navBtnPfo = constructHtmlElement(["button", [
        ["class", "btn btn-outline-primary"],
        ["type", "button"],
        ["onclick", `openPoligraf(${candId})`]
    ], 'Полиграф']);
    navBtnGroup.appendChild(navBtnPfo);
    const navBtnInvs = constructHtmlElement(["button", [
        ["class", "btn btn-outline-primary"],
        ["type", "button"],
        ["onclick", `openInvestigation(${candId})`]
    ], 'Расследования']);
    navBtnGroup.appendChild(navBtnInvs);
    const navBtnInqs = constructHtmlElement(["button", [
        ["class", "btn btn-outline-primary"],
        ["type", "button"],
        ["onclick", `openInquiry(${candId})`]
    ], 'Запросы']);
    navBtnGroup.appendChild(navBtnInqs);
    const divProfileContent = constructHtmlElement(["div", [
        ["class", "py-1"],
        ["id", "profileContentId"]
    ]]);
    divProfile.appendChild(divProfileContent)
    
    //anketa
    const resumeSubNames = [
        'Резюме', 'Должности', 'Документы', 'Адреса', 'Контакты', 'Работа','Связи'
    ]
    const anketaIds = [
        'resumeId', 'staffId', 'docId', 'addressId', 'contactId', 'workId','relationId'
    ]
    const labelNames = [
        ['id', 'Регион', 'Фамилия Имя Отчество', 'Изменение имени', 'Дата рождения', 'Место рождения', 'Гражданство', 'СНИЛС', 'ИНН', 'Образование', 'Дополнительная информация', 'Дата', 'Статус', 'Рекрутер', 'Внешний id'],
        ['Должность', 'Департамент'],
        ['Вид документа', 'Серия', 'Номер', 'Кем выдан', 'Дата'],
        ['Тип', 'Регион', 'Адрес'],
        ['Вид', 'Контакт'],
        ['Период', 'Организация', 'Адрес', 'Должность'],
        ['Связь', 'Полное ФИО', 'Дата рождения', 'Адрес', 'Место работы', 'Контакты'],
    ];
    
    const anketaDiv = document.createElement('div');
    const divAnketa = constructHtmlElement(["div", [
        ["class", "py-1"]
    ]]);
    for (let i = 0; i < resumeSubNames.length; i++) {
        const targetHeader = constructHtmlElement(["h6", resumeSubNames[i]]);
        divAnketa.appendChild(targetHeader);
        const idNames = constructHtmlElement(["div", [
            ["id", anketaIds[i]]
        ]]);
        divAnketa.appendChild(idNames)
    };
    anketaDiv.appendChild(divAnketa)
    
    //группа  кнопок Добавить информацию, Обновить статус, Отправить  на проверку
    const groupBtnResume = constructHtmlElement(["div", [
        ["class", "btn-group py-2 hidden-print"], 
        ["role", "group"]
    ]]);
    const grpBtnResumeAttr = {
        'Изменить  анкету': `createResume(${candId})`,
        'Добавить информацию': `addToAnketa(${candId})`,
        'Обновить статус': `updateStatus(${candId})`,
        'Отправить на проверку': `sendResume(${candId})`
    };
    for (let i = 0; i < Object.keys(grpBtnResumeAttr).length; i++){
        let updBtnResume = constructHtmlElement(["button", [
            ["class", "btn btn-outline-primary"], 
            ["onclick", Object.values(grpBtnResumeAttr)[i]]
        ], Object.keys(grpBtnResumeAttr)[i]]);
        groupBtnResume.appendChild(updBtnResume)
    };
    anketaDiv.appendChild(groupBtnResume)
    divProfileContent.appendChild(anketaDiv);
    document.getElementById('appContent').innerHTML = divProfile.outerHTML;
    
    getProfileItem("anketa", candId, labelNames, anketaIds)
};

//open check page
function openCheck(candId){
    const profileHead = constructHtmlElement(["h5", "Результаты проверки"]);
    document.getElementById('appHeaders').innerHTML = profileHead.outerHTML;
    const checkDiv = constructHtmlElement(["div", [
        ["class", "py-2"],
        ["id", "formCheckId"],
    ]]);
    //place for checks results
    const divCheck = constructHtmlElement(["div", [
        ["class", "py-1"],
        ["id", "checkId"],
    ]]);
    checkDiv.appendChild(divCheck);
    const groupBtnCheck = constructHtmlElement(["div", [
            ["class", "btn-group hidden-print"], 
            ["role", "group"],
        ]]);
    const checkBtn = constructHtmlElement(["a", [
        ["class", "btn btn-outline-info"],
        ["type", "button"],
        ["id", "checkBtn"]
    ], 'Добавить проверку']);
    groupBtnCheck.appendChild(checkBtn)
    const editBtn = constructHtmlElement(["a", [
        ["class", "btn btn-outline-info"],
        ["type", "button"],
        ["id", "editBtn"]
    ], 'Редактировать проверку']);
    groupBtnCheck.appendChild(editBtn)
    const delbtn = constructHtmlElement(["a", [
            ["class", "btn btn-outline-info"],
            ["type", "button"], 
            ["onclick", `deleteCheck(${candId})`]
        ], 'Удалить последнюю проверку']);
    groupBtnCheck.appendChild(delbtn)
    checkDiv.appendChild(groupBtnCheck);
    document.getElementById("profileContentId").innerHTML = checkDiv.outerHTML;

    const labelNames = [
        [
        'ID', 'Статус автопроверки', 'Проверка по местам работы', 'Бывший работник МТСБ', 
        'Проверка паспорта', 'Проверка ИНН', 'Проверка ФССП', 'Проверка банкротства', 'Проверка БКИ', 
        'Проверка судебных дел', 'Проверка аффилированности', 'Проверка в списке террористов', 
        'Проверка нахождения в розыске', 'Проверка в открытых источниках', 'Проверка Кронос', 'Проверка Крос', 
        'Дополнительная информация', 'Материалы проверки', 'ПФО', 'Комментарии', 'Результат проверки', 
        'Дата проверки', 'Сотрудник СБ'
        ]
    ];
    getProfileItem("check", candId, labelNames, ['checkId']);
    //прослушиваем событие на кнопке 'Добавить запрос'
    const addBtnListener = document.getElementById("checkBtn")
    addBtnListener.addEventListener('click', function (event){
        const formCheckId = constructForm(formCheck);
        document.getElementById("formCheckId").innerHTML = formCheckId.outerHTML;
    });
    //прослушиваем событие на кнопке  Принять
    const submitdBtnListener = document.getElementById("formCheckId")
    submitdBtnListener.addEventListener('submit', function (event){
        updateData("checkFormId", "check", candId)
    });
};


//delete last check
function deleteCheck(candId) {
    if (confirm("Вы действительно хотите удалить проверку?")) {
        fetch("/check/delete/"+candId)
        .then(response => response.json())
        .then(data => {
            let resp = data["data"][0];
            let divAlert = constructHtmlElement(["div", [
                ["class", "alert alert-warning"], 
                ["role", "alert"]
            ], resp['message']]);
            document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
            openProfile(candId)
        });
    };
};

//open registry page
function openRegistry (candId){
    const profileHead = constructHtmlElement(["h5", "Согласование кандидата"]);
    document.getElementById('appHeaders').innerHTML = profileHead.outerHTML;
    const registryDiv = constructHtmlElement(["div", [
        ["class", "py-2"],
        ["id", "formRegistryId"],
    ]]);
    const divRegistry = constructHtmlElement(["div", [
        ["class", "py-1"],
        ["id", "registryId"],
    ]]);
    registryDiv.appendChild(divRegistry);
    const addBtnReg = constructHtmlElement(["a", [
        ["class", "btn btn-outline-info hidden-print"],
        ["type", "button"], 
        ["id", "addBtnReg"]
    ], 'Открыть согласование']);
    registryDiv.appendChild(addBtnReg)
    const labelNames = [
        ['ID', 'Комментарий', 'Решение', 'Дата', 'Согласующий']
    ];
    document.getElementById("profileContentId").innerHTML = registryDiv.outerHTML;
    getProfileItem("registry", candId, labelNames, ['registryId']);
    //прослушиваем событие на кнопке 'Добавить запрос'
    const addBtnListener = document.getElementById("addBtnReg")
    addBtnListener.addEventListener('click', function (event){
        const formRegistryId = constructForm(formRegistry);
        document.getElementById("formRegistryId").innerHTML = formRegistryId.outerHTML;
    });
    //прослушиваем событие на кнопке  Принять
    const submitdBtnListener = document.getElementById("formRegistryId")
    submitdBtnListener.addEventListener('submit', function (event){
        updateData("registryFormId", "registr", candId)
    });
};

//open pfo page
function openPoligraf(candId) {
    const profileHead = constructHtmlElement(["h5", "Тестирование на полиграфе"]);
    document.getElementById('appHeaders').innerHTML = profileHead.outerHTML;
    const pfoDiv = constructHtmlElement(["div", [
        ["class", "py-2"],
        ["id", "formPoligrafId"],
    ]]);
    const divPfo = constructHtmlElement(["div", [
        ["class", "py-1"],
        ["id", "poligrafId"],
    ]]);
    pfoDiv.appendChild(divPfo);            
    const addBtnPfo = constructHtmlElement(["a", [
        ["class", "btn btn-outline-info hidden-print"],
        ["type", "button"], 
        ["id", "addBtnPfo"]
    ], 'Добавить тестирование']);
    pfoDiv.appendChild(addBtnPfo)
    document.getElementById("profileContentId").innerHTML = pfoDiv.outerHTML;
    
    const labelNames = [
        ['ID', 'Тематика', 'Результат', 'Полиграфолог', 'Дата проверки']
    ];
    getProfileItem("pfo", candId, labelNames, ['poligrafId']);
    //прослушиваем событие на кнопке 'Добавить запрос'
    const addBtnListener = document.getElementById("addBtnPfo")
    addBtnListener.addEventListener('click', function (event){
        const formPoligrafId = constructForm(formPoligraf);
        document.getElementById("formPoligrafId").innerHTML = formPoligrafId.outerHTML;
    });
    //прослушиваем событие на кнопке  Принять
    const submitdBtnListener = document.getElementById("formPoligrafId")
    submitdBtnListener.addEventListener('submit', function (event){
        updateData("poligrafFormId", "update/poligraf", candId)
    });
};

//open investigation page
function openInvestigation(candId){
    const profileHead = constructHtmlElement(["h5", "Служебные расследования"]);
    document.getElementById('appHeaders').innerHTML = profileHead.outerHTML;
    const investigationDiv = constructHtmlElement(["div", [
        ["class", "py-2"],
        ["id", "formInvestigationId"],
    ]]);
    const divInvestigation = constructHtmlElement(["div", [
        ["class", "py-1"],
        ["id", "investigationId"],
    ]]);
    investigationDiv.appendChild(divInvestigation); 
    const addBtnInvs = constructHtmlElement(["a", [
        ["class", "btn btn-outline-info hidden-print"],
        ["type", "button"],
        ["id", "addBtnInvs"]
    ], 'Добавить расследование']);
    investigationDiv.appendChild(addBtnInvs)
    document.getElementById("profileContentId").innerHTML = investigationDiv.outerHTML;
    const labelNames = [
        ['ID', 'Тематика', 'Информация', 'Дата проверки']
    ];
    getProfileItem("investigation", candId, labelNames, ['investigationId']);
    //прослушиваем событие на кнопке 'Добавить запрос'
    const addBtnListener = document.getElementById("addBtnInvs")
    addBtnListener.addEventListener('click', function (event){
        const formInvestigationId = constructForm(formInvestigation);
        document.getElementById("formInvestigationId").innerHTML = formInvestigationId.outerHTML;
    });
    //прослушиваем событие на кнопке  Принять
    const submitdBtnListener = document.getElementById("formInvestigationId")
    submitdBtnListener.addEventListener('submit', function (event){
        updateData("investigationFormId", "update/investigation", candId)
    });
};

//открываем страницу для просмотра/добавления запросов
function openInquiry(candId){
    const profileHead = constructHtmlElement(["h5", "Запросы по сотруднику"]);
    document.getElementById('appHeaders').innerHTML = profileHead.outerHTML;
    const inquiriesDiv = constructHtmlElement(["div", [
        ["class", "py-2"],
        ["id", "formInquiriesId"],
    ]]);
    const divInquiries = constructHtmlElement(["div", [
        ["class", "py-1"],
        ["id", "inquiriesId"],
    ]]);
    inquiriesDiv.appendChild(divInquiries);
    //создаем кнопку добавления запроса
    const addBtnInquiry = constructHtmlElement(["buton", [
        ["class", "btn btn-outline-primary hidden-print"],
        ["type", "button"], 
        ["id", "addBtnInquiry"]
    ], 'Добавить запрос']);
    inquiriesDiv.appendChild(addBtnInquiry);
    document.getElementById("profileContentId").innerHTML = inquiriesDiv.outerHTML;
    //выгружаем информацию по прошлым запросам на страницу
    const labelNames = [
        ['ID', 'Информация', 'Иннициатор', 'Источник', 'Дата запроса']
    ];
    getProfileItem("inquiry", candId, labelNames, ['inquiriesId']);
    //прослушиваем событие на кнопке 'Добавить запрос'
    const addBtnListener = document.getElementById("addBtnInquiry")
    addBtnListener.addEventListener('click', function (event){
        const inquiryFormId = constructForm(formInquiry);
        document.getElementById("formInquiriesId").innerHTML = inquiryFormId.outerHTML;
    });
    //прослушиваем событие на кнопке Принять
    const submitdBtnListener = document.getElementById("formInquiriesId")
    submitdBtnListener.addEventListener('submit', function (event){
        updateData("inquiryFormId", "update/inquiry", candId)
    });
};

//отправка GET запросов в БД для получения данных и передача их в конструктор таблиц
function getProfileItem(flag, candId, labelNames, profileDivs){
    fetch(`/profile/${flag}/${candId}`)
    .then(response => response.json())
    .then(data => {
        let resps
        if (flag == 'anketa'){
            resps = data;
        } else {
            resps = [data];
        }
        for (let i = 0; i < resps.length; i++) {
            const divTable = constrHorizTable(labelNames[i], resps[i]);
            const divId = document.getElementById(profileDivs[i]);
            divId.innerHTML = divTable.outerHTML;
        };
    });
};

//create table with candidate profile
function constrHorizTable(names, response) {
    if (response.length) {
        let division = document.createElement("div");
        for (let j = 0; j < response.length; j++) {
            let div = document.createElement("div");
            let tbl = document.createElement("table");
            tbl.setAttribute("class", "table");
            let tblBody = document.createElement("tbody")
            for (let i = 0; i < names.length; i++) {
                let cell1 = constructHtmlElement(["td", [
                    ["width", "25%"]], names[i]]);
                let cell2 = document.createElement("td");
                cell2.innerHTML = Object.values(response[j])[i];
                let row = document.createElement("tr");
                row.appendChild(cell1)
                row.appendChild(cell2)
                tblBody.appendChild(row)
            };
            tbl.appendChild(tblBody)
            div.appendChild(tbl)
            division.appendChild(div)
        };
        return division
    } else {
        let text = document.createElement("p");
        text.innerHTML = "Данные отсутствуют"
        return text
    };
}

//отправка POST запросов в БД с данными из форм
function updateData(formId, url, candId){
    const form = document.getElementById(formId)
    const formData = new FormData(form);
    fetch(`/${url}/${candId}`, {
        method: "post",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        let resp = data;
        let divAlert = constructHtmlElement(["div", [
            ["class", "alert alert-primary"], 
            ["role", "alert"]
        ], resp['message']]);
        document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
        openProfile(candId)
    });
};

//открываем страницу статинформации
function createInfo(){
    fetch("/info")
    .then(response => response.json())
    .then(data => {
    let resps = data;
    document.getElementById('appMessages').innerHTML = "";
    const resumeHead = document.createElement('h5');
    resumeHead.innerHTML = resps['title'];
    document.getElementById('appHeaders').innerHTML = resumeHead.outerHTML;
    const divTable = document.createElement("div");
    const table = constructHtmlElement(["table", [
        ["class", "table table-hover table-responsive align-middle py-1"],
        ["id", "divTable"]
    ]]);
    divTable.appendChild(table);
    const thead = document.createElement('thead');
    table.appendChild(thead);
    const tbody = document.createElement('tbody');
    table.appendChild(tbody);
    let tr = document.createElement('tr');
    let tableHeader = ["Решение", "Количество"];
    for (let i = 0; i < tableHeader.length; i++) {
        let th = constructHtmlElement(['th', tableHeader[i]]);
        tr.appendChild(th);
        thead.appendChild(tr);
    };
    for (let resp of resps["candidates"]) {
        let tr = document.createElement('tr');
        tr.setAttribute("height", "50px");
        for (let val of Object.entries(resp)) {
            let td = document.createElement('td');
            td.innerHTML = val[0]
            tr.appendChild(td);
            let td1 = document.createElement('td');
            td1.innerHTML = val[1]
            tr.appendChild(td1);
        }
        tbody.appendChild(tr);
    };
    document.getElementById('appContent').innerHTML = divTable.outerHTML;
    const statForm = constructHtmlElement(["form", [
        ["id", "statForm"]
    ]]);
    table.appendChild(statForm);
    });
};

//получем статинформацию по запросу
function takeStatinfo(){
    const form = document.getElementById("formId")
    const formData = new FormData(form);
    fetch(`/${url}/${candId}`, {
        method: "post",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        let resps = data;
        document.getElementById('appMessages').innerHTML = "";
        const resumeHead = document.createElement('h5');
        resumeHead.innerHTML = "Создать анкету";
        document.getElementById('appHeaders').innerHTML = resumeHead.outerHTML;
        const divResume = constructHtmlElement(["div", [
            ["class", "py-1"]
        ]]);
        document.getElementById('appContent').innerHTML = divResume.outerHTML;
    });
};
