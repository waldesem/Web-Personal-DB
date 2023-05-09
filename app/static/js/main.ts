'use strict';

class Application{

  appContainer = document.getElementById('App') as HTMLDivElement;
  appMessage = document.createElement("div") as HTMLDivElement;
  appHeader = document.createElement("div") as HTMLDivElement;
  appContent = document.createElement("div") as HTMLDivElement;

  /* Приведенный код определяет функцию-конструктор, которая устанавливает атрибуты для трех
  элементов (appMessage, appHeader и appContent) и добавляет их к элементу appContainer.
  Устанавливаемые атрибуты включают класс и идентификатор. */
  constructor(){
    for (let elem of [this.appMessage, this.appHeader, this.appContent]){
      this.appContainer.appendChild(elem)
    };

    this.appMessage.setAttribute("class", "container py-3");
    this.appMessage.setAttribute("id", "appMessage");

    this.appHeader.setAttribute("class", "container py-3");
    this.appHeader.setAttribute("id", "appHeader");

    this.appContent.setAttribute("class", "container py-3");
    this.appContent.setAttribute("id", "appContent");
    
    this.auth();
  };

  //проверка авторизации
  async auth () {
    let response = await fetch('/login');
    let { user } = await response.json();
    if (user != "None") {mainPage('/index/main/')} else {userLogin()}
  };

  /**
   * Creates and displays a message on the application.
   * 
   * @param {string} info - The type of message to display (e.g. "success", "error", etc.)
   * @param {string} text - The text to display in the message.
   */
  createMessage(info: string, text: string) {
    // Set the inner HTML of the appMessage element to a message div with the provided info and text.
    this.appMessage.innerHTML = `
      <div class="${info}" role="alert">
      ${text}
      </div>
    `;
  };

  /**
   * Creates a header element with the given text and sets it as the innerHTML of appHeader element.
   * @param text - The text to be displayed in the header element.
   */
  createHeader(text: string) {
    // Create a new h5 element
    const head = document.createElement("h5");
    // Set the innerHTML of the h5 element to the given text
    head.innerHTML = text;
    // Set the innerHTML of appHeader to the outerHTML of the h5 element
    this.appHeader.innerHTML = head.outerHTML;
  };
};


function userLogin() {
  main.createMessage("alert alert-info", "Авторизуйтесь чтобы продолжить работу");
  main.createHeader("Вход в систему");

  const appContent = document.querySelector('#appContent') as HTMLElement;
  appContent.innerHTML = formLogin;
  const loginForm = document.forms.namedItem("loginFormId") as HTMLFormElement;

  loginForm.addEventListener('submit', async function submitData (event: any){
    event.preventDefault();
    const formData = new FormData(loginForm);

    let response = await fetch('/login', {
      method: 'POST',
      body: formData
    });
    let { user } = await response.json();
    if (user == "None") {
      main.createMessage("alert alert-warning", "Неверный логин или пароль");
    } else {
      mainPage('/index/main/');
      loginForm.removeEventListener('submit', submitData)
    }
  });
};

function userLogout() {
	Promise.all([
		fetch('logout'),
		userLogin()
	])
};

