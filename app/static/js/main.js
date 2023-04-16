'use strict';

//check user session before starting
fetch('/login')
    .then(response => response.json())
    .then(response => {
        let resp = response["data"];
        if (resp['user'] != "None") {
            mainPage('/index/main/', 'alert alert-success', 'Новых анкет: ')
        } else {
            userLogin()
        };
    });

//implementation code for construct html elements
function constructElement(attrsArray) {
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

//check user authentification and login
function userLogin() {
    const divAlert = constructElement(["div", [
        ["class", "alert alert-info"], 
        ["role", "alert"]
    ], "Авторизуйтесь чтобы продолжить работу"]);
    document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
    const loginHead = constructElement(["h5", "Вход в систему"]);
    document.getElementById('appHeaders').innerHTML = loginHead.outerHTML;
    const divLogin = document.createElement('div');
    const divLoginId = constructElement(["div", [
        ["id", "divLoginId"]
    ]]);
    divLogin.appendChild(divLoginId);
    let submitBtn = constructElement(["button", [
        ["class", "btn btn-primary"], 
        ["type", "submit"], 
        ["onclick", "submitLogin()"]
    ], "Войти"]);
    divLogin.appendChild(submitBtn);
    document.getElementById('appContent').innerHTML = divLogin.outerHTML;
    document.getElementById('divLoginId').innerHTML = formLogin;
    let hiddden = constructElement(["input", [["class", "form-check-input"], ["type", "hidden"],
    ["value", ""], ["name", "remember"]]]);
    let appendHidden = document.getElementById("loginForm");
    appendHidden.appendChild(hiddden);
};

//login request
function submitLogin() {
    let form = document.getElementById('loginForm');
    let formData = new FormData(form);
    fetch('login', {
        method: "post",
        body: formData
    })
    .then(response => response.json())
    .then(response => {
        let resp = response["data"];
        if (resp['user'] == "None") {
            let divAlert = constructElement(["div", [
                ["class", "alert alert-warning"], 
                ["role", "alert"]
            ], "Неверный логин или пароль"]);
            document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
        } else {
            mainPage('/index/main/', 'alert alert-success', 'Новых анкет: ')
        };
    })
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
function mainPage(path, attr, message, currentPage=0) {
    fetch(path + currentPage)
        .then(response => response.json())
        .then(data => {
            let resp = data["data"];
            let countPages = resp[1].pager;
            let divAlert = constructElement(["div", [
                ["class", attr], 
                ["role", "alert"]
            ], message + resp[1].items]);
            document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
            if (path == '/index/main/') {
                const mainHead = constructElement(['h5', "Главная страница"]);
                document.getElementById('appHeaders').innerHTML = mainHead.outerHTML;
            } else {
                const mainHead = constructElement(['h5', "Cтраница пользователя"]);
                document.getElementById('appHeaders').innerHTML = mainHead.outerHTML;
            };
            const division = document.createElement('div');
            division.appendChild(createTable(resp[0]));
            division.appendChild(createPager());
            document.getElementById('appContent').innerHTML = division.outerHTML;
            //update pages button state
            listPages(currentPage, countPages);     
            //click to the next page
            document.getElementById("nextPage").addEventListener("click", function () {
                if (countPages != 0) {
                    mainPage(path, attr, message, currentPage + 1)
                } else {
                    mainPage(path, attr, message, currentPage)
                };
            });
            //click to the previous page
            document.getElementById("previousPage").addEventListener("click", function () {
                if (currentPage != 0) {
                    mainPage(path, attr, message, currentPage - 1)
                } else {
                    mainPage(path, attr, message, currentPage)
                };
            });
        });
};

//search page
function searchPage() {
    const mainHead = constructElement(
        ['h5', "Страница поиска"]
        );
    document.getElementById('appHeaders').innerHTML = mainHead.outerHTML;
    let divForm = document.createElement("div");
    let formSearchExt = constructElement(["form", [
        ["class", "form-check"], 
        ["id", "searchExtForm"], 
        ["onsubmit", "return false;"]
    ]]);
    divForm.appendChild(formSearchExt);
    //region
    let viewDiv = constructElement(["div", [
        ["class", "row mb-1"]
    ]]);
    formSearchExt.appendChild(viewDiv);
    let viewLbl = constructElement(["label", [
        ["class", "form-label"], 
        ["for", "searchExtForm"]
    ], "по региону"]);
    viewDiv.appendChild(viewLbl);
    let selDiv = constructElement(["div", [
        ["class", "col-sm-10"]
    ]]);
    viewDiv.appendChild(selDiv);
    let namesSearch = [
        '', 
        'Главный офис', 
        'Томск', 
        'РЦ Запад', 
        'РЦ Юг', 
        'РЦ Запад', 
        'РЦ Урал'
    ];
    let selectInp = constructElement(["select", [
        ["class", "form-select mb-2"], 
        ["name", "region"]
    ]]);
    for (let value of namesSearch) {
        let option = constructElement(["option", [
            ["class", "form-select mb-3"], 
            ["value", value]
        ], value]);
        selectInp.appendChild(option);
    };
    selDiv.appendChild(selectInp);
    //inputs
    let inpLabels = {
        "fullname": "по имени", 
        "birthday": "по дате рождения", 
        "number": "по номеру документа", 
        "contact": "по номеру телефона"
    };
    for (let i = 0; i < Object.keys(inpLabels).length; i++) {
        let lblDiv = constructElement(["div", [
            ["class", "row mb-2"]
        ]]);
        formSearchExt.appendChild(lblDiv);
        let checkLbl = constructElement(["label", [
            ["class", "form-label"], 
            ["for", "searchExtForm"]
        ], Object.values(inpLabels)[i]]);
        lblDiv.appendChild(checkLbl);
        let inpDiv = constructElement(["div", [
            ["class", "col-sm-10"]
        ]]);
        lblDiv.appendChild(inpDiv);
        if (Object.keys(inpLabels)[i] == "birthday") {
            let chckInp = constructElement(["input", [
                ["class", "form-control"], 
                ["type", "date"], 
                ["name", Object.values(inpLabels)[i]]
            ]]);
            inpDiv.appendChild(chckInp);
        } else {
            let chckInp = constructElement(["input", [
                ["class", "form-control"], 
                ["type", "text"], 
                ["name", Object.values(inpLabels)[i]]
            ]]);
            inpDiv.appendChild(chckInp);
        };
    };
    //button group 
    const extSearchButtonGroup = constructElement(["div", [
        ["class", "btn-group py-2"], 
        ["role", "group"]
    ]]);
    formSearchExt.appendChild(extSearchButtonGroup);
    const extSearchButton = constructElement(["button", [
        ["class", "btn btn-outline-primary"], 
        ["type", "submit"], 
        ["id", "extSearchButton"], 
        ["onclick", "searchItem('searchExtForm', '/extsearch/')"]
    ], 'Найти']);
    extSearchButtonGroup.appendChild(extSearchButton);
    const resetButton = constructElement(["button", [
        ["class", "btn btn-outline-secondary"], 
        ["type", "reset"], 
    ], 'Очистить форму']);
    extSearchButtonGroup.appendChild(resetButton);
    //search result place
    let searchResult = constructElement(["div", [
        ["class", "py-3"], 
        ["id", "searchResult"]
    ]]);
    divForm.appendChild(searchResult);
    document.getElementById('appContent').innerHTML = divForm.outerHTML;
};

//functionality for fast and extended search
function searchItem(idForm, path, currentPage=0) {
    const resp = postForm(path + currentPage, idForm)
    let countPages = resp[1].pager;
    //results of search
    let divAlert = constructElement(["div", [
        ["class", 'alert alert-warning'], 
        ["role", "alert"]
    ], 'Результатов на странице: ' + resp[1].items]);
    const mainHead = constructElement(['h5', "Результат поиска"]);
    document.getElementById('appHeaders').innerHTML = mainHead.outerHTML;
    document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
    const division = document.createElement('div');
    let divTable = createTable(resp[0]);
    division.appendChild(divTable);
    let divPager = createPager()
    division.appendChild(divPager);
    if (path != "/extsearch/"){
        document.getElementById('appContent').innerHTML = division.outerHTML;
    } else {
        document.getElementById('searchResult').innerHTML = division.outerHTML;
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
};

//create table with candidates list
function createTable(candidates) {
    const divTable = constructElement(["div", [
        ["id", "divTable"]
    ]]);
    const table = constructElement(["table", [
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
        let th = constructElement(['th', [
            tabbleAttrs[i]
        ], tableHeader[i]]);
        tr.appendChild(th);
        thead.appendChild(tr);
    };
    for (let candidate of candidates) {
        let tr = document.createElement('tr');
        let items = [
            candidate['id'],  candidate['region'],  candidate['fullname'], 
            candidate['birthday'],  candidate['status'],  candidate['deadline']
        ];
        for (let val of items) {
            let td = document.createElement('td');
            if (val == candidate['fullname']) {
                let a = constructElement(
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

//create pager element
function createPager() {
    const divPager = constructElement(["div", [
        ["id", "divPager"]
    ]]);
    const navPage = document.createElement('nav');
    divPager.appendChild(navPage);
    const pagerUl = constructElement(["ul", [
        ["class", "pagination justify-content-center"], 
        ["id", "pager"]
    ]]);
    navPage.appendChild(pagerUl);
    let idPagers = ["previousPage", "nextPage"];
    let namePagers = ["Предыдущая", "Следующая"];
    for (let i in namePagers) {
        const pageItem = constructElement(['li', [
            ["class", "page-item"], 
            ["id", idPagers[i]]
        ]]);
        pagerUl.appendChild(pageItem);
        const pageLink = constructElement(['a', [
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

//create resume
function createResume(resume=null) {
    document.getElementById('appMessages').innerHTML = "";
    const resumeHead = document.createElement('h5');
    resumeHead.innerHTML = "Создать анкету";
    document.getElementById('appHeaders').innerHTML = resumeHead.outerHTML;
    const divResume = constructElement(["div", [
        ["class", "py-1"]
    ]]);
    const divIdUpload = constructElement(["div", [
        ["id", "uploadId"]
    ]]);
    divResume.appendChild(divIdUpload);
    //resume form
    const divIdResume = constructElement(["div", [
        ["id", "resumeId"]
    ]]);
    divResume.appendChild(divIdResume);
    //submit button
    let submitBtn = constructElement(["button", [
        ["class", "btn btn-primary"], 
        ["type", "submit"],
        ["onclick", "submitResume('resumeForm', 'resume')"]
    ], "Сохранить"]);
    divResume.appendChild(submitBtn);
    //insert forms on page
    document.getElementById('appContent').innerHTML = divResume.outerHTML;
    //insert file and form in destination
    document.getElementById('uploadId').innerHTML = formUpload;
    document.getElementById('resumeId').innerHTML = formResume;
    if (resume != null) {
        let inputField = document.getElementsByName('name')
        console.log(inputField)
    }
};

//resume request
function submitResume(formId, url) {
    let form = document.getElementById(formId);
    let formData = new FormData(form);
    fetch(url, {
        method: "post",
        body: formData
    })
    .then(response => response.json())
    .then(response => {
        let resp = response["data"];
        let divAlert = constructElement(["div", [
            ["class", "alert alert-primary"], 
            ["role", "alert"]
        ], resp[1]['message']]);
        document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
        openProfile(resp[0]['cand_id'])
        });  
};
    
//open candidate profile
function openProfile(candId) {
    fetch("/profile/" + candId)
    .then(response => response.json())
    .then(data => {
        let resps = data["data"];
        let resume = resps[0][0]
        document.getElementById('appMessages').innerHTML = "";
        const profileHead = constructElement(["h5", resume['fullname']]);
        document.getElementById('appHeaders').innerHTML = profileHead.outerHTML;
        let divProfile = constructElement(["div", [
            ["class", "py-1"]
        ]]);
        //tab panel
        let navProfile = document.createElement("nav");
        divProfile.appendChild(navProfile);
        let divNav = constructElement(["div", [
            ["class", "nav nav-tabs"], 
            ["role", "tablist"]
        ]]);
        navProfile.appendChild(divNav);
        const tabsNames = [
            'Профиль', 'Проверки', 'Согласования', 'Полиграф', 'Расследования', 'Запросы'
        ]
        const tabsPanes = [
            'profilePane', 'checkPane', 'registryPane', 'poligrafPane', 'investigatePane', 'inquiryPane'
        ]
        //create tabs
        for (let i = 0; i < tabsNames.length; i++) {
            let navBtn = constructElement(["button", [
                ["data-bs-toggle", "tab"],
                ["data-bs-target", "#"+tabsPanes[i]], 
                ["type", "button"], 
                ["role", "tab"]
            ], tabsNames[i]]);
            if (i == 0) {
                navBtn.setAttribute("aria-selected", "true");
                navBtn.setAttribute("class", "nav-link active");
            } else {
                navBtn.setAttribute("aria-selected", "false")
                navBtn.setAttribute("class", "nav-link");
            };
            divNav.appendChild(navBtn)
        };
        let divContent = constructElement(["div", [
            ["class", "tab-content"]
        ]]);
        divProfile.appendChild(divContent);
        
        //tabs content and id divs
        for (let i = 0; i < tabsPanes.length; i++){
            let divPane
            if (i == 0) {
                divPane = constructElement(["div", [
                    ["class", "tab-pane fade show active py-1"], 
                    ["id", tabsPanes[i]], 
                    ["role", "tabpanel"], 
                ]])
            } else {
                divPane = constructElement(["div", [
                    ["class", "tab-pane fade show py-1"], 
                    ["id", tabsPanes[i]], 
                    ["role", "tabpanel"],
                ]])
            };
            divContent.appendChild(divPane);
            let contentDiv = constructElement(["div", [
                ["id", tabsPanes[i]+"Div"]
            ]]);
            divPane.appendChild(contentDiv)
        };
        document.getElementById('appContent').innerHTML = divProfile.outerHTML;

        //anketaDiv tab
        const resumeSubNames = [
            'Резюме', 'Должности', 'Документы', 'Адреса', 'Контакты', 'Работа','Связи'
        ]
        const resumeIds = [
            'resumeId', 'stafffId', 'docId', 'addressId', 'contactId', 'workId','relationId'
        ]
        const formTarget = [
            "", formStaff, `{{ form_document }}`, `{{ form_address }}`, 
            `{{ form_contact }}`, `{{ form_work }}`, `{{ form_relation }}`
        ]
        const formId = ['', "staffForm"]
        const anketaDiv = document.createElement('div');
        const divAnketa = constructElement(["div", [
            ["class", "py-1"]
        ]]);
        for (let i = 0; i < resumeSubNames.length; i++) {
            const divCollapse = constructElement(["div", [
                ["class", "py-1"]
            ]]);
            const targetHeader = constructElement(["button", [
                ["class", "btn btn-link"],
                ["type", "button"],
                ["data-bs-toggle", "collapse"],
                ["data-bs-target", "#collapse"+[i]]
            ], resumeSubNames[i]]);
            divCollapse.appendChild(targetHeader);
            const divColl = constructElement(["div", [
                ["class", "collapse"],
                ["id", "collapse"+[i]]
            ]]);
            divCollapse.appendChild(divColl);
            const divCard = constructElement(["div", [
                ["class", "card card-body"],
            ]]);
            if (i == 0) {
                divCard.innerHTML = constructElement(["a", [
                    ["class", "btn btn-outline-primary"],
                    ["onclick", `createResume(${JSON.stringify(resume)})`]
                ], "Редактировать анкету"]).outerHTML;
            } else {
                divCard.innerHTML = formTarget[i]
            };
            divColl.appendChild(divCard);
            if (i != 0) {
                const submitBtn = constructElement(["button", [
                    ["class", "btn btn-outline-primary"], 
                    ["type", "submit"], 
                    ["onclick", `cardUpdate(${formId[i]}, ${candId})`]
                ], "Сохранить"]);
                divCard.appendChild(submitBtn);
            };
            divAnketa.appendChild(divCollapse);
            const idNames = constructElement(["div", [
                ["id", resumeIds[i]]
            ]]);
            divAnketa.appendChild(idNames)
        };
        anketaDiv.appendChild(divAnketa)
        //button group
        let groupBtnResume = constructElement(["div", [
            ["class", "btn-group py-2 hidden-print"], 
            ["role", "group"]
        ]]);
        let grpBtnResumeAttr = {
            'Обновить статус': `updateStatus(${candId})`,
            'Отправить на проверку': `sendResume(${candId})`
        };
        for (let i = 0; i < Object.keys(grpBtnResumeAttr).length; i++){
            let updBtnResume = constructElement(["button", [
                ["class", "btn btn-outline-primary"], 
                ["onclick", Object.values(grpBtnResumeAttr)[i]]
            ], Object.keys(grpBtnResumeAttr)[i]]);
            groupBtnResume.appendChild(updBtnResume)
        };
        anketaDiv.appendChild(groupBtnResume)
        document.getElementById("profilePaneDiv").innerHTML = anketaDiv.outerHTML;

        //check tab
        let checkDiv = document.createElement('div');
        let divCheck = constructElement(["div", [
            ["class", "py-1"],
            ["id", "checkId"],
        ]]);
        checkDiv.appendChild(divCheck);
        let groupBtnCheck = constructElement(["div", [
                ["class", "btn-group hidden-print"], 
                ["role", "group"],
            ]]);
        const buttonNames = [
            'Добавить проверку',
            'Редактировать проверку',
        ];
        for (let i = 0; i < buttonNames.length; i++){
            let checkBtn = constructElement(["a", [
                ["class", "btn btn-outline-primary hidden-print"],
                ["type", "button"], 
                ["onclick", `checkForm()`]
            ], buttonNames[i]]);
            groupBtnCheck.appendChild(checkBtn)
        };
        let delbtn = constructElement(["a", [
                ["class", "btn btn-outline-primary hidden-print"],
                ["type", "button"], 
                ["onclick", `deleteCheck()`]
            ], 'Удалить последнюю проверку']);
        groupBtnCheck.appendChild(delbtn)
        checkDiv.appendChild(groupBtnCheck);
        document.getElementById("checkPaneDiv").innerHTML = checkDiv.outerHTML

        //registry tab
        let registryDiv = document.createElement('div');
        let divRegistry = constructElement(["div", [
            ["class", "py-1"],
            ["id", "registryId"],
        ]]);
        registryDiv.appendChild(divRegistry);        
        let addBtnReg = constructElement(["a", [
            ["class", "btn btn-outline-primary hidden-print"],
            ["type", "button"], 
            ["onclick", `registryForm()`]
        ], 'Отправить согласование']);
        registryDiv.appendChild(addBtnReg)
        document.getElementById("registryPaneDiv").innerHTML = registryDiv.outerHTML

        //pfo tab
        let pfoDiv = document.createElement('div');
        let divPfo = constructElement(["div", [
            ["class", "py-1"],
            ["id", "poligrafId"],
        ]]);
        pfoDiv.appendChild(divPfo);            
        let addBtnPfo = constructElement(["a", [
            ["class", "btn btn-outline-primary hidden-print"],
            ["type", "button"], 
            ["onclick", `poligrafForm()`]
        ], 'Добавить тестирование']);
        pfoDiv.appendChild(addBtnPfo)
        document.getElementById("poligrafPaneDiv").innerHTML = pfoDiv.outerHTML

        //investigation tab
        let investigationDiv = document.createElement('div');
        let divInvestigation = constructElement(["div", [
            ["class", "py-1"],
            ["id", "investigationId"],
        ]]);
        investigationDiv.appendChild(divInvestigation); 
        let addBtnInvs = constructElement(["a", [
            ["class", "btn btn-outline-primary hidden-print"],
            ["type", "button"], 
            ["onclick", `investigationForm()`]
        ], 'Добавить расследование']);
        investigationDiv.appendChild(addBtnInvs)
        document.getElementById("investigatePaneDiv").innerHTML = investigationDiv.outerHTML

        //inquiries tab
        let inquiriesDiv = document.createElement('div');
        let divInquiries = constructElement(["div", [
            ["class", "py-1"],
            ["id", "inquiriesId"],
        ]]);
        inquiriesDiv.appendChild(divInquiries); 
        let addBtnInquiry = constructElement(["a", [
            ["class", "btn btn-outline-primary hidden-print"],
            ["type", "button"], 
            ["onclick", `formInquiry()`]
        ], 'Добавить запрос']);
        inquiriesDiv.appendChild(addBtnInquiry)
        document.getElementById("inquiryPaneDiv").innerHTML = inquiriesDiv.outerHTML

        let profileDivs = [
            'resumeId', 'stafffId', 'docId', 'addressId', 'contactId', 'workId','relationId',
            'checkId', 'registryId', 'poligrafId', 'investigationId', 'inquiriesId'
        ];
        let labelNames = [
            ['id', 'Регион', 'Фамилия Имя Отчество', 'Изменение имени', 'Дата рождения', 'Место рождения', 'Гражданство',
                'СНИЛС', 'ИНН', 'Образование', 'Дополнительная информация', 'Дата', 'Статус', 'Рекрутер', 'Внешний id'],
            ['Должность', 'Департамент'],
            ['Вид документа', 'Серия', 'Номер', 'Кем выдан', 'Дата'],
            ['Тип', 'Регион', 'Адрес'],
            ['Вид', 'Контакт'],
            ['Период', 'Организация', 'Адрес', 'Должность'],
            ['Связь', 'Полное ФИО', 'Дата рождения', 'Адрес', 'Место работы', 'Контакты'],
            ['ID', 'Статус автопроверки', 'Проверка по местам работы', 'Бывший работник МТСБ', 
                'Проверка паспорта', 'Проверка ИНН', 'Проверка ФССП', 'Проверка банкротства', 'Проверка БКИ', 
                'Проверка судебных дел', 'Проверка аффилированности', 'Проверка в списке террористов', 
                'Проверка нахождения в розыске', 'Проверка в открытых источниках', 'Проверка Кронос', 'Проверка Крос', 
                'Дополнительная информация', 'Материалы проверки', 'ПФО', 'Комментарии', 'Результат проверки', 
                'Дата проверки', 'Сотрудник СБ'],
            ['ID', 'Комментарий', 'Решение', 'Дата', 'Согласующий'],
            ['ID', 'Тематика', 'Результат', 'Полиграфолог', 'Дата проверки'],
            ['ID', 'Тематика', 'Информация', 'Дата проверки'],
            ['ID', 'Информация', 'Иннициатор', 'Источник', 'Дата запроса']
        ]
        for (let i = 0; i < resps.length; i++) {
            const divTable = constructTables(labelNames[i], resps[i]);
            let divId = document.getElementById(profileDivs[i]);
            divId.innerHTML = divTable.outerHTML;
        };
        stateButton(resps)
    });
};

function stateButton(resps){
    if (resps[0]['status'] != state['NEWFAG'] && resps[0]['status'] != state['UPDATE']) {
            let sendResumeBtn = document.getElementById('sendResume');
            sendResumeBtn.setAttribute("class", "disabled btn btn-outline-success hidden-print");
            let addCheckBtn = document.getElementById('addCheck');
            addCheckBtn.setAttribute("class", "disabled btn btn-outline-primary hidden-print")
        };
        if (resps[0]['status'] != state['SAVE'] && resps[0]['status'] != state['REPLY']) {
            let delEditBtn = document.getElementById('delEdit');
            delEditBtn.setAttribute("class", "disabled btn-group py-2")
        };
        if (resps[0]['status'] != state['RESULT']) {
            let sendRegistryBtn = document.getElementById('openRegistry');
            sendRegistryBtn.setAttribute("class", "disabled btn btn-outline-primary hidden-print")
        };
}

function constructTables(names, response) {
    if (response.length) {
        let division = document.createElement("div");
        for (let j = 0; j < response.length; j++) {
            let div = document.createElement("div");
            let tbl = document.createElement("table");
            tbl.setAttribute("class", "table");
            let tblBody = document.createElement("tbody")
            for (let i = 0; i < names.length; i++) {
                let cell1 = constructElement(["td", [
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

function cardUpdate(formId, candId){
    let form = document.getElementById(formId);
    console.log(form)
    let formData = new FormData(form);
    fetch(`/add/${formId}/${candId}`, {
        method: "post",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        let resp = data["data"];
        let divAlert = constructElement(["div", [
            ["class", "alert alert-warning"], 
            ["role", "alert"]
        ], resp['message']]);
        document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
    openProfile(candId)
    });
};

//update status
function updateStatus(candId) {
    fetch("/resume/update/" + candidates[0]['id'])
        .then(response => response.json())
        .then(data => {
            let resp = data["data"];
            message = resp[1];
            resumeUpd(resp[0], resp[2]);
            if (resp[1] == "Статус обновлен") {
                let divAlert = constructElement(["div", [
                    ["class", "alert alert-success"], 
                    ["role", "alert"]
                ], resp[1]]);
                document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
            } else {
                let divAlert = constructElement(["div", [
                    ["class", "alert alert-warning"], 
                    ["role", "alert"]
                ], resp[1]]);
                document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
            };
        });
};

//send resume to check
function sendResume() {
    fetch("/resume/send/" + candidates[0]['id'])
        .then(response => response.json())
        .then(data => {
            let resp = data["data"];
            if (resp['message'] == "Анкета успешно отправлена") {
                mainPage('/index/main', 'alert alert-success', resp['message'])
            } else if (resp['message'] == "Отправка не удалась. Попробуйте позднее") {
                mainPage('/index/main', 'alert alert-warning', resp['message'])
            } else {
                mainPage('/index/main', 'alert alert-warning', resp['message'])
            };
        });
};

//удалить проверку
function deleteCheck(candId) {
    if (confirm("Вы действительно хотите удалить проверку?")) {
        fetch("/check/delete/" + candId)
            .then(response => response.json())
            .then(data => {
                let resp = data["data"][0];
                let divAlert = constructElement(["div", [
                    ["class", "alert alert-warning"], 
                    ["role", "alert"]
                ], resp['message']]);
                document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
                openProfile(candId)
            });
    };
};

function documentForm() {
    let formDocument = `multiform({{ form_document, extra_classes='form-check',
                    role='form', form_type='horizontal', 
                    horizontal_columns=(lg', 2, 10), id='documentForm', 
                    render_kw={"onsubmit": "return false"}}})`;
    let submitBtn = constructElement(["button", [
        ["class", "btn btn-primary"], 
        ["type", "submit"], 
        ["id", "submit"],
        ["data-bs-dismiss", "modal"]
    ], "Сохранить"]);
    formDocument.appendChild(submitBtn);

    return formDocument
};

function addressForm() {
    let formAddress = `multiform({{ form_address, extra_classes='form-check',
                    role='form', form_type='horizontal', 
                    horizontal_columns=(lg', 2, 10), id='addressForm', 
                    render_kw={"onsubmit": "return false"}}})`;
    let submitBtn = constructElement(["button", [
        ["class", "btn btn-primary"], 
        ["type", "submit"], 
        ["id", "submit"], 
        ["data-bs-dismiss", "modal"]
    ], "Сохранить"]);
    formAddress.appendChild(submitBtn);

    return formAddress
};

function contactForm() {
    let formContact = `multiform({{ form_contact, extra_classes='form-check',
                    role='form', form_type='horizontal', 
                    horizontal_columns=(lg', 2, 10), id='contactForm', 
                    render_kw={"onsubmit": "return false"}}})`;
    let submitBtn = constructElement(["button", [
        ["class", "btn btn-primary"], 
        ["type", "submit"], 
        ["id", "submit"], 
        ["data-bs-dismiss", "modal"]
    ], "Сохранить"]);
    formContact.appendChild(submitBtn);

    return formContact
};

function workplaceForm() {
    let formWorkplace = `multiform({{ form_work, extra_classes='form-check',
                    role='form', form_type='horizontal', 
                    horizontal_columns=(lg', 2, 10), id='workplaceForm', 
                    render_kw={"onsubmit": "return false"}}})`;
    let submitBtn = constructElement(["button", [
        ["class", "btn btn-primary"], 
        ["type", "submit"], 
        ["id", "submit"],
        ["data-bs-dismiss", "modal"]
    ], "Сохранить"]);
    formWorkplace.appendChild(submitBtn);

    return formWorkplace
};

function relationForm() {
    let formRelation = `multiform({{ form_relation, extra_classes='form-check',
                    role='form', form_type='horizontal', 
                    horizontal_columns=(lg', 2, 10), id='relationForm', 
                    render_kw={"onsubmit": "return false"}}})`;
    let submitBtn = constructElement(["button", [
        ["class", "btn btn-primary"], 
        ["type", "submit"], 
        ["id", "submit"], 
        ["data-bs-dismiss", "modal"]
    ], "Сохранить"]);
    formRelation.appendChild(submitBtn);
    
    return formRelation
};

function registryForm() {
    let formRegistry = `multiform({{ form_registry, extra_classes='form-check',
                    role='form', form_type='horizontal', 
                    horizontal_columns=(lg', 2, 10), id='registryForm', 
                    render_kw={"onsubmit": "return false"}}})`;
    let submitBtn = constructElement(["button", [
        ["class", "btn btn-primary"], 
        ["type", "submit"], 
        ["id", "submit"], 
        ["data-bs-dismiss", "modal"]
    ], "Сохранить"]);
    formRegistry.appendChild(submitBtn);

    return formRegistry
};

function poligrafForm() {
    let formPoligraf = `multiform({{ form_poligraf, extra_classes='form-check',
                    role='form', form_type='horizontal', 
                    horizontal_columns=(lg', 2, 10), id='poligrafForm', 
                    render_kw={"onsubmit": "return false"}}})`;
    //submit button
    let submitBtn = constructElement(["button", [
        ["class", "btn btn-primary"], 
        ["type", "submit"], 
        ["id", "submit"], 
        ["data-bs-dismiss", "modal"]
    ], "Сохранить"]);
    formPoligraf.appendChild(submitBtn);

    return formPoligraf
};

function investigationForm() {
    let formInvestigation = `multiform({{ form_investigation, 
                    extra_classes='form-check',
                    role='form', form_type='horizontal', 
                    horizontal_columns=(lg', 2, 10), id='investigationForm', 
                    render_kw={"onsubmit": "return false"}}})`;
    let submitBtn = constructElement(["button", [
        ["class", "btn btn-primary"], 
        ["type", "submit"], 
        ["id", "submit"], 
        ["data-bs-dismiss", "modal"]
    ], "Сохранить"]);
    formInvestigation.appendChild(submitBtn);

    return formInvestigation
};

function inquiryForm(divInquiry, candId, innerDiv) {
    let formInquiry = `multiform({{ form_inquiry, 
                    extra_classes='form-check',
                    role='form', form_type='horizontal', 
                    horizontal_columns=(lg', 2, 10), id='inquiryForm', 
                    render_kw={"onsubmit": "return false"}}})`;
    let submitBtn = constructElement(["button", [
        ["class", "btn btn-primary"], 
        ["type", "submit"], 
        ["id", "submit"], 
        ["onclick", uploadTabData("/add/inquiryForm/"+candId, "inquiryForm", innerDiv)]
    ], "Сохранить"]);
    formInquiry.appendChild(submitBtn);
    //place form into destination div
    divInquiry.appendChild(formInquiry)
};

function checkForm(candId, value = null) {
    const checkHead = document.createElement('h5');
    checkHead.innerHTML = "Создать проверку";
    document.getElementById('appHeaders').innerHTML = checkHead.outerHTML;
    const divResume = constructElement(["div", [
        ["class", "py-1"]
    ]]);
    document.getElementById('appContent').innerHTML = divResume.outerHTML;
    let divForm = constructElement(["div", [
        ["class", "py-3"]
    ]]);
    let formCheck = `multiform({{ form_check, 
                    extra_classes='form-check',
                    role='form', form_type='horizontal', 
                    horizontal_columns=(lg', 2, 10), id='checkForm', 
                    render_kw={"onsubmit": "return false"}}})`;
    //submit button
    let submitBtn = constructElement(["button", [
        ["class", "btn btn-primary"], 
        ["type", "submit"], 
        ["id", "submitCheck"]
    ], "Сохранить"]);
    formCheck.appendChild(submitBtn);
};
