'use strict';

const appContainer = document.getElementById('App') as HTMLDivElement;
const appMessage = document.createElement('div');
const appHeader = document.createElement('div');
const appContent = document.createElement('div');

[appMessage, appHeader, appContent].forEach((container) => {
  container.classList.add("container", "py-3");
  appContainer.appendChild(container);
});


/**
 * Asynchronously authenticates the user by making a request to the login endpoint and redirects to the main page 
 * if a user is logged in, otherwise displays the login page.
 *
 * @return {void} 
 */
(async (): Promise<void> => {
let response = await fetch('/login');
let { user } = await response.json();
if (user != "None") {
  mainPage('/index/main/')
} else {
  userLogin()
}
})();


/**
 * Creates a message with the given styling and text and replaces the existing message in appMessage.
 *
 * @param {string} styling - the class name of the styling for the message
 * @param {string} text - the text to be displayed in the message
 */
function createMessage(styling: string, text: string): void{
	const alert = document.createElement('div');
  alert.classList.add("alert", styling, "alert-dismissible");
  alert.setAttribute("role", "info");
  alert.innerHTML = text;
  const button = document.createElement('button');
  button.classList.add("btn-close");
  button.setAttribute("type", "button");
  button.setAttribute("data-bs-dismiss", "alert");
  alert.appendChild(button);
  appMessage.replaceChildren(alert);
};

/**
 * Creates a header element with the provided text and replaces any existing
 * header element in the appHeader container with the newly created one.
 *
 * @param {string} text - The text to display in the header element.
 * @return {void} This function does not return anything.
 */
function createHeader(text: string): void{
  const header = document.createElement("h5");
  header.textContent = text;
	appHeader.replaceChildren(header);
};

/**
 * Logs in the user and displays a login form for them to enter their credentials
 * 
 * @param {string} alert - The alert type to display to the user
 * @param {string} text - The text to display to the user
 */
function userLogin(
  alert: string="alert-info", 
  text: string="Авторизуйтесь чтобы продолжить работу"
  ) {
  // Display an info message to prompt the user to login
  createMessage(alert, text);

  // Create a header for the login form
  createHeader("Вход в систему");

  // Create the login form and add it to the DOM
  const login = document.createElement('div');
  login.classList.add("py-2");
  login.innerHTML = formLogin;

  // Replace the current content with the login form
  appContent.replaceChildren(login);

  // Add an event listener to the form for when it is submitted
  login.addEventListener('submit', async function submitData (event: any){
    event.preventDefault();

    // Send a POST request to the server with the form data
    const response = await fetch('/login', {
      method: 'POST', 
      body: new FormData(login.children[0] as HTMLFormElement)
    });

    // Parse the response JSON
    const { user } = await response.json();

    // If the login was unsuccessful, display a warning message
    if (user == "None") {
      createMessage("alert-danger", "Неверный логин или пароль");
    } else {
      // Otherwise, redirect the user to the main page
      mainPage('/index/main/');
      login.removeEventListener('submit', submitData);
    }
  });
};


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
	])
};


/**
 * Displays the main page with a table view of data and pagination controls.
 *
 * @param path The path to fetch data from.
 */
async function mainPage(path: string) {

  // Fetch user data from server
  const auth = await fetch('/login');
  const { user } = await auth.json();

  // Redirect to login if the user is not logged in
  if (user === "None") {
    return userLogin("alert-danger", "Для просмотра нужно войти в систему")
  };
  
  countItems();
  // Create the search bar HTML and add a submit event listener to it
  const search = document.createElement("div");
  search.classList.add("py-3");
  search.innerHTML = formSearch;
  search.children[0].addEventListener("submit", () => {
    tableView("/index/search/", 1);
  });

  // Create the candidate table HTML
  const table = document.createElement("div");
  table.classList.add("py-3");

  // Create the pagination controls HTML
  const pager = document.createElement("div");
  pager.classList.add("py-3");

  // Append the search bar, candidate table, and pagination controls to a document fragment
  const fragment = document.createDocumentFragment();
  [search, table, pager].forEach((element) => {
    fragment.appendChild(element)
  });

  // Replace the appContent element with the document fragment
  appContent.replaceChildren(fragment);

  /**
   * Fetches and displays a table view of data from a given path and page number.
   *
   * @param path The path to fetch data from.
   * @param currentPage The current page number to fetch.
   */
  async function tableView(path: string, currentPage = 1) {

    // Fetch data from the given path and page number.
    const response = path !== '/index/search/' ?
      await fetch(`${path}${currentPage}`) :
      await fetch(`${path}${currentPage}`, {
        method: "post",
        body: new FormData(search.children[0] as HTMLFormElement)
      });

    // Parse the response into data and metadata.
    const [data, metadata] = await response.json();
    const { title, has_next, has_prev } = metadata;

    // Create the page header and message to display the number of new items.
    createHeader(title);
    appMessage.textContent = '';

    // Create the pagination navigation.
    const nav = document.createElement('nav');
    const ul = document.createElement('ul')
    ul.classList.add("pagination", "justify-content-center");
    nav.appendChild(ul);

    const prevPage = document.createElement("li");
    const aPrev = document.createElement("a");
    const nextPage = document.createElement("li");
    const aNext = document.createElement("a");

    const aPages = [aPrev, aNext];

    [prevPage, nextPage].forEach((page, index) => {
      page.classList.add("page-item");
      aPages[index].classList.add("page-link");
      aPages[index].setAttribute("href", "#");
      page.appendChild(aPages[index]);
      ul.appendChild(page);
    });

    // Set the text content of the pagination navigation.
    aPrev.textContent = "<<<<<";
    aNext.textContent = ">>>>>";

    // Disable the previous and next buttons if there are no previous or next pages, respectively.
    has_prev === 0 ? prevPage.classList.add("disabled") : prevPage.classList.remove("disabled");
    has_next === 0 ? nextPage.classList.add("disabled") : nextPage.classList.remove("disabled");

    // Replace the pager element with the pagination navigation.
    pager.replaceChildren(nav);

    // Create the table HTML and display it.
    table.innerHTML = createCandidateTable(data);

    // Add a click event listener to the pagination navigation to switch pages.
    ul.addEventListener("click", function switchPage(event) {
      const targetElement = event.target as HTMLElement;
      const parentTarget = (targetElement as HTMLElement).parentElement as HTMLElement;
      if (parentTarget.isEqualNode(nextPage) && has_next !== 0) tableView(path, currentPage + 1);
      if (parentTarget.isEqualNode(prevPage) && has_prev !== 0) tableView(path, currentPage - 1);
    }, { once: true });
  };
  tableView(path);
};


/**
 * Creates a table displaying candidate information from an array of candidate objects.
 *
 * @param {Array<object>} candidates - An array of candidate objects containing properties such as id, region, fullname, birthday, status, and deadline.
 * @returns {string} - A string representing the HTML table.
 */
