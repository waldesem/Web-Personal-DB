'use strict'

//загрузка графического блока профиля кандидата
function createProfile(){
    
    // общий раздел для всех вложенных объектов
    let divProfile = document.createElement("div");

    //создаем панель вкладок для страницы профиля кандидата/сотрудника
    let navTabs = document.createElement("ul");
    navTabs.setAttribute("class", "nav nav-tabs hidden-print");
    navTabs.setAttribute("id", "navTabEvents");
    divProfile.appendChild(navTabs)
    const tabNames = ['Профиль', 'Проверки', 'Согласования', 'Полиграф', 'Расследования', 'Запросы', 'Другое']
    const tabValues = ["#profile", "#check", "#registr", "#poligraf", "#investigate", "#inquiry", "#other"]
    for (let tab in tabNames){
        let navItem = document.createElement("li");
        navItem.setAttribute("class", "nav-item");
        navTabs.appendChild(navItem)
        let navBtn = document.createElement("button");
        navBtn.setAttribute("class", "nav-link"); // "nav-link active"
        navBtn.setAttribute("type", "button");
        navBtn.setAttribute("data-bs-toggle", "tab");
        navBtn.setAttribute("data-bs-target", tabValues[tab]);
        navBtn.innerHTML = tabNames[tab];
        navItem.appendChild(navBtn)
    };
    
    //содержимое вкладок
    let divContent = document.createElement('div');
    divContent.setAttribute("class", "tab-content py-3");
    divProfile.appendChild(navTabs);
    
    //вкладка профиля
    let divPaneResume = document.createElement('div');
    divPaneResume.setAttribute("class", "tab-pane fade show active");
    divPaneResume.setAttribute("id", "profile");
    navTabs.appendChild(divPaneResume);
    
    //блоки для содержимого профиля
    let targetResume = document.createElement('div')
    divPaneResume.appendChild(targetResume)
    
    //блок для резюме
    let idResume = document.createElement('div')
    idResume.setAttribute("id", "resume");
    divPaneResume.appendChild(idResume)
    
    //другие блоки
    const nаmeHeaders = ['Должности', 'Документы', 'Адреса', 'Контакты', 'Работа', 'Связи'];
    const attrNames = ['staffs', 'documents', 'addresses', 'contacts', 'workplaces', 'relations'];
    const formTarget = ["formStaff", "formDocument", "formAddress", "formContact", "formWork", "formRelation"]
    for (let el in nаmeHeaders){
        let targetNames = document.createElement('div')
        divPaneResume.appendChild(targetNames)
        let targetHeader = document.createElement('p')
        targetHeader.setAttribute("class", "h5 p");
        targetHeader.innerHTML = nаmeHeaders[el];
        let idNames = document.createElement('div')
        idNames.setAttribute("id", attrNames[el]);
        divPaneResume.appendChild(idNames)
        let anchorTarget = document.createElement('a')
        anchorTarget.setAttribute("class", "btn btn-outline-primary btn-sm hidden-print");
        anchorTarget.setAttribute("data-bs-toggle", "modal");
        anchorTarget.setAttribute("data-bs-target", "#formModal");
        anchorTarget.setAttribute("data-bs-whatever", formTarget[el]);
        divPaneResume.appendChild(anchorTarget)
    };
    
    //группа кнопок на вкладке анкеты
    let groupBtnResume = document.createElement('div')
    groupBtnResume.setAttribute("class", "btn-group hidden-print");
    groupBtnResume.setAttribute("role", "group");
    groupBtnResume.setAttribute("aria-label", "Resume group");
    divPaneResume.appendChild(groupBtnResume)
    
    // кнопка Обновить статус
    let updBtnResume = document.createElement('a')
    updBtnResume.setAttribute("class", "btn btn-outline-secondary");
    updBtnResume.setAttribute("id", "updStatus");
    updBtnResume.setAttribute("onclick", "buttonEvent();");
    updBtnResume.innerHTML = 'Обновить статус';
    groupBtnResume.appendChild(updBtnResume)
    
    // кнопка Редактировать анкету
    let editBtnResume = document.createElement('button')
    editBtnResume.setAttribute("class", "btn btn-outline-primary");
    editBtnResume.setAttribute("data-bs-toggle", "modal");
    editBtnResume.setAttribute("data-bs-whatever", "formResume");
    editBtnResume.setAttribute("data-bs-target", "#formModal");
    editBtnResume.innerHTML = 'Редактировать анкету';
    groupBtnResume.appendChild(editBtnResume)
    
    // кнопка Отправить на проверку
    let sendBtnResume = document.createElement('a')
    sendBtnResume.setAttribute("class", "btn btn-outline-secondary");
    sendBtnResume.setAttribute("id", "sendResume");
    sendBtnResume.setAttribute("onclick", "buttonEvent();");
    sendBtnResume.innerHTML = 'Отправить на проверку';
    groupBtnResume.appendChild(sendBtnResume)

    //вкладка проверки
    let divPaneCheck = document.createElement('div');
    divPaneCheck.setAttribute("class", "tab-pane fade show");
    divPaneCheck.setAttribute("id", "check");
    navTabs.appendChild(divPaneCheck);
    
    // кнопка добавить проверку
    let addBtnCheck = document.createElement('a')
    addBtnCheck.setAttribute("class", "btn btn-outline-secondary");
    addBtnCheck.setAttribute("id", "addCheck");
    addBtnCheck.setAttribute("onclick", "buttonEvent();");
    addBtnCheck.innerHTML = 'Добавить проверку';
    divPaneCheck.appendChild(addBtnCheck)
    
    // блок для последней проверки
    let divLastCheck = document.createElement('div');
    divLastCheck.setAttribute("id", "lastCheck");
    divPaneCheck.appendChild(divLastCheck)
    
    //группа кнопок на вкладке проверки
    let groupBtnCheck = document.createElement('div')
    groupBtnCheck.setAttribute("class", "btn-group hidden-print");
    groupBtnCheck.setAttribute("role", "group");
    groupBtnCheck.setAttribute("id", "delEdit");
    groupBtnCheck.setAttribute("aria-label", "Check group");
    divPaneCheck.appendChild(groupBtnCheck)
    
    // кнопка редактировать проверку
    let editBtnCheck = document.createElement('a')
    editBtnCheck.setAttribute("class", "btn btn-outline-primary");
    editBtnCheck.setAttribute("id", "editCheck");
    editBtnCheck.setAttribute("onclick", "buttonEvent();");
    editBtnCheck.innerHTML = 'Редактировать проверку';
    groupBtnCheck.appendChild(editBtnCheck)
    
    // кнопка удалить проверку
    let delBtnCheck = document.createElement('a')
    delBtnCheck.setAttribute("class", "btn-outline-primary btn-outline-dange");
    delBtnCheck.setAttribute("id", "delCheck");
    delBtnCheck.setAttribute("onclick", "buttonEvent();");
    delBtnCheck.innerHTML = 'Удалить проверку';
    groupBtnCheck.appendChild(delBtnCheck)
    
    // кнопка согласовать проверку
    let openRegCheck = document.createElement('a')
    openRegCheck.setAttribute("class", "btn btn-outline-primary");
    openRegCheck.setAttribute("data-bs-toggle", "modal");
    openRegCheck.setAttribute("data-bs-whatever", "formRegistry");
    openRegCheck.setAttribute("data-bs-target", "#formModal");
    openRegCheck.setAttribute("id", "#openRegistry");
    openRegCheck.innerHTML = 'Открыть согласование';
    groupBtnCheck.appendChild(openRegCheck)
    
    // блок для других проверок
    let divOtherCheck = document.createElement('div');
    divOtherCheck.setAttribute("id", "otherChecks");
    divPaneCheck.appendChild(divOtherCheck)

    //вкладка согласования
    let divPaneReg = document.createElement('div');
    divPaneReg.setAttribute("class", "tab-pane fade");
    divPaneReg.setAttribute("id", "registries");
    navTabs.appendChild(divPaneReg);
    
    //вкладка полиграфа
    let divPanePfo = document.createElement('div');
    divPanePfo.setAttribute("class", "tab-pane fade");
    divPanePfo.setAttribute("id", "poligraf");
    navTabs.appendChild(divPanePfo);

    // кнопка добавить тестирование
    let addBtnPfo = document.createElement('a')
    addBtnCheck.setAttribute("class", "btn btn-outline-primary hidden-print");
    addBtnCheck.setAttribute("data-bs-toggle", "modal");
    addBtnCheck.setAttribute("data-bs-whatever", "formPoligraf");
    addBtnCheck.setAttribute("data-bs-target", "#formModal");
    addBtnCheck.innerHTML = 'Добавить тестирование';
    divPanePfo.appendChild(addBtnPfo)

    // блок для результаттов тестирования
    let divPfo = document.createElement('div');
    divPfo.setAttribute("id", "poligrafs");
    divPanePfo.appendChild(divPfo)

    //вкладка расследований
    let divPaneInvs = document.createElement('div');
    divPaneInvs.setAttribute("class", "tab-pane fade");
    divPaneInvs.setAttribute("id", "poligraf");
    navTabs.appendChild(divPaneInvs);

    // кнопка добавить расследование
    let addBtnInvs = document.createElement('a')
    addBtnCheck.setAttribute("class", "btn btn-outline-primary hidden-print");
    addBtnCheck.setAttribute("data-bs-toggle", "modal");
    addBtnCheck.setAttribute("data-bs-whatever", "formInvestigation");
    addBtnCheck.setAttribute("data-bs-target", "#formModal");
    addBtnCheck.innerHTML = 'Добавить расследование';
    divPaneInvs.appendChild(addBtnInvs)

    // блок для результаттов тестирования
    let divInvs = document.createElement('div');
    divInvs.setAttribute("id", "investigations");
    divPaneInvs.appendChild(divInvs)

    //вкладка запросов
    let divPaneInquiry = document.createElement('div');
    divPaneInquiry.setAttribute("class", "tab-pane fade");
    divPaneInquiry.setAttribute("id", "inquiry");
    navTabs.appendChild(divPaneInquiry);

    // кнопка добавить запрос
    let addBtnInquiry = document.createElement('a')
    addBtnInquiry.setAttribute("class", "btn btn-outline-primary hidden-print");
    addBtnInquiry.setAttribute("data-bs-toggle", "modal");
    addBtnInquiry.setAttribute("data-bs-whatever", "formInquiry");
    addBtnInquiry.setAttribute("data-bs-target", "#formModal");
    addBtnInquiry.innerHTML = 'Добавить запрос';
    divPaneInquiry.appendChild(addBtnInquiry)

    // блок для запросов
    let divInquiry = document.createElement('div');
    divInquiry.setAttribute("id", "inquiries");
    divPaneInquiry.appendChild(divInquiry)

    //блок модального окна
    let divModal = document.createElement('div')
    divModal.setAttribute("class", "modal");
    divModal.setAttribute("id", "formModal");
    divModal.setAttribute("data-bs-backdrop", "static");
    divModal.setAttribute("data-bs-keyboard", "true");
    divModal.setAttribute("tabindex", "-1");
    divModal.setAttribute("aria-hidden", "true");
    
    let divModalDialog = document.createElement('div')
    divModalDialog.setAttribute("class", "modal-dialog modal-xl");
    divModal.appendChild(divModalDialog)

    let divModalContent = document.createElement('div')
    divModalContent.setAttribute("class", "modal-content");
    divModal.appendChild(divModalContent)

    let divModalHeader = document.createElement('div')
    divModalHeader.setAttribute("class", "modal-content");
    divModalContent.appendChild(divModalHeader)

    let divModalTitle = document.createElement('h4')
    divModalTitle.setAttribute("class", "modal-content");
    divModalHeader.appendChild(divModalTitle)

    let btnModalClose = document.createElement('h4')
    btnModalClose.setAttribute("type", "button");
    btnModalClose.setAttribute("class", "btn-close");
    btnModalClose.setAttribute("data-bs-dismiss", "modal");
    btnModalClose.setAttribute("aria-label", "Закрыть");
    divModalHeader.appendChild(btnModalClose)

    let modalBody = document.createElement('div')
    modalBody.setAttribute("class", "modal-body");
    divModalContent.appendChild(modalBody)
    
    return divProfile
};

