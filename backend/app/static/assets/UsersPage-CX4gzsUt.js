const __vite__fileDeps=["assets/HeaderDiv-DM__yhnK.js","assets/index-BhT_3F5B.js","assets/index-D3owuatg.css","assets/UserForm-rjpLB3Iq.js","assets/SwitchBox-CrOICzmM.js","assets/TableSlots-CJWofkZ7.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as k,n as E,L as I,q as U,h as A,s as B,j as C,o as c,c as h,b as r,u as o,t as P,y as S,a as e,z as T,C as n,k as L,K as N,w as d,F as w,r as O,B as f,x as R,G as b,e as u,H as F,p as M,m as $,f as _}from"./index-BhT_3F5B.js";import{_ as j}from"./_plugin-vue_export-helper-DlAUqK2U.js";const H=i=>(M("data-v-9ac1911c"),i=i(),$(),i),q={class:"d-flex justify-content-between"},z=H(()=>e("tr",null,[e("th",{width:"10%"},"#"),e("th",null,"Имя пользователя"),e("th",{width:"20%"},"Логин"),e("th",{width:"15%"},"Блокировка"),e("th",{width:"15%"},"Создан"),e("th",{width:"15%"},"Вход")],-1)),G={colspan:"6"},K={width:"10%"},J={width:"20%"},Q={width:"15%"},W={width:"15%"},X={width:"15%"},Y=k({__name:"UsersPage",setup(i){const y=u(()=>_(()=>import("./HeaderDiv-DM__yhnK.js"),__vite__mapDeps([0,1,2]))),x=u(()=>_(()=>import("./UserForm-rjpLB3Iq.js"),__vite__mapDeps([3,1,2]))),g=u(()=>_(()=>import("./SwitchBox-CrOICzmM.js"),__vite__mapDeps([4,1,2]))),v=u(()=>_(()=>import("./TableSlots-CJWofkZ7.js"),__vite__mapDeps([5,1,2]))),m=F(()=>{t.value.search.length<3||p()},500);E(()=>{p()});const D=I(()=>t.value.users.filter(l=>l.deleted===t.value.viewDeleted)),t=U({action:"",search:"",viewDeleted:!1,users:[]});async function p(){try{const l=await A.get(`${B}/users`,{params:{search:t.value.search}});t.value.users=l.data}catch(l){C.setAlert("alert-success",l)}}return(l,s)=>{const V=O("router-link");return c(),h(w,null,[r(o(y),{"page-header":"Список пользователей",cls:"text-secondary py-3"}),P(e("input",{onInput:s[0]||(s[0]=T((...a)=>o(m)&&o(m)(...a),["prevent"])),class:"form-control mb-3",name:"search",id:"search",type:"text",placeholder:"Поиск по имени пользователя","onUpdate:modelValue":s[1]||(s[1]=a=>t.value.search=a)},null,544),[[S,t.value.search]]),e("div",q,[r(o(g),{name:"viewDeleted",label:"Показать удаленные",modelValue:t.value.viewDeleted,"onUpdate:modelValue":s[2]||(s[2]=a=>t.value.viewDeleted=a)},null,8,["modelValue"]),e("button",{class:"btn btn-link text-secondary",type:"button",onClick:s[3]||(s[3]=a=>t.value.action===""?t.value.action="create":t.value.action="")},n(t.value.action===""?"Добавить пользователя":"Закрыть"),1)]),t.value.action?(c(),L(o(x),{key:0,action:t.value.action,onUpdate:s[4]||(s[4]=a=>{t.value.action="",p()})},null,8,["action"])):N("",!0),r(o(v),{"tbl-class":"table align-middle"},{caption:d(()=>[f(n("Список пользователей"))]),thead:d(()=>[z]),tbody:d(()=>[e("tr",null,[e("td",G,[r(o(v),{id:"overflow","tbl-class":"table table-hover align-middle no-bottom-border"},{tbody:d(()=>[(c(!0),h(w,null,R(D.value,a=>(c(),h("tr",{height:"50px",key:a.id},[e("td",K,n(a.id),1),e("td",null,n(a.fullname),1),e("td",J,[r(V,{to:{name:"user",params:{id:a.id}}},{default:d(()=>[f(n(a.username),1)]),_:2},1032,["to"])]),e("td",Q,n(a.blocked),1),e("td",W,n(o(b)(a.pswd_create)),1),e("td",X,n(o(b)(a.last_login)),1)]))),128))]),_:1})])])]),_:1})],64)}}}),te=j(Y,[["__scopeId","data-v-9ac1911c"]]);export{te as default};
