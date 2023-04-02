'use strict'

//user login form
function loginForm () {
	//division for all blocks
	let divForm = document.createElement("div");
	divForm.setAttribute("class", "py-3");
	//form element
	let formLogin = document.createElement("form");
	formLogin.setAttribute("id", 'loginForm');
	formLogin.setAttribute("class", "form-check");
	formLogin.setAttribute("onsubmit", "return false;");
	divForm.appendChild(formLogin);
	
    //div for user label
	let usrDiv = document.createElement("div");
	usrDiv.setAttribute("class", "row mb-3");
	formLogin.appendChild(usrDiv);
	//user label
	let userLbl = document.createElement("label");
	userLbl.setAttribute("class", "form-label col-sm-2 col-form-label");
	userLbl.setAttribute("for", "loginForm");
	userLbl.innerHTML = "Пользователь";
	usrDiv.appendChild(userLbl);
	//div for input
	let inpDiv = document.createElement("div");
	inpDiv.setAttribute("class", "col-sm-3");
	usrDiv.appendChild(inpDiv);
	//input user
	let usrInp = document.createElement("input");
	usrInp.setAttribute("class", "form-control");
	usrInp.setAttribute("type", "text");
	usrInp.setAttribute("name", "username");
	inpDiv.appendChild(usrInp);
	
    //div for password label
	let pswdDiv = document.createElement("div");
	pswdDiv.setAttribute("class", "row mb-3");
	formLogin.appendChild(pswdDiv);
	//password label
	let pswdLbl = document.createElement("label");
	pswdLbl.setAttribute("class", "form-label col-sm-2 col-form-label");
	pswdLbl.setAttribute("for", "loginForm");
	pswdLbl.innerHTML = "Пароль";
	pswdDiv.appendChild(pswdLbl);
	//div for input label
	let inpPswdDiv = document.createElement("div");
	inpPswdDiv.setAttribute("class", "col-sm-3");
	pswdDiv.appendChild(inpPswdDiv);
	//input paswd
	let pswdInp = document.createElement("input");
	pswdInp.setAttribute("class", "form-control");
	pswdInp.setAttribute("type", "password");
	pswdLbl.setAttribute("autocomplete", "on");
	pswdInp.setAttribute("name", "password");
	usrInp.setAttribute("autocomplete", "current-password");
	inpPswdDiv.appendChild(pswdInp);
	
    //remember divs
	let rmbDiv1 = document.createElement("div");
	rmbDiv1.setAttribute("class", "row mb-3");
	formLogin.appendChild(rmbDiv1);
	//remember divs
	let rmbDiv2 = document.createElement("div");
	rmbDiv2.setAttribute("class", "col-sm-3 offset-sm-2");
	rmbDiv1.appendChild(rmbDiv2);
	//remember divs
	let rmbDiv3 = document.createElement("div");
	rmbDiv3.setAttribute("class", "form-check");
	rmbDiv2.appendChild(rmbDiv3);
	//remember hiddden input
	let hiddden = document.createElement("input");
	hiddden.setAttribute("class", "form-check-input");
	hiddden.setAttribute("type", "hidden");
	hiddden.setAttribute("class", "form-check-input");
	hiddden.setAttribute("value", "False") ;
	hiddden.setAttribute("name", "remember");
	rmbDiv3.appendChild(hiddden);
	//remember input
	let rmbInp = document.createElement("input");
	rmbInp.setAttribute("class", "form-check-input");
	rmbInp.setAttribute("type", "checkbox");
	rmbInp.setAttribute("class", "form-check-input");
	rmbInp.setAttribute("value", "True") ;
	rmbInp.setAttribute("name", "remember");
	rmbDiv3.appendChild(rmbInp);
	//remember label 
	let rmbLbl = document.createElement("label");
	rmbLbl.setAttribute("for", "loginForm");
	rmbLbl.innerHTML = "Запомнить";
	rmbDiv3.appendChild(rmbLbl);
	
    //login button
	let submitBtn = document.createElement("button");
	submitBtn.setAttribute("class", "btn btn-primary");
	submitBtn.setAttribute("for", "loginForm");
	submitBtn.setAttribute("id", "loginSubmit");
	submitBtn.innerHTML = "Войти";
	formLogin.appendChild(submitBtn);

	return divForm
};