function createCandidateTable(candidates: Array<object>): string {
  countItems();
  // Map over the array of candidates to create an array of table rows.
  const rows = candidates.map(candidate => {

    // Create a table row with the candidate's information.
    return `<tr height="50px">
      <td>${candidate["id" as keyof typeof candidate]}</td>
      <td>${candidate["region" as keyof typeof candidate]}</td>
      <td><a href="#" onclick="openProfile(${candidate['id' as keyof typeof candidate]})">
                                          ${candidate["fullname" as keyof typeof candidate]}</a></td>
      <td>${convertDate(candidate["birthday" as keyof typeof candidate] as string)}</td>
      <td>${candidate["status" as keyof typeof candidate]}</td>
      <td>${convertDate(candidate["deadline" as keyof typeof candidate] as string)}</td>
    </tr>`
  });

  // Define the width and headlines for the table headers.
  const width = ["10%", "15%", "30%", "15%", "15%", "15%"]
  const headlines = ["#", "Регион", "Фамилия Имя Отчество", "Дата рождения", "Статус", "Дата"]

  // Map over the headlines to create an array of table headers.
  const headers = headlines.map((headline, index) => {
    return `<th width=${width[index]}>${headline}</th>`
  });

  // Return the final table.
  return `<table class="table table-hover table-responsive align-middle">
            <thead><tr>${headers.join('')}</tr></thead>
            <tbody>${rows.join('')}</tbody>
          </table>`;
};


async function countItems(): Promise<void> {
  const {news, checks } = await fetch('/count').then(response => response.json());
  
  const badges = document.querySelectorAll('.badge');
  badges[0].innerHTML = news;
  badges[1].innerHTML = checks;
};
setInterval(countItems, 10 * 60 * 1000); // Execute countItems() every 10 minutes (10 * 60 * 1000 milliseconds)


/**
 * Converts a string date value into a formatted date string.
 *
 * @param {string} value - The input date string to be parsed.
 * @return {string} A formatted date string in the format "DD.MM.YYYY".
 */
function convertDate(value: string): string {
  const date = new Date(Date.parse(value));
  const day = date.getDate().toString().padStart(2, '0');
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const year = date.getFullYear().toString();
  return `${day}.${month}.${year}`;
}


/**
 * This function creates a resume form and allows for editing if a candidate ID is provided.
 * @param {object} resume - Optional candidate resume for edit
 * @returns {Promise<void>}
 */
async function createResume(resume: unknown = null): Promise<void> {
  countItems();
  // Fetch user data from server
  let response = await fetch('/login');
  let { user } = await response.json();
  // Redirect to login if the user is not logged in
  if (user === "None") {
    return userLogin("alert-danger", "Для просмотра нужно войти в систему")
  };

  // Create container for resume/upload form
	const fragment = document.createDocumentFragment();
  // Display message and header for resume form
	createMessage("alert-info", "Заполните обязательные поля, либо загрузите файл");
  const header = document.createElement("h5");
  if (!resume) {
    header.textContent = "Создать анкету"
    const divformUpload = document.createElement('div');
    divformUpload.classList.add("py-1");
    divformUpload.innerHTML = formUpload;
    fragment.appendChild(divformUpload);
  } else {
    header.textContent = "Изменить анкету"
  };
	appHeader.replaceChildren(header);

	const divformResume = document.createElement('div');
  divformResume.classList.add("py-1");
  divformResume.innerHTML = formResume;
	const resumeForm = divformResume.children[0] as HTMLFormElement;
	fragment.appendChild(divformResume);
  
	// Add container to app content and clear previous content
  appContent.replaceChildren(fragment);

  // If editing an existing resume, pre-fill form with existing data
  if (resume) {
    window.scrollTo(0,0);
    const inputs = Array.from(resumeForm.getElementsByTagName("input")).slice(0,-2);
    // Filter out unwanted fields and map values to array
    const anketaFiltred = Object.entries(resume)
      .filter(([key]) =>
        !['id', 'region', 'status', 'deadline', 'recruiter', 'addition', 
        'request_id'
        ].includes(key)
      )
      .map(([_, value]) => value);
    // Set input values to filtered values
    inputs.forEach((input, i) => {
      input.setAttribute("value", anketaFiltred[i] as string)
    })
  };
  // Add event listener to form submit button
  resumeForm.addEventListener('submit', function submitData (event) {
    event.preventDefault();
    submitResume("resumeForm", "create");
  }, {once: true});
};


/**
 * Submits the resume from a form to a specified URL using a POST request.
 * @param formId The ID of the form containing the resume.
 * @param url The URL to submit the resume to.
 */
async function submitResume(
  formId: string, 
  url: string
  ) {
  // Get the form and its data
  const form = document.forms.namedItem(formId) as HTMLFormElement;
  const formData = new FormData(form);

  // Send the resume data as a POST request to the specified URL
  const response = await fetch(`/resume/${url}`, { method: "POST", body: formData });
  const { message, cand_id } = await response.json();

  // Update the UI with the message and open the candidate's profile
	createMessage("alert-success", message);
  openProfile(cand_id);
};


/**
 * Opens the profile of a candidate and populates it with their information.
 * @param candId The ID of the candidate whose profile to open.
 */
async function openProfile(candId: number) {
  countItems();
  // Fetch candidate information from server
  const response = await fetch(`/profile/${candId}`)
  const [ anketa, check, registry, poligraf, investigation, inquiry, state ] = await response.json();
  
	const tablist = document.createElement('div');
	tablist.classList.add("nav", "nav-tabs", "nav-justified");
	tablist.setAttribute("role", "tablist");
	
	const tabContent = document.createElement ("div");
  tabContent.classList.add("tab-content");
  
  const anketaId = document.createElement('div');
  const checkId = document.createElement('div');
  const registryId = document.createElement('div');
  const poligrafId = document.createElement('div');
  const investigationId = document.createElement('div');
  const inquiryId = document.createElement('div');
 
  const childDiv = [anketaId, checkId, registryId, poligrafId, investigationId, inquiryId];
  const tabId = ["anketa", "check", "registry", "poligraf", "investigation", "inquiry"];
	const tabNames = ["Анкета", "Проверки", "Согласования", "Полиграф", "Расследования", "Запросы"];

	tabId.forEach((tab, index) => {
		const button = document.createElement('button');
		if (index == 0) {
      button.classList.add("nav-link", "active")
    } else {
      button.classList.add("nav-link")
    };
		button.setAttribute("data-bs-toggle", "tab");
		button.setAttribute("data-bs-target", `#${tab}Tab`);
		button.setAttribute("type", "button");
		button.setAttribute("role", "tab");
		button.textContent = tabNames[index];
		tablist.appendChild(button);
	
    const tabPane = document.createElement('div');
    index == 0 ? tabPane.classList.add("tab-pane", "active", "py-1") : 
      tabPane.classList.add("tab-pane", "py-1");
    tabPane.setAttribute("role", "tabpanel");
    tabPane.setAttribute("id", `${tab}Tab`);
    tabContent.appendChild(tabPane);

    childDiv[index].classList.add("py-3");
    tabPane.appendChild(childDiv[index]);
  });
  // Create a document fragment and add the container to it
  const fragment = document.createDocumentFragment();
  fragment.appendChild(tablist);
  fragment.appendChild(tabContent);

  // Replace the content of the app with the updated fragment
  appContent.replaceChildren(fragment);

  // Create the profile components asynchronously
  Promise.all([
    createAnketa(candId, anketa, state, anketaId),
    createCheck(candId, check, state, anketa[0][0]['status'], checkId),
    createRegistry(candId, registry, state, anketa[0][0]['status'], registryId),
    createPoligraf(candId, poligraf, poligrafId),
    createInvestigation(candId, investigation, investigationId),
    createInquiry(candId, inquiry, inquiryId)
  ]);
};


