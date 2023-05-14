'use strict';
class Application {
    /* Приведенный код определяет функцию-конструктор, которая устанавливает атрибуты для трех
    элементов (appMessage, appHeader и appContent) и добавляет их к элементу appContainer.
    Устанавливаемые атрибуты включают класс и идентификатор. */
    constructor() {
        this.appContainer = document.getElementById('App');
        this.appContainer.innerHTML = `
      <div class="container py-3" id="appMessage"></div>
      <div class="container py-3" id="appHeader"></div>
      <div class="container py-3" id="appContent"></div>
    `;
        this.auth();
    }
    ;
    /**
   * Asynchronously authenticates the user by making a request to the login endpoint and redirects to the main page
   * if a user is logged in, otherwise displays the login page.
   *
   * @return {void}
   */
    async auth() {
        let response = await fetch('/login');
        let { user } = await response.json();
        if (user != "None") {
            mainPage('/index/main/');
        }
        else {
            userLogin();
        }
    }
    ;
    /**
     * Creates and displays a message on the application.
     *
     * @param {string} info - The type of message to display (e.g. "success", "error", etc.)
     * @param {string} text - The text to display in the message.
     */
    createMessage(info, text) {
        // Set the inner HTML of the appMessage element to a message div with the provided info and text.
        const appMessage = document.getElementById("appMessage");
        appMessage.innerHTML = `<div class="${info}" role="alert">${text}</div>`;
    }
    ;
    /**
     * Creates a header element with the given text and sets it as the innerHTML of appHeader element.
     * @param text - The text to be displayed in the header element.
     */
    createHeader(text) {
        // Set the innerHTML of appHeader to the outerHTML of the h5 element
        const appHeader = document.getElementById("appHeader");
        appHeader.innerHTML = `<h5>${text}</h5>`;
    }
    ;
}
;
/**
 * Logs in the user and displays a login form for them to enter their credentials
 */
function userLogin() {
    // Display an info message to prompt the user to login
    main.createMessage("alert alert-info", "Авторизуйтесь чтобы продолжить работу");
    // Create a header for the login form
    main.createHeader("Вход в систему");
    // Create the login form and add it to the DOM
    const container = document.createElement('div');
    container.innerHTML = formLogin;
    const fragmentContent = document.createDocumentFragment();
    fragmentContent.appendChild(container);
    const appContent = document.getElementById('appContent');
    appContent.replaceChildren(fragmentContent);
    // Add an event listener to the form for when it is submitted
    appContent.addEventListener('submit', async function submitData(event) {
        event.preventDefault();
        const formData = new FormData(appContent.children[0].children[0]);
        const response = await fetch('/login', { method: 'POST', body: formData });
        const { user } = await response.json();
        // If the login was unsuccessful, display a warning message
        if (user == "None") {
            main.createMessage("alert alert-warning", "Неверный логин или пароль");
        }
        else {
            // Otherwise, redirect the user to the main page
            mainPage('/index/main/');
            appContent.removeEventListener('submit', submitData);
        }
    });
}
;
/**
 * Performs a user logout by sending a fetch request to the 'logout' endpoint
 * and calling the userLogin function. Returns a Promise that resolves when both
 * operations complete successfully.
 *
 * @return {Promise} A Promise that resolves when the user is successfully logged out.
 */
function userLogout() {
    Promise.all([
        fetch('logout'),
        userLogin()
    ]);
}
;
/**
 * Fetches data for the main page and renders it.
 *
 * @param path - The URL path to fetch data from.
 * @param currentPage - The current page of data to fetch. Defaults to 1.
 */