//staff form
function staffForm () {
	//division for all blocks
	let divForm = document.createElement("div");
	divForm.setAttribute("class", "py-3");
	//form element
	let formStaff = document.createElement("form");
	formStaff.setAttribute("id", 'staffForm');
	formStaff.setAttribute("class", "form-check");
	divForm.appendChild(formStaff);
	//div for user label
	let staffDiv = document.createElement("div");
	staffDiv.setAttribute("class", "row mb-3");
	formStaff.appendChild(staffDiv);
	//user label
	let staffLbl = document.createElement("label");
	staffLbl.setAttribute("class", "form-label col-sm-2 col-form-label");
	staffLbl.setAttribute("for", "staffForm");
	staffLbl.innerHTML = "Должность/подразделение";
	staffDiv.appendChild(staffLbl);
	//div for input
	let inpDiv = document.createElement("div");
	inpDiv.setAttribute("class", "col-sm-8");
	staffDiv.appendChild(inpDiv);
	//input user
	let staffInp = document.createElement("input");
	staffInp.setAttribute("class", "form-control");
	staffInp.setAttribute("type", "text");
	staffInp.setAttribute("name", "staffInp");
	inpDiv.appendChild(staffInp);
	
	//div for department label
	let deptdDiv = document.createElement("div");
	deptdDiv.setAttribute("class", "row mb-3");
	formStaff.appendChild(deptdDiv);
	//password label
	let deptdLbl = document.createElement("label");
	deptdLbl.setAttribute("class", "form-label col-sm-2 col-form-label");
	deptdLbl.setAttribute("for", "staffForm");
	deptdLbl.innerHTML = "Департамент/кластер";
	deptdDiv.appendChild(deptdLbl);
	//div for input label
	let inpDeptDiv = document.createElement("div");
	inpDeptDiv.setAttribute("class", "col-sm-8");
	deptdDiv.appendChild(inpDeptDiv);
	//input label
	let deptInp = document.createElement("input");
	deptInp.setAttribute("class", "form-control");
	deptInp.setAttribute("type", "text");
	deptInp.setAttribute("name", "deptInp");
	inpDeptDiv.appendChild(deptInp);
	
	//submit button
	let submitBtn = document.createElement("button");
	submitBtn.setAttribute("class", "btn btn-primary");
	submitBtn.setAttribute("for", "staffForm");
	submitBtn.innerHTML = "Сохранить";
	formStaff.appendChild(submitBtn);

	return divForm
};

function DocumentForm () {
	//division for all blocks
	let divForm = document.createElement("div");
	divForm.setAttribute("class", "py-3");
	//form element
	let formDocument = document.createElement("form");
	formDocument.setAttribute("id", 'documentForm');
	formDocument.setAttribute("class", "form-check");
	divForm.appendChild(formDocument);
	
	//div for select label
	let viewDiv = document.createElement("div");
	viewDiv.setAttribute("class", "row mb-3");
	formDocument.appendChild(viewDiv);
	//select label
	let viewLbl = document.createElement("label");
	viewLbl.setAttribute("class", "form-label col-sm-2 col-form-label");
	viewLbl.setAttribute("for", "documentForm");
	viewLbl.innerHTML = "Вид документа";
	viewDiv.appendChild(viewLbl);
	//div for input
	let inpDiv = document.createElement("div");
	inpDiv.setAttribute("class", "col-sm-8");
	viewDiv.appendChild(inpDiv);
	//input select
	let selectInp = document.createElement("select");
	selectInp.setAttribute("class", "form-select mb-3");
	inpDiv.appendChild(selectInp);
	for (let [index, value] of ["Паспорт гражданина России", "Иностранный документ", "Другое"].entries()) {
		let option = document.createElement("option");
		option.setAttribute("class", "form-select mb-3");
		option.setAttribute("value", index);
		option.innerHTML = value;
		selectInp.appendChild(option);
	}
	let docs = ["Серия", "Номер документа", "Орган выдавший", "Дата выдачи"]
	let names = ["docSeries", "docNumber", "docAgency", "docIssue"]
	//div for labeles/inputs
	for (item in docs) {
		let docDiv = document.createElement("div");
		docDiv.setAttribute("class", "row mb-3");
		formDocument.appendChild(docDiv);
		//series label
		let docLbl = document.createElement("label");
		docLbl.setAttribute("class", "form-label col-sm-2 col-form-label");
		docLbl.setAttribute("for", "documentForm");
		docLbl.innerHTML = docs[item];
		docDiv.appendChild(docLbl);
		//div for input
		let inpDiv = document.createElement("div");
		inpDiv.setAttribute("class", "col-sm-8");
		docDiv.appendChild(inpDiv);
		//input series
		let docInp = document.createElement("input");
		docInp.setAttribute("class", "form-control");
		docInp.setAttribute("type", "text");
		docInp.setAttribute("name", names[item]);
		inpDiv.appendChild(docInp);
	};
	//submit button
	let submitBtn = document.createElement("button");
	submitBtn.setAttribute("class", "btn btn-primary");
	submitBtn.setAttribute("for", "documentForm");
	submitBtn.innerHTML = "Сохранить";
	formDocument.appendChild(submitBtn);

	return divForm
};