/**
 * Creates an anketa for a candidate with the given ID and data
 * @param candId - ID of the candidate
 * @param anketa - data to use to create the anketa
 */
function createAnketa(
  candId: number, 
  anketa: Array<Array<object>>, 
  state: object,
  anketaId: HTMLDivElement,
  ) {
  const editResume = document.createElement('button');
  editResume.setAttribute("type", "button");
  editResume.classList.add("btn", "btn-outline-primary");
  editResume.onclick = function () {createResume(anketa[0][0])};
  editResume.textContent = "Изменить  анкету";
  
  //resume labeles and correspondinf forms
  const resumeSubDivNames = ['Резюме', 'Должности', 'Документы', 'Адреса', 'Контакты', 'Работа', 'Связи'];
  const forms = [editResume, formStaff, formDocument, formAddress, formContact, formWorkplace, formRelation
  ];

	// Create header with candidate name as a link to their profile
	const header = document.createElement("h5");
  header.innerHTML = `<a href="#" onclick=openProfile(${candId})>${anketa[0][0]
    ['fullname' as keyof typeof anketa[0][0]]}</a>`;
	appHeader.replaceChildren(header);

  // Create table with labels and data
  const fragment = document.createDocumentFragment();
  resumeSubDivNames.forEach((name, i) => {
    const details = document.createElement('details');
    const summary = document.createElement('summary');
    summary.innerHTML = `<b>${name}</b>`; // Create sub header with name
    details.appendChild(summary);
    const formDiv = document.createElement('div');
    formDiv.classList.add('card', 'card-body', 'py-3');
    i === 0 ? formDiv.replaceChildren(forms[0]) : formDiv.innerHTML = forms[i] as string;
    details.appendChild(formDiv);
    fragment.appendChild(details);
    fragment.appendChild(createItemTable(ANKETA_LABELES[i], anketa[i]));
  });
  
  anketaId.addEventListener('submit', async function (event) {
    event.preventDefault();
    // Get the form element that triggered the submit event
    const form = event.target as HTMLFormElement;
    // Get the path from the form's ID attribute
    const path = (form.getAttribute("id") as string);
    // Send a POST request to the server to update the candidate's information
    const formData = new FormData(form);
    const response = await fetch (`update/${path}/${candId}`, {method: "post", body: formData});
    const { message } = await response.json();
    // Display the message to the user
		createMessage("alert-success", message);
    openProfile(candId)
  });

  // Create div for buttons with appropriate classes
  const resumeBtnGroup = document.createElement('div');
  resumeBtnGroup.classList.add('btn-group', 'hidden-print'); 
  resumeBtnGroup.setAttribute("role", "group");

	const resetStatus = document.createElement('button');
	resetStatus.classList.add("btn", "btn-outline-primary");
	resetStatus.onclick = function () {updateStatus(candId)};
	resetStatus.textContent = "Обновить статус";
  resumeBtnGroup.appendChild(resetStatus)

	const dispatchResume = document.createElement('button');
	dispatchResume.classList.add("btn", "btn-outline-primary");
	dispatchResume.onclick = function () {sendResume(candId)};
	dispatchResume.textContent = "Отправить на проверку";
	resumeBtnGroup.appendChild(dispatchResume)

  fragment.appendChild(resumeBtnGroup); // Add button div to anketa
  anketaId.replaceChildren(fragment); // Replace anketa content with tables and sub headers

	// Disable the send resume button if the state is not NEW or UPDATE.
  if (anketa[0][0]["status" as keyof typeof anketa[0][0]] != state['NEW' as keyof typeof state] && 
			anketa[0][0]["status" as keyof typeof anketa[0][0]] !== state['UPDATE' as keyof typeof state]) {
    dispatchResume.setAttribute("class", "disabled btn btn-outline-success hidden-print");
	};
};


/**
 * Updates candidate status and displays a message
 * @param candId - The candidate ID
 */
async function updateStatus(candId: number): Promise<void> {
  // Fetch the candidate's status
  const response = await fetch(`/resume/status/${candId}`);
  const { message } = await response.json();

  // Display an alert message and open the candidate's profile
		createMessage("alert-info", message);
		openProfile(candId);
    window.scrollTo(0,0);
};


/**
 * Sends the resume of a candidate with the given ID.
 * @param candId - The ID of the candidate to send the resume for.
 * @returns A Promise that resolves when the resume has been sent.
 */
async function sendResume(candId: number): Promise<void> {
  // Send a request to the server to send the resume. Extract the message from the response.
  const response = await fetch(`/resume/send/${candId}`);
  const { message } = await response.json();

  // Create a message and open the candidate's profile once the resume has been sent.
	createMessage("alert-info", message);
  openProfile(candId);
  window.scrollTo(0,0);
};


/**
 * Creates a check for a candidate with the given ID and displays it on the page.
 * @param candId - the ID of the candidate
 * @param check - an array of arrays of objects representing the check to be created
 */
