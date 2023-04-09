'use strict';


/*implementation code for construct html elements
example: simpleElement = constructElement(["label", [["class", "form-label"], ["for", "simpleForm"]], "text"]);
or simpleElement = constructElement(["h5", "text"])*/

//construct element 
function constructElement(attrs) {
    let element = document.createElement(attrs[0]);
    if (!Array.isArray(attrs[1])) {
        element.innerHTML = attrs[1]
    } else {
        for (let attr of attrs[1]) {
            element.setAttribute(attr[0], attr[1]);
            if (attrs.length > 2) element.innerHTML = attrs[2];
        };
    };
    return element
};


/*implementation code for checking user authorization; 
login user and logout*/

//check user session before starting
fetch('/login')
    .then(response => response.json())
    .then(response => {
        let resp = response["data"];
        if (resp['user'] != "None") {
            mainPage('/index/', 'alert alert-success', 'Новых анкет: ')
        } else {
            userLogin()
        };
    });

//user authentification
function userLogin() {
    let loginHead = constructElement(["h5", "Вход в систему"]);
    document.getElementById('appHeaders').innerHTML = loginHead.outerHTML;

    const formLogin = loginForm()   //inner login form
    document.getElementById('appContent').innerHTML = formLogin.outerHTML;
    //listener button and response
    document.getElementById("loginSubmit").addEventListener("click", function () {
        let form = document.getElementById("loginForm");
        let formData = new FormData(form);      // listener for login form
        fetch('login', {
            method: "post",
            body: formData
        })
            .then(response => response.json())
            .then(response => {
                let data = response["data"];
                if (data['user'] == "None") {
                    let divAlert = constructElement(["div", [["class", "alert alert-warning"], ["role", "alert"]], "Неверный логин или пароль"]);
                    document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
                } else {
                    mainPage('/index/', 'alert alert-success', 'Новых анкет: ')
                };
            });
    });
}

//user logout
function userLogout() {
    fetch("/logout")
        .then(response => response.json());
    userLogin()
};

//user login form
function loginForm() {
    let divForm = constructElement(["div", [["class", "py-3"]]]);
    let formLogin = constructElement(["form", [["class", "form-check"], ["id", "loginForm"],
    ["onsubmit", "return false;"]]]);
    divForm.appendChild(formLogin);

    //labels and fields
    let labelNames = ["Пользователь", "Пароль"]
    let typeNames = ["text", "password"]
    let inputNames = ["username", "password"]
    for (let i in labelNames) {
        let usrDiv = constructElement(["div", [["class", "row mb-3"]]]);
        formLogin.appendChild(usrDiv);
        let userLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"],
        ["for", "loginForm"]], labelNames[i]])
        usrDiv.appendChild(userLbl);
        let inpDiv = constructElement(["div", [["class", "col-sm-3"]]]);
        usrDiv.appendChild(inpDiv);
        let usrInp = constructElement(["input", [["class", "form-control"], ["type", typeNames[i]],
        ["name", inputNames[i]]]]);
        inpDiv.appendChild(usrInp)
    };
    //remember
    let rmbDiv1 = constructElement(["div", [["class", "row mb-3"]]]);
    formLogin.appendChild(rmbDiv1);
    let rmbDiv2 = constructElement(["div", [["class", "col-sm-3 offset-sm-2"]]]);
    rmbDiv1.appendChild(rmbDiv2);
    let rmbDiv3 = constructElement(["div", [["class", "form-check"]]]);
    rmbDiv2.appendChild(rmbDiv3);
    let hiddden = constructElement(["input", [["class", "form-check-input"], ["type", "hidden"],
    ["value", "False"], ["name", "remember"]]]);
    rmbDiv3.appendChild(hiddden);
    let rmbInp = constructElement(["input", [["class", "form-check-input"], ["type", "checkbox"],
    ["value", "True"], ["name", "remember"]]]);
    rmbDiv3.appendChild(rmbInp);
    let rmbLbl = constructElement(["label", [["class", ""], ["for", "loginForm"]], "Запомнить"]);
    rmbDiv3.appendChild(rmbLbl);

    //login button
    let submitBtn = constructElement(["button", [["class", "btn btn-primary"], ["type", "submit"],
    ["for", "loginForm"], ["id", "loginSubmit"]], "Войти"]);
    formLogin.appendChild(submitBtn);

    return divForm
};


/*implementation code for the main page and user page; 
extended and fast search are included;
pagination work for all variants */

