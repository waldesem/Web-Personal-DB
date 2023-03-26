const statuses = JSON.parse(stat);
let candidates = JSON.parse(candidate)

resumeUpd (candidates);
staffUpd (JSON.parse(staffs));
documentUpd (JSON.parse(documents));
addressUpd (JSON.parse(addresses));
relationUpd (JSON.parse(relations));
workUpd (JSON.parse(workplaces));
contactUpd (JSON.parse(contacts));
checkUpd (JSON.parse(checks));
registryUpd (JSON.parse(registries));
inquiryUpd (JSON.parse(inquiries));
poligrafUpd (JSON.parse(pfos));
investigationUpd (JSON.parse(invs));

//создание, обновление резюме
function resumeUpd (resps){
    document.getElementById('header').innerHTML = resps[0]['fullname'];
    let names = ['Изменение имени', 'Дата рождения', 'Место рождения', 'Гражданство', 'СНИЛС', 'ИНН', 'Образование', 'Дополнительная информация', 'Регион', 'Статус', 'Дата', 'Рекрутер'];
    let response = [];
    for (resp of resps){
        response.push([resp['previous'], resp['birthday'], resp['birthplace'], resp['country'], resp['snils'], resp['inn'], resp['education'], resp['addition'], resp['region'], resp['status'], resp['deadline'], resp['recruiter']]);
    };
    if (resps[0]['status'] != statuses['NEWFAG'] && resps[0]['status'] != statuses['UPDATE']){
        let sendResumeBtn = document.getElementById('sendResume');
        sendResumeBtn.setAttribute("class", "disabled btn btn-outline-success hidden-print");
        let addCheckBtn = document.getElementById('addCheck');
        addCheckBtn.setAttribute("class", "disabled btn btn-outline-primary hidden-print")
    };
    if (response[0]['status'] != statuses['SAVE'] && response[0]['status'] !=statuses ['REPLY']){
        let delEditBtn = document.getElementById('delEdit');
        delEditBtn.setAttribute("class", "disabled btn-group py-2")
    };
    if (response[0]['status'] != statuses['RESULT']){
        let sendRegistryBtn = document.getElementById('openRegistry');
        sendRegistryBtn.setAttribute("class", "disabled btn btn-outline-primary hidden-print")
    };
    let division = createTable(names, response);
    document.getElementById('resume').innerHTML = division.outerHTML
};

//создание, обновление таблицы должностей
function staffUpd (resps){
    let names = ['Должность', 'Департамент'];
    let response = []
    for (resp of resps){
        response.push([resp['position'], resp['department']]);
    };
    let division = createTable(names, response);
    document.getElementById('staffs').innerHTML = division.outerHTML
};

//создание, обновление таблицы документов
function documentUpd (resps){
    let names = ['Вид документа', 'Серия', 'Номер', 'Кем выдан', 'Дата'];
    let response = []
    for (resp of resps){
        response.push([resp['view'], resp['series'], resp['number'], resp['agency'], resp['issue']]);
    };
    let division = createTable(names, response);
    document.getElementById('documents').innerHTML = division.outerHTML
};

//создание, обновление таблицы адресов
function addressUpd (resps){
    let names = ['Тип', 'Регион', 'Адрес'];
    let response = []
    for (resp of resps){
        response.push([resp['view'], resp['region'], resp['address']]);
    };
    let division = createTable(names, response);
    document.getElementById('addresses').innerHTML = division.outerHTML
};

function contactUpd (resps){
    let names = ['Вид', 'Контакт'];
    let response = []
    for (resp of resps){
        response.push([resp['view'], resp['contact']]);
    };
    let division = createTable(names, response);
    document.getElementById('contacts').innerHTML = division.outerHTML
};

function workUpd (resps){
    let names = ['Период', 'Организация', 'Адрес', 'Должность'];
    let response = []
    for (resp of resps){
        response.push([resp['period'], resp['workplace'], resp['address'], resp['position']]);
    };
    let division = createTable(names, response);
    document.getElementById('workplaces').innerHTML = division.outerHTML
};

function relationUpd (resps){
    let names = ['Связь', 'Полное ФИО', 'Дата рождения', 'Адрес', 'Место работы', 'Контакты'];
    let response = []
    for (resp of resps){
        response.push([resp['relation'], resp['fullname'], resp['birthday'], resp['address'], resp['workplace'], resp['contact']]);
    };
    let division = createTable(names, response);
    document.getElementById('relations').innerHTML = division.outerHTML
};