async function mainPage(path, currentPage = 1) {
    try {
        let response;
        const searchFormId = document.forms.namedItem("searchFormId");
        // If the path is for searching, fetch the data using a POST request with the search form data.
        if (path == '/index/search/') {
            const form = new FormData(searchFormId);
            response = await fetch(`/index/search/${currentPage}`, { method: "post", body: form });
        }
        else {
            // Otherwise, fetch the data using a GET request.
            response = await fetch(`${path}${currentPage}`);
        }
        ;
        const [data, metadata] = await response.json();
        const { items, title, has_next, has_prev } = metadata;
        // Create a message to display the number of new items.
        main.createMessage("alert alert-info", 
        // Link to fetch new items.
        `<a href="#" onclick="mainPage('/index/new/'); return false;">Новых анкет: ${items}</a>`);
        // Create the page header.
        main.createHeader(title);
        // If the search form doesn't exist, create it and add event listeners.
        if (!searchFormId) {
            const template = document.createElement("div");
            template.innerHTML = `
        <div class="py-3" id="divSearch">${formSearch}</div>
        <div class="py-3" id="divTable"></div>
        <div class="py-3" id="divPager"></div>
      `;
            const fragmentContent = document.createDocumentFragment();
            fragmentContent.appendChild(template);
            const appContent = document.getElementById("appContent");
            appContent.replaceChildren(fragmentContent);
            const form = document.forms[0];
            form.addEventListener("submit", () => {
                mainPage("/index/search/");
            });
        }
        ;
        // Render the candidate table and pagination controls.
        Promise.all([
            createCandidateTable(data),
            switchPage(has_next, has_prev, currentPage, path)
        ]);
    }
    catch (error) {
        // If an error occurs, redirect the user to the login page.
        userLogin();
    }
}
;
/**
 * Creates a table displaying candidate information from an array of candidate objects.
 *
 * @param {Array<object>} candidates - An array of candidate objects containing properties such as id, region, fullname, birthday, status, and deadline.
 */
function createCandidateTable(candidates) {
    const container = document.createElement('div');
    container.innerHTML = `
    <table class="table table-hover table-responsive align-middle py-1">
      <thead>
        <tr>
          <th width="5%">#</th>
          <th width="15%">Регион</th>
          <th width="30%">Фамилия Имя Отчество</th>
          <th width="15%">Дата рождения</th>
          <th width="15%">Статус</th>
          <th width="15%">Дата</th>
        </tr>
      </thead>
      <tbody>
        ${candidates.map(candidate => `
          <tr height="50px">
            <td>${candidate["id"]}</td>
            <td>${candidate["region"]}</td>
            <td><a href="#" onclick="openProfile(${candidate['id']})">
                                                ${candidate["fullname"]}</a></td>
            <td>${convertDate(candidate["birthday"])}</td>
            <td>${candidate["status"]}</td>
            <td>${convertDate(candidate["deadline"])}</td>
          </tr>
        `).join('')}
      </tbody>
    </table>`;
    const fragmentContent = document.createDocumentFragment();
    fragmentContent.appendChild(container);
    const divTable = document.getElementById('divTable');
    divTable.replaceChildren(fragmentContent);
}
;
/**
 * Converts a string date value into a formatted date string.
 *
 * @param {string} value - The input date string to be parsed.
 * @return {string} A formatted date string in the format "DD.MM.YYYY".
 */
function convertDate(value) {
    const date = new Date(Date.parse(value));
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear().toString();
    return `${day}.${month}.${year}`;
}
/**
 * Switches between pages based on the current page and whether there are next and previous pages available.
 *
 * @param has_next The number of the next page.
 * @param has_prev The number of the previous page.
 * @param currentPage The current page number.
 * @param path The path to the current page.
 */
function switchPage(has_next, has_prev, currentPage, path) {
    var _a;
    // Check if the pagination element exists and create it if it does not.
    const paginationElement = document.querySelector(".pagination");
    if (!paginationElement) {
        const container = document.createElement('nav');
        container.innerHTML = `
        <ul class="pagination justify-content-center">
            <li class="page-item" id="prevPage">
                <a class="page-link" href="#">Предыдущая</a>
            </li>
            <li class="page-item" id="nextPage">
                <a class="page-link" href="#">Следующая</a>
            </li>
        </ul>
    `;
        const fragmentContent = document.createDocumentFragment();
        fragmentContent.appendChild(container);
        const divPager = document.getElementById('divPager');
        divPager.replaceChildren(fragmentContent);
    }
    ;
    // Add a click listener to the pagination element to handle page switching.
    const divPager = (_a = document.getElementById('divPager')) === null || _a === void 0 ? void 0 : _a.children[0];
    divPager.addEventListener('click', function (event) {
        event.preventDefault();
        const target = event.target;
        const parentTarget = target.parentElement;
        if (parentTarget.matches('#nextPage') && has_next !== 0) {
            mainPage(path, currentPage + 1);
        }
        else if (parentTarget.matches('#prevPage') && has_prev !== 0) {
            mainPage(path, currentPage - 1);
        }
        // else {
        //         mainPage(path, currentPage);
        //     }
    }, { once: true });
    // Check if there is a next page and disable the next page button if there is not.
    const nextPage = document.getElementById('nextPage');
    if (has_next === 0) {
        nextPage.classList.add('disabled');
    }
    else {
        nextPage.classList.remove('disabled');
    }
    // Check if there is a previous page and disable the previous page button if there is not.
    const prevPage = document.getElementById('prevPage');
    if (has_prev === 0) {
        prevPage.classList.add('disabled');
    }
    else {
        prevPage.classList.remove('disabled');
    }
}
;
/**
 * This function creates a resume form and allows for editing if a candidate ID is provided.
 * @param {number} candId - Optional candidate ID to edit an existing resume
 * @returns {Promise<void>}
 */