// выгрузка данных профиля кандидата
function openProfile(candId){
    document.getElementById('appContent').innerHTML = createProfile().outerHTML

    fetch("/profile/"+candId)
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
            const checks =resp[7];
            const registries = resp[8];
            const inquiries = resp[9];
            const pfos = resp[10];
            const invs = resp[11];
            const state = resp[12];

            resumeUpd (candidate, state);
            staffUpd (staffs);
            documentUpd (documents);
            addressUpd (addresses);
            contactUpd (contacts);
            workUpd (workplaces);
            relationUpd (relations);
            checkUpd (checks);
            registryUpd (registries);
            poligrafUpd (pfos);
            investigationUpd (invs);
            inquiryUpd (inquiries);
        });
    };

//создание, обновление резюме
function resumeUpd (resps, state){
    const profileHead = document.createElement('h4');
    profileHead.innerHTML = resps[0]['fullname']
    document.getElementById('appHeaders').innerHTML = profileHead.outerHTML;

    let names = ['Изменение имени', 'Дата рождения', 'Место рождения', 'Гражданство', 'СНИЛС',
    'ИНН', 'Образование', 'Дополнительная информация', 'Регион', 'Статус', 'Дата', 'Рекрутер'];
    let response = [];
    for (let resp of resps){
        response.push([resp['previous'], resp['birthday'], resp['birthplace'], resp['country'], resp['snils'], resp['inn'], resp['education'], resp['addition'], resp['region'], resp['status'], resp['deadline'], resp['recruiter']]);
    };
    let division = constructTable(names, response);
    document.getElementById('resume').innerHTML = division.outerHTML

    if (resps[0]['status'] != state['NEWFAG'] && resps[0]['status'] != state['UPDATE']){
        let sendResumeBtn = document.getElementById('sendResume');
        sendResumeBtn.setAttribute("class", "disabled btn btn-outline-success hidden-print");
        let addCheckBtn = document.getElementById('addCheck');
        addCheckBtn.setAttribute("class", "disabled btn btn-outline-primary hidden-print")
    };
    if (response[0]['status'] != state['SAVE'] && response[0]['status'] !=state ['REPLY']){
        let delEditBtn = document.getElementById('delEdit');
        delEditBtn.setAttribute("class", "disabled btn-group py-2")
    };
    if (response[0]['status'] != state['RESULT']){
        let sendRegistryBtn = document.getElementById('openRegistry');
        sendRegistryBtn.setAttribute("class", "disabled btn btn-outline-primary hidden-print")
    };
    
};

