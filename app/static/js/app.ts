'use strict';

let formLogin: string;
let formUpload: string;
let formResume: string;
let formStaff: string;
let formDocument: string;
let formAddress: string;
let formContact: string;
let formWorkplace: string;
let formRelation: string;
let formCheck: string;
let formRegistry: string;
let formPoligraf: string;
let formInvestigation: string;
let formInquiry: string;
let formInfo: string;
let formExtSearch: string;

//запуск и структура приложения
class mainApplication {
    appContainer = document.getElementById('App') as HTMLElement;
    
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

    createDivId(arrayDivId: Array<string>, destID: string){
        let pageContainer = document.createElement("div");
        for (let id of arrayDivId){
            let division = document.createElement("div");
            division.setAttribute("class", "container py-3");
            division.setAttribute("id", id);
            pageContainer.appendChild(division);
        };
        let destDiv = document.getElementById(destID) as HTMLElement;
        destDiv.innerHTML = pageContainer.outerHTML;    
    };

    createMessage(info: string, text: string) {
    	let alert = document.createElement("div");
        alert.setAttribute("class", info);
        alert.setAttribute("role", "alert");
        alert.innerHTML = text;
        let destDiv = document.getElementById("appMessage") as HTMLElement;
        destDiv.innerHTML = alert.outerHTML; 
    };

    createHeader(text: string) {
    	let head = document.createElement("h5")
    	head.innerHTML = text;
        let destDiv = document.getElementById("appHeader") as HTMLElement;
        destDiv.innerHTML = head.outerHTML; 
    };
    
    createTab(candId: number, resps: any, tabId: string, contentID: string, buttonId: string, 
        buttonLabel: string, labelNames: Array<string>, formWTF: string, formId: string, path: string) {
        //
        const tabDiv = document.getElementById(tabId) as HTMLElement;
        const divTab = document.createElement("div");
        divTab.setAttribute("id", contentID);
        tabDiv.appendChild(divTab);
        //
        const addButton = document.createElement("a");
        addButton.setAttribute("class", "btn btn-outline-info hidden-print");
        addButton.setAttribute("type", "button");
        addButton.setAttribute("id", buttonId);
        addButton.innerHTML = buttonLabel;
        tabDiv.appendChild(addButton);
        //прослушиваем событие на кнопке 'Добавить...'
        const addBtnListener = document.getElementById(buttonId) as HTMLElement;
        addBtnListener.addEventListener('click', function addForm(event){
            let destId = document.getElementById(tabId) as HTMLElement;
            destId.innerHTML = formWTF;
            this.removeEventListener('click', addForm);
            //прослушиваем событие на кнопке  Принять
            const form = document.forms.namedItem(formId) as HTMLFormElement;
            form.addEventListener('submit', async function formSubmit(event: any){
                const formData = new FormData(form);
                let response = await fetch(`/${path}/${candId}`, {
                    method: "post",
                    body: formData
                })
                let resp = await response.json();
                appMain.createMessage("alert alert-primary", resp['message']);
                openProfile(candId)
                form.removeEventListener('click', formSubmit);
            });
        });
        const divId = document.getElementById(contentID) as HTMLElement;
        divId.innerHTML = createProfileTable(labelNames, resps).outerHTML;
    };
};

const appMain = new mainApplication();

//авторизация пользователя
function userLogin() {
    appMain.createMessage("alert alert-info", "Авторизуйтесь чтобы продолжить работу");
    appMain.createHeader("Вход в систему") ;
    //вставляем форму
    const destID = document.getElementById('appContent') as HTMLElement;
    destID.innerHTML = formLogin;
    //добавляем скрытое поле
    const hidden = document.createElement("input");
    hidden.setAttribute("class", "form-check-input");
    hidden.setAttribute("type", "hidden");
    hidden.setAttribute("value", "");
    hidden.setAttribute("name", "remember");
    const loginFormId = document.forms.namedItem("loginFormId") as HTMLFormElement;
    loginFormId.appendChild(hidden);
    //обработка события Войти
    const form = document.forms.namedItem("loginFormId") as HTMLFormElement;
    form.addEventListener('submit', async function submitLogin(event: any){
        const formData = new FormData(form);
        let response = await fetch('/login', {
            method: 'POST',
            body: formData
            });
        let result = await response.json();
        if (result['user'] == "None") {
            appMain.createMessage("alert alert-warning", "Неверный логин или пароль");
        } else {
            this.removeEventListener('submit', submitLogin)
            mainPage('/index/main/');
        }
    })
};