async function createResume(candId = null) {
    // Fetch user data from server
    let response = await fetch('/login');
    let { user } = await response.json();
    // Redirect to login if the user is not logged in
    if (user === "None") {
        return userLogin();
    }
    ;
    // Display message and header for resume form
    main.createMessage('alert alert-info', "Заполните обязательные поля, либо загрузите файл");
    main.createHeader("Создать/изменить анкету");
    // Create container for resume form and upload form
    const container = document.createElement('div');
    container.innerHTML = `
    <div class="py-1" id="divformUpload">${formUpload}</div>
    <div class="py-1" id="divformUpload">${formResume}</div>
  `;
    const fragmentContent = document.createDocumentFragment();
    fragmentContent.appendChild(container);
    // Add container to app content and clear previous content
    const appContent = document.getElementById("appContent");
    appContent.replaceChildren(fragmentContent);
    // If editing an existing resume, pre-fill form with existing data
    if (candId) {
        const response = await fetch(`/profile/${candId}`);
        const profile = await response.json();
        const resume = profile[0][0][0];
        const resumeForm = document.forms.namedItem("resumeFormId");
        const inputs = Array.from(resumeForm.getElementsByTagName("input"));
        // Filter out unwanted fields and map values to array
        const anketaFiltred = Object.entries(resume)
            .filter(([key]) => !['id', 'region', 'status', 'deadline', 'recruiter', 'addition',
            'request_id'
        ].includes(key))
            .map(([_, value]) => value);
        // Set input values to filtered values
        inputs.forEach((input, i) => {
            input.setAttribute("value", anketaFiltred[i]);
        });
    }
    ;
    // Add event listener to form submit button
    const form = document.forms.namedItem("resumeFormId");
    form.addEventListener('submit', function submitData(event) {
        event.preventDefault();
        submitResume("resumeFormId", "create");
    }, { once: true });
}
;
/**
 * Submits the resume from a form to a specified URL using a POST request.
 * @param formId The ID of the form containing the resume.
 * @param url The URL to submit the resume to.
 */
async function submitResume(formId, url) {
    // Get the form and its data
    const form = document.forms.namedItem(formId);
    const formData = new FormData(form);
    // Send the resume data as a POST request to the specified URL
    const response = await fetch(`/resume/create`, { method: "POST", body: formData });
    // Parse the response JSON to get the message and candidate ID
    const { message, cand_id } = await response.json();
    // Update the UI with the message and open the candidate's profile
    main.createMessage("alert alert-primary", message);
    openProfile(cand_id);
}
;
/**
 * Adds a resume item for a candidate with the provided ID
 * @param candId - The ID of the candidate
 */