//upload page of candidates table (index and officer recursive page) 
function mainPage(path, attr, message, currentPage = 0) {
    fetch(path + currentPage)
        .then(response => response.json())
        .then(data => {
            let resp = data["data"];
            let tableList = resp[0];
            let newItems = resp[1].items;
            let countPages = resp[2].pager;
            //graphical part of main page
            let divAlert = constructElement(["div", [["class", attr], ["role", "alert"]], message + newItems]);
            document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
            if (path == '/index/') {
                const mainHead = constructElement(['h5', "Главная страница"]);
                document.getElementById('appHeaders').innerHTML = mainHead.outerHTML;
            } else {
                const mainHead = constructElement(['h5', "Cтраница пользователя"]);
                document.getElementById('appHeaders').innerHTML = mainHead.outerHTML;
            };
            const division = document.createElement('div');
            let divTable = createTable(tableList);
            division.appendChild(divTable);
            let divPager = createPager();
            division.appendChild(divPager);
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

//create extended search page
function searchPage() {
    const mainHead = constructElement(['h5', "Страница поиска"]);
    document.getElementById('appHeaders').innerHTML = mainHead.outerHTML;
    //extended search form
    let divForm = document.createElement("div");
    let formSearchExt = constructElement(["form", [["class", "form-check"], ["id", "searchExtForm"],
    ["onsubmit", "return false;"]]]);
    divForm.appendChild(formSearchExt);
    //search result place
    let searchResult = constructElement(["div", [["class", "py-2"], ["id", "searchResult"]]]);
    divForm.appendChild(searchResult);
    //region
    let viewDiv = constructElement(["div", [["class", "row mb-1"]]]);
    formSearchExt.appendChild(viewDiv);
    let viewLbl = constructElement(["label", [["class", "form-label"], ["for", "searchExtForm"]], "по региону"]);
    viewDiv.appendChild(viewLbl);
    //lables and inputs
    let selDiv = constructElement(["div", [["class", "col-sm-8"]]]);
    viewDiv.appendChild(selDiv);
    let namesSearch = ['', 'Главный офис', 'Томск', 'РЦ Запад', 'РЦ Юг', 'РЦ Запад', 'РЦ Урал'];
    let selectInp = constructElement(["select", [["class", "form-select mb-2"],
    ["name", "region"]]]);
    for (let value of namesSearch) {
        let option = constructElement(["option", [["class", "form-select mb-3"], ["value", value]]]);
        option.innerHTML = value;
        selectInp.appendChild(option);
    };
    selDiv.appendChild(selectInp);
    //inputs
    let inpLabels = ["по имени", "по дате рождения", "по номеру документа", "по номеру телефона"]
    let inpNames = ["fullname", "birthday", "number", "contact"]
    for (let i in inpLabels) {
        let lblDiv = constructElement(["div", [["class", "row mb-2"]]]);
        formSearchExt.appendChild(lblDiv);
        let checkLbl = constructElement(["label", [["class", "form-label"], ["for", "searchExtForm"]]]);
        checkLbl.innerHTML = inpLabels[i];
        lblDiv.appendChild(checkLbl);
        let inpDiv = constructElement(["div", [["class", "col-sm-8"]]]);
        lblDiv.appendChild(inpDiv);
        if (inpNames[i] == "birthday") {
            let chckInp = constructElement(["input", [["class", "form-control"],
            ["type", "date"], ["name", inpNames[i]]]]);
            inpDiv.appendChild(chckInp);
        } else {
            let chckInp = constructElement(["input", [["class", "form-control"],
            ["type", "text"], ["name", inpNames[i]]]]);
            inpDiv.appendChild(chckInp);
        };
    };
    //button group 
    const extSearchButtonGroup = constructElement(["div", [["class", "btn-group py-2"], ["role", "group"]]]);
    formSearchExt.appendChild(extSearchButtonGroup);
    const extSearchButton = constructElement(["button", [["class", "btn btn-outline-primary btn-sm"],
    ["type", "submit"], ["for", "searchExtForm"],
    ["id", "extSearchButton"],
    ["onclick", "searchItem('searchExtForm', '/extsearch/')"]]]);
    extSearchButton.innerHTML = 'Найти'
    extSearchButtonGroup.appendChild(extSearchButton);
    const resetButton = constructElement(["button", [["class", "btn btn-outline-secondary btn-sm"],
    ["type", "reset"], ["for", "searchExtForm"],
    ["id", "resetButton"]]]);
    resetButton.innerHTML = 'Очистить форму'
    extSearchButtonGroup.appendChild(resetButton);

    document.getElementById('appContent').innerHTML = divForm.outerHTML;
};

//functionality for fast and extended search
function searchItem(idForm, path, currentPage = 0) {
    let form = document.getElementById(idForm);
    let formData = new FormData(form);
    fetch(path + currentPage, {
        method: "post",
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            let resp = data["data"];
            let tableList = resp[0];
            let newItems = resp[1].items;
            let countPages = resp[2].pager;

            //graphical part of search page
            let divAlert = constructElement(["div", [["class", 'alert alert-warning'], ["role", "alert"]],
                'Результатов поиска на странице: ' + newItems]);
            document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
            const mainHead = constructElement(['h5', "Результат поиска"]);
            document.getElementById('appHeaders').innerHTML = mainHead.outerHTML;
            const division = document.createElement('div');
            let divTable = createTable(tableList);
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
        });
};


//create table with candidates list
function createTable(candidates) {
    const divTable = constructElement(["div", [["id", "divTable"]]]);
    const table = constructElement(["table", [["class", "table table-hover table-responsive \
                                    align-middle py-1"]]]);
    divTable.appendChild(table);
    const thead = document.createElement('thead');
    table.appendChild(thead);
    const tbody = document.createElement('tbody');
    table.appendChild(tbody);
    let tr = document.createElement('tr');
    let tableHeader = ["#", "Регион", "Фамилия Имя Отчество", "Дата рождения", "Статус", "Дата"]
    let tabbleWidth = [["width", "5%"], ["width", "15%"], ["width", "30%"], ["width", "15%"],
    ["width", "15%"], ["width", "15%"]]
    for (let i in tableHeader) {
        let th = constructElement(['th', [tabbleWidth[i]], tableHeader[i]]);
        tr.appendChild(th);
        thead.appendChild(tr);
    };
    "width", "25%"
    for (let candidate of candidates) {
        let tr = document.createElement('tr');
        for (let val of [candidate['id'], candidate['region'], candidate['fullname'],
        candidate['birthday'], candidate['status'], candidate['deadline']]) {
            let td = document.createElement('td');
            if (val == candidate['fullname']) {
                let a = constructElement(["a", [["href", "#"], ["class", "link-underline-primary"],
                ["onclick", "openProfile(" + candidate['id'] + ")"]]]);
                a.innerHTML = val;
                td.appendChild(a);
            } else {
                td.innerHTML = val
            };
            if (val == candidate['deadline'] || val == candidate['birthday']) {
                let date = new Date(Date.parse(val));
                let formatted = date.toLocaleDateString('ru-RU')
                td.innerHTML = formatted
            };
            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    };
    return divTable
}

//create pager element
function createPager() {
    const divPager = constructElement(["div", [["id", "divPager"]]]);
    const navPage = document.createElement('nav');
    divPager.appendChild(navPage);
    const pagerUl = constructElement(["ul", [["class", "pagination justify-content-center"], ["id", "pager"]]]);
    navPage.appendChild(pagerUl);
    let idPagers = ["previousPage", "nextPage"];
    let namePagers = ["Предыдущая", "Следующая"];
    for (let i in namePagers) {
        const pageItem = constructElement(['li', [["class", "page-item"], ["id", idPagers[i]]]]);
        pagerUl.appendChild(pageItem);
        const pageLink = constructElement(['a', [["class", "page-link"], ["href", "#"]]]);
        pageLink.innerHTML = namePagers[i];
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

/*profile code implementation with forms  
for loading, editing and deleting items*/

//staff-department form
function staffForm() {
    let divForm = constructElement(["div", [["class", "py-3"]]]);
    let formStaff = constructElement(["form", [["class", "form-check"], ["id", "staffForm"], ["onsubmit", "return false;"]]]);
    divForm.appendChild(formStaff);
    let labelNames = ["Должность/подразделение", "Департамент/кластер"]
    let inputNames = ["position", "department"]
    //fields
    for (let i in labelNames) {
        let staffDiv = constructElement(["div", [["class", "row mb-3"]]]);
        formStaff.appendChild(staffDiv);
        let staffLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], ["for", "staffForm"]]]);
        staffLbl.innerHTML = labelNames[i];
        staffDiv.appendChild(staffLbl);
        let inpDiv = constructElement(["div", [["class", "col-sm-8"]]]);
        staffDiv.appendChild(inpDiv);
        let staffInp = constructElement(["input", [["class", "form-control"], ["type", "text"], ["name", inputNames[i]]]]);
        inpDiv.appendChild(staffInp);
    };
    let submitBtn = constructElement(["button", [["class", "btn btn-primary"], ["type", "submit"], ["for", "staffForm"], ["id", "submit"]], "Сохранить"]);
    formStaff.appendChild(submitBtn);
    return divForm
};

//documents form
function documentForm() {
    let divForm = constructElement(["div", [["class", "py-3"]]]);
    let formDocument = constructElement(["form", [["class", "form-check"], ["id", "documentForm"], ["onsubmit", "return false;"]]]);
    divForm.appendChild(formDocument);
    let viewDiv = constructElement(["div", [["class", "row mb-3"]]]);
    formDocument.appendChild(viewDiv);
    //select
    let viewLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], ["for", "documentForm"]]]);
    viewLbl.innerHTML = "Вид документа";
    viewDiv.appendChild(viewLbl);
    let inpDiv = constructElement(["div", [["class", "col-sm-8"]]]);
    viewDiv.appendChild(inpDiv);
    let selectNames = ["Паспорт гражданина России", "Иностранный документ", "Другое"];
    let selectInp = constructElement(["select", [["class", "form-select mb-3"], ["name", "view"]]]);
    for (let [index, value] of selectNames.entries()) {
        let option = constructElement(["option", [["class", "form-select mb-3"], ["value", index]]]);
        option.innerHTML = value;
        select.appendChild(option);
    };
    inpDiv.appendChild(selectInp);
    //input
    let docLabels = ["Серия", "Номер документа", "Орган выдавший", "Дата выдачи"]
    let docNames = ["series", "number", "agency", "issue"]
    for (let i in docLabels) {
        let docDiv = constructElement(["div", [["class", "row mb-3"]]]);
        formDocument.appendChild(docDiv);
        let docLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], ["for", "documentForm"]]]);
        docLbl.innerHTML = docLabels[i];
        docDiv.appendChild(docLbl);
        let inpDiv = constructElement(["div", [["class", "col-sm-8"]]]);
        docDiv.appendChild(inpDiv);
        if (docNames[i] == "issue") {
            let docInp = constructElement(["input", [["class", "form-control"], ["type", "date"], ["name", docNames[i]]]]);
            inpDiv.appendChild(docInp);
        } else {
            let docInp = constructElement(["input", [["class", "form-control"], ["type", "text"], ["name", docNames[i]]]]);
            inpDiv.appendChild(docInp);
        };
    };
    //submit button
    let submitBtn = constructElement(["button", [["class", "btn btn-primary"], ["type", "submit"], ["for", "documentForm"], ["id", "submit"]], "Сохранить"]);
    formDocument.appendChild(submitBtn);
    return divForm
};