//user logout
function userLogout() {
    fetch('logout');
    userLogin()
};

async function mainPage(path: string, currentPage=0){
    //проверка ранее созданной структуры страницы
    if (!document.getElementById("divExtSearch")) {
        appMain.createDivId(["divExtSearch", "divTable", "divPager"], 'appContent');
        //форма поиска
        let destID = document.getElementById('divExtSearch') as HTMLElement;
        destID.innerHTML = formExtSearch;
        const form = document.forms.namedItem("searchExtFormId") as HTMLFormElement
        form.addEventListener('submit', function() {
            mainPage('/index/search/')
        });
    };
    let response
    if (path == '/index/search/') {
        const searchExtFormId = document.forms.namedItem("searchExtFormId") as HTMLFormElement;
        const form = new FormData(searchExtFormId);
        response = await fetch('/index/search/'+currentPage.toString(), {
            method: "post",
            body: form
        })
    } else {
        response = await fetch(path+currentPage.toString())
    };
    const resp = await response.json();
    //сообщение о количестве новых кандидатов
    appMain.createMessage('alert alert-info', `<a href="#" onclick=mainPage('/index/new/'); \
        return false>Новых анкет: ${resp[1].items}</a>`);
    //заголовок в зависимости от страницы
    appMain.createHeader(resp[1].title);
    //таблица constrVertTable(resp[0])
    const divTable = document.getElementById('divTable') as HTMLElement;
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
    const candidates: Array<Object> = resp[0];
    for (let cand of candidates) {
        let tr = document.createElement('tr');
        tr.setAttribute("height", "50px");
        //
        for (let i = 0; i <  Object.keys(cand).length; i++) {
            let td = document.createElement('td');
            if (Object.keys(cand)[i] == 'fullname') {
                td.innerHTML = `<a href="#" onclick=openProfile(${Object.values(cand)[0]})>
                                                                ${Object.values(cand)[i]}</a>`;
            } else if (Object.keys(cand)[i] == 'deadline' || Object.keys(cand)[i] == 'birthday') {
                let date = new Date(Date.parse(Object.values(cand)[i]));
                td.innerHTML =  date.toLocaleDateString('ru-RU')
            } else {
                td.innerHTML = Object.values(cand)[i]
            };
            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    };
    divTable.innerHTML = table.outerHTML;
    //переключатель страниц
    const divPager = document.getElementById('divPager') as HTMLElement;
    const navPage = document.createElement('nav');
    const pagerUl = document.createElement("ul");
    pagerUl.setAttribute("class", "pagination justify-content-center");
    navPage.appendChild(pagerUl);
    //кнопка назад
    const prevPageItem = document.createElement('li');
    prevPageItem.setAttribute("class", "page-item"); 
    prevPageItem.setAttribute("id", "prevPage");
    if (currentPage == 0) {
        prevPageItem.setAttribute("class", "disabled")
    } else {
        if (prevPageItem.hasAttribute("disabled")) {
            prevPageItem.removeAttribute("disabled")
        };
    };
    pagerUl.appendChild(prevPageItem);
    const prevPageLink = document.createElement('a')
    prevPageLink.setAttribute("class", "page-link");
    prevPageLink.setAttribute("href", "#");
    prevPageLink.innerHTML = "Предыдущая";
    prevPageItem.appendChild(prevPageLink);
    //кнопка вперед
    const nextPageItem = document.createElement('li');
    nextPageItem.setAttribute("class", "page-item"); 
    nextPageItem.setAttribute("id", "nextPage");
    if (resp[1].pager == 0) {
        nextPageItem.setAttribute("class", "disabled")
    } else {
        if (nextPageItem.hasAttribute("disabled")) {
            nextPageItem.removeAttribute("disabled")
        }
    };
    pagerUl.appendChild(nextPageItem);
    const nextPageLink = document.createElement('a')
    nextPageLink.setAttribute("class", "page-link");
    nextPageLink.setAttribute("href", "#");
    nextPageLink.innerHTML = "Следующая";
    nextPageItem.appendChild(nextPageLink);
    divPager.innerHTML = navPage.outerHTML;
    //событие кнопок страниц
    const nextPage = document.getElementById('nextPage') as HTMLElement;
    nextPage.addEventListener("click", function nextPage() {
        if (resp[1].pager != 0) {
            mainPage(path, currentPage + 1)
        } else {
            mainPage(path, currentPage)
        }
        this.removeEventListener('click', nextPage);
    });
    const prevPage = document.getElementById('prevPage') as HTMLElement;
    prevPage.addEventListener("click", function prevPage() {
        if (currentPage != 0) {
            mainPage(path, currentPage - 1)
        } else {
            mainPage(path, currentPage)
        }
        this.removeEventListener('click', prevPage);
    });    
};

//страница для заполнения/редактирования анкеты
function createResume(anketa: Object) {
    appMain.createMessage('alert alert-info', "Заполните обязательные поля, либо загрузите файл");
    appMain.createHeader("Создать/изменить анкету")
    appMain.createDivId(["divformUpload", "divformResume"], 'appContent');
    const divformUpload = document.getElementById("divformUpload") as HTMLDivElement;
    divformUpload.innerHTML = formUpload;
    const divformResume = document.getElementById("divformResume") as HTMLDivElement;
    divformResume.innerHTML = formResume;
    //если передана анкета для редактирования, выводим занчения в полях для заполнения
    if (anketa) {
        let resumeId = document.forms.namedItem("resumeFormId") as HTMLFormElement;
        let tagName = resumeId.getElementsByTagName("input");
        
        let anketaFiltred = []  //фильтруем неиспользуемые значения для подстановки в форму
        for (let i = 0; i < Object.keys(anketa).length; i++) {
            if (!['id', 'region', 'status', 'deadline', 'recruiter',
                'request_id'].includes((Object.keys(anketa)[i]))) {
                    anketaFiltred.push(Object.values(anketa)[i]);
            };
        };
        for (let i = 0; i < anketaFiltred.length; i++) {
            tagName[i].setAttribute("value", anketaFiltred[i]);
        };
    };
    const form = document.forms.namedItem("resumeFormId") as HTMLFormElement;
    form.addEventListener('submit', async function resumeForm(event: any){
        form.removeEventListener('submit', resumeForm);
        const formData = new FormData(form);
        let response = await fetch ("/resume/create", {
            method: "post",
            body: formData
        });     //отправка резюме в БД
        let resp = await response.json();
        appMain.createMessage("alert alert-primary", resp['message']);
        openProfile(resp['cand_id'])
        });
};

//открываем страницу профиля кандидата
async function openProfile(candId: number) {
    let response = await fetch(`/profile/${candId}`)
    //структура страницы
    appMain.createDivId(["navDiv", "navContent"], "appContent");
    //переключатели вкладок
    const divNav = document.getElementById("navDiv") as HTMLElement;
    divNav.setAttribute("class", "nav nav-tabs nav-justified");
    divNav.setAttribute("role", "tablist");
    const tabsNames = ['Профиль', 'Проверки', 'Согласования', 'Полиграф', 'Расследования', 'Запросы'];
    const tabsPanes = ['profileTab', 'checkTab', 'registryTab', 'poligrafTab', 'investigationTab', 'inquiryTab'];
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
    let resps = await response.json();
    //вкладки и содержание
    const navContent = document.getElementById("navContent") as HTMLElement;
    navContent.setAttribute("class", "tab-content");
    for (let i = 0; i < tabsPanes.length; i++){
        let divPane = document.createElement("div");
        divPane.setAttribute("class", "tab-pane fade show py-1");
        divPane.setAttribute("role", "tabpanel");
        divPane.setAttribute("id", tabsPanes[i]);
        if (i == 0) divPane.setAttribute("class", "tab-pane fade show active py-1");
        navContent.appendChild(divPane);
        //создаем разделы для содержимого вкладок
        let contentTab = document.createElement("div");
        contentTab.setAttribute("id", tabsPanes[i]+"Id");
        contentTab.setAttribute("class", "py-3");
        divPane.appendChild(contentTab);
    };
    //вкладка анкеты
    anketaTab(candId, resps[0]);

    //вкладка проверки
    checkTab(candId, resps[1])

    //вкладка согласования
    appMain.createTab(candId, resps[2], "registryTabId", "registryId", 'addRegistryBtn', 
        'Добавить согласование', ['ID', 'Комментарий', 'Решение', 'Дата', 'Согласующий'], 
        formRegistry, 'registryFormId', "registry");

    //вкладка ПФО
    appMain.createTab(candId, resps[3], "poligrafTabId", "poligrafId", 'addPoligrafBtn', 
        'Добавить тестирование', ['ID', 'Тематика', 'Результат', 'Полиграфолог', 'Дата проверки'], 
        formPoligraf, 'poligrafFormId', "poligraf");

    //вкладка Расследований
    appMain.createTab(candId, resps[4], "investigationTabId", "investigationId", 'addInvestigationBtn', 
        'Добавить расследование', ['ID', 'Тематика', 'Информация', 'Дата проверки'], formInvestigation, 
        'investigationFormId', "investigation");

    //вкладка Запрос
    appMain.createTab(candId, resps[5], "inquiryTabId", "inquiryId", 'addInquiryBtn', 'Добавить запрос', 
        ['ID', 'Информация', 'Иннициатор', 'Источник', 'Дата запроса'], formInquiry, 'inquiryFormId', "inquiry")

    //устанаввливаем статус кнопок в зависимости от статуса кандидата
    if (resps[0]['status'] != resps[6]['NEWFAG' as keyof typeof resps[6]] || 
        resps[0]['status'] != resps[6]['UPDATE'as keyof typeof resps[6]]) {
        let sendResumeBtn = document.getElementById('sendResume') as HTMLButtonElement;
        sendResumeBtn.setAttribute("class", "disabled btn btn-outline-success hidden-print");
        let addCheckBtn = document.getElementById('checkBtn') as HTMLButtonElement;
        addCheckBtn.setAttribute("class", "disabled btn btn-outline-primary hidden-print")
    };
    if (resps[0]['status'] != resps[6]['SAVE'  as keyof typeof resps[6]] ||
         resps[0]['status'] != resps[6]['REPLY' as keyof typeof resps[6]]) {
        let editBtn = document.getElementById('editBtn') as HTMLButtonElement;
        editBtn.setAttribute("class", "disabled btn btn-outline-info")
        let delBtn = document.getElementById('deleteBtn') as HTMLButtonElement;;
        delBtn.setAttribute("class", "disabled btn btn-outline-info")
    };
    if (resps[0]['status'] != resps[6]['RESULT' as keyof typeof resps[6]]) {
        let sendRegistryBtn = document.getElementById('addRegistryBtn') as HTMLButtonElement;;
        sendRegistryBtn.setAttribute("class", "disabled btn btn-outline-primary hidden-print")
    };
};

//открыть анкету
function anketaTab(candId: any, anketa: string | any[]){
    appMain.createHeader(`<a href="#" onclick=openProfile(${candId})>${anketa[0][0]['fullname']}</a>`);
    appMain.createDivId(["anketaId", "buttonGroupId"], "profileTabId");
    const resumeSubDivNames = ['Резюме', 'Должности', 'Документы', 'Адреса', 'Контакты', 'Работа', 'Связи'];
    const resumeSubDivIds = ['resume', 'staffs', 'documents', 'addresses', 'contacts', 'workplaces', 'relations'];
    const labelNames = [
        ['id', 'Регион', 'Фамилия Имя Отчество', 'Изменение имени', 'Дата рождения', 'Место рождения', 'Гражданство', 
        'СНИЛС', 'ИНН', 'Образование', 'Дополнительная информация', 'Статус', 'Дата', 'Рекрутер', 'Внешний id'],
        ['Должность', 'Департамент'],
        ['Вид документа', 'Серия', 'Номер', 'Кем выдан', 'Дата'],
        ['Тип', 'Регион', 'Адрес'],
        ['Вид', 'Контакт'],
        ['Период', 'Организация', 'Адрес', 'Должность'],
        ['Связь', 'Полное ФИО', 'Дата рождения', 'Адрес', 'Место работы', 'Контакты'],
    ];
    appMain.createDivId(resumeSubDivIds, "anketaId");
    //группа Изменить анкету, Добавить информацию, Обновить статус, Отправить на проверку
    const groupBtnResume = document.getElementById("buttonGroupId") as HTMLElement;
    groupBtnResume.setAttribute("class", "btn-group py-2 hidden-print");
    groupBtnResume.setAttribute("role", "group");
    const grpBtnResumeAttr = {
        'Изменить  анкету': `createResume(${JSON.stringify(anketa[0][0])})`,
        'Добавить информацию': `addResumeItem(${candId}, ${JSON.stringify(resumeSubDivIds.slice(1))})`,
        'Обновить статус': `updateStatus(${candId})`,
        'Отправить на проверку': `sendResume(${candId})`
    };
    for (let i = 0; i < Object.keys(grpBtnResumeAttr).length; i++){
        let updBtnResume = document.createElement("button");
        updBtnResume.setAttribute("class", "btn btn-outline-primary");
        if (i == 3) updBtnResume.setAttribute("id", "sendResume");
        updBtnResume.setAttribute("onclick", Object.values(grpBtnResumeAttr)[i])
        updBtnResume.innerHTML = Object.keys(grpBtnResumeAttr)[i];
        groupBtnResume.appendChild(updBtnResume)
    };
    //создаем таблицы с данными анкеты и вставляем их на таблицу
    for (let i = 0; i < anketa.length; i++) {
        let subSubdivs = document.getElementById(resumeSubDivIds[i]) as HTMLElement;
        let targetHeader = document.createElement('h6');
        targetHeader.innerHTML = resumeSubDivNames[i];
        subSubdivs.appendChild(targetHeader);
        let divTable = createProfileTable(labelNames[i], anketa[i]);
        subSubdivs.appendChild(divTable);
    };
};

//добавление данных в анкету
function addResumeItem(candId: any, formDivIds: string | any[]){
    appMain.createMessage('alert alert-info', "Заполните обязательные поля в нужной форме");
    //вставляем формы на месте таблиц с данными анкеты. Оставляем заголовки. Резюме - удаляем.
    let destID = document.getElementById("resume") as HTMLDivElement;
    destID.innerHTML = '';
    const anketaForms = [formStaff, formDocument, formAddress, formContact, formWorkplace, formRelation];
    for (let i = 0; i < formDivIds.length; i++) {
        let subDestID = document.getElementById(formDivIds[i]) as HTMLElement;
        subDestID.children[1].innerHTML = anketaForms[i]
        //вставка обработчиков
        let form = document.forms[i];
        form.addEventListener('submit', async function (event){        
            const formData = new FormData(form);
            let response = await fetch (`update/${formDivIds[i]}/${candId}`, {
                method: "post",
                body: formData
            })
            let resp = await response.json();
            appMain.createMessage("alert alert-primary", resp['message']);
        });
    };
    let buttonGroupId = document.getElementById("buttonGroupId") as HTMLElement;
    buttonGroupId.innerHTML = '';
};

//сброс статуса анкеты на UPDATE при необходимости
async function updateStatus(candId: number) {
    let response = await fetch("/resume/status/" + candId.toString());
    let resp = await response.json();
    appMain.createMessage("alert alert-info", resp['message']);
    openProfile(candId);
};

//отправка анкеты на автопроверку
async function sendResume(candId: number) {
    let response = await fetch("/resume/send/" + candId.toString());
    let resp = await response.json();
    appMain.createMessage("alert alert-info", resp['message']);
};

//открыть проверки
function checkTab(candId: number, checks: Array<Object>){
    const divPage = document.getElementById("checkTabId") as HTMLElement;
    //точка для подключения результатов проверки
    const divCheck = document.createElement("div");
    divCheck.setAttribute("id", "checkId");
    divPage.appendChild(divCheck);
    //группа кнопок
    const groupBtnCheck = document.createElement("div");
    groupBtnCheck.setAttribute("class", "btn-group hidden-print");
    groupBtnCheck.setAttribute("role", "group");
    divPage.appendChild(groupBtnCheck);
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
        'ID', 'Статус автопроверки', 'Проверка по местам работы', 'Бывший работник МТСБ', 
        'Проверка паспорта', 'Проверка ИНН', 'Проверка ФССП', 'Проверка банкротства', 'Проверка БКИ', 
        'Проверка судебных дел', 'Проверка аффилированности', 'Проверка в списке террористов', 
        'Проверка нахождения в розыске', 'Проверка в открытых источниках', 'Проверка Кронос', 'Проверка Крос', 
        'Дополнительная информация', 'Материалы проверки', 'ПФО', 'Комментарии', 'Результат проверки', 
        'Дата проверки', 'Сотрудник СБ'
    ];
    const divId = document.getElementById("checkId") as HTMLElement;
    divId.innerHTML = createProfileTable(labelNames, checks).outerHTML;
    //прослушиваем событие на кнопке 'Добавить проверку'
    const addBtnListener = document.getElementById("checkBtn") as HTMLElement;
    addBtnListener.addEventListener('click', async function addCheck(event){
        let checkTabId = document.getElementById("checkTabId") as HTMLElement;
        checkTabId.innerHTML = formCheck;
        //проверка статуса анкеты, если уже взята в работу - выход
        let response = await fetch("/check/status/"+candId);
        let resp = await response.json();
        appMain.createMessage("alert alert-warning", resp['message']);
        if (resp['message'] == "Анкета взята в работу и еще не закончена"){
            return mainPage("/index/main/");
        }
        //прослушиваем событие на кнопке  Принять
        let form = document.getElementById("checkFormId") as HTMLFormElement;
        form.addEventListener('submit', async function formCheck(event){
            const formData = new FormData(form);
            let response = await fetch (`/check/${candId}`, {
                method: "post",
                body: formData
            })
            let resp = await response.json();
            appMain.createMessage("alert alert-primary", resp['message']);
            this.removeEventListener('submit', formCheck)
            openProfile(candId)
        });
    });
    //прослушиваем событие на кнопке 'Удалить проверку'
    const delBtnListener = document.getElementById("deleteBtn") as HTMLElement;
    delBtnListener.addEventListener('click', async function (event){
        if (confirm("Вы действительно хотите удалить проверку?")) {
            let response = await fetch("/check/delete/"+candId);
            let resp = await response.json();
            appMain.createMessage("alert alert-warning", resp['message']);
            openProfile(candId)
        };
    });
    //прослушиваем событие на кнопке 'Редактировать проверку'
    const editBtnListener = document.getElementById("editBtn") as HTMLElement;
    editBtnListener.addEventListener('click', function (event){
        let checkId = document.forms.namedItem("checkFormId") as HTMLFormElement;
        let tagName = checkId.getElementsByTagName("textarea");
        let checkTabId = document.getElementById("checkTabId") as HTMLElement;
        checkTabId.innerHTML = formCheck;

        //фильтруем неиспользуемые значения для подстановки в форму
        let checkFiltred = []
        for (let i = 0; i < Object.keys(checks[0]).length; i++) {
            if (!['id', 'autostatus', 'path', 'pfo', 'comments', 'conclusion', 'deadline', 'officer', 'cand_id'].includes((Object.keys(checks[0])[i]))) {
                checkFiltred.push(Object.values(checks[0])[i]);
            };
        };
        for (let i = 0; i < checkFiltred.length; i++) {
            tagName[i].setAttribute("value", checkFiltred[i]);
        };
    });
};

