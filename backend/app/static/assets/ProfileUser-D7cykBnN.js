const __vite__fileDeps=["./HeaderDiv-DTm--MTY.js","./index-1yFXvMEA.js","./index-BqKjTnG4.css","./LabelSlot-DmfbviAy.js","./_plugin-vue_export-helper-DlAUqK2U.js","./LabelSlot-BKRWK_aH.css","./UserForm-Ckdwsgb0.js","./state-QybiP1xm.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as k,k as A,r as C,c as m,b as a,u as t,m as E,e as u,l as s,t as l,F as $,B as h,o as p,p as n,h as f,j as _}from"./index-1yFXvMEA.js";import{c as b,b as y,s as v,f as g,e as x}from"./state-QybiP1xm.js";import{_ as L}from"./_plugin-vue_export-helper-DlAUqK2U.js";const R={key:1},T={class:"mb-5"},B={class:"btn-group row mb-3",role:"group"},I=["disabled"],P=k({__name:"ProfileUser",setup(V){const w=f(()=>_(()=>import("./HeaderDiv-DTm--MTY.js"),__vite__mapDeps([0,1,2]),import.meta.url)),o=f(()=>_(()=>import("./LabelSlot-DmfbviAy.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),D=f(()=>_(()=>import("./UserForm-Ckdwsgb0.js"),__vite__mapDeps([6,1,2,7]),import.meta.url));A(async()=>{const i=h();e.value.id=i.params.id,await d("view")});const e=C({id:"",action:"",profile:{}});async function d(i){try{const r=await b.get(`${y}/users/${e.value.id}`,{params:{action:i}});e.value.profile=r.data,i==="drop"&&v.setAlert("alert-success","Пароль сброшен")}catch(r){g(r)}}async function U(){if(confirm("Вы действительно хотите удалить пользователя?"))try{(await b.delete(`${y}/users/${e.value.id}`)).status===204?(v.setAlert("alert-success","Пользователь отмечен к удалению"),d("view")):v.setAlert("alert-danger","Произошла ошибка")}catch(i){g(i)}}return(i,r)=>(p(),m($,null,[a(t(w),{"page-header":e.value.profile.fullname,cls:"text-secondary py-5"},null,8,["page-header"]),e.value.action?(p(),E(t(D),{key:0,action:e.value.action,item:e.value.profile,onUpdate:r[0]||(r[0]=c=>{e.value.action="",d("view")}),onCancel:r[1]||(r[1]=c=>{e.value.action=""})},null,8,["action","item"])):(p(),m("div",R,[u("div",T,[a(t(o),{label:"ID"},{default:s(()=>[n(l(e.value.profile.id),1)]),_:1}),a(t(o),{label:"Регион"},{default:s(()=>[n(l(e.value.profile.region),1)]),_:1}),a(t(o),{label:"Имя пользователя"},{default:s(()=>[n(l(e.value.profile.fullname),1)]),_:1}),a(t(o),{label:"Логин"},{default:s(()=>[n(l(e.value.profile.username),1)]),_:1}),a(t(o),{label:"E-mail"},{default:s(()=>[n(l(e.value.profile.email),1)]),_:1}),a(t(o),{label:"Дата создания пароля"},{default:s(()=>[n(l(new Date(e.value.profile.pswd_create+" UTC").toLocaleString("ru-RU")),1)]),_:1}),a(t(o),{label:"Требует смены пароля"},{default:s(()=>[n(l(e.value.profile.change_pswd?"Да":"Нет"),1)]),_:1}),a(t(o),{label:"Дата последнего входа"},{default:s(()=>[n(l(new Date(e.value.profile.last_login+" UTC").toLocaleString("ru-RU")),1)]),_:1}),a(t(o),{label:"Попытки входа"},{default:s(()=>[n(l(e.value.profile.attempt),1)]),_:1}),a(t(o),{label:"Заблокирован"},{default:s(()=>[n(l(e.value.profile.blocked?"Заблокирован":"Разблокирован"),1)]),_:1}),a(t(o),{label:"Активность"},{default:s(()=>[n(l(e.value.profile.deleted?"Удален":"Активен"),1)]),_:1}),a(t(o),{label:"Администратор"},{default:s(()=>[n(l(e.value.profile.has_admin?"Да":"Нет"),1)]),_:1}),a(t(o),{label:"Дата создания профиля"},{default:s(()=>[n(l(new Date(e.value.profile.created+" UTC").toLocaleString("ru-RU")),1)]),_:1})]),u("div",B,[u("button",{class:"btn btn-outline-primary",type:"button",onClick:r[2]||(r[2]=c=>e.value.action===""?e.value.action="edit":e.value.action="")},l(e.value.action===""?"Редактировать":"Отменить"),1),u("button",{onClick:r[3]||(r[3]=c=>d("drop")),type:"button",class:"btn btn-outline-secondary"}," Сбросить пароль "),u("button",{onClick:U,type:"button",class:"btn btn-outline-danger",disabled:e.value.profile.deleted||e.value.id==t(x).userId}," Удалить ",8,I)])]))],64))}}),O=L(P,[["__scopeId","data-v-2f7d0f99"]]);export{O as default};