function addressForm() {
    let divForm = constructElement(["div", [["class", "py-3"]]]);
    let formAddress = constructElement(["form", [["class", "form-check"], ["id", "addressForm"], ["onsubmit", "return false;"]]]);
    divForm.appendChild(formAddress);
    let viewDiv = constructElement(["div", [["class", "row mb-3"]]]);
    formAddress.appendChild(viewDiv);
    let viewLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], ["for", "addressForm"]]]);
    viewLbl.innerHTML = "Вид адреса";
    viewDiv.appendChild(viewLbl);
    let inpDiv = constructElement(["div", [["class", "col-sm-8"]]]);
    viewDiv.appendChild(inpDiv);
    let namesAddr = ['Адрес регистрации', 'Адрес проживания', 'Другое']
    let selectInp = constructElement(["select", [["class", "form-select mb-3"], ["name", "view"]]]);
    for (let [index, value] of namesAddr.entries()) {
        let option = constructElement(["option", [["class", "form-select mb-3"], ["value", index]]]);
        option.innerHTML = value;
        selectInp.appendChild(option);
    };
    inpDiv.appendChild(selectInp);
    let addrLabels = ["Регион", "Полный адрес"]
    let addrNames = ["region", "address"]
    for (let i in addrLabels) {
        let addrDiv = constructElement(["div", [["class", "row mb-3"]]]);
        formAddress.appendChild(addrDiv);
        let addrLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], ["for", "addressForm"]]]);
        docLbl.innerHTML = addrLabels[i];
        addrDiv.appendChild(addrLbl);
        let inpDiv = constructElement(["div", [["class", "col-sm-8"]]]);
        addrDiv.appendChild(inpDiv);
        let addrInp = constructElement(["input", [["class", "form-control"], ["type", "text"], ["name", addrNames[i]]]]);
        inpDiv.appendChild(addrInp);
    };
    let submitBtn = constructElement(["button", [["class", "btn btn-primary"], ["type", "submit"], ["for", "addressForm"], ["id", "submit"]], "Сохранить"]);
    formAddress.appendChild(submitBtn);
    return divForm
};

function contactForm() {
    let divForm = constructElement(["div", [["class", "py-3"]]]);
    let formContact = constructElement(["form", [["class", "form-check"], ["id", "contactForm"], ["onsubmit", "return false;"]]]);
    divForm.appendChild(formContact);
    let viewDiv = constructElement(["div", [["class", "row mb-3"]]]);
    formContact.appendChild(viewDiv);
    let viewLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], ["for", "ContactForm"]]]);
    viewLbl.innerHTML = "Вид контакта";
    viewDiv.appendChild(viewLbl);
    let inpDiv = constructElement(["div", [["class", "col-sm-8"]]]);
    viewDiv.appendChild(inpDiv);
    let namesCont = ['Телефон', 'Электронная почта', 'Другое']
    let selectInp = constructElement(["select", [["class", "form-select mb-3"], ["name", "view"]]]);
    for (let [index, value] of namesCont.entries()) {
        let option = constructElement(["option", [["class", "form-select mb-3"], ["value", index]]]);
        option.innerHTML = value;
        selectInp.appendChild(option);
    };
    inpDiv.appendChild(selectInp);
    let contDiv = constructElement(["div", [["class", "row mb-3"]]]);
    formContact.appendChild(contDiv);
    let contLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], ["for", "ContactForm"]]]);
    docLbl.innerHTML = "Контакт";
    contDiv.appendChild(contLbl);
    let contInpDiv = constructElement(["div", [["class", "col-sm-8"]]]);
    contDiv.appendChild(contInpDiv);
    let contInp = constructElement(["input", [["class", "form-control"], ["type", "text"], ["name", "сontact"]]]);
    inpDiv.appendChild(contInp);
    let submitBtn = constructElement(["button", [["class", "btn btn-primary"], ["type", "submit"], ["for", "ContactForm"], ["id", "submit"]], "Сохранить"]);
    formContact.appendChild(submitBtn);
    return divForm
};

function workplaceForm() {
    let divForm = constructElement(["div", [["class", "py-3"]]]);
    let formWorkplace = constructElement(["form", [["class", "form-check"], ["id", "workplaceForm"], ["onsubmit", "return false;"]]]);
    divForm.appendChild(formWorkplace);
    let viewDiv = constructElement(["div", [["class", "row mb-3"]]]);
    formWorkplace.appendChild(viewDiv);
    let workLabels = ["Период работы", "Место работы", "Адрес организации", "Должность"]
    let workNames = ["period", "workplace", "address", "position"]
    //div for labeles/inputs
    for (let i in workLabels) {
        let workDiv = constructElement(["div", [["class", "row mb-3"]]]);
        formWorkplace.appendChild(workDiv);
        let workLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], ["for", "workplaceForm"]]]);
        workLbl.innerHTML = workLabels[i];
        let inpDiv = constructElement(["div", [["class", "col-sm-8"]]]);
        workDiv.appendChild(inpDiv);
        let workInp = constructElement(["input", [["class", "form-control"], ["type", "text"], ["name", workNames[i]]]]);
        inpDiv.appendChild(workInp)
    };
    let submitBtn = constructElement(["button", [["class", "btn btn-primary"], ["type", "submit"], ["for", "workplaceForm"], ["id", "submit"]], "Сохранить"]);
    formWorkplace.appendChild(submitBtn);
    return divForm
};

function relationForm() {
    let divForm = constructElement(["div", [["class", "py-3"]]]);
    let formRelation = constructElement(["form", [["class", "form-check"], ["id", "relationForm"], ["onsubmit", "return false;"]]]);
    divForm.appendChild(formRelation);
    let viewDiv = constructElement(["div", [["class", "row mb-3"]]]);
    formRelation.appendChild(viewDiv);
    let viewLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], ["for", "relationForm"]]]);
    viewLbl.innerHTML = "Вид связи";
    let inpDiv = constructElement(["div", [["class", "col-sm-8"]]]);
    viewDiv.appendChild(inpDiv);
    let namesRelation = ['Отец/Мать', 'Брат/Сестра', 'Супруг', 'Дети', 'Другое']
    let selectInp = constructElement(["select", [["class", "form-select mb-3"], ["name", "realtion"]]]);
    for (let [index, value] of namesRelation.entries()) {
        let option = constructElement(["option", [["class", "form-select mb-3"], ["value", index]]]);
        option.innerHTML = value;
        selectInp.appendChild(option);
    };
    inpDiv.appendChild(selectInp);
    let relationLabels = ["Полное ФИО", "Дата рождения", "Адрес", "Место работы", "Контакт"]
    let relationNames = ["fullname", "birthday", "address", "workplace", "contact"]
    //div for labeles/inputs
    for (let i in relationLabels) {
        let relationDiv = constructElement(["div", [["class", "row mb-3"]]]);
        formRelation.appendChild(relationDiv);
        let relationLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], ["for", "relationForm"]]]);
        relationLbl.innerHTML = relationLabels[i];
        relationDiv.appendChild(relationLbl);
        let inpDiv = constructElement(["div", [["class", "col-sm-8"]]]);
        relationDiv.appendChild(inpDiv);
        if (relationNames[i] == "birthday") {
            let relationInp = constructElement(["input", [["class", "form-control"], ["type", "date"], ["name", relationNames[i]]]]);
            inpDiv.appendChild(relationInp);
        } else {
            constructElement(["input", [["class", "form-control"], ["type", "text"], ["name", relationNames[i]]]]);
            inpDiv.appendChild(relationInp);
        };
    };
    let submitBtn = constructElement(["button", [["class", "btn btn-primary"], ["type", "submit"], ["for", "relationForm"], ["id", "submit"]], "Сохранить"]);
    formRelation.appendChild(submitBtn);
    return divForm
};

function registryForm() {
    let divForm = constructElement(["div", [["class", "py-3"]]]);
    let formRegistry = constructElement(["form", [["class", "form-check"], ["id", "registryForm"], ["onsubmit", "return false;"]]]);
    divForm.appendChild(formRegistry);
    let regDiv = constructElement(["div", [["class", "row mb-3"]]]);
    formRegistry.appendChild(regDiv);
    let regLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], ["for", "registryForm"]]]);
    regLbl.innerHTML = "Комментарий";
    regDiv.appendChild(regLbl);
    let areaDiv = constructElement(["div", [["class", "col-sm-8"]]]);
    regDiv.appendChild(areaDiv);
    let textfield = constructElement(["textarea", [["class", "form-control"], ["rows", "2"], ["name", "comments"]]]);
    areaDiv.appendChild(textfield);
    let viewDiv = constructElement(["div", [["class", "row mb-3"]]]);
    formRegistry.appendChild(viewDiv);
    let viewLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], ["for", "registryForm"]]]);
    regLbl.innerHTML = "Решение";
    regLbl.appendChild(viewLbl);
    let inpDiv = constructElement(["div", [["class", "col-sm-8"]]]);
    viewDiv.appendChild(inpDiv);
    let namesReg = ['СОГЛАСОВАНО', 'СОГЛАСОВАНО С КОММЕНТАРИЕМ', 'СОГЛАСОВАНО С РИСКОМ', 'ОТКАЗАНО В СОГЛАСОВАНИИ', 'ОТМЕНЕНО'];
    let selectInp = constructElement(["select", [["class", "form-select mb-3"], ["name", "decision"]]]);
    for (let [index, value] of namesReg.entries()) {
        let option = constructElement(["option", [["class", "form-select mb-3"], ["value", index]]]);
        option.innerHTML = value;
        selectInp.appendChild(option);
    };
    inpDiv.appendChild(selectInp);
    //submit button
    let submitBtn =
        constructElement(["button", [["class", "btn btn-primary"], ["type", "submit"], ["for", "registryForm"], ["id", "submit"]], "Сохранить"]);
    submitBtn.innerHTML = "Сохранить";
    formRegistry.appendChild(submitBtn);
    return divForm
};