function createCheck(
  candId: number, 
  check: Array<Array<object>>, 
  state: object, 
  status: string,
  checkId: HTMLDivElement
  ) {
  // Create a new 'div' element to hold the buttons for the check
	const checkBtnGroup = document.createElement('div');
  checkBtnGroup.classList.add('btn-group', 'hidden-print');
  checkBtnGroup.setAttribute("role", "group");
  
	// Set the elements of the 'checkBtnGroup' element to three buttons with their onclick events
	const checkBtn = document.createElement('button');
	checkBtn.onclick = function () {checkEditNew(candId, 'new', checkId)};
	const editBtn = document.createElement('button');
	editBtn.onclick = function () {checkEditNew(candId, 'edit', checkId, check[0])};
	const deleteBtn = document.createElement('button');
	deleteBtn.onclick = function () {deleteLastCheck(candId)};

  const buttonLabeles = ["Добавить проверку", "Изменить проверку", "Удалить проверку"];
  [checkBtn, editBtn, deleteBtn].forEach((button, index) => {
    button.classList.add("btn", "btn-outline-primary");
    button.textContent = buttonLabeles[index];
    checkBtnGroup.appendChild(button)
  });
  // Disable check button if the state is not NEW or UPDATE.
	if (status != state['NEWFAG' as keyof typeof state] && status !== state['UPDATE' as keyof typeof state]) {
    checkBtn.setAttribute("class", "disabled btn btn-outline-primary");
  };
  // Disable the edit button if the state is not SAVE or CANSEL.
  if (status !== state['SAVE' as keyof typeof state] && status !== state['CANSEL' as keyof typeof state]) {
    editBtn.setAttribute("class", "disabled btn btn-outline-primary");
  };
  // Disable the delete button if the status is FINISH.
  if (status !== state['FINISH' as keyof typeof state]) {
    deleteBtn.setAttribute("class", "disabled btn btn-outline-primary");
  };

  // Append the elements to the 'checkId' element
	const fragment = document.createDocumentFragment();
	fragment.appendChild(createItemTable(CHECK_LABELES, check));
	fragment.appendChild(checkBtnGroup); // Add button div to anketa
	checkId.replaceChildren(fragment);
};


/**
 * Checks if a candidate profile needs to be edited or if it's new, 
 * and handles the corresponding actions.
 * @param candId - the identifier of the candidate profile to check
 * @param flag - a string indicating whether the profile is being edited or is new
 */
async function checkEditNew(
  candId: number, 
  flag: string,
  checkId: HTMLDivElement,
  check: unknown = null
  ): Promise<void> {
  // If the profile is not being edited, check the status of the profile
  if (flag === "new") {  
    const status = await fetch(`/check/status/${candId}`);
    const { message } = await status.json();
		createMessage("alert-warning", message)
    // If the profile is already being worked on, return to the profile page
    if (message === "Анкета взята в работу и еще не закончена") {
      return openProfile(candId);
    };
  };
  // Create a new form element and import the formCheck HTML
  const form = document.createElement("div");
  form.innerHTML = formCheck;

  // If the profile is being edited, prefill the form with the previous data
  if (flag === "edit") {
    const textareas = Array.from(form.getElementsByTagName("textarea"));
    const checkFiltred = Object.entries(check as object)
      .filter(([key]) =>
        ![
          "id", "autostatus", "path", "pfo", "comments", "conclusion", "deadline", "officer", "cand_id",
        ].includes(key)
      )
      .map(([_, value]) => value);
    textareas.forEach((textarea, i) => {
      textarea.innerHTML = checkFiltred[i] as string;
    });
  }
  // Add a submit event listener to the form, to send the data to the server
  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    const formData = new FormData(form.children[0] as HTMLFormElement);
    const response = await fetch(`/check/${flag}/${candId}`, {
      method: "post",
      body: formData,
    });
    const { message } = await response.json();
    // Show a message and return to the profile page
    Promise.all([
			createMessage("alert-primary", message),
      openProfile(candId),
      window.scrollTo(0,0)
    ]);
  });
  // Replace the content of the checkTabId element with the form element
  checkId.replaceChildren(form);
};

/**
 * Deletes the last check for a candidate.
 * @param candId The ID of the candidate to delete the check for.
 * @returns A Promise that resolves with void when the check has been deleted.
 */
async function deleteLastCheck(candId: number): Promise<void> {
  // Confirm with the user that they want to delete the check.
  if (confirm("Вы действительно хотите удалить проверку?")) {
    // Make a fetch request to delete the check for the candidate.
    let response = await fetch(`/check/delete/${candId}`);
    // Get the message from the response JSON.
    let { message } = await response.json();
    // Create a warning message and open the candidate's profile.
      createMessage("alert-warning", message);
      openProfile(candId);
      window.scrollTo(0,0);
  }
};


/**
 * Creates a registry table and adds a button to add a new item to the table
 * @param candId The candidate ID
 * @param registry The array of registry items
 */
function createRegistry(
  candId: number, 
  registry: Array<Array<object>>, 
  state: object, 
  status: string,
  registryId: HTMLDivElement
  ) {
  // Create a new element to hold the button
  const addRegistryBtn = document.createElement('a');
	addRegistryBtn.classList.add("btn", "btn-outline-info", "hidden-print");
	addRegistryBtn.setAttribute("type", "button");
	addRegistryBtn.setAttribute("id", "addRegistryBtn");
	addRegistryBtn.textContent = "Добавить согласование";

	const fragment = document.createDocumentFragment();
	fragment.appendChild(createItemTable(REGISTRY_LABELES, registry));
	fragment.appendChild(addRegistryBtn);

	// Get the element with ID 'registryId'
	registryId.replaceChildren(fragment);
	
	// Disable the send registry button if the state is not RESULT.
	if (status != state['RESULT' as keyof typeof state]) {
    const sendRegistryButton = document.getElementById('addRegistryBtn') as HTMLButtonElement;
    sendRegistryButton.classList.add("disabled", "btn", "btn-outline-primary", "hidden-print");
  }
  // Call 'createTabAction' function with arguments 'candId', 'registryTabId', 'formRegistry', and 'registry'
  createTabAction(candId, registryId, formRegistry, "registry");
};


/**
 * Creates the poligraf element for a candidate with the provided id and data.
 * @param candId - The id of the candidate.
 * @param poligraf - The data for the poligraf element.
 */
function createPoligraf(
  candId: number, 
  poligraf: Array<Array<object>>,
  poligrafId: HTMLDivElement
  ) {
  // Create a new button to add a new poligraf test.
  const addPoligrafBtn = document.createElement('div');
  addPoligrafBtn.innerHTML = `<a class="btn btn-outline-info hidden-print" type="button">Добавить тестирование</a>`;

	// Replace the children of the poligraf element with a new table.
	const fragment = document.createDocumentFragment();
	fragment.appendChild(createItemTable(POLIGRAF_LABELES, poligraf));
	fragment.appendChild(addPoligrafBtn);
	poligrafId.replaceChildren(fragment);
  // Create a new tab action for the poligraf element.
  createTabAction(candId, poligrafId, formPoligraf, "poligraf");
};


/**
 * Creates an investigation for a candidate and adds it to the page
 * @param candId - the ID of the candidate
 * @param investigation - an array of arrays of objects representing the investigation
 */
function createInvestigation(
  candId: number, 
  investigation: Array<Array<object>>,
  investigationId: HTMLDivElement
  ) {
  // Create a button to add a new investigation and add it to the investigation element
  const addInvestigationBtn = document.createElement('div');
  addInvestigationBtn.innerHTML = `<a class="btn btn-outline-info hidden-print" type="button">Добавить расследование</a>`;
  
	// Replace the current content of the investigation element with a new table created using the provided labels and investigation data
	const fragment = document.createDocumentFragment();
	fragment.appendChild(createItemTable(INVESTIGATION_LABELES, investigation));
	fragment.appendChild(addInvestigationBtn);
	investigationId.replaceChildren(fragment);
	
	// Create a tab action for the investigation using the provided candidate ID and form function
  createTabAction(candId, investigationId, formInvestigation, "investigation");
};