function addResumeItem(candId) {
    // Define array of target names and corresponding forms
    const targetNames = ['Должности', 'Документы', 'Адреса', 'Контакты', 'Работа', 'Связи'];
    const forms = [formStaff, formDocument, formAddress, formContact, formWorkplace, formRelation];
    // Display message to user
    main.createMessage('alert alert-info', "Заполните обязательные поля в нужной форме");
    // Create container array of HTML for each target name and form
    const container = [];
    targetNames.forEach(function (targetName, index) {
        container.push(`<h6>${targetName}</h6>${forms[index]}`);
    });
    // Create a temporary div element
    const temp = document.createElement('div');
    // Add the container HTML to the temporary div element
    temp.innerHTML = container.join('');
    // Create a document fragment and append the temporary div element to it
    const fragments = document.createDocumentFragment();
    fragments.append(temp);
    // Get the resume element by ID and clear its contents
    const resumeElement = document.getElementById("anketaTabId");
    resumeElement.innerHTML = '';
    // Append the document fragment to the resume element
    resumeElement.appendChild(fragments);
    // Add a submit event listener to the resume element
    resumeElement.addEventListener('submit', async function (event) {
        event.preventDefault();
        // Get the form element that triggered the submit event
        const form = event.target;
        // Get the path from the form's ID attribute
        const path = form.getAttribute("id");
        // Get the form data
        const formData = new FormData(form);
        // Send a POST request to the server to update the candidate's information
        const response = await fetch(`update/${path}/${candId}`, {
            method: "post",
            body: formData
        });
        // Get the response message from the server
        const { message } = await response.json();
        // Display the message to the user
        main.createMessage("alert alert-primary", message);
        // Scroll to the top of the page
        window.scrollTo(0, 0);
    });
}
;
/**
 * Opens the profile of a candidate and populates it with their information.
 * @param candId The ID of the candidate whose profile to open.
 */