async function mainPage(path: string, currentPage=1){

  let divSearch = document.getElementById("searchExtFormId");
  if (!divSearch) {
    let temp = document.createElement("div") as HTMLElement;
    divSearch = document.createElement("div");
    divSearch.setAttribute("class", "py-2");
    divSearch.innerHTML = formSearch;
    
    const divTable = document.createElement("div");
    divTable.setAttribute("class", "py-2");
    divTable.setAttribute("id", "divTable");

    const divPager = document.createElement("div");
    divPager.setAttribute("class", "py-2");
    divPager.setAttribute("id", "divPager");
    
    [divSearch, divTable, divPager].forEach(function (item) {
      temp.appendChild(item);
    });

    const appContent = document.getElementById("appContent") as HTMLElement;
    appContent.innerHTML = temp.outerHTML;

    const form = document.forms.namedItem("searchExtFormId") as HTMLFormElement;
    form.addEventListener("submit", () => {
      mainPage("/index/search/");
    });
  };

  let response: Response;
  if (path == '/index/search/') {
    const searchExtFormId = document.forms.namedItem("searchExtFormId") as HTMLFormElement;
    const form = new FormData(searchExtFormId);

    response = await fetch(`/index/search/${currentPage}`, {
      method: "post",
      body: form
    })
  } else {
    try {
      response = await fetch(`${path}${currentPage}`)
      const [data, metadata] = await response.json();
      const { items, title, has_next, has_prev } = metadata;
      main.createMessage(
        "alert alert-info",
        `<a href="#" onclick="mainPage('/index/new/'); return false;">Новых анкет: ${items}</a>`
      );
      main.createHeader(title);
      createCandidateTable(data);
      switchPage(has_next, has_prev , currentPage, path);
    } catch (error) {
      userLogin();
    }
  };
};


function createCandidateTable(candidates: Array<Object>) {
  const table = document.createElement("table") as HTMLTableElement;
  table.setAttribute("class", "table table-hover table-responsive align-middle py-1");

  const thead = document.createElement('thead') as HTMLElement;
  table.appendChild(thead);

  const tr = document.createElement('tr');
  const candTableHeadlines = ["#", "Регион", "Фамилия Имя Отчество", "Дата рождения", "Статус", "Дата"];

  let tabbleAttrs = ["5%", "15%", "30%", "15%", "15%", "15%"];
  for (let i = 0; i < candTableHeadlines.length; i++) {
    let th = document.createElement('th');
    th.setAttribute("width", tabbleAttrs[i]);
    th.textContent = candTableHeadlines[i];
    tr.appendChild(th);
  }
  thead.appendChild(tr);

  const tbody = document.createElement('tbody');
  const fragment = document.createDocumentFragment();

  for (const candidate of candidates) {
    const tr = document.createElement('tr');
    tr.setAttribute('height', '50px');

    for (const [key, value] of Object.entries(candidate)) {
      const td = document.createElement('td');

      if (key === 'fullname') {
        const link = document.createElement('a');
        link.href = '#';
				link.onclick = () => openProfile((candidate as {id: number})['id']);
        link.textContent = value as string;
        td.appendChild(link);

      } else if (key === 'deadline' || key === 'birthday') {
        const date = new Date(Date.parse(value as string));
        td.textContent = date.toLocaleDateString('ru-RU');
      } else {
        td.textContent = value as string;
      }
      tr.appendChild(td);
    }
    fragment.appendChild(tr);
  }
  tbody.appendChild(fragment);
  table.appendChild(tbody);

  const divTable = document.getElementById('divTable') as HTMLElement;
  divTable.innerHTML = '';
  divTable.appendChild(table);
};

