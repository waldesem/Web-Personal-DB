const __vite__fileDeps=["./HeaderDiv-CPHSjRiY.js","./index-a1q1DOXp.js","./index-6fGrG267.css","./UserForm-CSBi2cv-.js","./state-8kq10HP3.js","./utilities-DuY9392d.js","./SwitchBox-CFLQVn1J.js","./TableSlots-DBoAf_h4.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as I,i as U,D as k,n as S,j as C,c as m,b as l,u as a,a as e,q as p,v as P,s as T,z as f,w as i,F as b,l as A,o as v,r as B,t as r,x as L,e as c,p as O,m as R,f as u}from"./index-a1q1DOXp.js";import{d as $,c as q}from"./state-8kq10HP3.js";import{s as F,t as g,d as M}from"./utilities-DuY9392d.js";import{_ as N}from"./_plugin-vue_export-helper-DlAUqK2U.js";const j=d=>(O("data-v-6144cfc5"),d=d(),R(),d),z={class:"row mb-3"},H={class:"d-flex justify-content-between mb-3"},G=j(()=>e("tr",null,[e("th",{width:"10%"},"#"),e("th",null,"Имя пользователя"),e("th",{width:"15%"},"Логин"),e("th",{width:"10%"},"Блокировка"),e("th",{width:"15%"},"Создан"),e("th",{width:"15%"},"Вход"),e("th",{width:"15%"},"Регион")],-1)),J={colspan:"7"},K={width:"10%"},Q={width:"15%"},W={width:"10%"},X={width:"15%"},Y={width:"15%"},Z={width:"15%"},ee=I({__name:"UsersPage",setup(d){const x=c(()=>u(()=>import("./HeaderDiv-CPHSjRiY.js"),__vite__mapDeps([0,1,2]),import.meta.url)),y=c(()=>u(()=>import("./UserForm-CSBi2cv-.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),D=c(()=>u(()=>import("./SwitchBox-CFLQVn1J.js"),__vite__mapDeps([6,1,2]),import.meta.url)),h=c(()=>u(()=>import("./TableSlots-DBoAf_h4.js"),__vite__mapDeps([7,1,2]),import.meta.url)),w=M(()=>{_()},500);U(()=>{_()});const V=k(()=>o.value.users.filter(n=>n.deleted==o.value.viewDeleted)),o=S({action:"",search:"",viewDeleted:!1,users:[]});async function _(){try{const n=await $.get(`${F}/users`,{params:{search:o.value.search}});o.value.users=n.data}catch(n){n.request.status==401||n.request.status==403?C.push({name:"login"}):console.error(n)}}return(n,s)=>{const E=A("router-link");return v(),m(b,null,[l(a(x),{"page-header":"Список пользователей",cls:"text-secondary py-5"}),e("div",z,[p(e("input",{onInput:s[0]||(s[0]=T((...t)=>a(w)&&a(w)(...t),["prevent"])),class:"form-control mb-3",name:"search",id:"search",type:"text",placeholder:"Поиск по имени пользователя","onUpdate:modelValue":s[1]||(s[1]=t=>o.value.search=t)},null,544),[[P,o.value.search]])]),e("div",H,[l(a(D),{name:"viewDeleted",label:"Показать удаленные",modelValue:o.value.viewDeleted,"onUpdate:modelValue":s[2]||(s[2]=t=>o.value.viewDeleted=t)},null,8,["modelValue"])]),p(l(a(y),{action:o.value.action,onUpdate:s[3]||(s[3]=t=>{o.value.action="",_()}),onCancel:s[4]||(s[4]=t=>o.value.action="")},null,8,["action"]),[[f,o.value.action]]),p(l(a(h),{"tbl-class":"table align-middle"},{caption:i(()=>[e("button",{class:"btn btn-link text-secondary",type:"button",onClick:s[5]||(s[5]=t=>o.value.action===""?o.value.action="create":o.value.action="")}," Добавить пользователя ")]),thead:i(()=>[G]),tbody:i(()=>[e("tr",null,[e("td",J,[l(a(h),{id:"overflow","tbl-class":"table table-hover align-middle no-bottom-border"},{tbody:i(()=>[(v(!0),m(b,null,B(V.value,t=>(v(),m("tr",{height:"50px",key:t.id},[e("td",K,r(t.id),1),e("td",null,r(t.fullname),1),e("td",Q,[l(E,{to:{name:"user",params:{id:t.id}}},{default:i(()=>[L(r(t.username),1)]),_:2},1032,["to"])]),e("td",W,r(t.blocked?"Да":"Нет"),1),e("td",X,r(a(g)(t.pswd_create)),1),e("td",Y,r(a(g)(t.last_login)),1),e("td",Z,r(a(q).regions[t.region]),1)]))),128))]),_:1})])])]),_:1},512),[[f,o.value.action===""]])],64)}}}),ne=N(ee,[["__scopeId","data-v-6144cfc5"]]);export{ne as default};