/**
 * Creates an inquiry for a given candidate ID and array of inquiry objects.
 * @param candId - The ID of the candidate to create an inquiry for.
 * @param inquiry - An array of inquiry objects to display.
 */
function createInquiry(
  candId: number, 
  inquiry: Array<Array<object>>,
  inquiryId: HTMLDivElement
  ) {
    // Create and append a "Add Inquiry" button to the inquiry ID.
  const addInquiryBtn = document.createElement('div');
  addInquiryBtn.innerHTML = `<a class="btn btn-outline-info hidden-print" type="button">Добавить запрос</a>`;

	// Replace the children of the inquiry ID with a new item table.
	const fragment = document.createDocumentFragment();
	fragment.appendChild(createItemTable(INQUIRY_LABELES, inquiry));
	fragment.appendChild(addInquiryBtn);
	inquiryId.replaceChildren(fragment);

  // Create a tab action for the inquiry tab.
  createTabAction(candId, inquiryId, formInquiry, "inquiry");
};


/**
 * Creates an action listener that displays a form in a tab and submits the form data to the server
 * @param candId - The ID of the candidate
 * @param tabId - The ID of the tab in which to display the form
 * @param formHTML - The HTML content of the form to display
 * @param path - The path to post the form data to on the server
 */
function createTabAction(
  candId: number,
  parentDiv: HTMLDivElement,
  formHTML: string,
  path: string
  ) {
  // Get the "add" button element. Add a click listener to the "add" button
  const addBtnListener = parentDiv.children[1] as HTMLElement;
  addBtnListener.addEventListener('click', function (event){
    // Replace the tab content with the form HTML
    const container = document.createElement('div');
    container.innerHTML = formHTML;
    const fragment = document.createDocumentFragment();
    fragment.appendChild(container);
    parentDiv.replaceChildren(fragment);

    // Get the form element. Add a submit listener to the form
    const form = parentDiv.children[0].children[0] as HTMLFormElement;
    form.addEventListener('submit', async function (event: any){
      event.preventDefault(); // Prevent default form submission

      // Post the form data to the server
      const formData = new FormData(form);
      const response = await fetch(`/${path}/${candId}`, {method: "post", body: formData});
      const { message } = await response.json();

      // Call the openProfile function and create a message
      createMessage("alert-primary", message),
      openProfile(candId),
      window.scrollTo(0,0)
    }, {once: true});
  }, {once: true});
};


/**
 * Creates a table with candidate profiles
 * @param names - an array of strings representing the column names
 * @param response - an array of objects representing the candidate profiles
 * @returns a string representing an HTML table with the candidate profiles
 */