async function openProfile(candId) {
    // Fetch candidate information from server
    const response = await fetch(`/profile/${candId}`);
    const [anketa, check, registry, poligraf, investigation, inquiry, state] = await response.json();
    // Create container element and add profile tabs to it
    const container = document.createElement('div');
    container.innerHTML = `
    <div class="nav nav-tabs nav-justified" role="tablist">
      <button data-bs-toggle="tab" data-bs-target="#anketaTab" type="button" role="tab" class="nav-link active">Профиль</button>
      <button data-bs-toggle="tab" data-bs-target="#checkTab" type="button" role="tab" class="nav-link">Проверки</button>
      <button data-bs-toggle="tab" data-bs-target="#registryTab" type="button" role="tab" class="nav-link">Согласования</button>
      <button data-bs-toggle="tab" data-bs-target="#poligrafTab" type="button" role="tab" class="nav-link">Полиграф</button>
      <button data-bs-toggle="tab" data-bs-target="#investigationTab" type="button" role="tab" class="nav-link">Расследования</button>
      <button data-bs-toggle="tab" data-bs-target="#inquiryTab" type="button" role="tab" class="nav-link">Запросы</button>
    </div>
    <div class="tab-content">
      <!-- Use a loop to create the tab content -->
      ${['anketa', 'check', 'registry', 'poligraf', 'investigation', 'inquiry'].map(tab => `
        <div class="tab-pane py-1 ${tab === 'anketa' ? 'active' : ''}" role="tabpanel" id="${tab}Tab">
          <div id="${tab}TabId" class="py-3">
            <div id="${tab}Id"></div>
          </div>
        </div>
      `).join('')}
    </div>
  `;
    const fragmentContent = document.createDocumentFragment();
    fragmentContent.appendChild(container);
    const appContent = document.getElementById("appContent");
    appContent.replaceChildren(fragmentContent);
    Promise.all([
        createAnketa(candId, anketa),
        createCheck(candId, check),
        createRegistry(candId, registry),
        createPoligraf(candId, poligraf),
        createInvestigation(candId, investigation),
        createInquiry(candId, inquiry)
    ]);
    //update button state
    stateProfileButtons(anketa[0][0]['status'], state);
}
;
function createAnketa(candId, anketa) {
    //resume tab
    const resumeSubDivNames = ['Резюме', 'Должности', 'Документы', 'Адреса', 'Контакты', 'Работа', 'Связи'];
    const anketaTabId = document.getElementById("anketaTabId");
    main.createHeader(`<a href="#" onclick=openProfile(${candId})>${anketa[0][0]['fullname']}</a>`);
    const fragment = document.createDocumentFragment();
    resumeSubDivNames.forEach((name, i) => {
        const subHeader = document.createElement('h6');
        subHeader.innerHTML = name;
        fragment.appendChild(subHeader);
        fragment.appendChild(createItemTable(ANKETA_LABELES[i], anketa[i]));
    });
    const anketaId = document.getElementById("anketaId");
    anketaId.replaceChildren(fragment);
    const resumeBtnGroup = document.createElement('div');
    resumeBtnGroup.classList.add('btn-group', 'hidden-print');
    resumeBtnGroup.setAttribute("role", "group");
    resumeBtnGroup.innerHTML = `
    <button class="btn btn-outline-primary" onclick="createResume(${candId})">Изменить  анкету</button>
    <button class="btn btn-outline-primary" onclick="addResumeItem(${candId})">Добавить информацию</button>
    <button class="btn btn-outline-primary" onclick="updateStatus(${candId})">Обновить статус</button>
    <button class="btn btn-outline-primary" id="sendResume" onclick="sendResume(${candId})">Отправить на проверку</button>
  `;
    anketaId.appendChild(resumeBtnGroup);
}
;
function createCheck(candId, check) {
    const checkId = document.getElementById('checkId');
    checkId.replaceChildren(createItemTable(CHECK_LABELES, check));
    const checkBtnGroup = document.createElement('div');
    checkBtnGroup.classList.add('btn-group', 'hidden-print');
    checkBtnGroup.setAttribute("role", "group");
    checkBtnGroup.innerHTML = `
    <button class="btn btn-outline-primary" id="checkBtn" onclick="checkEditNew(${candId}, 'new')">Добавить проверку</button>
    <button class="btn btn-outline-primary" id="editBtn" onclick="checkEditNew(${candId}, 'edit')">Редактировать проверку</button>
    <button class="btn btn-outline-primary" id="deleteBtn" onclick="deleteLastCheck(${candId})">Удалить последнюю проверку</button>
  `;
    checkId.appendChild(checkBtnGroup);
}
;
function createRegistry(candId, registry) {
    const registryId = document.getElementById('registryId');
    registryId.replaceChildren(createItemTable(REGISTRY_LABELES, registry));
    const addRegistryBtn = document.createElement('div');
    addRegistryBtn.innerHTML = `<a class="btn btn-outline-info hidden-print" type="button" id="addRegistryBtn">Добавить согласование</a>`;
    registryId.appendChild(addRegistryBtn);
    createTabAction(candId, "registryTabId", formRegistry, "registry");
}
;
function createPoligraf(candId, poligraf) {
    const poligrafId = document.getElementById('poligrafId');
    poligrafId.replaceChildren(createItemTable(POLIGRAF_LABELES, poligraf));
    const addPoligrafBtn = document.createElement('div');
    addPoligrafBtn.innerHTML = `<a class="btn btn-outline-info hidden-print" type="button">Добавить тестирование</a>`;
    poligrafId.appendChild(addPoligrafBtn);
    createTabAction(candId, "poligrafTabId", formPoligraf, "poligraf");
}
;
function createInvestigation(candId, investigation) {
    const investigationId = document.getElementById('investigationId');
    investigationId.replaceChildren(createItemTable(INVESTIGATION_LABELES, investigation));
    const addInvestigationBtn = document.createElement('div');
    addInvestigationBtn.innerHTML = `<a class="btn btn-outline-info hidden-print" type="button">Добавить расследование</a>`;
    investigationId.appendChild(addInvestigationBtn);
    createTabAction(candId, "investigationTabId", formInvestigation, "investigation");
}
;
function createInquiry(candId, inquiry) {
    const inquiryId = document.getElementById('inquiryId');
    inquiryId.replaceChildren(createItemTable(INQUIRY_LABELES, inquiry));
    const addInquiryBtn = document.createElement('div');
    addInquiryBtn.innerHTML = `<a class="btn btn-outline-info hidden-print" type="button">Добавить запрос</a>`;
    inquiryId.appendChild(addInquiryBtn);
    createTabAction(candId, "inquiryTabId", formInquiry, "inquiry");
}
;
/**
 * Updates candidate status and displays a message
 * @param candId - The candidate ID
 */
async function updateStatus(candId) {
    // Fetch the candidate's status
    const response = await fetch(`/resume/status/${candId}`);
    const { message } = await response.json();
    // Display an alert message and open the candidate's profile
    main.createMessage("alert alert-info", message);
    openProfile(candId);
    window.scrollTo(0, 0);
}
;
/**
 * Sends the resume of a candidate with the given ID.
 * @param candId - The ID of the candidate to send the resume for.
 * @returns A Promise that resolves when the resume has been sent.
 */
