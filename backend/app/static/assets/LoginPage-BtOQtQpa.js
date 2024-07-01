const __vite__fileDeps=["./HeaderDiv-DTm--MTY.js","./index-1yFXvMEA.js","./index-BqKjTnG4.css","./AlertMessage-VhGy8HDg.js","./state-QybiP1xm.js","./InputElement-Cnyk_q3h.js","./BtnGroup-B6UFTBMn.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as V,r as _,a as y,c as v,b as o,u as n,e as r,w as k,f as A,g as x,v as E,t as h,o as f,h as p,i as D,j as m}from"./index-1yFXvMEA.js";import{s as d,a as I,b as L}from"./state-QybiP1xm.js";import{_ as P}from"./_plugin-vue_export-helper-DlAUqK2U.js";const C={class:"container pt-5"},S={class:"border border-primary rounded p-5"},$={class:"mb-3"},B={class:"mb-3"},N={key:0},O={class:"mb-3"},R={class:"mb-3"},T={class:"row mb-3 col-lg-9"},U=V({__name:"LoginPage",setup(M){const c=p(()=>m(()=>import("./HeaderDiv-DTm--MTY.js"),__vite__mapDeps([0,1,2]),import.meta.url)),w=p(()=>m(()=>import("./AlertMessage-VhGy8HDg.js"),__vite__mapDeps([3,4,1,2]),import.meta.url)),i=p(()=>m(()=>import("./InputElement-Cnyk_q3h.js"),__vite__mapDeps([5,1,2]),import.meta.url)),b=p(()=>m(()=>import("./BtnGroup-B6UFTBMn.js"),__vite__mapDeps([6,1,2]),import.meta.url)),l=_(!0),a=_("create"),t=y({});async function g(){if(l.value=!0,a.value==="update"){if(t.password===t.new_pswd){d.setAlert("alert-warning","Старый и новый пароли совпадают");return}if(t.conf_pswd!==t.new_pswd){d.setAlert("alert-warning","Новый пароль и подтверждение не совпадают");return}}try{const u=await I.post(`${L}/login/${a.value}`,t);switch(u.status){case 201:a.value="create",d.setAlert("alert-success","Войдите с новым паролем");break;case 200:const{user_token:e}=u.data;localStorage.setItem("user_token",e),D.push({name:"persons"});break;case 205:a.value="update",d.setAlert("alert-warning","Пароль просрочен. Измените пароль");break;case 204:a.value="create",d.setAlert("alert-danger","Неверный логин или пароль");break}}catch(u){d.setAlert("alert-warning",u)}}return(u,e)=>(f(),v("div",C,[o(n(w)),o(n(c),{cls:"text-danger py-3","page-header":"StaffSec - кадровая безопасность"}),r("div",S,[o(n(c),{cls:"text-primary mb-3 text-center","page-header":a.value==="create"?"Вход в систему":"Изменить пароль"},null,8,["page-header"]),r("form",{class:"form form-check",role:"form",onSubmit:k(g,["prevent"])},[r("div",$,[o(n(i),{need:!0,name:"username",place:"Логин",modelValue:t.username,"onUpdate:modelValue":e[0]||(e[0]=s=>t.username=s)},null,8,["modelValue"])]),r("div",B,[o(n(i),{need:!0,name:"password",place:"Пароль",typeof:l.value?"password":"text",modelValue:t.password,"onUpdate:modelValue":e[1]||(e[1]=s=>t.password=s)},null,8,["typeof","modelValue"])]),a.value==="update"?(f(),v("div",N,[r("div",O,[o(n(i),{need:!0,name:"new_pswd",place:"Новый пароль",min:8,max:16,typeof:l.value?"password":"text",modelValue:t.new_pswd,"onUpdate:modelValue":e[2]||(e[2]=s=>t.new_pswd=s)},null,8,["typeof","modelValue"])]),r("div",R,[o(n(i),{need:!0,name:"conf_pswd",place:"Повтор пароля",typeof:l.value?"password":"text",modelValue:t.conf_pswd,"onUpdate:modelValue":e[3]||(e[3]=s=>t.conf_pswd=s)},null,8,["typeof","modelValue"])])])):A("",!0),r("div",T,[x(r("a",{class:"link-primary mb-2",href:"#",onClick:e[4]||(e[4]=s=>a.value="update")}," Изменить пароль ",512),[[E,a.value==="create"]]),r("a",{class:"link-primary",href:"#",onClick:e[5]||(e[5]=s=>l.value=!l.value)},h(l.value?"Показать":"Скрыть")+" пароль ",1)]),o(n(b),{offset:!1,"submit-btn":a.value==="create"?"Войти":"Изменить",onCancel:e[6]||(e[6]=s=>a.value="create")},null,8,["submit-btn"])],32)])]))}}),H=P(U,[["__scopeId","data-v-8beb3886"]]);export{H as default};
