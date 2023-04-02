'use strict'

//create header
function createHeader(text){
    const mainHead = document.createElement('h4');
    mainHead.innerHTML = text
    document.getElementById('appHeaders').innerHTML = mainHead.outerHTML;
};

//create message block element
function createMessage(attr, text){
    const divAlert = document.createElement('div');
    divAlert.setAttribute("class", attr);
    divAlert.setAttribute("role", "alert");
    divAlert.innerHTML = text;
    document.getElementById('appMessages').innerHTML = divAlert.outerHTML;
};

//create table with candidates list
function createTable (candidates) {
    const divTable = document.createElement('div');
    divTable.setAttribute("id", "divTable");

    const table = document.createElement('table');
    table.setAttribute("class", "table table-hover table-responsive py-1");
    divTable.appendChild(table);

    const thead = document.createElement('thead');
    table.appendChild(thead);
    const tbody = document.createElement('tbody');
    table.appendChild(tbody);

    let tr = document.createElement('tr');
    let tableHeader = ["#", "Регион", "Фамилия Имя Отчество", "Дата рождения", "Статус", "Дата"]
    for (let title of tableHeader) {
        let th = document.createElement('th');
        th.innerHTML = title;
        tr.appendChild(th);
        thead.appendChild(tr);
    };
    for (let candidate of candidates) {
        let tr = document.createElement('tr');
        for (let val of [candidate['id'], candidate['region'], candidate['fullname'], candidate['birthday'], candidate['status'], candidate['deadline']]){
            let td = document.createElement('td');
            if (val == candidate['fullname']){
                let a = document.createElement('a');
                a.setAttribute("href", "#");
                a.setAttribute("onclick", "openProfile("+candidate['id']+")")
                a.setAttribute("class", "link-underline-primary");
                a.innerHTML = val;
                td.appendChild(a);
            } else {
                td.innerHTML = val
            };
            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    };
    return divTable
};


//create pager block element
function createPager (){
    const divPager = document.createElement('div');
    divPager.setAttribute("id", "divPager");

    const navPage = document.createElement('nav');
    divPager.appendChild(navPage);

    const pagerUl = document.createElement('ul');
    pagerUl.setAttribute("class", "pagination justify-content-center");
    pagerUl.setAttribute("id", "pager");
    navPage.appendChild(pagerUl);

    const liOne = document.createElement('li');
    liOne.setAttribute("class", "page-item");
    liOne.setAttribute("id", "previousPage");
    pagerUl.appendChild(liOne);

    const pageLinkOne = document.createElement('a');
    pageLinkOne.setAttribute("class", "page-link");
    pageLinkOne.setAttribute("href", "#");
    pageLinkOne.setAttribute("id", "pageLinkOne");
    pageLinkOne.innerHTML = 'Предыдущая'
    liOne.appendChild(pageLinkOne);

    const pageItemTwo = document.createElement('li');
    pageItemTwo.setAttribute("class", "page-item");
    pageItemTwo.setAttribute("id", "nextPage");
    pagerUl.appendChild(pageItemTwo);

    const pageLinkTwo = document.createElement('a');
    pageLinkTwo.setAttribute("class", "page-link");
    pageLinkTwo.setAttribute("href", "#");
    pageLinkTwo.setAttribute("id", "pageLinkTwo");
    pageLinkTwo.innerHTML = 'Следующая'
    pageItemTwo.appendChild(pageLinkTwo);

    return divPager
};

//create extended search block
function createExtSearch (){
    const divExtSearch = document.createElement('div');
    divExtSearch.setAttribute("class", "py-1");

    const collapseButton = document.createElement('button');
    collapseButton.setAttribute("class", "btn btn-outline-primary");
    collapseButton.setAttribute("type", "button");
    collapseButton.setAttribute("data-bs-toggle", "collapse");
    collapseButton.setAttribute("data-bs-target", "collapseSearch");
    collapseButton.innerHTML = 'Расширенный поиск'
    divExtSearch.appendChild(collapseButton);

    const collapse = document.createElement('div');
    collapse.setAttribute("class", "collapse");
    collapse.setAttribute("id", "collapseSearch");
    divExtSearch.appendChild(collapse);

    const collapseCard = document.createElement('div');
    collapseCard.setAttribute("class", "card card-body py-1");
    collapse.appendChild(collapseCard);

    const extSearchForm = document.createElement('form');
    extSearchForm.setAttribute("onsubmit", "return false");
    extSearchForm.setAttribute("id", "formExtSearch");
    collapseCard.appendChild(extSearchForm);

    const extSearchButtonGroup = document.createElement('div');
    extSearchButtonGroup.setAttribute("class", "btn-group py-2 px-2");
    extSearchButtonGroup.setAttribute("role", "group");
    extSearchForm.appendChild(extSearchButtonGroup);

    const extSearchButton = document.createElement('button');
    extSearchButton.setAttribute("class", "btn btn-outline-primary btn-sm");
    extSearchButton.setAttribute("type", "submit");
    extSearchButton.setAttribute("onclick", "searchItem('formExtSearch', '/extsearch/')");
    extSearchButtonGroup.appendChild(extSearchButton);
    extSearchButton.innerHTML = 'Найти'

    const resetButton = document.createElement('button');
    resetButton.setAttribute("class", "btn btn-outline-secondary btn-sm");
    resetButton.setAttribute("type", "reset");
    extSearchButtonGroup.appendChild(resetButton);
    resetButton.innerHTML = 'Очистить форму'

    return divExtSearch
};