function poligrafForm() {
    let divForm = constructElement(["div", [["class", "py-3"]]]);
    let formPoligraf = constructElement(["form", [["class", "form-check"], ["id", "poligrafForm"], ["onsubmit", "return false;"]]]);
    divForm.appendChild(formPoligraf);
    let viewDiv = constructElement(["div", [["class", "row mb-3"]]]);
    formPoligraf.appendChild(viewDiv);
    let viewLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], ["for", "poligrafForm"]]]);
    viewLbl.innerHTML = "Тема проверки";
    viewDiv.appendChild(viewLbl);
    let selDiv = constructElement(["div", [["class", "col-sm-8"]]]);
    viewDiv.appendChild(selDiv);
    let namesPoligraf = ['Проверка кандидата', 'Служебная проверка', 'Служебное расследование', 'Другое'];
    let selectInp = constructElement(["select", [["class", "form-select mb-3"], ["name", "theme"]]]);
    for (let [index, value] of namesPoligraf.entries()) {
        let option = constructElement(["option", [["class", "form-select mb-3"], ["value", index]]]);
        option.innerHTML = value;
        selectInp.appendChild(option);
    };
    selDiv.appendChild(selectInp);
    //info
    let addDiv = constructElement(["div", [["class", "row mb-3"]]]);
    formPoligraf.appendChild(addDiv);
    let addLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], ["for", "poligrafForm"]]]);
    addLbl.innerHTML = "Информация";
    addDiv.appendChild(addLbl);
    let areaDiv = constructElement(["div", [["class", "col-sm-8"]]]);
    addDiv.appendChild(areaDiv);
    let textfield = constructElement(["textarea", [["class", "form-control"], ["rows", "3"], ["name", "results"]]]);
    areaDiv.appendChild(textfield);
    //date
    let poligrafDiv = constructElement(["div", [["class", "row mb-3"]]]);
    formPoligraf.appendChild(poligrafDiv);
    let poligrafLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], ["for", "poligrafForm"]]]);
    regLbl.innerHTML = "Дата проведения";
    poligrafDiv.appendChild(poligrafLbl);
    let inpDiv = constructElement(["div", [["class", "col-sm-8"]]]);
    poligrafDiv.appendChild(inpDiv);
    let poligrafInp = constructElement(["input", [["class", "form-control"], ["type", "date"], ["name", "deadline"]]]);
    inpDiv.appendChild(poligrafInp);
    //submit button
    let submitBtn = constructElement(["button", [["class", "btn btn-primary"], ["type", "submit"], ["for", "poligrafForm"], ["id", "submit"]], "Сохранить"]);
    formPoligraf.appendChild(submitBtn);
    return divForm
};

function investigationForm() {
    let divForm = constructElement(["div", [["class", "py-3"]]]);
    let formInvestigation = constructElement(["form", [["class", "form-check"], ["id", "investigationForm"], ["onsubmit", "return false;"]]]);
    divForm.appendChild(formInvestigation);
    //theme
    let investigationThemeDiv = constructElement(["div", [["class", "row mb-3"]]]);
    formInvestigation.appendChild(investigationThemeDiv);
    let investigationThemeLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], ["for", "investigationForm"]]]);
    investigationThemeLbl.innerHTML = "Тема проверки";
    investigationThemeDiv.appendChild(investigationThemeLbl);
    let inpThemeDiv = constructElement(["div", [["class", "col-sm-8"]]]);
    investigationThemeDiv.appendChild(inpThemeDiv);
    let investigationThemeInp = constructElement(["input", [["class", "form-control"], ["type", "text"], ["name", "theme"]]]);
    inpThemeDiv.appendChild(investigationThemeInp);
    //info
    let addDiv = constructElement(["div", [["class", "row mb-3"]]]);
    formInvestigation.appendChild(addDiv);
    let addLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], ["for", "investigationForm"]]]);
    addLbl.innerHTML = "Информация";
    addDiv.appendChild(addLbl);
    let areaDiv = constructElement(["div", [["class", "col-sm-8"]]]);
    addDiv.appendChild(areaDiv);
    let textfield = constructElement(["textarea", [["class", "form-control"], ["rows", "3"], ["name", "results"]]]);
    areaDiv.appendChild(textfield);
    //date
    let investigationDiv = constructElement(["div", [["class", "row mb-3"]]]);
    formInvestigation.appendChild(investigationDiv);
    let investigationLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], ["for", "investigationForm"]]]);
    investigationLbl.innerHTML = "Дата проведения";
    investigationDiv.appendChild(investigationLbl);
    let inpDiv = constructElement(["div", [["class", "col-sm-8"]]]);
    investigationDiv.appendChild(inpDiv);
    let investigationInp = constructElement(["input", [["class", "form-control"], ["type", "date"], ["name", "deadline"]]]);
    inpDiv.appendChild(investigationInp);
    //submit button
    let submitBtn = constructElement(["button", [["class", "btn btn-primary"], ["type", "submit"], ["for", "investigationForm"], ["id", "submit"]], "Сохранить"]);
    formInvestigation.appendChild(submitBtn);
    return divForm
};

function inquiryForm() {
    let divForm = constructElement(["div", [["class", "py-3"]]]);
    let formInquiry = constructElement(["form", [["class", "form-check"], ["id", "inquiryForm"], ["onsubmit", "return false;"]]]);
    divForm.appendChild(formInquiry);
    //info
    let addDiv = constructElement(["div", [["class", "row mb-3"]]]);
    formInquiry.appendChild(addDiv);
    let addLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], ["for", "inquiryForm"]]]);
    addLbl.innerHTML = "Информация";
    addDiv.appendChild(addLbl);
    let areaDiv = constructElement(["div", [["class", "col-sm-8"]]]);
    addDiv.appendChild(areaDiv);
    let textfield = constructElement(["textarea", [["class", "form-control"], ["rows", "3"], ["name", "results"]]]);
    areaDiv.appendChild(textfield);
    let inpLabels = ["Инициатор", "Источник", "Дата запроса"]
    let inpNames = ["initiator", "source", "deadline"]
    for (let i in inpLabels) {
        let lblDiv = constructElement(["div", [["class", "row mb-3"]]]);
        formInquiry.appendChild(lblDiv);
        let checkLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], ["for", "addressForm"]]]);
        checkLbl.innerHTML = inpLabels[i];
        lblDiv.appendChild(checkLbl);
        let inpDiv = constructElement(["div", [["class", "col-sm-8"]]]);
        lblDiv.appendChild(inpDiv);
        if (inpNames[i] == "deadline") {
            let chckInp = constructElement(["input", [["class", "form-control"], ["type", "date"], ["name", inpNames[i]]]]);
            inpDiv.appendChild(chckInp);
        } else {
            let chckInp = constructElement(["input", [["class", "form-control"], ["type", "text"], ["name", inpNames[i]]]]);
            inpDiv.appendChild(chckInp);
        };
    };
    let submitBtn = constructElement(["button", [["class", "btn btn-primary"], ["type", "submit"], ["for", "inquiryForm"], ["id", "submit"]], "Сохранить"]);
    formInquiry.appendChild(submitBtn);
    return divForm
};


/*implementation code for adding candidate's resume; 
upload resume from Excel file*/