async function sendResume(candId) {
    // Send a request to the server to send the resume.
    const response = await fetch(`/resume/send/${candId}`);
    // Extract the message from the response.
    const { message } = await response.json();
    // Create a message and open the candidate's profile once the resume has been sent.
    main.createMessage("alert alert-info", message);
    openProfile(candId);
    window.scrollTo(0, 0);
}
;
/**
 * Checks if a candidate profile needs to be edited or if it's new,
 * and handles the corresponding actions.
 * @param candId - the identifier of the candidate profile to check
 * @param flag - a string indicating whether the profile is being edited or is new
 */
async function checkEditNew(candId, flag) {
    // If the profile is not being edited, check the status of the profile
    if (flag === "new") {
        const status = await fetch(`/check/status/${candId}`);
        const { message } = await status.json();
        main.createMessage("alert alert-warning", message);
        // If the profile is already being worked on, return to the profile page
        if (message === "Анкета взята в работу и еще не закончена") {
            return openProfile(candId);
        }
        ;
    }
    ;
    // Create a new form element and import the formCheck HTML
    const form = document.createElement("div");
    form.innerHTML = formCheck.trim();
    // If the profile is being edited, prefill the form with the previous data
    if (flag === "edit") {
        const response = await fetch(`/profile/${candId}`);
        const profile = await response.json();
        const check = profile[1][0];
        const textareas = Array.from(form.getElementsByTagName("textarea"));
        const checkFiltred = Object.entries(check)
            .filter(([key]) => ![
            "id",
            "autostatus",
            "path",
            "pfo",
            "comments",
            "conclusion",
            "deadline",
            "officer",
            "cand_id",
        ].includes(key))
            .map(([_, value]) => value);
        textareas.forEach((textarea, i) => {
            textarea.innerHTML = checkFiltred[i];
        });
    }
    // Add a submit event listener to the form, to send the data to the server
    form.addEventListener("submit", async function (event) {
        event.preventDefault();
        const formData = new FormData(form.children[0]);
        const response = await fetch(`/check/${flag}/${candId}`, {
            method: "post",
            body: formData,
        });
        const { message } = await response.json();
        // Show a message and return to the profile page
        Promise.all([
            main.createMessage("alert alert-primary", message),
            openProfile(candId),
            window.scrollTo(0, 0)
        ]);
    });
    // Replace the content of the checkTabId element with the form element
    const checkTabId = document.getElementById("checkTabId");
    checkTabId.replaceChildren(form);
}
/**
 * Deletes the last check for a candidate.
 * @param candId The ID of the candidate to delete the check for.
 * @returns A Promise that resolves with void when the check has been deleted.
 */
async function deleteLastCheck(candId) {
    // Confirm with the user that they want to delete the check.
    if (confirm("Вы действительно хотите удалить проверку?")) {
        // Make a fetch request to delete the check for the candidate.
        let response = await fetch(`/check/delete/${candId}`);
        // Get the message from the response JSON.
        let { message } = await response.json();
        // Create a warning message and open the candidate's profile.
        main.createMessage("alert alert-warning", message);
        openProfile(candId);
        window.scrollTo(0, 0);
    }
}
;
/**
 * Creates an action listener that displays a form in a tab and submits the form data to the server
 * @param candId - The ID of the candidate
 * @param tabId - The ID of the tab in which to display the form
 * @param formHTML - The HTML content of the form to display
 * @param path - The path to post the form data to on the server
 */
function createTabAction(candId, tabId, formHTML, path) {
    // Get the tab element
    const tabDiv = document.getElementById(tabId);
    // Get the "add" button element
    const addBtnListener = tabDiv.children[0].children[1].children[0];
    // Add a click listener to the "add" button
    addBtnListener.addEventListener('click', function (event) {
        // Replace the tab content with the form HTML
        const container = document.createElement('div');
        container.innerHTML = formHTML;
        const fragment = document.createDocumentFragment();
        fragment.appendChild(container);
        tabDiv.replaceChildren(fragment);
        // Get the form element
        const form = tabDiv.children[0].children[0];
        // Add a submit listener to the form
        form.addEventListener('submit', async function (event) {
            event.preventDefault(); // Prevent default form submission
            // Get the form data
            const formData = new FormData(form);
            // Post the form data to the server
            const response = await fetch(`/${path}/${candId}`, { method: "post", body: formData });
            // Get the response message
            const { message } = await response.json();
            // Call the openProfile function and create a message
            Promise.all([
                main.createMessage("alert alert-primary", message),
                openProfile(candId),
                window.scrollTo(0, 0)
            ]);
        }, { once: true });
    }, { once: true });
}
;
/**
 * Sets the appropriate button states based on the current status and state.
 * @param status - A string representing the current status.
 * @param state - An object representing the current state.
 */