function checkUpd (resps){
    let names = ['ID', 'Материалы проверки', 'Статус автопроверки', 'Бывший работник МТСБ',
     'Проверка по местам работы', 'Проверка паспорта', 'Проверка ИНН', 'Проверка ФССП', 
     'Проверка банкротства', 'Проверка БКИ', 'Проверка судебных дел', 'Проверка '/ 'аффилированности', 'Проверка в списке террористов', 'Проверка нахождения в розыске',
     'Проверка в открытых источниках', 'Проверка Кронос', 'Проверка Крос', 'Дополнительная'/ 'информация', 'Результат проверки', 'Дата проверки', 'Сотрудник СБ'];
     let response = []
     for (resp of resps){
        response.push([resp['id'], resp['path'], resp['autostatus'], resp['employee'], resp['workplace'], resp['document'], resp['inn'], resp['debt'], resp['bankruptcy'], resp['bki'], resp['courts'], resp['affiliation'], resp['terrorist'], resp['mvd'], resp['internet'], resp['cronos'], resp['cros'], resp['addition'], resp['conclusion'], resp['deadline'], resp['officer']]);
     };
    let division = createTable(names, response);
    if (division){
        document.getElementById('lastCheck').innerHTML = division.firstChild.outerHTML
        //document.getElementById('lastCheck').innerHTML = division.firstChild.outerHTML
        //document.getElementById('otherChecks').innerHTML = division.childNodes.slice(1).outerHTML
    };
};
    
function registryUpd (resps){
    let names = ['ID проверки', 'Комментарий', 'Решение', 'Согласующий', 'Дата'];
    let response = []
    for (resp of resps){
        response.append([resp['check_id'], resp['comments'], resp['decision'], resp['supervisor'], resp['deadline']]);
    };
    let division = createTable(names, response);
    document.getElementById('registries').innerHTML = division.outerHTML
};

function poligrafUpd (resps){
    let names = ['ID', 'Тематика', 'Результат', 'Полиграфолог', 'Дата проверки'];
    let response = []
    for (resp of resps){
        response.push([resp['id'], resp['theme'], resp['results'], resp['officer'], resp['deadline']]);
    };
    let division = createTable(names, response);
    document.getElementById('poligrafs').innerHTML = division.outerHTML
};

function investigationUpd (resps){
    let names = ['ID', 'Тематика', 'Информация', 'Дата проверки'];
    let response = []
    for (resp of resps){
        response.push([resp['id'], resp['theme'], resp['info'], resp['deadline']]);
    };
    let division = createTable(names, response);
    document.getElementById('investigations').innerHTML = division.outerHTML
};

function inquiryUpd (resps){
    let names = ['ID', 'Информация', 'Иннициатор', 'Источник', 'Дата запроса'];
    let response = []
    for (resp of resps){
        response.push([resp['id'], resp['info'], resp['initiator'], resp['source'], resp['deadline']]);
    };
    let division = createTable(names, response);
    document.getElementById('inquiries').innerHTML = division.outerHTML
};

// создание горизонтальной таблицы для данных профиля
function createTable(names, response){
    if (response.length){ 
        let division = document.createElement("div");
        for (j in response){
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

// отработка нажатий кнопок на странице профиля, кроме вызова модальных окон
function buttonEvent(event){
    let button = event.relatedTarget;
    let getAction = button.getAttribute('id');
    switch (getAction){
        case 'updStatus':
            fetch("/actions/update/"+candidates[0]['id'])
                .then(response => response.json())
                .then(data => {
                    let resp = data["data"];
                    resumeUpd (resp);
                });
            break;
        case 'sendResume':
            fetch("/send_resume/"+candidates[0]['id'])
                .then(response => response.json())
                .then(data => {
                    let resp = data["data"];
                    resumeUpd (resp);
                });
            break;
        case 'addCheck':
            fetch("/check/"+candidates[0]['id'])
            .then(response => response.json());
            break;
        case 'editCheck':
            fetch("/check/"+candidates[0]['id']+'/'+checks[0]['id'])
            .then(response => response.json());
            break;
        case 'delCheck':
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
})
