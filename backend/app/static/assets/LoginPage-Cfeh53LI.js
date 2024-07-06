const __vite__fileDeps=["./HeaderDiv-BS-N29cR.js","./index-D1U1a8b2.js","./index-BqKjTnG4.css","./AlertMessage-CVZBkBai.js","./state-u74uZLPD.js","./InputElement-CpP_zLuD.js","./BtnGroup-DCfcNJ97.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as V,r as _,a as y,c as v,b as r,u as n,e as o,w as k,f as A,g as h,v as x,t as E,o as f,h as p,i as P,j as m}from"./index-D1U1a8b2.js";import{s as d,a as D,b as I}from"./state-u74uZLPD.js";import{_ as L}from"./_plugin-vue_export-helper-DlAUqK2U.js";const C={class:"container pt-5"},S={class:"border border-primary rounded p-5"},$={class:"mb-3"},B={class:"mb-3"},O={key:0},R={class:"mb-3"},T={class:"mb-3"},U={class:"row mb-3 col-lg-9"},N=V({__name:"LoginPage",setup(M){const c=p(()=>m(()=>import("./HeaderDiv-BS-N29cR.js"),__vite__mapDeps([0,1,2]),import.meta.url)),w=p(()=>m(()=>import("./AlertMessage-CVZBkBai.js"),__vite__mapDeps([3,4,1,2]),import.meta.url)),u=p(()=>m(()=>import("./InputElement-CpP_zLuD.js"),__vite__mapDeps([5,1,2]),import.meta.url)),g=p(()=>m(()=>import("./BtnGroup-DCfcNJ97.js"),__vite__mapDeps([6,1,2]),import.meta.url)),l=_(!1),a=_("create"),t=y({});async function b(){if(l.value=!1,a.value==="update"){if(t.passhash===t.new_pswd){d.setAlert("alert-warning","Старый и новый пароли совпадают");return}if(t.conf_pswd!==t.new_pswd){d.setAlert("alert-warning","Новый пароль и подтверждение не совпадают");return}}try{const i=await D.post(`${I}/login/${a.value}`,t);switch(i.status){case 201:a.value="create",d.setAlert("alert-success","Войдите с новым паролем");break;case 200:const{user_token:e}=i.data;localStorage.setItem("user_token",e),P.push({name:"persons"});break;case 205:a.value="update",d.setAlert("alert-warning","Пароль просрочен. Измените пароль");break;case 204:a.value="create",d.setAlert("alert-danger","Неверный логин или пароль");break}}catch(i){d.setAlert("alert-warning",i)}}return(i,e)=>(f(),v("div",C,[r(n(w)),r(n(c),{cls:"text-danger py-3","page-header":"StaffSec - кадровая безопасность"}),o("div",S,[r(n(c),{cls:"text-primary mb-3 text-center","page-header":a.value==="create"?"Вход в систему":"Изменить пароль"},null,8,["page-header"]),o("form",{class:"form form-check",role:"form",onSubmit:k(b,["prevent"])},[o("div",$,[r(n(u),{need:!0,name:"username",place:"Логин",modelValue:t.username,"onUpdate:modelValue":e[0]||(e[0]=s=>t.username=s)},null,8,["modelValue"])]),o("div",B,[r(n(u),{need:!0,name:"password",place:"Пароль",typeof:l.value?"text":"password",modelValue:t.password,"onUpdate:modelValue":e[1]||(e[1]=s=>t.password=s)},null,8,["typeof","modelValue"])]),a.value==="update"?(f(),v("div",O,[o("div",R,[r(n(u),{need:!0,name:"new_pswd",place:"Новый пароль",min:8,max:16,typeof:l.value?"text":"password",modelValue:t.new_pswd,"onUpdate:modelValue":e[2]||(e[2]=s=>t.new_pswd=s)},null,8,["typeof","modelValue"])]),o("div",T,[r(n(u),{need:!0,name:"conf_pswd",place:"Повтор пароля",typeof:l.value?"text":"password",modelValue:t.conf_pswd,"onUpdate:modelValue":e[3]||(e[3]=s=>t.conf_pswd=s)},null,8,["typeof","modelValue"])])])):A("",!0),o("div",U,[h(o("a",{class:"link-primary mb-2",href:"#",onClick:e[4]||(e[4]=s=>a.value="update")}," Изменить пароль ",512),[[x,a.value==="create"]]),o("a",{class:"link-primary",href:"#",onClick:e[5]||(e[5]=s=>l.value=!l.value)},E(l.value?"Скрыть":"Показать")+" пароль ",1)]),r(n(g),{offset:!1,"submit-btn":a.value==="create"?"Войти":"Изменить",onCancel:e[6]||(e[6]=s=>a.value="create")},null,8,["submit-btn"])],32)])]))}}),H=L(N,[["__scopeId","data-v-3a7dfe7f"]]);export{H as default};