function stateProfileButtons(status, state) {
    // Disable the send resume and add check buttons if the state is not NEW or UPDATE.
    if (status != state['NEW'] && status !== state['UPDATE']) {
        const sendResumeButton = document.getElementById('sendResume');
        sendResumeButton.setAttribute("class", "disabled btn btn-outline-success hidden-print");
        const addCheckButton = document.getElementById('checkBtn');
        addCheckButton.setAttribute("class", "disabled btn btn-outline-primary hidden-print");
    }
    ;
    // Disable the edit button if the state is not SAVE or CANSEL.
    if (status != state['SAVE'] && status !== state['CANSEL']) {
        const editButton = document.getElementById('editBtn');
        editButton.setAttribute("class", "disabled btn btn-outline-info");
    }
    ;
    // Disable the delete button if the status is FINISH.
    if (status != state['RESULT']) {
        const deleteButton = document.getElementById('deleteBtn');
        deleteButton.setAttribute("class", "disabled btn btn-outline-info");
    }
    ;
    // Disable the send registry button if the state is not RESULT.
    if (status != state['RESULT']) {
        const sendRegistryButton = document.getElementById('addRegistryBtn');
        sendRegistryButton.setAttribute("class", "disabled btn btn-outline-primary hidden-print");
    }
}
;
/**
 * Creates a table with candidate profiles
 * @param names - an array of strings representing the column names
 * @param response - an array of objects representing the candidate profiles
 * @returns a string representing an HTML table with the candidate profiles
 */
function createItemTable(names, response) {
    // if there are no profiles, return a message indicating so
    if (!response.length) {
        const paragraph = document.createElement('p');
        paragraph.innerHTML = "Данные отсутствуют";
        const fragment = document.createDocumentFragment();
        fragment.appendChild(paragraph);
        return fragment;
    }
    ;
    // map each profile object to an HTML table row
    const rows = response.map((item) => {
        // map each column name to an HTML table cell
        return names.map((name, i) => {
            // if the current column is 'deadline' or 'birthday', format the date
            if (Object.keys(item)[i] === 'deadline' || Object.keys(item)[i] === 'birthday') {
                const date = new Date(Object.values(item)[i]);
                return `<tr><td width="25%">${name}</td><td>${date.toLocaleDateString('ru-RU')}</td></tr>`;
            }
            // otherwise, just use the value of the current column
            else {
                return `<tr><td width="25%">${name}</td><td>${Object.values(item)[i]}</td></tr>`;
            }
        }).join('');
    });
    // join the HTML table rows together to form the table body
    const body = `<tbody>${rows.join('')}</tbody>`;
    // wrap the table body in an HTML table and return it
    const table = `<table class="table table-responsive">${body}</table>`;
    const container = document.createElement("div");
    container.innerHTML = table;
    const fragment = document.createDocumentFragment();
    fragment.appendChild(container);
    return fragment;
}
;
/**
 * Opens the page with statistical information.
 * @returns {Promise<void>}
 */
