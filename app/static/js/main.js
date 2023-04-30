'use strict';

//запуск и структуура приложения
class mainApplication {
    appContainer = document.getElementById('App');
    constructor(){
        for (let id of ['appMessage', 'appHeader', 'appContent']) {
            let division = document.createElement("div");
            division.setAttribute("class", "container py-3");
            division.setAttribute("id", id);
            this.appContainer.appendChild(division);
        };
        //проверка авторизации, если нет, то редирект на страницу логина
        (async () => {
            let response = await fetch('/login');
            let result = await response.json();
            if (result['user'] != "None") {
                mainPage('/index/main/')
            } else {
                userLogin()
            };
        })();
    }
    createDivId(arrayDivId, destID){
        let pageContainer = document.createElement("div");
        for (let id of arrayDivId){
            let division = document.createElement("div");
            division.setAttribute("class", "container py-3");
            division.setAttribute("id", id);
            pageContainer.appendChild(division);
        };
        document.getElementById(destID).innerHTML = pageContainer.outerHTML;
    }
    createMessage(info, text) {
    	let alert = document.createElement("div");
        alert.setAttribute("class", info);
        alert.setAttribute("role", "alert");
        alert.innerHTML = text;
    document.getElementById('appMessage').innerHTML = alert.outerHTML;
    } 
    createHeader(text) {
    	let head = document.createElement("h5")
    	head.innerHTML = text;
        document.getElementById("appHeader").innerHTML = head.outerHTML;
    }
};

const appMain = new mainApplication();

//авторизация пользователя
function userLogin() {
    appMain.createMessage("alert alert-info", "Авторизуйтесь чтобы продолжить работу");
    appMain.createHeader("Вход в систему") ;
    //вставляем форму
    document.getElementById('appContent').innerHTML = formLogin;
    //добавляем скрытое поле
    const hidden = document.createElement("input");
    hidden.setAttribute("class", "form-check-input");
    hidden.setAttribute("type", "hidden");
    hidden.setAttribute("value", "");
    hidden.setAttribute("name", "remember");
    document.forms["loginFormId"].appendChild(hidden);
    //обработка события Войти
    const form = document.forms["loginFormId"];
    form.addEventListener('submit', async function submitLogin (event){
        const formData = new FormData(form);
        let response = await fetch('/login', {
            method: 'POST',
            body: formData
            });
        let result = await response.json();
        if (result['user'] == "None") {
            appMain.createMessage("alert alert-warning", "Неверный логин или пароль");
        } else {
            mainPage('/index/main/');
            this.removeEventListener('submit', submitLogin (event))
        }
    })
};

//user logout
function userLogout() {
    fetch('logout');
    userLogin()
};

async function mainPage(path, currentPage=0){
    //проверка ранее созданной структуры страницы
    if (!document.getElementById("divExtSearch")) {
        appMain.createDivId(["divExtSearch", "divTable", "divPager"], 'appContent');
        document.getElementById('divExtSearch').innerHTML = formExtSearch;
        const divPager = document.getElementById('divPager');
        divPager.innerHTML = createPager().outerHTML;
        //форма расширенного поиска
        const form = document.forms["searchExtFormId"]
        form.addEventListener('submit', function() {
            mainPage(path)
        });
        const nextPageEvent = document.getElementById("nextPage")
        nextPageEvent.addEventListener("click", function() {
            if (countPages != 0) mainPage(path, currentPage + 1);
        });
        const prevPageEvent = document.getElementById("prevPage")
        prevPageEvent.addEventListener("click", function() {
            if (currentPage != 0) mainPage(path, currentPage - 1)
        });
    };
    const form = new FormData(document.forms["searchExtFormId"]);
    let response = await fetch(path+currentPage, {
        method: "post",
        body: form
    })
    const resp = await response.json();
    //сообщение о количестве новых кандидатов
    appMain.createMessage('alert alert-info', `<a href="#" onclick=mainPage('/index/new/'); \
        return false>Новых анкет: ${resp[1].items}</a>`);
    //заголовок в зависимости от страницы
    appMain.createHeader(resp[1].title);
    //таблица
    const divTable = document.getElementById('divTable');
    divTable.innerHTML = constrVertTable(resp[0]).outerHTML;
    //состояние кнопок страниц
    const countPages = resp[1].pager;
    const nextItem = document.getElementById("nextPage");
    if (countPages == 0) nextItem.setAttribute("class", "disabled");
    const prevItem = document.getElementById("prevPage");
    if (currentPage == 0) prevItem.setAttribute("class", "disabled");
};