//create resume
function createResume(value = null) {
    const loginHead = document.createElement('h5');
    loginHead.innerHTML = "Создать анкету";
    document.getElementById('appHeaders').innerHTML = loginHead.outerHTML;
    const divResume = constructElement(["div", [["class", "py-1"]]]);
    //upload file form
    const formUpload = constructElement(["form", [["id", "formFile"], ["class", "form-check"],
                                                ["onsubmit", "return false;"], ["method", "post"]]]);
    divResume.appendChild(formUpload);
    const fileDiv = constructElement(["div", [["class", "row mb-3"]]]);
    formUpload.appendChild(fileDiv);
    const uplLabel = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], 
                                                ["for", "formFile"]], "Загрузить файл Excel"]);
    fileDiv.appendChild(uplLabel);
    let inpFileDiv = constructElement(["div", [["class", "col-sm-10"]]]);
    fileDiv.appendChild(inpFileDiv);
    const inputUpload = constructElement(["input", [["class", "form-control"], ["type", "file"],
                                                    ["name", "file"]]]);
    inpFileDiv.appendChild(inputUpload);

    //ручной ввод данных анкеты
    const formResume = constructElement(["form", [["class", "form-check"], ["id", "resumeForm"],
    ["onsubmit", "return false;"]]]);
    divResume.appendChild(formResume);
    let viewDiv = constructElement(["div", [["class", "row mb-3"]]]);
    formResume.appendChild(viewDiv);
    let viewLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"],
    ["for", "resumeForm"]], "Регион"]);
    viewDiv.appendChild(viewLbl);
    let inpDiv = constructElement(["div", [["class", "col-sm-10"]]]);
    viewDiv.appendChild(inpDiv);
    let namesResume = ['Главный офис', 'Томск', 'РЦ Запад', 'РЦ Юг', 'РЦ Запад', 'РЦ Урал'];
    let selectInp = constructElement(["input", [["class", "form-select mb-3"], ["type", namesResume],
    ["name", "region"]]]);
    inpDiv.appendChild(selectInp);
    let resumeLabels = ["Полное ФИО", "Изменение имени", "Дата рождения", "Место рождения", "Гражданство",
        "СНИЛС", "ИНН", "Образование", "Рекрутер"]
    let resumeNames = ["fullname", "previous", "birthday", "birthplace", "country", "snils", "inn",
        "education", "recruiter"]
    //div for labeles/inputs
    for (let i in resumeLabels) {
        let resumeDiv = constructElement(["div", [["class", "row mb-3"]]]);
        formResume.appendChild(resumeDiv);
        let resumeLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"],
        ["for", "resumeForm"]], resumeLabels[i]]);
        resumeDiv.appendChild(resumeLbl);
        let inpDiv = constructElement(["div", [["class", "col-sm-10"]]]);
        resumeDiv.appendChild(inpDiv);

        //open new form or prefilled form for editing 
        if (value == null) {
            if (resumeNames[i] == "birthday") {
                let resumeInp = constructElement(["input", [["class", "form-control"], ["type", "date"],
                ["name", resumeNames[i]]]]);
                inpDiv.appendChild(resumeInp);
            } else {
                let resumeInp = constructElement(["input", [["class", "form-control"], ["type", "text"],
                ["name", resumeNames[i]]]]);
                inpDiv.appendChild(resumeInp);
            };
        } else {
            let values = Object.keys(value)
            if (resumeNames[i] == "birthday") {
                let resumeInp = constructElement(["input", [["class", "form-control"], ["type", "date"],
                ["name", resumeNames[i]], ["value", values[i]]]]);
                inpDiv.appendChild(resumeInp);
            } else {
                let resumeInp = constructElement(["input", [["class", "form-control"], ["type", "text"],
                ["name", resumeNames[i]], ["value", values[i]]]]);
                inpDiv.appendChild(resumeInp);
            };
        };
    };
    let addDiv = constructElement(["div", [["class", "row mb-3"]]]);
    formResume.appendChild(addDiv);
    let addLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"],
    ["for", "resumeForm"]], "Дополнительно"]);
    addDiv.appendChild(addLbl);
    let areaDiv = constructElement(["div", [["class", "col-sm-10"]]]);
    addDiv.appendChild(areaDiv);
    let textfield = constructElement(["textarea", [["class", "form-control"], ["rows", "3"],
    ["name", "addition"]]]);
    areaDiv.appendChild(textfield);
    //submit button
    let submitBtn = constructElement(["button", [["class", "btn btn-primary"], ["type", "submit"],
    ["for", "resumeForm"], ["id", "submitResume"]], "Сохранить"]);
    formResume.appendChild(submitBtn);
    document.getElementById('appContent').innerHTML = divResume.outerHTML;

    // прослушиваем событие от нажатии кнопки на форме загрузки файла
    document.getElementById('formFile').onchange = function() {
    //document.getElementById("submitFile").addEventListener("click", function () {
        let form = document.getElementById("formFile");
        form.submit();
        let formData = new FormData(form);
        fetch('/upload', {
            method: "post",
            body: formData
        })
            .then(response => response.json())
            .then(response => {
                let resp = response["data"];
                let candId = resp[0]['cand_id'];
                let message = resp[1]['message'];
                let divAlert = constructElement(["div", [["class", "alert alert-primary"], ["role", "alert"]]]);
                divAlert.innerHTML = message;
                document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
                openProfile(candId)
            });
    };
    // прослушиваем событие от нажатии кнопки на форме загрузки данных
    document.getElementById("submitResume").addEventListener("click", function () {
        let form = document.getElementById("resumeForm");
        let formData = new FormData(form);
        fetch('/resume', {
            method: "post",
            body: formData
        })
            .then(response => response.json())
            .then(response => {
                let resp = response["data"];
                let message = resp[1]['message'];
                let divAlert = constructElement(["div", [["class", "alert alert-primary"], ["role", "alert"]]]);
                divAlert.innerHTML = message;
                document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
                openProfile(resp[0]['cand_id'])
            });
    });
};

/*implementation code for candidate's profile
various actions with profile*/

//open candidate profile
function openProfile(candId) {
    fetch("/profile/" + candId)
        .then(response => response.json())
        .then(data => {
            let resp = data["data"];
            const candidate = resp[0];
            const staffs = resp[1];
            const documents = resp[2];
            const addresses = resp[3];
            const relations = resp[4];
            const workplaces = resp[5];
            const contacts = resp[6];
            const checks = resp[7];
            const registries = resp[8];
            const inquiries = resp[9];
            const pfos = resp[10];
            const invs = resp[11];
            const state = resp[12];

            let htmlProfile = createProfile(candId)
            document.getElementById('appContent').innerHTML = htmlProfile.outerHTML

            resumeUpd(candidate, state);
            staffUpd(staffs);
            documentUpd(documents);
            addressUpd(addresses);
            contactUpd(contacts);
            workUpd(workplaces);
            relationUpd(relations);
            checkUpd(checks);
            registryUpd(registries);
            poligrafUpd(pfos);
            investigationUpd(invs);
            inquiryUpd(inquiries);
        });
};