function switchPage(has_next: number, has_prev: number, currentPage: number, path: string): void {
  const paginationElement = document.querySelector(".pagination") as HTMLElement;
  if (!paginationElement){
    const pagerFragment = document.createDocumentFragment();
    const pagerUl = document.createElement("ul") as HTMLElement;
    pagerUl.setAttribute("class", "pagination justify-content-center");
    pagerFragment.appendChild(pagerUl);

    const pageItemPrev = document.createElement('li') as HTMLElement;
    pageItemPrev.setAttribute("class", "page-item"); 
    pageItemPrev.setAttribute("id", "prevPage");
    pagerUl.appendChild(pageItemPrev);

    const pageLinkPrev = document.createElement('a') as HTMLAnchorElement;
    pageLinkPrev.setAttribute("class", "page-link");
    pageLinkPrev.setAttribute("href", "#");
    pageLinkPrev.innerHTML = "Предыдущая";
    pageItemPrev.appendChild(pageLinkPrev);

    const pageItemNext = document.createElement('li') as HTMLElement;
    pageItemNext.setAttribute("class", "page-item"); 
    pageItemNext.setAttribute("id", "nextPage");
    pagerUl.appendChild(pageItemNext);

    const pageLinkNext = document.createElement('a') as HTMLAnchorElement;
    pageLinkNext.setAttribute("class", "page-link");
    pageLinkNext.setAttribute("href", "#");
    pageLinkNext.innerHTML = "Следующая";
    pageItemNext.appendChild(pageLinkNext);

    const navPager = document.createElement('nav') as HTMLElement;
    navPager.appendChild(pagerFragment);

    const divPager = document.getElementById('divPager') as HTMLElement;
    divPager.innerHTML = navPager.outerHTML;
  }
  const divPager = document.getElementById('divPager') as HTMLElement;
  divPager.addEventListener('click', function clickPage (event) {
    const target = event.target as HTMLElement;
    const parentTarget = target.parentElement as HTMLElement;

    if (parentTarget.matches('#nextPage') && has_next !== 0) {
      mainPage(path, currentPage + 1);
    } else if (parentTarget.matches('#prevPage') && has_prev !== 0) {
      mainPage(path, currentPage - 1);
    } else {
			mainPage(path, currentPage);
		}
    divPager.removeEventListener('click', clickPage);
  });

  const nextPage = document.getElementById('nextPage') as HTMLElement;
  if (has_next === 0) {
    nextPage.classList.add('disabled');
  } else {
    nextPage.classList.remove('disabled');
  }
  const prevPage = document.getElementById('prevPage') as HTMLElement;
  if (has_prev === 0) {
    prevPage.classList.add('disabled');
  } else {
    prevPage.classList.remove('disabled');
  }
};


// страница для заполнения/редактирования анкеты
function createResume(resume = null) {
  main.createMessage('alert alert-info', "Заполните обязательные поля, либо загрузите файл");
  main.createHeader("Создать/изменить анкету");

  const resumePage = document.createElement('div') as HTMLDivElement;

  const divformUpload = document.createElement("div");
  divformUpload.setAttribute("class", "py-2");
  divformUpload.setAttribute("id", "divformUpload");
  divformUpload.innerHTML = `${formUpload}`;
  resumePage.appendChild(divformUpload);

  const divformResume = document.createElement("div");
  divformResume.setAttribute("class", "py-2");
  divformResume.setAttribute("id", "divformResume");
  divformResume.innerHTML = `${formResume}`;
  resumePage.appendChild(divformResume);

  const appContent = document.getElementById("appContent") as HTMLElement;
  appContent.innerHTML = resumePage.outerHTML;

  if (resume) {
    const resumeForm = document.forms.namedItem("resumeFormId")  as HTMLFormElement;
    const tagName = resumeForm.getElementsByTagName("input");

    const anketaFiltred: Array<string>= [];
    for(let i = 0; i < Object.keys(resume).length; i++){
      if (!['id', 'region', 'status', 'deadline', 'recruiter', 'addition', 
      'request_id'].includes(Object.keys(resume)[i])) {
        anketaFiltred.push(Object.values(resume)[i] as string);
      }
    };
    for (const [i, value] of anketaFiltred.entries()) {
      tagName[i].setAttribute("value", value as string);
    }
  }
  const form = document.forms.namedItem("resumeFormId") as HTMLFormElement;
  form.addEventListener('submit', function submitData (event) {
    event.preventDefault();
    form.removeEventListener('submit', submitData);
    submitResume("resumeFormId", "create");
  });
}


async function submitResume(formId: string, url: string) {
  const form = document.forms.namedItem(formId) as HTMLFormElement;
  const formData = new FormData(form);
  const response = await fetch(`/resume/${url}`, { method: "POST", body: formData });
  const { message, cand_id } = await response.json();
  main.createMessage("alert alert-primary", message);
  openProfile(cand_id);
}