//создание, обновление таблицы должностей
function staffUpd (resps){
    let names = ['Должность', 'Департамент'];
    let response = []
    for (let resp of resps){
        response.push([resp['position'], resp['department']]);
    };
    let division = constructTable(names, response);
    document.getElementById('staffs').innerHTML = division.outerHTML
};

//создание, обновление таблицы документов
function documentUpd (resps){
    let names = ['Вид документа', 'Серия', 'Номер', 'Кем выдан', 'Дата'];
    let response = []
    for (resp of resps){
        response.push([resp['view'], resp['series'], resp['number'], resp['agency'], resp['issue']]);
    };
    let division = constructTable(names, response);
    document.getElementById('documents').innerHTML = division.outerHTML
};

//создание, обновление таблицы адресов
function addressUpd (resps){
    let names = ['Тип', 'Регион', 'Адрес'];
    let response = []
    for (resp of resps){
        response.push([resp['view'], resp['region'], resp['address']]);
    };
    let division = constructTable(names, response);
    document.getElementById('addresses').innerHTML = division.outerHTML
};

//создание, обновление таблицы контактов
function contactUpd (resps){
    let names = ['Вид', 'Контакт'];
    let response = []
    for (resp of resps){
        response.push([resp['view'], resp['contact']]);
    };
    let division = constructTable(names, response);
    document.getElementById('contacts').innerHTML = division.outerHTML
};