async function statInfo() {
    // Check if the element with id "infoFormId" exists
    if (!document.getElementById("infoFormId")) {
        // Get the element with id "appContent" and set its innerHTML
        const container = document.createElement("div");
        container.innerHTML = `
      <div class="py-3" id="divCandTable"></div>
      <div class="py-3" id="divPfoTable"></div>
      <div class="py-3" id="divForm">${formInfo}</div>
    `;
        const fragment = document.createDocumentFragment();
        fragment.appendChild(container);
        const appContent = document.getElementById("appContent");
        appContent.replaceChildren(fragment);
    }
    ;
    // Get the elements with ids "divCandTable", "divPfoTable", and"appMessage"
    const [divCandTable, divPfoTable, appMessage] = ["divCandTable", "divPfoTable", "appMessage"].map(id => document.getElementById(id));
    // Get the form with name "infoFormId" and its data
    const form = document.forms.namedItem("infoFormId");
    const dataForm = new FormData(form);
    // Send a POST request to the server with the form data
    const response = await fetch('/information', {
        method: "post",
        body: dataForm
    });
    // Get the JSON data from the response and destructure it
    const { title, candidates, poligraf } = await response.json();
    // Call the createHeader function from the main module
    main.createHeader(title);
    // Set the innerHTML of appMessage to an empty string
    appMessage.innerHTML = '';
    // Set the appendChild of divCandTable and divPfoTable fragments to the tables created by the createStatTable function
    divCandTable.replaceChildren(createStatTable(candidates, "Статистика по кандидатам"));
    divPfoTable.replaceChildren(createStatTable(poligraf, "Статистика по ПФО"));
    // Add an event listener to the form that calls statInfo when submitted
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        statInfo();
    }, { once: true });
}
/**
 * Creates a table element with the specified stats and caption
 * @param stats Array of objects with key-value pairs to be displayed in the table
 * @param caption Caption for the table
 * @returns A table element with the specified stats and caption
 */
function createStatTable(stats, caption) {
    // Create the table element
    const table = document.createElement("table");
    // Add classes to the table element
    table.classList.add("table", "table-hover", "table-responsive", "align-middle");
    // Set the inner HTML of the table element
    table.innerHTML = `
    <caption>${caption}</caption>
    <thead>
      <tr>
        <th width="50%">Решение</th>
        <th width="50%">Количество</th>
      </tr>
    </thead>
    <tbody>
      ${stats.map(stat => `
        <tr height="50px">
          <td width="50%">${Object.keys(stat)}</td>
          <td width="50%">${Object.values(stat)}</td>
        </tr>
      `).join('')}
    </tbody>
  `;
    const fragment = document.createDocumentFragment();
    fragment.appendChild(table);
    // Return the table fragment
    return fragment;
}
;
let formLogin;
let formUpload;
let formResume;
let formStaff;
let formDocument;
let formAddress;
let formContact;
let formWorkplace;
let formRelation;
let formCheck;
let formRegistry;
let formPoligraf;
let formInvestigation;
let formInquiry;
let formInfo;
let formSearch;
const main = new Application();
const ANKETA_LABELES = [
    ['id', 'Регион', 'Фамилия Имя Отчество', 'Изменение имени', 'Дата рождения', 'Место рождения', 'Гражданство',
        'СНИЛС', 'ИНН', 'Образование', 'Дополнительная информация', 'Статус', 'Дата', 'Рекрутер', 'Внешний id'],
    ['Должность', 'Департамент'],
    ['Вид документа', 'Серия', 'Номер', 'Кем выдан', 'Дата'],
    ['Тип', 'Регион', 'Адрес'],
    ['Вид', 'Контакт'],
    ['Период', 'Организация', 'Адрес', 'Должность'],
    ['Связь', 'Полное ФИО', 'Дата рождения', 'Адрес', 'Место работы', 'Контакты'],
];
const CHECK_LABELES = [
    'ID', 'Статус автопроверки', 'Проверка по местам работы', 'Бывший работник МТСБ',
    'Проверка паспорта', 'Проверка ИНН', 'Проверка ФССП', 'Проверка банкротства', 'Проверка БКИ',
    'Проверка судебных дел', 'Проверка аффилированности', 'Проверка в списке террористов',
    'Проверка нахождения в розыске', 'Проверка в открытых источниках', 'Проверка Кронос', 'Проверка Крос',
    'Дополнительная информация', 'Материалы проверки', 'ПФО', 'Комментарии', 'Результат проверки',
    'Дата проверки', 'Сотрудник СБ'
];
const REGISTRY_LABELES = ['ID', 'Комментарий', 'Решение', 'Дата', 'Согласующий'];
const POLIGRAF_LABELES = ['ID', 'Тематика', 'Результат', 'Полиграфолог', 'Дата проверки'];
const INVESTIGATION_LABELES = ['ID', 'Тематика', 'Информация', 'Дата проверки'];
const INQUIRY_LABELES = ['ID', 'Информация', 'Иннициатор', 'Источник', 'Дата запроса'];