function addResumeItem(candId: number, formDivIds: Array<string>){
  main.createMessage('alert alert-info', "Заполните обязательные поля в нужной форме");

  const resumeElement = document.getElementById("resume") as HTMLDivElement;
  const buttonGroupElement = document.querySelector(".btn-group") as HTMLElement;
  resumeElement.remove();
  buttonGroupElement.remove();

  const forms = [formStaff, formDocument, formAddress, formContact, formWorkplace, formRelation];

  for (let i = 0; i < formDivIds.length; i++) {
    const currentDiv = document.getElementById(formDivIds[i]) as HTMLElement;
    const formContainer = currentDiv.children[1];
    formContainer.innerHTML = forms[i];
  }
  const anketaId = document.getElementById('anketaId') as HTMLElement;
  anketaId.addEventListener('submit', async function clickAdd (event) {
    event.preventDefault();

    const form = event.target as HTMLFormElement;
    const parent = form.parentElement as HTMLElement;
    const path = (parent.parentElement as HTMLElement).getAttribute("id") as string;
    
    const formData = new FormData(form);
    const response = await fetch (`update/${path}/${candId}`, {
      method: "post",
      body: formData
    })
    const { message } = await response.json();
    main.createMessage("alert alert-primary", message);
  });
};


async function createNavbar() {
  const tabNames = ['Профиль', 'Проверки', 'Согласования', 'Полиграф', 'Расследования', 'Запросы'];
  const tabPanes = ['profileTab', 'checkTab', 'registryTab', 'poligrafTab', 'investigationTab', 'inquiryTab'];

  const navDiv = document.createElement("div");
  navDiv.classList.add("nav", "nav-tabs", "nav-justified");
  navDiv.setAttribute("role", "tablist");

  const contentNav = document.createElement("div");
  contentNav.classList.add("tab-content");

  for (let i = 0; i < tabNames.length; i++) {
    const navBtn = document.createElement("button");
    navBtn.dataset.bsToggle = "tab";
    navBtn.dataset.bsTarget = "#" + tabPanes[i];
    navBtn.type = "button";
    navBtn.role = "tab";
    navBtn.classList.add("nav-link");
    if (i === 0) navBtn.classList.add("active");
    navBtn.innerHTML = tabNames[i];
    navDiv.appendChild(navBtn);

    const divPane = document.createElement("div");
    divPane.classList.add("tab-pane", "fade", "show", "py-1");
    divPane.role = "tabpanel";
    divPane.id = tabPanes[i];
    if (i === 0) divPane.classList.add("active");
    contentNav.appendChild(divPane);

    const contentTab = document.createElement("div");
    contentTab.id = tabPanes[i] + "Id";
    contentTab.classList.add("py-3");
    divPane.appendChild(contentTab);
  }

  const temp = document.createElement("div");
  temp.classList.add("py-2");
  temp.id = "navDiv";
  temp.appendChild(navDiv);
  temp.appendChild(contentNav);

  const appContent = document.getElementById("appContent") as HTMLDivElement;
  appContent.innerHTML = temp.outerHTML;
}


async function openProfile(candId: number){
  createNavbar();
  const response = await fetch(`/profile/${candId}`)
  const [ anketa, check, registry, poligraf, investigation, inquiry, state ] = await response.json();

  //вкладка анкеты
  antetaTabActions(candId, anketa)

  //вкладка проверок
  checkTabActions(candId, check);

  //вкладка согласования
  createTab(registry, "registryTabId", "registryId", REGISTRY_LABELES);
  createTabAction(candId, 'addRegistryBtn', "registryTabId", 'Добавить согласование', formRegistry, 'registryFormId', "registry");
  
  //вкладка ПФО
  createTab(poligraf, "poligrafTabId", "poligrafId", POLIGRAF_LABELES);
  createTabAction(candId, 'addPoligrafBtn', "poligrafTabId", 'Добавить тестирование', formPoligraf, 'poligrafFormId', "poligraf");
  
  //вкладка Расследований
  createTab(investigation, "investigationTabId", "investigationId", INVESTIGATION_LABELES);
  createTabAction(candId, 'addInvestigationBtn', "investigationTabId", 'Добавить расследование', formInvestigation, 
  'investigationFormId', "investigation");
  
  //вкладка Запрос
  createTab(inquiry, "inquiryTabId", "inquiryId", INQUIRY_LABELES)
  createTabAction(candId, 'addInquiryBtn', "inquiryTabId", 'Добавить запрос',formInquiry, 'inquiryFormId', "inquiry");

  //stateProfileButtons(anketa[0][0]['status'], state)
};