//create html for candidate profile
function createProfile(candId) {
    //summary division
    let divProfile = constructElement(["div", [["class", "py-1"]]]);
    divProfile.appendChild(createModal());
    //tab panel
    let navProfile = document.createElement("nav");
    divProfile.appendChild(navProfile);
    let divNav = constructElement(["div", [["class", "nav nav-tabs"], ["role", "tablist"]]]);
    navProfile.appendChild(divNav);
    const tabNames = ['Профиль', 'Проверки', 'Согласования', 'Полиграф', 'Расследования', 'Запросы', 'Другое']
    const tabValues = ["profilePane", "checkPane", "registryPane", "poligrafPane", "investigatePane",
        "inquiryPane", "otherPane"]
    for (let i in tabNames) {
        let navBtn = constructElement(["button", [["data-bs-toggle", "tab"],
        ["data-bs-target", "#"+tabValues[i]], ["id", tabValues[i]+"tab"], ["type", "button"], ["role", "tab"]], tabNames[i]]);
        if (tabNames[i] == tabNames[0]) {
            navBtn.setAttribute("aria-selected", "true");
            navBtn.setAttribute("class", "nav-link active");
        } else {
            navBtn.setAttribute("aria-selected", "false")
            navBtn.setAttribute("class", "nav-link");
        };
        divNav.appendChild(navBtn)
    };
    //tabs content
    let divContent = constructElement(["div", [["class", "tab-content py-1"]]]);
    divProfile.appendChild(divContent);

    //profile tab
    let divPaneResume = constructElement(["div", [["class", "tab-pane fade show active py-1"], ["id", tabValues[0]], ["role", "tabpanel"], ["aria-labelledby", tabValues[0]+"tab"]]]);
    divContent.appendChild(divPaneResume);
    //resume content
    let resumeDiv = constructElement(["div", [["id", "resume"]]]);
    divPaneResume.appendChild(resumeDiv)
    //others contents
    const nаmeHeaders = ['Должности', 'Документы', 'Адреса', 'Контакты', 'Работа', 'Связи'];
    const attrNames = ['staffs', 'documents', 'addresses', 'contacts', 'workplaces', 'relations'];
    const formTarget = [staffForm, documentForm, addressForm, contactForm, workplaceForm, relationForm]
    const updateTarget = [staffUpd, documentUpd, addressUpd, contactUpd, workUpd, relationUpd]
    const buttonNames = ['Добавить должность', 'Добавить документ', 'Добавить адрес', 'Добавить контакт',
        'Добавить работу', 'Добавить связь'];
    for (let i in nаmeHeaders) {
        let targetNames = constructElement(["div", [["class", "py-1"]]]);
        divPaneResume.appendChild(targetNames);
        let targetHeader = constructElement(["p", [["class", "h6 p"]], nаmeHeaders[i]]);
        targetNames.appendChild(targetHeader);
        let idNames = constructElement(["div", [["id", attrNames[i]]]]);
        targetNames.appendChild(idNames)
        let anchorTarget = constructElement(["a", [["class", "btn btn-outline-primary btn-sm hidden-print"],
        ["data-bs-toggle", "modal"], ["data-bs-target", "#formModal"], ["onclick", `modalControl(${formTarget[i]}(), ${updateTarget[i]}, ${candId})`]], buttonNames[i]]);
        targetNames.appendChild(anchorTarget)
    };
    //button group
    let groupBtnResume = constructElement(["div", [["class", "btn-group py-2 hidden-print"], ["role", "group"]]]);
    divPaneResume.appendChild(groupBtnResume)

    //update status button
    let updBtnResume = constructElement(["button", [["class", "btn btn-outline-secondary"], ["id", "updStatus"],
    ["onclick", `updateStatus(${candId})`]], 'Обновить статус']);
    groupBtnResume.appendChild(updBtnResume)

    //edit button
    let editBtnResume = constructElement(["button", [["class", "btn btn-outline-primary"], ["onclick", `sendResume(${candId})`]], "Редактировать анкету"]);
    groupBtnResume.appendChild(editBtnResume)

    //send button
    let sendBtnResume = constructElement(["button", [["class", "btn btn-outline-secondary"],
    ["onclick", `sendResume(${candId})`]], 'Отправить на проверку']);
    groupBtnResume.appendChild(sendBtnResume)

    //check tab
    let divPaneCheck = constructElement(["div", [["class", "tab-pane fade py-1"], ["id", tabValues[1]], ["role", "tabpanel"], ["aria-labelledby", tabValues[1]+"tab"]]]);
    divContent.appendChild(divPaneCheck);

    // кнопка добавить проверку
    let addBtnCheck = constructElement(["a", [["class", "btn btn-outline-secondary"], ["id", "addCheck"],
    ["onclick", `checkForm(${candId})`]], 'Добавить проверку']);
    divPaneCheck.appendChild(addBtnCheck)

    // блок для последней проверки
    let divLastCheck = constructElement(["div", [["id", "lastCheck"]]]);
    divPaneCheck.appendChild(divLastCheck);

    //группа кнопок на вкладке проверки
    let groupBtnCheck = constructElement(["div", [["class", "btn-group hidden-print"], ["role", "group"],
    ["id", "delEdit"]]]);
    divLastCheck.appendChild(groupBtnCheck)

    // кнопка редактировать проверку
    let editBtnCheck = constructElement(["a", [["class", "btn btn-outline-primary"], ["id", "editCheck"],
    ["onclick", `editCheck(${candId})`]], 'Редактировать проверку']);
    groupBtnCheck.appendChild(editBtnCheck)

    // кнопка удалить проверку
    let delBtnCheck = constructElement(["a", [["class", "btn-outline-primary btn-outline-dange"], ["id", "delCheck"],
    ["onclick", `deleteCheck(${candId})`]], 'Удалить проверку']);
    groupBtnCheck.appendChild(delBtnCheck)

    // кнопка согласовать проверку
    let openRegCheck = constructElement(["a", [["class", "btn btn-outline-primary"], ["data-bs-toggle", "modal"],
    ["data-bs-whatever", "formRegistry"], ["data-bs-target", "#formModal"],["id", "openRegistry"]], 'Открыть согласование']);
    groupBtnCheck.appendChild(openRegCheck)
    // блок для других проверок
    let divOtherCheck = constructElement(["div", [["id", "otherChecks"]]]);
    divPaneCheck.appendChild(divOtherCheck)

    //вкладка согласования
    let divPaneReg = constructElement(["div", [["class", "tab-pane fade py-1"], ["id", tabValues[2]], ["role", "tabpanel"], ["aria-labelledby", tabValues[2]+"tab"]]]);
    divContent.appendChild(divPaneReg);
    // блок для последней проверки
    let divReg = constructElement(["div", [["id", "registries"]]]);
    divPaneReg.appendChild(divReg)

    //вкладка полиграфа
    let divPanePfo = constructElement(["div", [["class", "tab-pane fade py-1"], ["id", tabValues[3]], ["role", "tabpanel"], ["aria-labelledby", tabValues[3]+"tab"]]]);
    divContent.appendChild(divPanePfo);
    // кнопка добавить тестирование
    let addBtnPfo = constructElement(["a", [["class", "btn btn-outline-primary hidden-print"],
    ["data-bs-whatever", "formPoligraf"], ["data-bs-toggle", "modal"], ["data-bs-target", "#formModal"]]]);
    addBtnPfo.innerHTML = 'Добавить тестирование';
    divPanePfo.appendChild(addBtnPfo)
    // блок для результаттов тестирования
    let divPfo = constructElement(["div", [["id", "poligrafs"]]]);
    divPanePfo.appendChild(divPfo)

    //investigation tab
    let divPaneInvs = constructElement(["div", [["class", "tab-pane fade py-1"], ["id", tabValues[4]], ["role", "tabpanel"], ["aria-labelledby", tabValues[4]+"tab"]]]);
    divContent.appendChild(divPaneInvs);
    //add button
    let addBtnInvs = constructElement(["a", [["class", "btn btn-outline-primary hidden-print"],
    ["data-bs-whatever", "formInvestigation"], ["data-bs-toggle", "modal"], ["data-bs-target", "#formModal"]]]);
    addBtnInvs.innerHTML = 'Добавить расследование';
    divPaneInvs.appendChild(addBtnInvs)
    //investigation place
    let divInvs = constructElement(["div", [["id", "investigations"]]]);
    divPaneInvs.appendChild(divInvs)

    //inquiries tab
    let divPaneInquiry = constructElement(["div", [["class", "tab-pane fade py-1"], ["id", tabValues[5]], ["role", "tabpanel"], ["aria-labelledby", tabValues[5]+"tab"]]]);
    divContent.appendChild(divPaneInquiry);
    //add button
    let addBtnInquiry = constructElement(["a", [["class", "btn btn-outline-primary hidden-print"],
    ["data-bs-toggle", "modal"], ["data-bs-whatever", "formInquiry"], ["data-bs-target", "#formModal"]]]);
    addBtnInquiry.innerHTML = 'Добавить запрос';
    divPaneInquiry.appendChild(addBtnInquiry)
    //inquiries place
    let divInquiry = constructElement(["div", [["id", "inquiries"]]]);
    divPaneInquiry.appendChild(divInquiry)

    return divProfile
};