function createItemTable(
  names: string[], 
  response: Array<object>
  ) {
  // if there are no profiles, return a message indicating so
  if (!response.length) {
    const paragraph = document.createElement('p');
    paragraph.innerHTML = "Данные отсутствуют";
    return paragraph
  };
  // map each profile object to an HTML table row
  const rows = response.map((item) => {
    // map each column name to an HTML table cell
    return names.map((name, i) => {
      // if the current column is 'deadline' or 'birthday', format the date
      if (Object.keys(item)[i] === 'deadline' || Object.keys(item)[i] === 'birthday') {
        const date = new Date(Object.values(item)[i]);
        return `<tr><td width="25%">${name}</td><td>${date.toLocaleDateString('ru-RU')}</td></tr>`;
      // if the current column is 'id' create subheaders
      } else if (Object.keys(item)[i] === 'id' ) {
        return `<tr height="50px"><th colspan="2">${name} #${Object.values(item)[i]}</th></tr>`;
      } else if (Object.keys(item)[i] === 'path' ) {
        return `<tr><td width="25%">${name}</td><td><a href="${Object.values(item)[i]}">Открыть</a></td></tr>`;
      // else create row
      } else {
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

  return container;
};


/**
 * Opens the page with statistical information.
 * @returns {Promise<void>}
 */
async function statInfo(flag=false): Promise<void> {
  countItems();
  // Check if new page opened or reload and create form Info
  if (!flag) {
    const fragment = document.createDocumentFragment();
    for (let i = 0; i < 3; i++) {
      const div = document.createElement("div");
      div.classList.add("py-3");
      if (i == 2) {div.innerHTML = formInfo};
      fragment.appendChild(div);
    };
    appContent.replaceChildren(fragment);
  };
  // Get the form and its data. Send a POST.
  const form = appContent.children[2].children[0] as HTMLFormElement;
  const dataForm = new FormData(form);
  const response = await fetch('/information', {
      method: "post", body: dataForm
  });
  const { title, candidates, poligraf } = await response.json();

  // Create Header
	const header = document.createElement('h5');
  header.textContent = title;
	appHeader.replaceChildren(header);
  // Set the innerHTML of appMessage to an empty string
  appMessage.innerHTML = '';

  // Set the appendChild of divCandTable and divPfoTable fragments to the tables
  appContent.children[0].replaceChildren(createStatTable(candidates, "Статистика по кандидатам"));
  appContent.children[1].replaceChildren(createStatTable(poligraf, "Статистика по ПФО"));

  // Add an event listener to the form that calls statInfo when submitted
  form.addEventListener('submit', (event: any) => {
    event.preventDefault();
    statInfo(true);  
  }, {once: true});
}


/**
 * Creates a table element with the specified stats and caption
 * @param stats Array of objects with key-value pairs to be displayed in the table
 * @param caption Caption for the table
 * @returns A table element with the specified stats and caption
 */
function createStatTable(
  stats: Array<object>, 
  caption: string
  ): HTMLTableElement {
  // Create the table element
  const table = document.createElement("table");
  table.classList.add("table", "table-hover", "align-middle");
  // Set the inner HTML of the table element
  table.innerHTML = `
    <caption>${caption}</caption>
    <thead><tr><th>Решение</th><th>Количество</th></tr></thead>
    <tbody>
      ${stats.map(stat => `
        <tr height="50px">
          <td>${Object.keys(stat)}</td><td>${Object.values(stat)}</td>
        </tr>
      `).join('')}
    </tbody>
  `;
  return table;
};


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


const formSearch: string = `
  <form id="searchForm" onsubmit="return false">
      <div class="row">
          <div class="col-md-2">
              <div class="mb-3">
                  <label class="visually-hidden" for="region">Region</label>
                  <select class="form-select mb-2 mr-sm-2 mb-sm-0" id="region" name="region">
                      <option value="">По региону</option>
                      <option value="Главный офис">Главный офис</option>
                      <option value="Томск">Томск</option><option value="РЦ Запад">РЦ Запад</option>
                      <option value="РЦ Юг">РЦ Юг</option><option value="РЦ Запад">РЦ Запад</option>
                      <option value="РЦ Урал">РЦ Урал</option>
                  </select>
              </div>
          </div>
          <div class="col-md-4">
              <div class="mb-3">
                  <label class="visually-hidden" for="fullname">Fullname</label>
                  <input class="form-control mb-2 mr-sm-2 mb-sm-0" id="fullname" maxlength="250" minlength="3" name="fullname" placeholder="поиск по ФИО" type="text" value="">
              </div>
          </div>
              <div class="col-md-2">
                  <div class="mb-3">
                      <label class="visually-hidden" for="birthday">Birthday</label>
                      <input class="form-control mb-2 mr-sm-2 mb-sm-0" id="birthday" name="birthday" placeholder="по дате рождения" type="date" value="">
                  </div>
              </div>
              <div class="col-md-2">
              <div class="mb-3">
                  <label class="visually-hidden" for="status">Status</label>
                  <select class="form-select mb-2 mr-sm-2 mb-sm-0" id="status" name="status">
                      <option value="">По статусу</option>
                      <option value="Новый">Новый</option>
                      <option value="Обновлен">Обновлен</option>
                      <option value="Проверка">Проверка</option>
                      <option value="Сохранено">Сохранено</option>
                      <option value="Автомат">Автомат</option>
                      <option value="Робот">Робот</option>
                      <option value="Обработано">Обработано</option>
                      <option value="ПФО">ПФО</option>
                      <option value="Результат">Результат</option>
                      <option value="Окончено">Окончено</option>
                      <option value="Отмена">Отмена</option>
                      <option value="Ошибка">Ошибка</option>
                  </select>
              </div>
          </div>
          <div class="col">
              <input class="btn btn-primary btn-md" id="submit" name="submit" type="submit" value="Найти">
          </div>
      </div>
  </form>`;

const formLogin: string= `
  <form action="" id="loginForm" method="post" class="form form-check" role="form" onsubmit="return false">
      <div class="mb-3 row required">
          <label class="col-form-label col-lg-1" for="username">Логин: </label>
          <div class="col-lg-4">
              <input autocomplete="username" class="form-control" id="username" maxlength="25" name="username" placeholder="Имя пользователя" required="" type="text" value="">
          </div>
      </div>
      <div class="mb-3 row required">
          <label class="col-form-label col-lg-1" for="password">Пароль: </label>
              <div class="col-lg-4">
                  <input autocomplete="current-password" class="form-control" id="password" maxlength="25" name="password" placeholder="Пароль" required="" type="password" value="">
              </div>
          </div>
      <div class=" row">
          <div class="offset-lg-1 col-lg-4">
              <div class="mb-3 form-check"><input class="form-check-input" id="remember" name="remember" type="checkbox" value="y">
                  <label class="form-check-label" for="remember">Запомнить </label>
              </div>
          </div>
      </div>
      <div class=" row">
          <div class="offset-lg-1 col-lg-4">
              <input class="btn btn-primary btn-md" id="submit" name="submit" type="submit" value="Войти">
          </div>
      </div>
  </form>`;

const formUpload: string = `
  <form action="" id="formFile" method="post" class="form form-check" enctype="multipart/form-data" role="form" onchange="submitResume('formFile', 'upload')">
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="file">Загрузить файл</label>
        <div class="col-lg-10">
            <input class="form-control" id="file" name="file" type="file">    
        </div>
    </div>
  </form>`;

const formResume: string = `
<form action="" id="resumeForm" method="post" class="form form-check" role="form" onsubmit="return false">
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="region">Регион</label>
        <div class="col-lg-10">
            <select class="form-select" id="region" name="region">
                <option value="ГО">ГО</option>
                <option value="Томск">Томск</option>
                <option value="РЦ Запад">РЦ Запад</option>
                <option value="РЦ Юг">РЦ Юг</option>
                <option value="РЦ Запад">РЦ Запад</option>
                <option value="РЦ Урал">РЦ Урал</option>
            </select>
        </div>
    </div>
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="fullname">Полное ФИО</label>
        <div class="col-lg-10">
            <input class="form-control" id="fullname" maxlength="250" name="fullname" required="" type="text" value="">
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="previous">Изменение имени</label>
        <div class="col-lg-10">
            <input class="form-control" id="previous" maxlength="250" name="previous" type="text" value="">
        </div>
        </div>
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="birthday">Дата рождения</label>
        <div class="col-lg-10">
            <input class="form-control" id="birthday" name="birthday" required="" type="date" value="">
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="birthplace">Место рождения</label>
        <div class="col-lg-10">
            <input class="form-control" id="birthplace" maxlength="250" name="birthplace" type="text" value="">
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="country">Гражданство</label>
        <div class="col-lg-10">
            <input class="form-control" id="country" maxlength="50" name="country" type="text" value="">
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="snils">СНИЛС</label>
        <div class="col-lg-10">
            <input class="form-control" id="snils" maxlength="11" minlength="11" name="snils" type="text" value="">
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="inn">ИНН</label>
        <div class="col-lg-10">
            <input class="form-control" id="inn" maxlength="12" minlength="12" name="inn" type="text" value="">
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="education">Образование</label>
        <div class="col-lg-10">
            <input class="form-control" id="education" maxlength="250" name="education" type="text" value="">
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="addition">Дополнительно</label>
        <div class="col-lg-10">
            <textarea class="form-control" id="addition" name="addition"></textarea>
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="recruiter">Рекрутер</label>
        <div class="col-lg-10">
            <input class="form-control" id="recruiter" maxlength="250" name="recruiter" type="text" value="">
        </div>
    </div>
    <div class=" row">
        <div class="offset-lg-2 col-lg-10">
            <input class="btn btn-primary btn-md" id="submit" name="submit" type="submit" value="Принять">
        </div>
    </div>
  </form>`;

const formCheck: string = `
  <form action="" id="checkFormId" method="post" class="form form-check" role="form" onsubmit="return false">
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="workplace">Проверка по месту работы</label>
        <div class="col-lg-10">
            <textarea class="form-control" id="workplace" name="workplace"></textarea>
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="employee">Проверка по кадровому учету</label>
        <div class="col-lg-10">
            <textarea class="form-control" id="employee" name="employee"></textarea>
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="document">Проверка документов</label>
        <div class="col-lg-10">
            <textarea class="form-control" id="document" name="document"></textarea>
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="inn">Проверка паспорта</label>
        <div class="col-lg-10">
            <textarea class="form-control" id="inn" name="inn"></textarea>
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="debt">Проверка задолженностей</label>
        <div class="col-lg-10">
            <textarea class="form-control" id="debt" name="debt"></textarea>
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="bankruptcy">Проверка банкротства</label>
        <div class="col-lg-10">
            <textarea class="form-control" id="bankruptcy" name="bankruptcy"></textarea>
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="bki">Проверка кредитной истории</label>
        <div class="col-lg-10">
            <textarea class="form-control" id="bki" name="bki"></textarea>
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="courts">Проверка по решениям судов</label>
        <div class="col-lg-10">
            <textarea class="form-control" id="courts" name="courts"></textarea>
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="affiliation">Проверка аффилированности</label>
        <div class="col-lg-10">
            <textarea class="form-control" id="affiliation" name="affiliation"></textarea>
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="terrorist">Проверка списка террористов</label>
        <div class="col-lg-10">
            <textarea class="form-control" id="terrorist" name="terrorist"></textarea>
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="mvd">Проверка учетам МВД</label>
        <div class="col-lg-10">
            <textarea class="form-control" id="mvd" name="mvd"></textarea>
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="internet">Проверка по открытым источникам</label>
        <div class="col-lg-10">
            <textarea class="form-control" id="internet" name="internet"></textarea>
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="cronos">Проверка Кронос</label>
        <div class="col-lg-10">
            <textarea class="form-control" id="cronos" name="cronos"></textarea>
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="cros">Проверка Крос</label>
        <div class="col-lg-10">
            <textarea class="form-control" id="cros" name="cros"></textarea>
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="addition">Дополнительная информация</label>
        <div class="col-lg-10">
            <textarea class="form-control" id="addition" name="addition"></textarea>
        </div>
    </div>
    <div class=" row">
        <div class="offset-lg-2 col-lg-10">
            <div class="mb-3 form-check"><input class="form-check-input" id="pfo" name="pfo" type="checkbox" value="y">
                <label class="form-check-label" for="pfo">Полиграф</label>
            </div>
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="conclusion">Результат</label>
        <div class="col-lg-10">
            <select class="form-select" id="conclusion" name="conclusion">
                <option value="Без замечаний">Без замечаний</option>
                <option value="С комментарием">С комментарием</option>
                <option value="Негатив">Негатив</option>
                <option value="Отмена">Отмена</option>
                <option value="Сохранено">Сохранено</option>
            </select>
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="comments">Комментарий</label>
        <div class="col-lg-10">
            <input class="form-control" id="comments" maxlength="250" name="comments" type="text" value="">
        </div>
    </div>
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="deadline">Дата проверки</label>
        <div class="col-lg-10">
            <input class="form-control" id="deadline" name="deadline" required="" type="date" value="2023-05-16">
        </div>
    </div>
    <div class=" row">
        <div class="offset-lg-2 col-lg-10">
            <input class="btn btn-primary btn-md" id="submit" name="submit" type="submit" value="Принять">
        </div>
    </div>
  </form>`;

const formRegistry: string = `
  <form action="" id="registryFormId" method="post" class="form form-check" role="form" onsubmit="return false">
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="comments">Комментарий</label>
        <div class="col-lg-10">
            <textarea class="form-control" id="comments" name="comments"></textarea>
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="decision">Решение</label>
        <div class="col-lg-10">
            <select class="form-select" id="decision" name="decision"><option value="СОГЛАСОВАНО">СОГЛАСОВАНО</option><option value="СОГЛАСОВАНО С КОММЕНТАРИЕМ">СОГЛАСОВАНО С КОММЕНТАРИЕМ</option><option value="СОГЛАСОВАНО С РИСКОМ">СОГЛАСОВАНО С РИСКОМ</option><option value="ОТКАЗАНО В СОГЛАСОВАНИИ">ОТКАЗАНО В СОГЛАСОВАНИИ</option><option value="Отмена">Отмена</option></select>
        </div>
    </div>
        <div class=" row">
        <div class="offset-lg-2 col-lg-10">
            <input class="btn btn-primary btn-md" id="submit" name="submit" type="submit" value="Принять">
        </div>
    </div>
  </form>`;

const formPoligraf: string = `
  <form action="" id="poligrafFormId" method="post" class="form form-check" role="form" onsubmit="return false">
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="theme">Тема проверки</label>
        <div class="col-lg-10">
            <select class="form-select" id="theme" name="theme"><option value="Проверка кандидата">Проверка кандидата</option><option value="Служебная проверка">Служебная проверка</option><option value="Служебное расследование">Служебное расследование</option><option value="Другое">Другое</option></select>
        </div>
    </div>
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="results">Информация</label>
        <div class="col-lg-10">
            <textarea class="form-control" id="results" name="results" required=""></textarea>
        </div>
    </div>
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="deadline">Дата проведения</label>
        <div class="col-lg-10">
            <input class="form-control" id="deadline" name="deadline" required="" type="date" value="2023-05-16">
        </div>
    </div>
    <div class=" row">
        <div class="offset-lg-2 col-lg-10">
            <input class="btn btn-primary btn-md" id="submit" name="submit" type="submit" value="Принять">
        </div>
    </div>
  </form>`;

const formInvestigation: string = `
  <form action="" id="investigationFormId" method="post" class="form form-check" role="form" onsubmit="return false">
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="theme">Тема проверки</label>
        <div class="col-lg-10">
            <input class="form-control" id="theme" maxlength="250" name="theme" required="" type="text" value="">
        </div>
    </div>
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="info">Информация</label>
        <div class="col-lg-10">
            <textarea class="form-control" id="info" name="info" required=""></textarea>
        </div>
    </div>
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="deadline">Дата проверки</label>
        <div class="col-lg-10">
            <input class="form-control" id="deadline" name="deadline" required="" type="date" value="2023-05-16">
        </div>
    </div>
    <div class=" row">
        <div class="offset-lg-2 col-lg-10">
            <input class="btn btn-primary btn-md" id="submit" name="submit" type="submit" value="Принять">
        </div>
    </div>
  </form>`;

const formInquiry: string = `
  <form action="" id="inquiryFormId" method="post" class="form form-check" role="form" onsubmit="return false">
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="info">Информация</label>
        <div class="col-lg-10">
            <textarea class="form-control" id="info" name="info" required=""></textarea>
        </div>
    </div>
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="initiator">Инициатор</label>
        <div class="col-lg-10">
            <input class="form-control" id="initiator" maxlength="250" name="initiator" required="" type="text" value="">
        </div>
    </div>
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="source">Источник</label>
        <div class="col-lg-10">
            <input class="form-control" id="source" maxlength="250" name="source" required="" type="text" value="">
        </div>
    </div>
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="deadline">Дата запроса</label>
        <div class="col-lg-10">
            <input class="form-control" id="deadline" name="deadline" required="" type="date" value="2023-05-16">
        </div>
    </div>
    <div class=" row">
        <div class="offset-lg-2 col-lg-10">
            <input class="btn btn-primary btn-md" id="submit" name="submit" type="submit" value="Принять">
        </div>
    </div>
  </form>`;

const formStaff: string = `
  <form action="" id="staff" method="post" class="form form-check" role="form" onsubmit="return false">
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="position">Должность</label>
        <div class="col-lg-10">
            <input class="form-control" id="position" maxlength="250" name="position" required="" type="text" value="">
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="department">Деператамент/Кластер</label>
        <div class="col-lg-10">
            <input class="form-control" id="department" maxlength="250" name="department" type="text" value="">
        </div>
    </div>
    <div class=" row">
        <div class="offset-lg-2 col-lg-10">
            <input class="btn btn-primary btn-md" id="submit" name="submit" type="submit" value="Принять">
        </div>
    </div>
  </form>`;

const formDocument: string = `
  <form action="" id="document" method="post" class="form form-check" role="form" onsubmit="return false">
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="view">Выбрать</label>
        <div class="col-lg-10">
            <select class="form-select" id="view" name="view"><option value="Паспорт гражданина России">Паспорт гражданина России</option><option value="Иностранный документ">Иностранный документ</option><option value="Другое">Другое</option></select>
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="series">Серия документа</label>
        <div class="col-lg-10">
            <input class="form-control" id="series" maxlength="25" name="series" type="text" value="">
        </div>
    </div>
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="number">Номер документа</label>
        <div class="col-lg-10">
            <input class="form-control" id="number" maxlength="25" name="number" required="" type="text" value="">
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="agency">Орган выдавший</label>
        <div class="col-lg-10">
            <input class="form-control" id="agency" maxlength="250" name="agency" type="text" value="">
        </div>
    </div>
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="issue">Дата выдачи</label>
        <div class="col-lg-10">
            <input class="form-control" id="issue" name="issue" required="" type="date" value="">
        </div>
    </div>
    <div class=" row">
        <div class="offset-lg-2 col-lg-10">
            <input class="btn btn-primary btn-md" id="submit" name="submit" type="submit" value="Принять">
        </div>
    </div>
  </form>`;

const formAddress: string = `
  <form action="" id="address" method="post" class="form form-check" role="form" onsubmit="return false">
      <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="view">Выбрать</label>
          <div class="col-lg-10">
              <select class="form-select" id="view" name="view"><option value="Адрес регистрации">Адрес регистрации</option><option value="Адрес проживания">Адрес проживания</option><option value="Другое">Другое</option></select>
          </div>
      </div>
      <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="region">Регион</label>
          <div class="col-lg-10">
              <input class="form-control" id="region" maxlength="250" name="region" type="text" value="">
          </div>
      </div>
      <div class="mb-3 row required">
          <label class="col-form-label col-lg-2" for="address">Полный</label>
          <div class="col-lg-10">
              <input class="form-control" id="address" maxlength="250" name="address" required="" type="text" value="">
          </div>
      </div>
      <div class=" row">
          <div class="offset-lg-2 col-lg-10">
              <input class="btn btn-primary btn-md" id="submit" name="submit" type="submit" value="Принять">
          </div>
      </div>
  </form>`;

const formContact: string = `
  <form action="" id="contact" method="post" class="form form-check" role="form" onsubmit="return false">
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="view">Выбрать</label>
        <div class="col-lg-10">
            <select class="form-select" id="view" name="view">
                <option value="Телефон">Телефон</option>
                <option value="E-mail">E-mail</option>
                <option value="Другое">Другое</option>
            </select>
        </div>
    </div>
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="contact">Контакт</label>
        <div class="col-lg-10">
            <input class="form-control" id="contact" maxlength="250" name="contact" required="" type="text" value="">
        </div>
    </div>
    <div class=" row">
        <div class="offset-lg-2 col-lg-10">
            <input class="btn btn-primary btn-md" id="submit" name="submit" type="submit" value="Принять">
        </div>
    </div>
  </form>`;

const formWorkplace: string = `
  <form action="" id="workplace" method="post" class="form form-check" role="form" onsubmit="return false">
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="period">Период работы</label>
        <div class="col-lg-10">
            <input class="form-control" id="period" maxlength="25" name="period" type="text" value="">
        </div>
    </div>
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="workplace">Место работы</label>
        <div class="col-lg-10">
            <input class="form-control" id="workplace" maxlength="250" name="workplace" required="" type="text" value="">
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="address">Адрес организации</label>
        <div class="col-lg-10">
            <input class="form-control" id="address" maxlength="250" name="address" type="text" value="">
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="position">Должность</label>
        <div class="col-lg-10">
            <input class="form-control" id="position" maxlength="250" name="position" type="text" value="">
        </div>
    </div>
    <div class=" row">
        <div class="offset-lg-2 col-lg-10">
            <input class="btn btn-primary btn-md" id="submit" name="submit" type="submit" value="Принять">
        </div>
    </div>
  </form>`;
    
const formRelation: string = `
  <form action="" id="relation" method="post" class="form form-check" role="form" onsubmit="return false">
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="relation">Вид связи</label>
        <div class="col-lg-10">
            <select class="form-select" id="relation" name="relation">
                <option value="Отец/Мать">Отец/Мать</option>
                <option value="Брат/Сестра">Брат/Сестра</option>
                <option value="Супруг">Супруг</option>
                <option value="Дети">Дети</option>
                <option value="Другое">Другое</option>
            </select>
        </div>
    </div>
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="fullname">Полное ФИО</label>
        <div class="col-lg-10">
            <input class="form-control" id="fullname" maxlength="250" name="fullname" required="" type="text" value="">
        </div>
    </div>
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="birthday">Дата рождения</label>
        <div class="col-lg-10">
            <input class="form-control" id="birthday" name="birthday" required="" type="date" value="">
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="address">Адрес</label>
        <div class="col-lg-10">
            <input class="form-control" id="address" maxlength="250" name="address" type="text" value="">
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="workplace">Место работы</label>
        <div class="col-lg-10">
            <input class="form-control" id="workplace" maxlength="250" name="workplace" type="text" value="">
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="contact">Контакт</label>
        <div class="col-lg-10">
            <input class="form-control" id="contact" maxlength="250" name="contact" type="text" value="">
        </div>
    </div>
    <div class=" row">
        <div class="offset-lg-2 col-lg-10">
            <input class="btn btn-primary btn-md" id="submit" name="submit" type="submit" value="Принять">
        </div>
    </div>
</form>`;

const formInfo: string = `
  <form action="" id="infoForm" method="post" class="form form-check" role="form" onsubmit="return false">
      <div class="mb-3 row required">
          <label class="col-form-label col-md-2" for="start">Начало периода</label>
          <div class="col-md-2">
              <input class="form-control" id="start" name="start" required="" type="date" value="2023-05-01">
          </div>
      </div>
      <div class="mb-3 row required">
          <label class="col-form-label col-md-2" for="end">Конец периода</label>
          <div class="col-md-2">
              <input class="form-control" id="end" name="end" required="" type="date" value="2023-05-18">
          </div>
      </div>
      <div class=" row">
          <div class="offset-md-2 col-md-2">
              <input class="btn btn-primary btn-md" id="submit" name="submit" type="submit" value="Принять">
          </div>
      </div>
  </form>`;