function antetaTabActions(candId: number, anketa: Array<Array<Object>>){

  const resumeSubDivNames = ['Резюме', 'Должности', 'Документы', 'Адреса', 'Контакты', 'Работа', 'Связи'];
  const resumeSubDivIds = ['resume', 'staffs', 'documents', 'addresses', 'contacts', 'workplaces', 'relations'];
  
  const profileTabId = document.getElementById("profileTabId") as HTMLElement;

  const anketaId = document.createElement("div");
  anketaId.setAttribute("class", "py-2");
  anketaId.setAttribute("id", "anketaId");
  profileTabId.appendChild(anketaId);

  for (let id of resumeSubDivIds){
    let division = document.createElement("div");
    division.setAttribute("class", "py-2");
    division.setAttribute("id", id);
    anketaId.appendChild(division);
  };

	main.createHeader(`<a href="#" onclick=openProfile(${candId})>${anketa[0][0]
    ['fullname' as keyof typeof anketa[0][0]]}</a>`);

  const groupBtnResume = document.createElement("div");
  groupBtnResume.setAttribute("class", "btn-group py-2 hidden-print");
  groupBtnResume.setAttribute("role", "group");
  const grpBtnResumeAttr = {
    'Изменить  анкету': `createResume(${JSON.stringify(anketa[0][0])})`,
    'Добавить информацию': `addResumeItem(${candId}, ${JSON.stringify(resumeSubDivIds.slice(1))})`,
    'Обновить статус': `updateStatus(${candId})`,
    'Отправить на проверку': `sendResume(${candId})`
  };
  for (const [label, action] of Object.entries(grpBtnResumeAttr)) {
    const updBtnResume = document.createElement('button');
    updBtnResume.setAttribute('class', 'btn btn-outline-primary');
    if (label === 'Отправить на проверку') updBtnResume.setAttribute('id', 'sendResume');
    updBtnResume.setAttribute('onclick', action);
    updBtnResume.innerHTML = label;
    groupBtnResume.appendChild(updBtnResume);
  }
  profileTabId.appendChild(groupBtnResume);

  for (let i = 0; i < anketa.length; i++) {
    let subSubdivs = document.getElementById(resumeSubDivIds[i]) as HTMLElement;
    let targetHeader = document.createElement('h6');
    targetHeader.innerHTML = resumeSubDivNames[i];
    subSubdivs.appendChild(targetHeader);
    let divTable = createItemTable(ANKETA_LABELES[i], anketa[i]);
    subSubdivs.appendChild(divTable);
  };
};


async function updateStatus(candId: number): Promise<void> {
	const response = await fetch(`/resume/status/${candId}`);
	const { message } = await response.json();
	main.createMessage("alert alert-info", message);
	openProfile(candId);
}


async function sendResume(candId: number) {
  const response = await fetch(`/resume/send/${candId}`);
  const { message } = await response.json();
  openProfile(candId);
  main.createMessage("alert alert-info", message);
};