//создание, обновление таблицы мест работы
function workUpd (resps){
    let names = ['Период', 'Организация', 'Адрес', 'Должность'];
    let response = []
    for (resp of resps){
        response.push([resp['period'], resp['workplace'], resp['address'], resp['position']]);
    };
    let division = constructTable(names, response);
    document.getElementById('workplaces').innerHTML = division.outerHTML
};

//создание, обновление таблицы связей
function relationUpd (resps){
    let names = ['Связь', 'Полное ФИО', 'Дата рождения', 'Адрес', 'Место работы', 'Контакты'];
    let response = []
    for (resp of resps){
        response.push([resp['relation'], resp['fullname'], resp['birthday'], resp['address'], resp['workplace'], resp['contact']]);
    };
    let division = constructTable(names, response);
    document.getElementById('relations').innerHTML = division.outerHTML
};

//создание, обновление таблицы проверки
function checkUpd (resps){
    let names = ['ID', 'Материалы проверки', 'Статус автопроверки', 'Бывший работник МТСБ',
     'Проверка по местам работы', 'Проверка паспорта', 'Проверка ИНН', 'Проверка ФССП', 
     'Проверка банкротства', 'Проверка БКИ', 'Проверка судебных дел', 'Проверка '/ 'аффилированности', 'Проверка в списке террористов', 'Проверка нахождения в розыске',
     'Проверка в открытых источниках', 'Проверка Кронос', 'Проверка Крос', 'Дополнительная'/ 'информация', 'Результат проверки', 'Дата проверки', 'Сотрудник СБ'];
     let response = []
     for (resp of resps){
        response.push([resp['id'], resp['path'], resp['autostatus'], resp['employee'], resp['workplace'], resp['document'], resp['inn'], resp['debt'], resp['bankruptcy'], resp['bki'], resp['courts'], resp['affiliation'], resp['terrorist'], resp['mvd'], resp['internet'], resp['cronos'], resp['cros'], resp['addition'], resp['conclusion'], resp['deadline'], resp['officer']]);
     };
    let division = constructTable(names, response);
    if (division){
        document.getElementById('lastCheck').innerHTML = division.firstChild.outerHTML
        document.getElementById('lastCheck').innerHTML = division.firstChild.outerHTML
        document.getElementById('otherChecks').innerHTML = division.childNodes.slice(1).outerHTML
    };
};