//modal window
function createModal() {
    //modal dialog
    let divModal = constructElement(["div", [["class", "modal"], ["id", "formModal"],
    ["data-bs-backdrop", "static"], ["data-bs-keyboard", "false"], ["tabindex", "-1"]]]);
    let divModalDialog = constructElement(["div", [["class", "modal-dialog modal-xl"]]]);
    divModal.appendChild(divModalDialog)
    let divModalContent = constructElement(["div", [["class", "modal-content"]]]);
    divModalDialog.appendChild(divModalContent)
    let divModalHeader = constructElement(["div", [["class", "modal-header"]]]);
    divModalContent.appendChild(divModalHeader)
    let divModalTitle = constructElement(["h5", [["class", "modal-title"]],'Добавить информацию']);
    divModalHeader.appendChild(divModalTitle)
    let btnModalClose = constructElement(["h5", [["class", "btn-close"], ["type", "button"],
    ["data-bs-dismiss", "modal"]]]);
    divModalHeader.appendChild(btnModalClose)
    let modalBody = constructElement(["div", [["id", "modalBody"]]]);
    divModalContent.appendChild(modalBody)
    
    return divModal
};

function modalControl(formTarget, updateTarget, candId){
    let innerModal = document.getElementById("modalBody");
    innerModal.innerHTML = formTarget.outerHTML;
    document.getElementById("submit").addEventListener("click", function () {
        let form = document.getElementsByTagName("form");
        console.log(form);
        console.log(form.id)
        let formData = new FormData(form);
        fetch(`/add/${form.id}/${candId}`, {
            method: "post",
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                let resp = data["data"];
                updateTarget(resp[0])
                let divAlert = constructElement(["div", [["class", "alert alert-warning"], ["role", "alert"]], resp[1]]);
                document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
            });
    });
};


//создание, обновление резюме
function resumeUpd(resps, state) {
    const profileHead = constructElement(["h5", resps[0]['fullname']]);
    document.getElementById('appHeaders').innerHTML = profileHead.outerHTML;
    let names = ['Изменение имени', 'Дата рождения', 'Место рождения', 'Гражданство', 'СНИЛС',
        'ИНН', 'Образование', 'Дополнительная информация', 'Регион', 'Статус', 'Дата', 'Рекрутер'];
    let response = [];
    for (let resp of resps) {
        response.push([resp['previous'], resp['birthday'], resp['birthplace'], resp['country'], resp['snils'], resp['inn'],
        resp['education'], resp['addition'], resp['region'], resp['status'], resp['deadline'], resp['recruiter']]);
    };
    let division = constructTable(names, response);
    document.getElementById('resume').innerHTML = division.outerHTML

    if (resps[0]['status'] != state['NEWFAG'] && resps[0]['status'] != state['UPDATE']) {
        let sendResumeBtn = document.getElementById('sendResume');
        sendResumeBtn.setAttribute("class", "disabled btn btn-outline-success hidden-print");
        let addCheckBtn = document.getElementById('addCheck');
        addCheckBtn.setAttribute("class", "disabled btn btn-outline-primary hidden-print")
    };
    if (response[0]['status'] != state['SAVE'] && response[0]['status'] != state['REPLY']) {
        let delEditBtn = document.getElementById('delEdit');
        delEditBtn.setAttribute("class", "disabled btn-group py-2")
    };
    if (response[0]['status'] != state['RESULT']) {
        let sendRegistryBtn = document.getElementById('openRegistry');
        sendRegistryBtn.setAttribute("class", "disabled btn btn-outline-primary hidden-print")
    };
};

//создание, обновление таблицы должностей
function staffUpd(resps) {
    let names = ['Должность', 'Департамент'];
    let response = []
    for (let resp of resps) {
        response.push([resp['position'], resp['department']]);
    };
    let division = constructTable(names, response);
    document.getElementById('staffs').innerHTML = division.outerHTML
};

//создание, обновление таблицы документов
function documentUpd(resps) {
    let names = ['Вид документа', 'Серия', 'Номер', 'Кем выдан', 'Дата'];
    let response = []
    for (let resp of resps) {
        response.push([resp['view'], resp['series'], resp['number'], resp['agency'], resp['issue']]);
    };
    let division = constructTable(names, response);
    document.getElementById('documents').innerHTML = division.outerHTML
};

//создание, обновление таблицы адресов
function addressUpd(resps) {
    let names = ['Тип', 'Регион', 'Адрес'];
    let response = []
    for (let resp of resps) {
        response.push([resp['view'], resp['region'], resp['address']]);
    };
    let division = constructTable(names, response);
    document.getElementById('addresses').innerHTML = division.outerHTML
};

//создание, обновление таблицы контактов
function contactUpd(resps) {
    let names = ['Вид', 'Контакт'];
    let response = []
    for (let resp of resps) {
        response.push([resp['view'], resp['contact']]);
    };
    let division = constructTable(names, response);
    document.getElementById('contacts').innerHTML = division.outerHTML
};

//создание, обновление таблицы мест работы
function workUpd(resps) {
    let names = ['Период', 'Организация', 'Адрес', 'Должность'];
    let response = []
    for (let resp of resps) {
        response.push([resp['period'], resp['workplace'], resp['address'], resp['position']]);
    };
    let division = constructTable(names, response);
    document.getElementById('workplaces').innerHTML = division.outerHTML
};

//создание, обновление таблицы связей
function relationUpd(resps) {
    let names = ['Связь', 'Полное ФИО', 'Дата рождения', 'Адрес', 'Место работы', 'Контакты'];
    let response = []
    for (let resp of resps) {
        response.push([resp['relation'], resp['fullname'], resp['birthday'], resp['address'], resp['workplace'], resp['contact']]);
    };
    let division = constructTable(names, response);
    document.getElementById('relations').innerHTML = division.outerHTML
};

//создание, обновление таблицы проверки
function checkUpd(resps) {
    let names = ['ID', 'Материалы проверки', 'Статус автопроверки', 'Бывший работник МТСБ',
        'Проверка по местам работы', 'Проверка паспорта', 'Проверка ИНН', 'Проверка ФССП',
        'Проверка банкротства', 'Проверка БКИ', 'Проверка судебных дел', 'Проверка ' / 'аффилированности',
        'Проверка в списке террористов', 'Проверка нахождения в розыске',
        'Проверка в открытых источниках', 'Проверка Кронос', 'Проверка Крос', 'Дополнительная' / 'информация',
        'Результат проверки', 'Дата проверки', 'Сотрудник СБ'];
    let response = []
    for (let resp of resps) {
        response.push([resp['id'], resp['path'], resp['autostatus'], resp['employee'], resp['workplace'],
        resp['document'], resp['inn'], resp['debt'], resp['bankruptcy'], resp['bki'], resp['courts'],
        resp['affiliation'], resp['terrorist'], resp['mvd'], resp['internet'], resp['cronos'], resp['cros'],
        resp['addition'], resp['conclusion'], resp['deadline'], resp['officer']]);
    };
    let division = constructTable(names, response);
    document.getElementById('lastCheck').innerHTML = division.outerHTML;
};

//создание, обновление таблицы согласований
function registryUpd(resps) {
    let names = ['ID проверки', 'Комментарий', 'Решение', 'Согласующий', 'Дата'];
    let response = []
    for (let resp of resps) {
        response.push([resp['check_id'], resp['comments'], resp['decision'], resp['supervisor'], resp['deadline']]);
    };
    let division = constructTable(names, response);
    document.getElementById('registries').innerHTML = division.outerHTML
};

//создание, обновление таблицы проверки на полиграфе
function poligrafUpd(resps) {
    let names = ['ID', 'Тематика', 'Результат', 'Полиграфолог', 'Дата проверки'];
    let response = []
    for (let resp of resps) {
        response.push([resp['id'], resp['theme'], resp['results'], resp['officer'], resp['deadline']]);
    };
    let division = constructTable(names, response);
    document.getElementById('poligrafs').innerHTML = division.outerHTML
};

//создание, обновление таблицы расследований
function investigationUpd(resps) {
    let names = ['ID', 'Тематика', 'Информация', 'Дата проверки'];
    let response = []
    for (let resp of resps) {
        response.push([resp['id'], resp['theme'], resp['info'], resp['deadline']]);
    };
    let division = constructTable(names, response);
    document.getElementById('investigations').innerHTML = division.outerHTML
};

//создание, обновление таблицы запросов
function inquiryUpd(resps) {
    let names = ['ID', 'Информация', 'Иннициатор', 'Источник', 'Дата запроса'];
    let response = []
    for (let resp of resps) {
        response.push([resp['id'], resp['info'], resp['initiator'], resp['source'], resp['deadline']]);
    };
    let division = constructTable(names, response);
    document.getElementById('inquiries').innerHTML = division.outerHTML
};