//create table with candidate profile
function createProfileTable(names: string[], response: Array<Object>) {
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

//открываем страницу стат информации
async function createInfo(){
    //были элементы созданы ранее или нет
    if (!document.getElementById("infoFormId")) {
        appMain.createDivId(["divCandTable", "divPfoTable", "divForm"], 'appContent');
        let destID = document.getElementById("divForm") as HTMLElement;
        destID.innerHTML = formInfo;
    }
    const form = document.forms.namedItem("infoFormId") as HTMLFormElement;
    const formData = new FormData(form);
    const response = await fetch('/information', {
        method: "post",
        body: formData
    });
    let resps = await response.json();
    appMain.createHeader(resps['title']);
    let appMessage = document.getElementById('appMessage') as HTMLElement;
    appMessage.innerHTML = '';
    //присоединяем стат таблицы и форму к элементам приложения по ID
    const divCandTable = document.getElementById("divCandTable") as HTMLElement;
    divCandTable.innerHTML = createStatData(resps["candidates"], "Статистика по кандидатам").outerHTML;
    const divPfoTable = document.getElementById("divPfoTable") as HTMLElement;
    divPfoTable.innerHTML = createStatData(resps["poligraf"], "Статистика по ПФО").outerHTML;
    //прослушиваем событие на кнопке Принять
    form.addEventListener('submit', function submitData (event: any){
        createInfo();
        this.removeEventListener('submit', submitData)
    });
};

//создаем таблицу со статданными
function createStatData (stats: Array<Object>, caption: string){
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