function checkTabActions(candId: number, checks: Array<Object>){
  createTab(checks, "checkTabId", "checkId", CHECK_LABELES);

  const divPage = document.getElementById("checkTabId") as HTMLElement;
  
  const groupBtnCheck = document.createElement("div");
  groupBtnCheck.setAttribute("class", "btn-group hidden-print");
  groupBtnCheck.setAttribute("role", "group");
  divPage.appendChild(groupBtnCheck);
  
  const buttonLabels = ['Добавить проверку', 'Редактировать проверку', 'Удалить последнюю проверку'];
  const actionButtons = [`checkEditNew(${candId})`, `checkEditNew(${candId}, 
    ${JSON.stringify(checks[0])})`, `deleteLastCheck(${candId})`];
  for (let i = 0; i < actionButtons.length; i++){
    let addBtn = document.createElement("a");
    addBtn.setAttribute("class", "btn btn-outline-info");
    addBtn.setAttribute("type", "button");
    addBtn.setAttribute("onclick", actionButtons[i]);
    addBtn.innerHTML = buttonLabels[i];
    groupBtnCheck.appendChild(addBtn)
  }
};


async function checkEditNew(candId: number, check: Object={}): Promise<void> {
    let response = await fetch("/check/status/"+candId);
    let { message } = await response.json();
    main.createMessage("alert alert-warning", message);
    if (message == "Анкета взята в работу и еще не закончена"){
      return openProfile(candId);
    };
  let checkTabId = document.getElementById("checkTabId") as HTMLElement;
  checkTabId.innerHTML = formCheck;
  const form = document.forms.namedItem("checkFormId") as HTMLFormElement;

  if (check){
    const tagName = form.getElementsByTagName("textarea");
    let checkFiltred = []
    for (let i = 0; i < Object.keys(check).length; i++) {
      if (!['id', 'autostatus', 'path', 'pfo', 'comments', 'conclusion', 'deadline', 'officer', 
          'cand_id'].includes((Object.keys(check)[i]))) {
        checkFiltred.push(Object.values(check)[i]);
      };
    };
    checkFiltred.forEach((value, i) => {
      tagName[i].innerHTML = value;
    });
  };

  form.addEventListener('submit', async function formCheck(event){
    const formData = new FormData(form);
    let response = await fetch (`/check/${candId}`, {
      method: "post",
      body: formData
    })
    let { message } = await response.json();
    main.createMessage("alert alert-primary", message);
    this.removeEventListener('submit', formCheck)
    openProfile(candId)
  });
};


async function deleteLastCheck(candId: number) {
    if (confirm("Вы действительно хотите удалить проверку?")) {
      let response = await fetch(`/check/delete/${candId}`);
      let { message } = await response.json();
      
      main.createMessage("alert alert-warning", message);
      openProfile(candId);
    }
};


function createTab(resps: any, tabId: string, contentID: string, labeles: Array<string>) {
  const tabDiv = document.getElementById(tabId) as HTMLElement;
  const divTab = document.createElement("div");
  divTab.setAttribute("id", contentID);
  tabDiv.appendChild(divTab);
  const divId = document.getElementById(contentID) as HTMLElement;
  divId.innerHTML = createItemTable(labeles, resps).outerHTML;
};


function createTabAction(
    candId: number,
    buttonId: string,
    tabId: string,
    buttonLabel: string,
    formHTML: string,
    formId: string,
    path: string
  ) {
  const addButton = document.createElement("a");
  addButton.classList.add("btn", "btn-outline-info", "hidden-print");
  addButton.setAttribute("type", "button");
  addButton.setAttribute("id", buttonId);
  addButton.textContent = buttonLabel;

  const tabDiv = document.getElementById(tabId) as HTMLElement;
  tabDiv.appendChild(addButton);

  const addBtnListener = document.getElementById(buttonId) as HTMLElement;
  addBtnListener.addEventListener('click', function addForm(event){
    tabDiv.innerHTML = formHTML;
    addBtnListener.removeEventListener('click', addForm);

    const form = document.forms.namedItem(formId) as HTMLFormElement;
    form.addEventListener('submit', async function formSubmit(event: any){
      event.preventDefault(); // Prevent default form submission

      const formData = new FormData(form);
      const response = await fetch(`/${path}/${candId}`, {
        method: "post",
        body: formData
      })
      const { message } = await response.json();
      main.createMessage("alert alert-primary", message);
      openProfile(candId)

      form.removeEventListener('submit', formSubmit);
    })
  })
};


