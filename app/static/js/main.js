'use strict'

//check user session before starting
fetch('/login')
    .then(response => response.json())
    .then(response => {
        let resp = response["data"];
        if (resp['user'] != "None"){
            tablePage('/index/', 'alert alert-success', 'Новых анкет: ')        
        } else {
            userLogin()
        };
    });

//upload page of candidates table 
function tablePage (path, attr, message, currentPage=0) {
    fetch(path+currentPage)
        .then(response => response.json())
        .then(data => {
            let resp = data["data"];
            let tableList = resp[0];
            let newItems = resp[1].items;
            let countPages = resp[2].pager;
            createMessage(attr, message+newItems)
            createHeader("");
            const division = document.createElement('div');
            //let divExtSearch = createExtSearch ()
            //division.appendChild(divExtSearch)
            let divTable = createTable(tableList);
            division.appendChild(divTable);
            let divPager = createPager()
            division.appendChild(divPager);
            document.getElementById('appContent').innerHTML = division.outerHTML;
            listPages(currentPage, countPages);
            //check to the next page
            document.getElementById("nextPage").addEventListener("click", function (){
                if (countPages != 0){
                    tablePage (path, attr, message, currentPage+1)
                } else {
                    tablePage (path, attr, message, currentPage)
                };
            });
            //check to the previous page
            document.getElementById("previousPage").addEventListener("click", function (){
                if (currentPage != 0){
                    tablePage (path, attr, message, currentPage-1)
                } else {
                    tablePage (path, attr, message, currentPage)
                };
            });
        });
    };

//functionality for fast and extended search
function searchItem(idForm, path, currentPage=0){
    let form = document.getElementById(idForm);
    let formData = new FormData(form);
    //let csrf_token = document.getElementById("csrf_token").value
    //formData.append("csrf_token", csrf_token)
    fetch(path+currentPage, {
        method: "post",
        body: formData
        })
        .then(response => response.json())
        .then(data => {
            let resp = data["data"];
            let tableList = resp[0];
            let newItems = resp[1].items;
            let countPages = resp[2].pager;
            createMessage('alert alert-warning', 'Результатов поиска на странице: '+newItems)
            createHeader("");
            const division = document.createElement('div');
            //let divExtSearch = createExtSearch ()
            //division.appendChild(divExtSearch)
            let divTable = createTable(tableList);
            division.appendChild(divTable);
            let divPager = createPager()
            division.appendChild(divPager);
            document.getElementById('appContent').innerHTML = division.outerHTML;
            listPages (currentPage, countPages);
            console.log(currentPage, countPages);

            //check to the next page
            document.getElementById("nextPage").addEventListener("click", function (){
                if (countPages != 0){
                    searchItem(idForm, path, currentPage+1)
                } else {
                    searchItem(idForm, path, currentPage)
                };
            });
            //check to the previous page
            document.getElementById("previousPage").addEventListener("click", function (){
                if (currentPage != 0){
                    searchItem(idForm, path, currentPage-1)
                } else {
                    searchItem(idForm, path, currentPage)
                };
            });
        });
    };

//update pager
function listPages (currentPage, countPages){
    let nextItem = document.getElementById('nextPage');
    let previousItem = document.getElementById('previousPage');

    if (currentPage == 0){
        previousItem.setAttribute("class", "disabled")
    } else { 
        if (previousItem.hasAttribute("class", "disabled")){
            previousItem.removeAttribute("class", "disabled")
        };
    };
    if (countPages == 0){
        nextItem.setAttribute("class", "disabled")
    } else {
        if (nextItem.hasAttribute("class", "disabled")){
            nextItem.removeAttribute("class", "disabled")
        };
    };
}