//horizontal table for candidates data
function constructTable(names, response) {
    if (response.length) {
        let division = document.createElement("div");
        for (let j in response) {
            let div = document.createElement("div");
            let tbl = document.createElement("table");
            tbl.setAttribute("class", "table");
            let tblBody = document.createElement("tbody")
            for (let i in names) {
                let cell1 = constructElement(["td", [["width", "25%"]], names[i]]);
                let cell2 = document.createElement("td");
                cell2.innerHTML = response[j][i];
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

//update status
function updateStatus(candId) {
    fetch("/resume/update/" + candidates[0]['id'])
        .then(response => response.json())
        .then(data => {
            let resp = data["data"];
            message = resp[1];
            resumeUpd(resp[0], resp[2]);
            if (resp[1] == "Статус обновлен") {
                let divAlert = constructElement(["div", [["class", "alert alert-success"], ["role", "alert"]], resp[1]]);
                document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
            } else {
                let divAlert = constructElement(["div", [["class", "alert alert-warning"], ["role", "alert"]], resp[1]]);
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
                mainPage('/index/', 'alert alert-success', resp['message'])
            } else if (resp['message'] == "Отправка не удалась. Попробуйте позднее") {
                mainPage('/index/', 'alert alert-warning', resp['message'])
            } else {
                mainPage('/index/', 'alert alert-warning', resp['message'])
            };
        });
};

//edit resume
function editResume(candId) {
    fetch("/resume/edit/" + candId)
        .then(response => response.json())
        .then(data => {
            let resp = data["data"][0];
            createResume(resp)
        });
};

//редактировать проверку
function editCheck(candId) {
    fetch("/check/edit/" + candId)
        .then(response => response.json())
        .then(data => {
            let resp = data["data"];
            if (resp[-1]["meessage"] == "Проверку с текущим статусом нельзя отредактировать") {
                let divAlert = constructElement(["div", [["class", "alert alert-warning"], ["role", "alert"]], "Проверку с текущим статусом нельзя отредактировать"]);
                document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
            } else {
                checkForm(candId, resp)
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
                let divAlert = constructElement(["div", [["class", "alert alert-warning"], ["role", "alert"]], resp['message']]);
                document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
                openProfile(candId)
            });
    };
};


/*implementation code for add candidate's check
also edit check functioanality*/

function checkForm(candId, value = null) {
    const loginHead = document.createElement('h5');
    loginHead.innerHTML = "Создать проверку";
    document.getElementById('appHeaders').innerHTML = loginHead.outerHTML;
    const divResume = constructElement(["div", [["class", "py-1"]]]);
    document.getElementById('appContent').innerHTML = divResume.outerHTML;

    let divForm = constructElement(["div", [["class", "py-3"]]]);
    let formCheck = constructElement(["form", [["class", "form-check"], ["id", "checkForm"], ["onsubmit", "return false;"]]]);
    divForm.appendChild(formCheck);
    let checkLabels = ["Проверка по кадровому учету", "Проверка по месту работы", "Проверка документов", "Проверка паспорта", "Проверка задолженностей", "Проверка банкротства", "Проверка кредитной истории", "Проверка по решениям судов", "Проверка аффилированности", "Проверка списка террористов", "Проверка учетам МВД", "Проверка по открытым источникам", "Проверка Кронос", "Проверка Крос", "Дополнительная информация"]
    let checkNames = ["employee", "workplace", "document", "inn", "debt", "bankruptcy", "bki", "courts", "affiliation", "terrorist", "mvd", "internet", "cronos", "cros", "addition"]

    //open new form or prefilled form for editing 
    let values = Object.keys(value)
    for (let i in checkLabels) {
        let checkDiv = constructElement(["div", [["class", "row mb-3"]]]);
        formCheck.appendChild(checkDiv);
        let checkLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], ["for", "checkForm"]]]);
        checkLbl.innerHTML = checkLabels[i];
        checkDiv.appendChild(checkLbl);
        let inpDiv = constructElement(["div", [["class", "col-sm-8"]]]);
        checkDiv.appendChild(inpDiv);
        if (value == null) {
            let checkInp = constructElement(["textarea", [["class", "form-control"], ["rows", "3"], ["name", checkNames[i]]]]);
            inpDiv.appendChild(checkInp)
        } else {
            let checkInp = constructElement(["textarea", [["class", "form-control"], ["rows", "3"], ["name", checkNames[i]], ["value", values[i]]]]);
            inpDiv.appendChild(checkInp)
        };
    };
    //pfo
    let pfoDiv1 = constructElement(["div", [["class", "row mb-3"]]]);
    formCheck.appendChild(pfoDiv1);
    let pfoDiv2 = constructElement(["div", [["class", "col-sm-3 offset-sm-2"]]]);
    pfoDiv1.appendChild(pfoDiv2);
    let pfoDiv3 = constructElement(["div", [["class", "form-check"]]]);
    pfoDiv2.appendChild(pfoDiv3);
    let hiddden = constructElement(["input", [["class", "form-check-input"], ["type", "hidden"], ["value", "False"], ["name", "pfo"]]]);
    pfoDiv3.appendChild(hiddden);
    let pfoInp = constructElement(["input", [["class", "form-check-input"], ["type", "checkbox"], ["value", "True"], ["name", "pfo"]]]);
    pfoDiv3.appendChild(pfoInp);
    let pfoLbl = constructElement(["label", [["for", "checkForm"]]]);
    pfoLbl.innerHTML = "Полиграф";
    pfoDiv3.appendChild(pfoLbl);
    //conclusion
    let viewDiv = constructElement(["div", [["class", "row mb-3"]]]);
    formCheck.appendChild(viewDiv);
    let viewLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], ["for", "checkForm"]]]);
    viewLbl.innerHTML = "Результат";
    viewDiv.appendChild(viewLbl);
    let inpDiv = constructElement(["div", [["class", "col-sm-8"]]]);
    viewDiv.appendChild(inpDiv);
    let namesCheck = ['Без замечаний', 'С комментарием', 'Негатив', 'Отменено', 'Сохранено'];
    let selectInp = constructElement(["select", [["class", "form-select mb-3"], ["name", "conclusion"]]]);
    for (let [index, value] of namesCheck.entries()) {
        let option = constructElement(["option", [["class", "form-select mb-3"], ["value", index]]]);
        option.innerHTML = value;
        selectInp.appendChild(option);
    };
    inpDiv.appendChild(selectInp);
    //final
    let inpLabels = ["Комментарий", "Дата проверки"]
    let inpNames = ["comments", "deadline"]
    for (let i in inpLabels) {
        let lblDiv = constructElement(["div", [["class", "row mb-3"]]]);
        formCheck.appendChild(lblDiv);
        let checkLbl = constructElement(["label", [["class", "form-label col-sm-2 col-form-label"], ["for", "addressForm"]]]);
        checkLbl.innerHTML = inpLabels[i];
        lblDiv.appendChild(checkLbl);
        let inpDiv = constructElement(["div", [["class", "col-sm-8"]]]);
        lblDiv.appendChild(inpDiv);
        if (inpNames[i] == "deadline") {
            let chckInp = constructElement(["input", [["class", "form-control"], ["type", "date"], ["name", inpNames[i]]]]);
            inpDiv.appendChild(chckInp);
        } else {
            let chckInp = constructElement(["input", [["class", "form-control"], ["type", "text"], ["name", inpNames[i]]]]);
            inpDiv.appendChild(chckInp);
        };
    };
    //submit button
    let submitBtn = constructElement(["button", [["class", "btn btn-primary"], ["type", "submit"], ["for", "checkForm"], ["id", "submitCheck"]], "Сохранить"]);
    formCheck.appendChild(submitBtn);

    // прослушиваем событие от нажатии кнопки на форме загрузки данных
    document.getElementById("submitCheck").addEventListener("click", function () {
        let form = document.getElementById("checkForm");
        let formData = new FormData(form);
        fetch(`/check/${candId}`, {
            method: "post",
            body: formData
        })
            .then(response => response.json())
            .then(response => {
                let resp = response["data"];
                let message = resp['message'];
                mainPage("/index/", 'alert alert-success', message);
            });
    });
};
