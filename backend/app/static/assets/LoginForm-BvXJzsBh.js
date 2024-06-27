const __vite__fileDeps=["./HeaderDiv-ylIJgkZu.js","./index-cloJKXpO.js","./index-6fGrG267.css","./LabelSlot-DfErfg11.js","./_plugin-vue_export-helper-DlAUqK2U.js","./LabelSlot-BKRWK_aH.css","./GroupInput-FKBuiUwo.js","./BtnGroup-BnWeIZfC.js","./GroupContent-Dykh_J7p.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as V,m as y,o as c,c as v,a as t,u as o,h as l,q as g,w as n,y as x,n as h,z as k,C as A,b as i,e as d,r as E}from"./index-cloJKXpO.js";import{a as C,s as D}from"./utilities-B52xYZ_9.js";import{d as s}from"./state-CaQwaOis.js";const L={class:"border border-primary rounded p-5"},I={class:"mb-3"},P={class:"input-group-text"},O={class:"row mb-3 col-lg-9 offset-lg-2"},R={key:0},U=V({__name:"LoginForm",setup(T){const _=i(()=>d(()=>import("./HeaderDiv-ylIJgkZu.js"),__vite__mapDeps([0,1,2]),import.meta.url)),m=i(()=>d(()=>import("./LabelSlot-DfErfg11.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),p=i(()=>d(()=>import("./GroupInput-FKBuiUwo.js"),__vite__mapDeps([6,1,2]),import.meta.url)),f=i(()=>d(()=>import("./BtnGroup-BnWeIZfC.js"),__vite__mapDeps([7,1,2]),import.meta.url)),w=i(()=>d(()=>import("./GroupContent-Dykh_J7p.js"),__vite__mapDeps([8,1,2]),import.meta.url)),e=y({action:"create",hidden:!0,form:{}});async function b(){if(e.value.hidden=!0,e.value.action==="update"){if(e.value.form.password===e.value.form.new_pswd){s.setAlert("alert-warning","Старый и новый пароли совпадают");return}if(e.value.form.conf_pswd!==e.value.form.new_pswd){s.setAlert("alert-warning","Новый пароль и подтверждение не совпадают");return}}try{const u=await C.post(`${D}/login/${e.value.action}`,e.value.form);switch(u.status){case 201:e.value.action="create",s.setAlert("alert-success","Войдите с новым паролем");break;case 200:const{user_token:a}=u.data;localStorage.setItem("user_token",a),E.push({name:"persons"});break;case 205:e.value.action="update",s.setAlert("alert-warning","Пароль просрочен. Измените пароль");break;case 204:e.value.action="create",s.setAlert("alert-danger","Неверный логин или пароль");break}}catch(u){s.setAlert("alert-warning",u)}}return(u,a)=>(c(),v("div",L,[t(o(_),{cls:"text-primary mb-3 text-center","page-header":e.value.action==="create"?"Вход в систему":"Изменить пароль"},null,8,["page-header"]),l("div",I,[l("form",{class:"form form-check",role:"form",onSubmit:g(b,["prevent"])},[t(o(m),{label:"Логин"},{default:n(()=>[t(o(p),{name:"username",place:"Логин",min:3,max:16,modelValue:e.value.form.username,"onUpdate:modelValue":a[0]||(a[0]=r=>e.value.form.username=r)},null,8,["modelValue"])]),_:1}),t(o(m),{label:"Пароль"},{default:n(()=>[t(o(p),{name:"password",place:"Пароль",min:8,max:16,type:e.value.hidden?"password":"text",modelValue:e.value.form.password,"onUpdate:modelValue":a[2]||(a[2]=r=>e.value.form.password=r)},{default:n(()=>[l("span",P,[l("a",{role:"button",onClick:a[1]||(a[1]=r=>e.value.hidden=!e.value.hidden)},[l("i",{class:x(e.value.hidden?"bi bi-eye":"bi bi-eye-slash")},null,2)])])]),_:1},8,["type","modelValue"])]),_:1}),h(l("div",O,[l("a",{class:"link-primary",href:"#",onClick:a[3]||(a[3]=r=>e.value.action="update")}," Изменить пароль ")],512),[[k,e.value.action==="create"]]),e.value.action==="update"?(c(),v("div",R,[t(o(m),{label:"Новый пароль"},{default:n(()=>[t(o(p),{name:"new_pswd",place:"Новый",min:8,max:16,type:e.value.hidden?"password":"text",modelValue:e.value.form.new_pswd,"onUpdate:modelValue":a[4]||(a[4]=r=>e.value.form.new_pswd=r)},null,8,["type","modelValue"])]),_:1}),t(o(m),{label:"Повтор пароля"},{default:n(()=>[t(o(p),{name:"conf_pswd",place:"Повтор",min:8,max:16,type:e.value.hidden?"password":"text",modelValue:e.value.form.conf_pswd,"onUpdate:modelValue":a[5]||(a[5]=r=>e.value.form.conf_pswd=r)},null,8,["type","modelValue"])]),_:1})])):A("",!0),t(o(f),null,{default:n(()=>[t(o(w),{"submit-btn":e.value.action==="create"?"Войти":"Изменить",onCancel:a[6]||(a[6]=r=>e.value.action="create")},null,8,["submit-btn"])]),_:1})],32)])]))}});export{U as default};
