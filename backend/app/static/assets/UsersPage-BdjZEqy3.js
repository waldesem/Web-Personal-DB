const __vite__fileDeps=["./HeaderDiv-CS3Db4U2.js","./index-Cj2pYzZu.js","./index-BqKjTnG4.css","./UserForm-Bc58ow0X.js","./utilities-BY8xKrXT.js","./state-Kc3gs5o9.js","./SwitchBox-C4Dx5rtd.js","./TableSlots-B4Fl7LRq.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as k,f as I,A as U,n as S,c as p,a as r,u as s,g as e,q as m,v as A,s as P,B as b,w as d,F as f,j as T,o as v,x as B,t as n,k as C,b as c,p as L,m as O,e as u}from"./index-Cj2pYzZu.js";import{a as R,s as $,b as F,t as x,d as M}from"./utilities-BY8xKrXT.js";import{_ as N}from"./_plugin-vue_export-helper-DlAUqK2U.js";const j=i=>(L("data-v-a37d0ba8"),i=i(),O(),i),H={class:"row mb-3"},q={class:"d-flex justify-content-between mb-3"},z=j(()=>e("tr",null,[e("th",{width:"5%"},"#"),e("th",null,"Имя пользователя"),e("th",{width:"15%"},"Логин"),e("th",{width:"10%"},"Блокировка"),e("th",{width:"15%"},"Создан"),e("th",{width:"15%"},"Вход"),e("th",{width:"15%"},"Регион")],-1)),G={colspan:"7"},J={width:"5%"},K={width:"15%"},Q={width:"10%"},W={width:"15%"},X={width:"15%"},Y={width:"15%"},Z=k({__name:"UsersPage",setup(i){const g=c(()=>u(()=>import("./HeaderDiv-CS3Db4U2.js"),__vite__mapDeps([0,1,2]),import.meta.url)),y=c(()=>u(()=>import("./UserForm-Bc58ow0X.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),D=c(()=>u(()=>import("./SwitchBox-C4Dx5rtd.js"),__vite__mapDeps([6,1,2]),import.meta.url)),h=c(()=>u(()=>import("./TableSlots-B4Fl7LRq.js"),__vite__mapDeps([7,1,2]),import.meta.url)),w=M(()=>{_()},500);I(()=>{_()});const V=U(()=>o.value.users.filter(l=>l.deleted==o.value.viewDeleted)),o=S({action:"",search:"",viewDeleted:!1,users:[]});async function _(){try{const l=await R.get(`${$}/users`,{params:{search:o.value.search}});o.value.users=l.data}catch(l){F(l)}}return(l,a)=>{const E=T("router-link");return v(),p(f,null,[r(s(g),{"page-header":"Список пользователей",cls:"text-secondary py-5"}),e("div",H,[m(e("input",{onInput:a[0]||(a[0]=P((...t)=>s(w)&&s(w)(...t),["prevent"])),class:"form-control mb-3",name:"search",id:"search",type:"text",placeholder:"Поиск по имени пользователя","onUpdate:modelValue":a[1]||(a[1]=t=>o.value.search=t)},null,544),[[A,o.value.search]])]),e("div",q,[r(s(D),{name:"viewDeleted",label:"Показать удаленные",modelValue:o.value.viewDeleted,"onUpdate:modelValue":a[2]||(a[2]=t=>o.value.viewDeleted=t)},null,8,["modelValue"])]),m(r(s(y),{action:o.value.action,onUpdate:a[3]||(a[3]=t=>{o.value.action="",_()}),onCancel:a[4]||(a[4]=t=>o.value.action="")},null,8,["action"]),[[b,o.value.action]]),m(r(s(h),{"tbl-class":"table align-middle"},{caption:d(()=>[e("button",{class:"btn btn-link text-secondary",type:"button",onClick:a[5]||(a[5]=t=>o.value.action===""?o.value.action="create":o.value.action="")}," Добавить пользователя ")]),thead:d(()=>[z]),tbody:d(()=>[e("tr",null,[e("td",G,[r(s(h),{id:"overflow","tbl-class":"table table-hover align-middle no-bottom-border"},{tbody:d(()=>[(v(!0),p(f,null,B(V.value,t=>(v(),p("tr",{height:"50px",key:t.id},[e("td",J,n(t.id),1),e("td",null,n(t.fullname),1),e("td",K,[r(E,{to:{name:"user",params:{id:t.id}}},{default:d(()=>[C(n(t.username),1)]),_:2},1032,["to"])]),e("td",Q,n(t.blocked?"Да":"Нет"),1),e("td",W,n(s(x)(t.pswd_create)),1),e("td",X,n(s(x)(t.last_login)),1),e("td",Y,n(t.region),1)]))),128))]),_:1})])])]),_:1},512),[[b,o.value.action===""]])],64)}}}),ae=N(Z,[["__scopeId","data-v-a37d0ba8"]]);export{ae as default};