//переключатель страниц
function createPager(){
    const navPage = document.createElement('nav');
    const pagerUl = document.createElement("ul");
    pagerUl.setAttribute("class", "pagination justify-content-center");
    navPage.appendChild(pagerUl);
    const idPagers = ["prevPage", "nextPage"];
    const namePagers = ["Предыдущая", "Следующая"];
    for (let i = 0; i < namePagers.length; i++) {
        let pageItem = document.createElement('li');
        pageItem.setAttribute("class", "page-item"); 
        pageItem.setAttribute("id", idPagers[i]);
        pagerUl.appendChild(pageItem);
        let pageLink = document.createElement('a')
        pageLink.setAttribute("class", "page-link");
        pageLink.setAttribute("href", "#");
        pageLink.innerHTML = namePagers[i];
        pageItem.appendChild(pageLink);
    };
    return navPage
};

//вертикальная таблица со списком кандидатов
function constrVertTable(candidates) {
    const table = document.createElement("table");
    table.setAttribute("class", "table table-hover table-responsive align-middle py-1");
    const thead = document.createElement('thead');
    table.appendChild(thead);
    const tbody = document.createElement('tbody');
    table.appendChild(tbody);
    const tr = document.createElement('tr');
    const tableHeader = ["#", "Регион", "Фамилия Имя Отчество", "Дата рождения", "Статус", "Дата"];
    let tabbleAttrs = ["5%", "15%", "30%", "15%", "15%", "15%"];
    for (let i = 0; i < tableHeader.length; i++) {
        let th = document.createElement('th');
        th.setAttribute("width", tabbleAttrs[i]);
        th.innerHTML = tableHeader[i];
        tr.appendChild(th);
        thead.appendChild(tr);
    };
    for (let candidate of candidates) {
        let tr = document.createElement('tr');
        tr.setAttribute("height", "50px");
        //
        for (let val of Object.values(candidate)) {
            let td = document.createElement('td');
            if (val == candidate['fullname']) {
                td.innerHTML = `<a href="#" onclick=openProfile(${candidate['id']})>${val}</a>`;
            } else if (val == candidate['deadline'] || val == candidate['birthday']) {
                let date = new Date(Date.parse(val));
                td.innerHTML =  date.toLocaleDateString('ru-RU')
            } else {
                td.innerHTML = val
            };
            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    };
    return table
}

//страница для заполнения/редактирования анкеты
async function createResume(candId=null) {
    appMain.createMessage('alert alert-info',
        "Заполните обязательные поля, либо загрузите файл");
    appMain.createHeader("Создать/изменить анкету")
    const appContent = document.createElement('div');
    const divformUpload = document.createElement('div');
    divformUpload.innerHTML = formUpload;
    appContent.appendChild(divformUpload);
    //
    const divformResume = document.createElement('div');
    divformResume.innerHTML = formResume;
    appContent.appendChild(divformResume);
    document.getElementById('appContent').innerHTML = appContent.outerHTML;
    //
    if (candId != null) {
        let response = await fetch("/profile/resume/" + candId);
        let resumeId = document.forms["resumeFormId"];
        let tagName = resumeId.getElementsByTagName("input");
        let resps = await response.json();
        for (let i = 0; i < tagName.length; i++){
            tagName[i].setAttribute("value", Object.values(resps)[i])
        }
    };
    const form = document.forms["resumeFormId"];
    form.addEventListener('submit', async function resumeForm(event){
        updateData(form, `profile/resume/${anketaIds[i]}`, candId, "post", openProfile)
        this.removeEventListener('submit', resumeForm(event));
    });
};

//добавление данных в анкету
function addToAnketa(candId){
    appMain.createMessage('alert alert-info', "Заполните обязательные поля в нужной форме");
    appMain.createHeader("Добавление информацию в анкету");
    //подзаголовки и структура
    const resumeSubNames = ['Должности', 'Документы', 'Адреса', 'Контакты', 'Работа', 'Связи'];
    const anketaIds = ['staffId', 'docId', 'addressId', 'contactId', 'workId','relationId']
    appMain.createDivId[anketaIds, 'profileContentId']
    //формы для добавления данных
    const anketaForms = [formStaff, formDocument, formAddress, formContact, formWorkplace, formRelation];
    for (let i = 0; i < anketaIds.length; i++) {
        let anketaIdsDivs = document.getElementById(anketaIds);
        //вставка форм
        anketaIdsDivs.innerHTML = anketaForms[i];
        //вставка подзаголовков
        let targetHeader = document.createElement("h6");
        targetHeader.innerHTML = resumeSubNames[i];
        anketaIdsDivs.insertBefore(targetHeader, anketaIdsDivs.firstElementChild);
        //вставка обработчиков
        let addListener = document.forms[i]
        addListener.addEventListener('submit', function (event){
            updateData(document.forms[i]['id'], `profile/update/${anketaIds[i]}`, candId, "put")
        });
    };
};

//открываем страницу профиля кандидата
function openProfile(candId) {
    appMain.createHeader("Профиль кандидата/сотрудника");
    //структура страницы
    appMain.createDivId(["navDiv", "navContent", "profileContent"], "appContent");
    //переключатели вкладок
    const divNav = document.getElementById("navDiv");
    divNav.setAttribute("class", "nav nav-tabs nav-justified");
    divNav.setAttribute("role", "tablist");
    const tabsNames = ['Профиль', 'Проверки', 'Согласования', 'Полиграф', 'Расследования', 'Запросы'];
    const tabsPanes = ['profileTab', 'checkTab', 'registryTab', 'poligrafTab', 'investigateTab', 'inquiryTab'];
    const tabsActions = [openAnketa, openCheck, openRegistry, openPoligraf, openInvestigation, openInquiry];
    for (let i = 0; i < tabsNames.length; i++) {
        let navBtn = document.createElement("button");
        navBtn.setAttribute("data-bs-toggle", "tab");
        navBtn.setAttribute("data-bs-target", "#"+tabsPanes[i]);
        navBtn.setAttribute("type", "button");
        navBtn.setAttribute("role", "tab");
        navBtn.setAttribute("class", "nav-link");
        if (i == 0) navBtn.setAttribute("class", "nav-link active")
        navBtn.innerHTML = tabsNames[i];
        divNav.appendChild(navBtn)
    };
    //вкладки и содержание
    const navContent = document.getElementById("navContent");
    navContent.setAttribute("class", "tab-content");
    for (let i = 0; i < tabsPanes.length; i++){
        let divPane = document.createElement("div");
        divPane.setAttribute("class", "tab-pane fade show py-1");
        divPane.setAttribute("role", "tabpanel");
        divPane.setAttribute("id", tabsPanes[i]);
        if (i == 0) divPane.setAttribute("class", "tab-pane fade show active py-1");
        navContent.appendChild(divPane);
        let contentTab = document.createElement("div");
        contentTab.setAttribute("id", tabsPanes[i]+"Id");
        divPane.appendChild(contentTab);
        tabsActions[i](candId)
    };
};

//открыть анкету
async function openAnketa(candId){
    let response = await fetch(`/profile/anketa/${candId}`)
    appMain.createDivId(["anketaId", "buttonGroupId"], "profileTabId");
    const resumeSubDivNames = ['Резюме', 'Должности', 'Документы', 'Адреса', 'Контакты', 'Работа', 'Связи'];
    const resumeSubDivIds = ['resumeId', 'staffId', 'docId', 'addressId', 'contactId', 'workId', 'relationId'];
    const labelNames = [
        ['id', 'Регион', 'Фамилия Имя Отчество', 'Изменение имени', 'Дата рождения', 
        'Место рождения', 'Гражданство', 'СНИЛС', 'ИНН', 'Образование', 
        'Дополнительная информация', 'Статус', 'Дата', 'Рекрутер', 'Внешний id'],
        ['Должность', 'Департамент'],
        ['Вид документа', 'Серия', 'Номер', 'Кем выдан', 'Дата'],
        ['Тип', 'Регион', 'Адрес'],
        ['Вид', 'Контакт'],
        ['Период', 'Организация', 'Адрес', 'Должность'],
        ['Связь', 'Полное ФИО', 'Дата рождения', 'Адрес', 'Место работы', 'Контакты'],
    ];
    appMain.createDivId(resumeSubDivIds, "anketaId");
    //группа Изменить анкету, Добавить информацию, Обновить статус, Отправить на проверку
    const groupBtnResume = document.getElementById("buttonGroupId")
    groupBtnResume.setAttribute("class", "btn-group py-2 hidden-print");
    groupBtnResume.setAttribute("role", "group");
    const grpBtnResumeAttr = {
        'Изменить  анкету': `editResume(${candId})`,
        'Добавить информацию': `addToAnketa(${candId})`,
        'Обновить статус': `updateStatus(${candId})`,
        'Отправить на проверку': `sendResume(${candId})`
    };
    for (let i = 0; i < Object.keys(grpBtnResumeAttr).length; i++){
        let updBtnResume = document.createElement("button");
        updBtnResume.setAttribute("class", "btn btn-outline-primary");
        updBtnResume.setAttribute("onclick", Object.values(grpBtnResumeAttr)[i])
        updBtnResume.innerHTML = Object.keys(grpBtnResumeAttr)[i];
        groupBtnResume.appendChild(updBtnResume)
    };
    let resps = await response.json();
    //создаем таблицы с данными анкеты и вставляем их на таблицу
    for (let i = 0; i < resps.length; i++) {
        let subSubdivs = document.getElementById(resumeSubDivIds[i])
        let targetHeader = document.createElement('h6');
        targetHeader.innerHTML = resumeSubDivNames[i];
        subSubdivs.appendChild(targetHeader);
        let divTable = constrHorizTable(labelNames[i], resps[i]);
        subSubdivs.appendChild(divTable);
    };
};


//сброс статуса анкеты на UPDATE при необходимости
async function updateStatus(candId) {
    let response = await fetch("/resume/status/" + candId);
    let resp = await response.json();
    openProfile(candId);
    appMain.createMessage("alert alert-info", resp['message']);
};

//отправка анкеты на автопроверку
async function sendResume(candId) {
    let response = await fetch("/resume/send/" + candId);
    let resp = await response.json();
    appMain.createMessage("alert alert-info", resp['message']);
    mainPage('/index/main/')
};

//открыть проверки
async function openCheck(candId){
    let response = await fetch(`/check/${candId}`)
    const divPage = document.getElementById("checkTabId");
    //точка для подключения формы проверки
    const checkDiv = document.createElement("div");
    checkDiv.setAttribute("id", "formCheckId");
    divPage.appendChild(checkDiv)
    //точка для подключения результатов проверки
    const divCheck = document.createElement("div");
    divCheck.setAttribute("id", "checkId");
    checkDiv.appendChild(divCheck);
    //группа кнопок
    const groupBtnCheck = document.createElement("div");
    groupBtnCheck.setAttribute("class", "btn-group hidden-print");
    groupBtnCheck.setAttribute("role", "group");
    checkDiv.appendChild(groupBtnCheck);
    const buttonLabels = ['Добавить проверку', 'Редактировать проверку', 'Удалить последнюю проверку'];
    const actionButtons = ["checkBtn", "editBtn", 'deleteBtn'];
    for (let i = 0; i < actionButtons.length; i++){
        let addBtn = document.createElement("a");
        addBtn.setAttribute("class", "btn btn-outline-info");
        addBtn.setAttribute("type", "button");
        addBtn.setAttribute("id", actionButtons[i]);
        addBtn.innerHTML = buttonLabels[i];
        groupBtnCheck.appendChild(addBtn)
    };
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
    let resps = await response.json();
    for (let i = 0; i < resps.length; i++) {
        const divTable = constrHorizTable(labelNames[i], resps[i]);
        const divId = document.getElementById("checkId");
        divId.innerHTML = divTable.outerHTML;
    };
    //прослушиваем событие на кнопке 'Добавить проверку'
    const addBtnListener = document.getElementById("checkBtn")
    addBtnListener.addEventListener('click', function (event){
        document.getElementById("formCheckId").innerHTML = formCheck;
    });
    //прослушиваем событие на кнопке 'Удалить проверку'
    const delBtnListener = document.getElementById("deleteBtn")
    delBtnListener.addEventListener('click', async function (event){
        if (confirm("Вы действительно хотите удалить проверку?")) {
            let response = await fetch("/check/delete/"+candId);
            let resp = await response.json();
            appMain.createMessage("alert alert-warning", resp['message']);
            openCheck(candId)
        };
    });
    //прослушиваем событие на кнопке 'Редактировать проверку'
    const editBtnListener = document.getElementById("editBtn")
    editBtnListener.addEventListener('click', async function (event){
        document.getElementById("formCheckId").innerHTML = formCheck;
        let response = await fetch("/profile/check/" + candId);
        let resps = await response.json();
        // удаляем неиспользуемые значения для подстановки в форму
        for (let key of Object.keys(resps[0])) {
            if ([
                'id', 'autostatus', 'path', 'pfo', 'comments', 
                'conclusion', 'deadline', 'officer', 'cand_id'
            ].includes(key)){
                delete resps[0][key];
            }
        };  //вставляем значения в текстовые поля
        let checkId = document.getElementById("checkFormId");
        let tagName = checkId.getElementsByTagName("textarea");
        for (let i = 0; i < tagName.length; i++){
            tagName[i].value = Object.values(resps[0])[i]
        };
    });
    //прослушиваем событие на кнопке  Принять
    const submitdBtnListener = document.getElementById("checkFormId")
    submitdBtnListener.addEventListener('submit', function formCheck(event){
        updateData("checkFormId", "check", candId, 'post', openCheck)
        this.removeEventListener('submit', formCheck(event))
    });
};

//открыть согласование
async function openRegistry (candId){
    let response = await fetch(`/registry/${candId}`)
    const registryDiv = document.getElementById("registryTabId");
    //
    const divRegistry = document.createElement("div");
    divRegistry.setAttribute("id", "registryId");
    registryDiv.appendChild(divRegistry);
    //
    const addBtnReg = document.createElement("a");
    addBtnReg.setAttribute("class", "btn btn-outline-info hidden-print");
    addBtnReg.setAttribute("type", "button");
    addBtnReg.setAttribute("id", "addBtnReg");
    addBtnReg.innerHTML = 'Открыть согласование';
    registryDiv.appendChild(addBtnReg)
    const labelNames = ['ID', 'Комментарий', 'Решение', 'Дата', 'Согласующий'];
    //прослушиваем событие на кнопке 'Открыть согласование'
    const addBtnListener = document.getElementById("addBtnReg")
    addBtnListener.addEventListener('click', function addReg (event){
        document.getElementById("registryTabId").innerHTML = formRegistry;
        this.removeEventListener('click', addReg(event));
    });
    //прослушиваем событие на кнопке  Принять
    const submitdBtnListener = document.forms["registryFormId"];
    submitdBtnListener.addEventListener('submit', function formRegistry(event){
        updateData("registryFormId", "registr", candId, openRegistry)
        this.removeEventListener('click', formRegistry(event));
    });
    let resps = await response.json();
    for (let i = 0; i < resps.length; i++) {
        const divTable = constrHorizTable(labelNames, resps[i]);
        const divId = document.getElementById('registryId');
        divId.innerHTML = divTable.outerHTML;
    };
};

//вкладка полиграфа
async function openPoligraf(candId) {
    let response = await fetch(`/poligraf/${candId}`)
    const poligrafDiv = document.getElementById("poligrafTabId");
    //
    const divpoligraf = document.createElement("div");
    divpoligraf.setAttribute("id", "poligrafId");
    poligrafDiv.appendChild(divpoligraf);
    //
    const addBtnReg = document.createElement("a");
    addBtnReg.setAttribute("class", "btn btn-outline-info hidden-print");
    addBtnReg.setAttribute("type", "button");
    addBtnReg.setAttribute("id", "addBtnReg");
    addBtnReg.innerHTML = 'Открыть согласование';
    poligrafDiv.appendChild(addBtnReg)
    const labelNames = ['ID', 'Тематика', 'Результат', 'Полиграфолог', 'Дата проверки'];
    //прослушиваем событие на кнопке 'Открыть согласование'
    const addBtnListener = document.getElementById("addBtnReg")
    addBtnListener.addEventListener('click', function addReg (event){
        document.getElementById("poligrafTabId").innerHTML = formpoligraf;
        this.removeEventListener('click', addReg(event));
    });
    //прослушиваем событие на кнопке  Принять
    const submitdBtnListener = document.forms["poligrafFormId"];
    submitdBtnListener.addEventListener('submit', function formPoligraf(event){
        updateData("poligrafFormId", "registr", candId, openPoligraf)
        this.removeEventListener('click', formPoligraf(event));
    });
    let resps = await response.json();
    for (let i = 0; i < resps.length; i++) {
        const divTable = constrHorizTable(labelNames, resps[i]);
        const divId = document.getElementById('poligrafId');
        divId.innerHTML = divTable.outerHTML;
    };
};

//open investigation page
async function openInvestigation(candId) {
    let response = await fetch(`/poligraf/${candId}`)
    const investigationDiv = document.getElementById("investigationTabId");
    //
    const divinvestigation = document.createElement("div");
    divinvestigation.setAttribute("id", "investigationId");
    investigationDiv.appendChild(divinvestigation);
    //
    const addBtnReg = document.createElement("a");
    addBtnReg.setAttribute("class", "btn btn-outline-info hidden-print");
    addBtnReg.setAttribute("type", "button");
    addBtnReg.setAttribute("id", "addBtnReg");
    addBtnReg.innerHTML = 'Открыть согласование';
    investigationDiv.appendChild(addBtnReg)
    const labelNames = ['ID', 'Тематика', 'Информация', 'Дата проверки'];
    //прослушиваем событие на кнопке 'Открыть согласование'
    const addBtnListener = document.getElementById("addBtnReg")
    addBtnListener.addEventListener('click', function addReg (event){
        document.getElementById("investigationTabId").innerHTML = forminvestigation;
        this.removeEventListener('click', addReg(event));
    });
    //прослушиваем событие на кнопке  Принять
    const submitdBtnListener = document.forms["investigationFormId"];
    submitdBtnListener.addEventListener('submit', function formInvestigation(event){
        updateData("investigationFormId", "registr", candId, openInvestigation)
        this.removeEventListener('click', formInvestigation(event));
    });
    let resps = await response.json();
    for (let i = 0; i < resps.length; i++) {
        const divTable = constrHorizTable(labelNames, resps[i]);
        const divId = document.getElementById('investigationId');
        divId.innerHTML = divTable.outerHTML;
    };
};

//открываем страницу для просмотра/добавления запросов
async function openInquiry(candId) {
    let response = await fetch(`/poligraf/${candId}`)
    const inquiryDiv = document.getElementById("inquiryTabId");
    //
    const divinquiry = document.createElement("div");
    divinquiry.setAttribute("id", "inquiryId");
    inquiryDiv.appendChild(divinquiry);
    //
    const addBtnReg = document.createElement("a");
    addBtnReg.setAttribute("class", "btn btn-outline-info hidden-print");
    addBtnReg.setAttribute("type", "button");
    addBtnReg.setAttribute("id", "addBtnReg");
    addBtnReg.innerHTML = 'Открыть согласование';
    inquiryDiv.appendChild(addBtnReg)
    const labelNames = ['ID', 'Информация', 'Иннициатор', 'Источник', 'Дата запроса'];
    //прослушиваем событие на кнопке 'Открыть согласование'
    const addBtnListener = document.getElementById("addBtnReg")
    addBtnListener.addEventListener('click', function addReg (event){
        document.getElementById("inquiryTabId").innerHTML = forminquiry;
        this.removeEventListener('click', addReg(event));
    });
    //прослушиваем событие на кнопке  Принять
    const submitdBtnListener = document.forms["inquiryFormId"];
    submitdBtnListener.addEventListener('submit', function formInquiry(event){
        updateData("inquiryFormId", "registr", candId, openInquiry)
        this.removeEventListener('click', formInquiry(event));
    });
    let resps = await response.json();
    for (let i = 0; i < resps.length; i++) {
        const divTable = constrHorizTable(labelNames, resps[i]);
        const divId = document.getElementById('inquiryId');
        divId.innerHTML = divTable.outerHTML;
    };
};

//create table with candidate profile
function constrHorizTable(names, response) {
    if (response.length) {
        let division = document.createElement("div");
        //
        for (let j = 0; j < response.length; j++) {
            let div = document.createElement("div");
            let tbl = document.createElement("table");
            tbl.setAttribute("class", "table");
            let tblBody = document.createElement("tbody")
            //
            for (let i = 0; i < names.length; i++) {
                let cell1 = document.createElement("td");
                cell1.setAttribute("width", "25%");
                cell1.innerHTML = names[i];
                let cell2 = document.createElement("td");
                //конвертация даты в локальный формат
                if (Object.keys(response[j])[i] == 'deadline' || Object.keys(response[j])[i] == 'birthday') {
                    let date = new Date(Date.parse(Object.values(response[j])[i]));
                    cell2.innerHTML =  date.toLocaleDateString('ru-RU')
                } else {
                cell2.innerHTML = Object.values(response[j])[i]
                };
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
async function updateData(formId, url, candId, rest, action=null){
    const form = document.getElementById(formId)
    const formData = new FormData(form);
    let response = await fetch (`/${url}/${candId}`, {
        method: rest,
        body: formData
    })
    let resp = await response.json();
    appMain.createMessage("alert alert-primary", resp['message']);
    if (action != null) action(candId)
};

//открываем страницу стат информации
async function createInfo(){
    //были элементы созданы ранее или нет
    if (!document.getElementById("infoFormId")) {
        appMain.createDivId(["divCandTable", "divPfoTable", "divForm"], 'appContent');
        document.getElementById("divForm").innerHTML = formInfo;
    }
    const form = document.forms["infoFormId"];
    const formData = new FormData(form);
    const response = await fetch('/info', {
        method: "post",
        body: formData
    });
    let resps = await response.json();
    appMain.createHeader(resps['title']);
    document.getElementById('appMessage').innerHTML = '';
    //присоединяем стат таблицы и форму к элементам приложения по ID
    const divCandTable = document.getElementById("divCandTable");
    divCandTable.innerHTML = createStatData(resps["candidates"], "Статистика по кандидатам").outerHTML;
    const divPfoTable = document.getElementById("divPfoTable");
    divPfoTable.innerHTML = createStatData(resps["poligraf"], "Статистика по ПФО").outerHTML;
    //прослушиваем событие на кнопке Принять
    form.addEventListener('submit', function submitData (event){
        createInfo();
        this.removeEventListener('submit', submitData)
    });
};

//создаем таблицу со статданными
function createStatData (stats, caption){
    const table = document.createElement("table");
    table.setAttribute("class", "table table-hover table-responsive align-middle");
    table.createCaption();
    table.innerHTML = caption;
    const thead = document.createElement('thead');
    table.appendChild(thead);
    const tbody = document.createElement('tbody');
    table.appendChild(tbody);
    const tr = document.createElement('tr');
    for (let headline of ["Решение", "Количество"]) {
        let th = document.createElement('th');
        th.innerHTML = headline;
        tr.appendChild(th);
        thead.appendChild(tr);
    };
    for (let stat of stats) {
        let tr = document.createElement('tr');
        tr.setAttribute("height", "50px");
        for (let val of Object.entries(stat)) {
            let td = document.createElement('td');
            td.setAttribute("width", "50%")
            td.innerHTML = val[0]
            tr.appendChild(td);
            let td1 = document.createElement('td');
            td.setAttribute("width", "50%")
            td1.innerHTML = val[1]
            tr.appendChild(td1);
        }
        tbody.appendChild(tr);
    };
    return table
};