function stateProfileButtons(state: string, status: string): void {
  if (state !== status) {
    const sendResumeButton = document.getElementById('sendResume') as HTMLButtonElement;
    sendResumeButton.setAttribute("class", "disabled btn btn-outline-success hidden-print");

    const addCheckButton = document.getElementById('checkBtn') as HTMLButtonElement;
    addCheckButton.setAttribute("class", "disabled btn btn-outline-primary hidden-print");

    const editButton = document.getElementById('editBtn') as HTMLButtonElement;
    editButton.setAttribute("class", "disabled btn btn-outline-info");

    const deleteButton = document.getElementById('deleteBtn') as HTMLButtonElement;
    deleteButton.setAttribute("class", "disabled btn btn-outline-info");

    if (state !== status) {
      const sendRegistryButton = document.getElementById('addRegistryBtn') as HTMLButtonElement;
      sendRegistryButton.setAttribute("class", "disabled btn btn-outline-primary hidden-print");
    }
  };
};


//create table with candidate profile
function createItemTable(names: string[], response: Array<Object>) {
  if (response.length) {
    let division = document.createElement("div");
    //
    for (const item of response) {
      const div = document.createElement("div");
      const tbl = document.createElement("table");
      tbl.setAttribute("class", "table");
      const tblBody = document.createElement("tbody");
      for (const name of names) {
        const cell1 = document.createElement("td");
        cell1.setAttribute("width", "25%");
        cell1.innerHTML = name;
        const cell2 = document.createElement("td");
        const key = Object.keys(item)[names.indexOf(name)];
        const value = Object.values(item)[names.indexOf(name)];
        if (key === 'deadline' || key === 'birthday') {
          const date = new Date(Date.parse(value));
          cell2.innerHTML = date.toLocaleDateString('ru-RU')
        } else {
          cell2.innerHTML = value
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
};


  //открываем страницу стат информации
  async function statInfo(){
    if (!document.getElementById("infoFormId")) {
      let temp = document.createElement("div") as HTMLDivElement;
      const divCandTable = document.createElement("div");
      divCandTable.setAttribute("class", "py-2");
      divCandTable.setAttribute("id", "divCandTable");

      const divPfoTable = document.createElement("div");
      divPfoTable.setAttribute("class", "py-2");
      divPfoTable.setAttribute("id", "divPfoTable");

      const divForm = document.createElement("div");
      divForm.setAttribute("class", "py-2");
      divForm.setAttribute("id", "divForm");
      divForm.innerHTML = formInfo;

      [divCandTable, divPfoTable, divForm].forEach(div => {
        temp.appendChild(div);
        })
      const appContent = document.getElementById("appContent") as HTMLElement;
      appContent.innerHTML = temp.outerHTML;
      }; 

  const form = document.forms.namedItem("infoFormId") as HTMLFormElement;
  const dataForm = new FormData(form);
  const response = await fetch('/information', {
      method: "post",
      body: dataForm

  });
  let resps = await response.json();

  const [divCandTable, divPfoTable, appMessage] = ["divCandTable", "divPfoTable", "appMessage"].map(id => document.getElementById(id) as HTMLElement);

  main.createHeader(resps['title']);
  appMessage.innerHTML = '';

  divCandTable.innerHTML = createStatTable(resps["candidates"], "Статистика по кандидатам").outerHTML;
  divPfoTable.innerHTML = createStatTable(resps["poligraf"], "Статистика по ПФО").outerHTML;

  form.addEventListener('submit', (event: any) => {
    event.preventDefault();
    statInfo();  
  }, {once: true});
}


function createStatTable(stats: Array<Object>, caption: string) {
  const table = document.createElement("table");
  table.classList.add("table", "table-hover", "table-responsive", "align-middle");
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
  return table;
}


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
let formSearch: string;


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