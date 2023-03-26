// получаем данные из Flask со старта страницы
let flaskData = JSON.parse(results);
let countPages = pages
let currentPage = 0
createTable (flaskData);
tablePages (currentPage, countPages);

// создаем таблицу со списком кандидатов
function createTable (candidates) {
    const table = document.createElement('table');
    table.setAttribute("class", "table table-hover table-responsive");
    const thead = document.createElement('thead');
    const tbody = document.createElement('tbody');
    table.appendChild(thead);
    table.appendChild(tbody);
    let tr = document.createElement('tr');
    let = tableHeader = ["#", "Регион", "Фамилия Имя Отчество", "Дата рождения", "Статус", "Дата"]
    for (let title of tableHeader) {
        let th = document.createElement('th');
        th.innerHTML = title;
        tr.appendChild(th);
        thead.appendChild(tr);
    };
    for (candidate of candidates) {
        let tr = document.createElement('tr');
        for (val of [candidate['id'], candidate['region'], candidate['fullname'], candidate['birthday'], candidate['status'], candidate['deadline']]){
            let td = document.createElement('td');
            let a = document.createElement('a');
            //a.setAttribute("class", "link-underline-light");
            if (val == candidate['fullname']){
                a.setAttribute("href", "/profile/"+candidate['id'])
            };
            a.innerHTML = val;
            td.appendChild(a);
            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    };
    document.getElementById('newTable').innerHTML = table.outerHTML;
};

//обновление счетчика и кнопок пролистывания
function tablePages (currentPage, countPages){
    let nextItem = document.getElementById('next');
    let previousItem = document.getElementById('previous');
    if (currentPage == 0){
        previousItem.setAttribute("class", "disabled")
    } else { 
        if (previousItem.hasAttribute("class", "disabled")){
            previousItem.removeAttribute("class", "disabled")
        };
    };
    if (currentPage == countPages){
        nextItem.setAttribute("class", "disabled")
    } else {
        if (nextItem.hasAttribute("class", "disabled")){
            nextItem.removeAttribute("class", "disabled")
        };
    };
}
// пролистывание вперед
document.getElementById("next").addEventListener("click", function (){
    if (currentPage == countPages){
        currentPage == countPages-1
    } else {
        currentPage = currentPage+1
    };
    fetch("/"+currentPage)
        .then(response => response.json())
        .then(data => {
            let resp = data["data"];
            countPages = Object.keys(resp).length
            createTable (resp);
            tablePages (currentPage, countPages);
        });
    });

//пролистывание назад
document.getElementById("previous").addEventListener("click", function (){
    if (currentPage == 0){
        currentPage == 1
    } else {
        currentPage = currentPage-1
    };
    fetch("/"+currentPage)
        .then(response => response.json())
        .then(data => {
            let resp = data["data"];
            countPages = Object.keys(resp).length
            createTable (resp);
            tablePages (currentPage, countPages);
        });
    });

// получаем событие клик на кнопке расширенного поиска
document.getElementById("submit").addEventListener("click", function (){
    let form = document.getElementById("searchForm");
    let formData = new FormData(form);
    let csrf_token = document.getElementById("csrf_token").value
    formData.append("csrf_token", csrf_token)
    fetch('/', {
        method: "post",
        body: formData
        })
    .then(response => response.json())
    .then(response => {
        let resp = response["data"];
        createTable(resp)
    });
});