//создание, обновление таблицы согласований
function registryUpd (resps){
    let names = ['ID проверки', 'Комментарий', 'Решение', 'Согласующий', 'Дата'];
    let response = []
    for (resp of resps){
        response.append([resp['check_id'], resp['comments'], resp['decision'], resp['supervisor'], resp['deadline']]);
    };
    let division = constructTable(names, response);
    document.getElementById('registries').innerHTML = division.outerHTML
};

//создание, обновление таблицы проверки на полиграфе
function poligrafUpd (resps){
    let names = ['ID', 'Тематика', 'Результат', 'Полиграфолог', 'Дата проверки'];
    let response = []
    for (resp of resps){
        response.push([resp['id'], resp['theme'], resp['results'], resp['officer'], resp['deadline']]);
    };
    let division = constructTable(names, response);
    document.getElementById('poligrafs').innerHTML = division.outerHTML
};

//создание, обновление таблицы расследований
function investigationUpd (resps){
    let names = ['ID', 'Тематика', 'Информация', 'Дата проверки'];
    let response = []
    for (resp of resps){
        response.push([resp['id'], resp['theme'], resp['info'], resp['deadline']]);
    };
    let division = constructTable(names, response);
    document.getElementById('investigations').innerHTML = division.outerHTML
};

//создание, обновление таблицы запросов
function inquiryUpd (resps){
    let names = ['ID', 'Информация', 'Иннициатор', 'Источник', 'Дата запроса'];
    let response = []
    for (resp of resps){
        response.push([resp['id'], resp['info'], resp['initiator'], resp['source'], resp['deadline']]);
    };
    let division = constructTable(names, response);
    document.getElementById('inquiries').innerHTML = division.outerHTML
};