function addressForm () {
	//division for all blocks
	let divForm = document.createElement("div");
	divForm.setAttribute("class", "py-3");
	//form element
	let formAddress = document.createElement("form");
	formAddress.setAttribute("id", 'addressForm');
	formAddress.setAttribute("class", "form-check");
	divForm.appendChild(formAddress);
	
	//div for select label
	let viewDiv = document.createElement("div");
	viewDiv.setAttribute("class", "row mb-3");
	formAddress.appendChild(viewDiv);
	//select label
	let viewLbl = document.createElement("label");
	viewLbl.setAttribute("class", "form-label col-sm-2 col-form-label");
	viewLbl.setAttribute("for", "addressForm");
	viewLbl.innerHTML = "Вид адреса";
	viewDiv.appendChild(viewLbl);
	//div for input
	let inpDiv = document.createElement("div");
	inpDiv.setAttribute("class", "col-sm-8");
	viewDiv.appendChild(inpDiv);
	//input select
	let selectInp = document.createElement("select");
	selectInp.setAttribute("class", "form-select mb-3");
	inpDiv.appendChild(selectInp);
	for (let [index, value] of ['Адрес регистрации', 'Адрес проживания', 'Другое'].entries()) {
		let option = document.createElement("option");
		option.setAttribute("class", "form-select mb-3");
		option.setAttribute("value", index);
		option.innerHTML = value;
		selectInp.appendChild(option);
	}
	let addr = ["Регион", "Полный адрес"]
	let names = ["addrRegion", "fullAddress"]
	//div for labeles/inputs
	for (item in addr) {
		let docDiv = document.createElement("div");
		docDiv.setAttribute("class", "row mb-3");
		formAddress.appendChild(docDiv);
		//series label
		let docLbl = document.createElement("label");
		docLbl.setAttribute("class", "form-label col-sm-2 col-form-label");
		docLbl.setAttribute("for", "addressForm");
		docLbl.innerHTML = addr[item];
		docDiv.appendChild(docLbl);
		//div for input
		let inpDiv = document.createElement("div");
		inpDiv.setAttribute("class", "col-sm-8");
		docDiv.appendChild(inpDiv);
		//input series
		let docInp = document.createElement("input");
		docInp.setAttribute("class", "form-control");
		docInp.setAttribute("type", "text");
		docInp.setAttribute("name", names[item]);
		inpDiv.appendChild(docInp);
	};
	//submit button
	let submitBtn = document.createElement("button");
	submitBtn.setAttribute("class", "btn btn-primary");
	submitBtn.setAttribute("for", "addressForm");
	submitBtn.innerHTML = "Сохранить";
	formAddress.appendChild(submitBtn);

	return divForm
};