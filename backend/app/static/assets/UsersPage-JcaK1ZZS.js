const __vite__fileDeps=["./HeaderDiv-CE5d1A68.js","./index-D1GedQkO.js","./index-BqKjTnG4.css","./LabelSlot-CxsZjle4.js","./_plugin-vue_export-helper-DlAUqK2U.js","./LabelSlot-BKRWK_aH.css","./InputElement-BVvBog7z.js","./SelectDiv-tCS8aW-8.js","./SwitchBox-bt-JDwTs.js","./TableSlots-vNQWibgY.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as T,k as P,D as O,r as R,c as f,b as n,u as a,e,g as $,z as B,w as E,m as d,t as s,F as k,o as v,B as j,q as c,x as M,y as N,h as u,j as p}from"./index-D1GedQkO.js";import{c as h,b as w,d as z,s as U}from"./state-z_tMSp-o.js";import{d as F}from"./utilities-Dot1e486.js";import{_ as q}from"./_plugin-vue_export-helper-DlAUqK2U.js";const g=m=>(M("data-v-557dad4c"),m=m(),N(),m),H={class:"row mb-3"},Z={class:"d-flex justify-content-between mb-3"},G=g(()=>e("button",{class:"btn btn-link text-secondary",type:"button","data-bs-toggle":"collapse",href:"#user-form"}," Добавить пользователя ",-1)),J={class:"collapse card card-body",id:"user-form"},K={class:"row"},Q={class:"col-4"},W={class:"col-3"},X={class:"col-3"},Y={class:"col-1"},ee=g(()=>e("div",{class:"col-1"},[e("button",{class:"btn btn-md btn-outline-primary",name:"submit",type:"submit"}," Сохранить ")],-1)),te=g(()=>e("tr",null,[e("th",{width:"5%"},"#"),e("th",null,"Имя пользователя"),e("th",{width:"15%"},"Логин"),e("th",{width:"10%"},"Блокировка"),e("th",{width:"15%"},"Создан"),e("th",{width:"15%"},"Администратор"),e("th",{width:"20%"},"Регион")],-1)),le={colspan:"7"},oe={width:"5%"},ae={width:"15%"},se=["onClick"],ne={width:"10%"},re={width:"15%"},de={width:"15%"},ie={width:"20%"},ce={class:"modal modal fade",id:"user-modal",tabindex:"-1"},ue={class:"modal-dialog"},pe={class:"modal-content"},me={class:"modal-body"},_e={class:"p-3"},be={class:"btn-group p-3",role:"group"},fe=T({__name:"UsersPage",setup(m){const A=u(()=>p(()=>import("./HeaderDiv-CE5d1A68.js"),__vite__mapDeps([0,1,2]),import.meta.url)),i=u(()=>p(()=>import("./LabelSlot-CxsZjle4.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),y=u(()=>p(()=>import("./InputElement-BVvBog7z.js"),__vite__mapDeps([6,1,2]),import.meta.url)),I=u(()=>p(()=>import("./SelectDiv-tCS8aW-8.js"),__vite__mapDeps([7,1,2]),import.meta.url)),V=u(()=>p(()=>import("./SwitchBox-bt-JDwTs.js"),__vite__mapDeps([8,1,2]),import.meta.url)),D=u(()=>p(()=>import("./TableSlots-vNQWibgY.js"),__vite__mapDeps([9,1,2]),import.meta.url));P(()=>{_()});const S=O(()=>t.value.users.filter(r=>r.deleted==t.value.viewDeleted)),t=R({search:"",users:[],profile:{},viewDeleted:!1});async function _(){try{const r=await h.get(`${w}/users`,{params:{search:t.value.search}});t.value.users=r.data}catch(r){console.error(r)}}const x=F(()=>{_()},500);async function b(r){if(!(r==="delete"&&!confirm("Вы действительно хотите удалить/восстановить пользователя?")))try{const l=await h.get(`${w}/users/${t.value.profile.id}`,{params:{action:r}});console.log(l.status),_()}catch(l){console.error(l)}}async function C(){try{(await h.post(`${w}/users`,t.value.profile)).status===205?U.setAlert("alert-warning","Пользователь уже существует"):U.setAlert("alert-success","Запись успешно добавлена"),L(),_()}catch(r){console.error(r)}}function L(){Object.keys(t.value.profile).forEach(l=>delete t.value[l]);const r=document.getElementById("user-form");r==null||r.setAttribute("class","collapse card card-body mb-3")}return(r,l)=>(v(),f(k,null,[n(a(A),{"page-header":"Список пользователей",cls:"text-secondary py-5"}),e("div",H,[$(e("input",{onInput:l[0]||(l[0]=E((...o)=>a(x)&&a(x)(...o),["prevent"])),class:"form-control mb-3",name:"search",id:"search",type:"text",placeholder:"Поиск по имени пользователя","onUpdate:modelValue":l[1]||(l[1]=o=>t.value.search=o)},null,544),[[B,t.value.search]])]),e("div",Z,[n(a(V),{name:"viewDeleted",label:"Показать удаленные",modelValue:t.value.viewDeleted,"onUpdate:modelValue":l[2]||(l[2]=o=>t.value.viewDeleted=o)},null,8,["modelValue"]),G]),e("div",J,[e("form",{onSubmit:E(C,["prevent"]),class:"form form-check",role:"form"},[e("div",K,[e("div",Q,[n(a(y),{name:"fullname",place:"Имя пользователя",need:!0,modelValue:t.value.profile.fullname,"onUpdate:modelValue":l[3]||(l[3]=o=>t.value.profile.fullname=o)},null,8,["modelValue"])]),e("div",W,[n(a(y),{name:"username",place:"Учетная запись",pattern:"[a-zA-Z_]+",need:!0,modelValue:t.value.profile.username,"onUpdate:modelValue":l[4]||(l[4]=o=>t.value.profile.username=o)},null,8,["modelValue"])]),e("div",X,[n(a(I),{name:"region",place:"Регион",need:!0,select:a(z).regions,modelValue:t.value.profile.region,"onUpdate:modelValue":l[5]||(l[5]=o=>t.value.profile.region=o)},null,8,["select","modelValue"])]),e("div",Y,[n(a(V),{name:"admin",title:"Администратор",modelValue:t.value.profile.has_admin,"onUpdate:modelValue":l[6]||(l[6]=o=>t.value.profile.has_admin=o)},null,8,["modelValue"])]),ee])],32)]),n(a(D),{"tbl-class":"table align-middle"},{thead:d(()=>[te]),tbody:d(()=>[e("tr",null,[e("td",le,[n(a(D),{id:"overflow","tbl-class":"table table-hover align-middle no-bottom-border"},{tbody:d(()=>[(v(!0),f(k,null,j(S.value,o=>(v(),f("tr",{height:"50px",key:o.id},[e("td",oe,s(o.id),1),e("td",null,s(o.fullname),1),e("td",ae,[e("button",{class:"btn btn-link text-secondary",type:"button","data-bs-toggle":"modal","data-bs-target":"#user-modal",onClick:ve=>t.value.profile=o},s(o.username),9,se)]),e("td",ne,s(o.blocked?"Да":"Нет"),1),e("td",re,s(new Date(o.pswd_create).toLocaleString()),1),e("td",de,s(o.has_admin?"Да":"Нет"),1),e("td",ie,s(o.region),1)]))),128))]),_:1})])])]),_:1}),e("div",ce,[e("div",ue,[e("div",pe,[e("div",me,[e("div",_e,[n(a(i),{"label-class":"col-5","input-class":"col-7",label:"ID"},{default:d(()=>[c(s(t.value.profile.id),1)]),_:1}),n(a(i),{"label-class":"col-5","input-class":"col-7",label:"Регион"},{default:d(()=>[c(s(t.value.profile.region),1)]),_:1}),n(a(i),{"label-class":"col-5","input-class":"col-7",label:"Имя пользователя"},{default:d(()=>[c(s(t.value.profile.fullname),1)]),_:1}),n(a(i),{"label-class":"col-5","input-class":"col-7",label:"Логин"},{default:d(()=>[c(s(t.value.profile.username),1)]),_:1}),n(a(i),{"label-class":"col-5","input-class":"col-7",label:"Дата создания пароля"},{default:d(()=>[c(s(new Date(t.value.profile.pswd_create+" UTC").toLocaleString("ru-RU")),1)]),_:1}),n(a(i),{"label-class":"col-5","input-class":"col-7",label:"Требует смены пароля"},{default:d(()=>[c(s(t.value.profile.change_pswd?"Да":"Нет"),1)]),_:1}),n(a(i),{"label-class":"col-5","input-class":"col-7",label:"Попытки входа"},{default:d(()=>[c(s(t.value.profile.attempt),1)]),_:1}),n(a(i),{"label-class":"col-5","input-class":"col-7",label:"Заблокирован"},{default:d(()=>[c(s(t.value.profile.blocked?"Заблокирован":"Разблокирован"),1)]),_:1}),n(a(i),{"label-class":"col-5","input-class":"col-7",label:"Активность"},{default:d(()=>[c(s(t.value.profile.deleted?"Удален":"Активен"),1)]),_:1}),n(a(i),{"label-class":"col-5","input-class":"col-7",label:"Администратор"},{default:d(()=>[c(s(t.value.profile.has_admin?"Да":"Нет"),1)]),_:1}),n(a(i),{"label-class":"col-5","input-class":"col-7",label:"Дата создания профиля"},{default:d(()=>[c(s(new Date(t.value.profile.created+" UTC").toLocaleString("ru-RU")),1)]),_:1})]),e("div",be,[e("button",{class:"btn btn-outline-primary",type:"button",onClick:l[7]||(l[7]=o=>b("admin"))},s(t.value.profile.has_admin?"Отобрать админа":"Сделать админом"),1),e("button",{onClick:l[8]||(l[8]=o=>b("drop")),type:"button",class:"btn btn-outline-secondary"}," Сбросить пароль "),e("button",{onClick:l[9]||(l[9]=o=>b("delete")),type:"button",class:"btn btn-outline-danger"},s(t.value.profile.deleted?"Восстановить":"Удалить"),1)])])])])])],64))}}),Ve=q(fe,[["__scopeId","data-v-557dad4c"]]);export{Ve as default};