// создание горизонтальной таблицы для данных профиля
function constructTable(names, response){
    if (response.length){ 
        let division = document.createElement("div");
        for (let j in response){
            let div = document.createElement("div");
            let tbl = document.createElement("table");
            tbl.setAttribute("class", "table");
            let tblBody = document.createElement("tbody")
            for (i in names){
                let cell1 = document.createElement("td");
                cell1.setAttribute("width", "25%");
                cell1.innerHTML = names[i];
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

// отработка нажатий группы кнопок на странице профиля кроме вызова модальных окон
function buttonEvent(event){
    let button = event.relatedTarget;
    let getAction = button.getAttribute('id');
    switch (getAction){
        case 'updStatus':   //обновить статус анкеты
            fetch("/actions/update/"+candidates[0]['id'])
                .then(response => response.json())
                .then(data => {
                    let resp = data["data"];
                    resumeUpd (resp);
                });
            break;
        case 'sendResume':  //отправить анкету на проверку
            fetch("/send_resume/"+candidates[0]['id'])
                .then(response => response.json())
                .then(data => {
                    let resp = data["data"];
                    resumeUpd (resp);
                });
            break;
        case 'addCheck':    //добавить проверку
            fetch("/check/"+candidates[0]['id'])
            .then(response => response.json());
            break;
        case 'editCheck':   //редактировать проверку
            fetch("/check/"+candidates[0]['id']+'/'+checks[0]['id'])
            .then(response => response.json());
            break;
        case 'delCheck':    //удалить проверку
            if (confirm("Вы действительно хотите удалить проверку?")){    
                fetch("/delete/"+candidates[0]['id']+'/'+checks[0]['id'])
                    .then(response => response.json());
            };
            break;
    };
}

// получение информации из формы, передача запроса и получение json
function addInfo (url){
    document.getElementById("submit").addEventListener("click", function (){
        let form = document.getElementById("addInfo");
        let formData = new FormData(form);
        let csrf_token = document.getElementById("csrf_token").value
        formData.append("csrf_token", csrf_token)
        fetch(url, {
            method: "post",
            body: formData
            })
        .then(response => response.json())
        .then(data => {
            let resp = data["data"];
            flag = resp[resp.length-1]['flag']
            resp.splice(-1)
            console.log(resp)
            switch (flag){
                case 'resume':
                    (resumeUpd (resp));
                    break;
                case 'staff':
                    (staffUpd(resp));
                    break;
                case 'document':
                    (documentUpd(resp));
                    break;
                case 'address':
                    (addressUpd(resp));
                    break;
                case 'contact':
                    (contactUpd(resp));
                    break;
                case 'work':
                    (workUpd(resp));
                    break;
                case 'relation':
                    (relationUpd(resp));
                    break;
                case 'check':
                    (checkUpd(resp));
                    break;
                case 'registr':
                    (poligrafUpd(resp));
                    break;
                case 'investigation':
                    (investigationUpd(resp));
                    break;
                case 'inquiry':
                    (inquiryUpd(resp));	
                    break;
                case 'impossible':
                    window.alert('Ошибка');
                break;
                    default:
                    window.alert('Ошибка')
            };
        });
    });
}

// запуск модального окна и передача в него формы по условию
function modalWindow (){
    let formModal = document.getElementById('formModal')
    formModal.addEventListener('show.bs.modal', function (event) {
    let button = event.relatedTarget;
    let get_form = button.getAttribute('data-bs-whatever');
    switch (get_form) {
        case 'formResume':
            formModal.querySelector('.modal-body').innerHTML = formResume;
            addInfo("/actions/edit/"+candidates[0]['id']);
            break;
        case 'formStaff':
            formModal.querySelector('.modal-body').innerHTML = formStaff;
            addInfo("/add/form_staff/"+candidates[0]['id']);
            break;
        case 'formDocument':
            formModal.querySelector('.modal-body').innerHTML = formDocument;
            addInfo("/add/form_document/"+candidates[0]['id']);
            break;
        case 'formAddress':
            formModal.querySelector('.modal-body').innerHTML = formAddress;
            addInfo("/add/form_address/"+candidates[0]['id']);
            break;
        case 'formContact':
            formModal.querySelector('.modal-body').innerHTML = formContact;
            addInfo("/add/form_contact/"+candidates[0]['id']);
            break;
        case 'formWork':
            formModal.querySelector('.modal-body').innerHTML = formWork;
            addInfo("/add/form_work/"+candidates[0]['id']);
            break;
        case 'formRelation':
            formModal.querySelector('.modal-body').innerHTML = formRelation;
            addInfo("/add/form_relation/"+candidates[0]['id']);
            break;
        case 'formInvestigation':
            formModal.querySelector('.modal-body').innerHTML = formInvestigation;
            addInfo("/add/form_investigation/"+candidates[0]['id']);
            break;
        case 'formInquiry':
            const formInquiry = `{{ multiform(form_inquiry) }}`
            formModal.querySelector('.modal-body').innerHTML = formInquiry;
            addInfo("/add/form_inquiry/"+candidates[0]['id']);
            break;
        case 'formPoligraf':
            formModal.querySelector('.modal-body').innerHTML = formPoligraf;
            addInfo("/add/form_poligraf/"+candidates[0]['id']);
            break;
        case 'formRegistry':
            formModal.querySelector('.modal-body').innerHTML = formRegistry;
            addInfo("/registry/"+candidates[0]['id'], check_id=check.id);
            formModal.querySelector('.modal-body').innerHTML = formRegistry;
            addInfo("/registry/"+candidates[0]['id'], check_id=0);
            break;
        default:
            window.alert('Ошибка формы')
        };
    });
}