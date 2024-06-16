const __vite__fileDeps=["./HeaderDiv-CPHSjRiY.js","./index-a1q1DOXp.js","./index-6fGrG267.css","./TableSlots-DBoAf_h4.js","./ModalWin-BGDWPiVz.js","./ConnectDiv-DUBiPgYR.js","./PageSwitcher-VX3h290t.js","./ConnectForm-BxcjsKB-.js","./state-8kq10HP3.js","./utilities-DuY9392d.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as V,i as I,n as O,j as T,c as _,b as u,u as o,g as L,B,q as g,z as R,a as t,s as S,v as N,w as m,C as q,y as M,F as f,o as v,r as j,t as d,e as l,f as r}from"./index-a1q1DOXp.js";import{b as z,d as w,e as b}from"./state-8kq10HP3.js";import{s as p,d as F}from"./utilities-DuY9392d.js";const G={class:"mb-3"},H=t("tr",null,[t("th",{width:"18%"},"Название"),t("th",{width:"18%"},"Имя"),t("th",{width:"18%"},"Телефон"),t("th",{width:"18%"},"Добавочный"),t("th",{width:"18%"},"Мобильный"),t("th",{width:"5%"}),t("th",{width:"5%"})],-1),U=["onClick"],W=["onClick"],J=t("i",{class:"bi bi-pencil-square"},null,-1),K=[J],Q={width:"5%"},X=["onClick"],Y=t("i",{class:"bi bi-trash"},null,-1),Z=[Y],ne=V({__name:"ContactPage",setup(ee){const C=l(()=>r(()=>import("./HeaderDiv-CPHSjRiY.js"),__vite__mapDeps([0,1,2]),import.meta.url)),y=l(()=>r(()=>import("./TableSlots-DBoAf_h4.js"),__vite__mapDeps([3,1,2]),import.meta.url)),k=l(()=>r(()=>import("./ModalWin-BGDWPiVz.js"),__vite__mapDeps([4,1,2]),import.meta.url)),x=l(()=>r(()=>import("./ConnectDiv-DUBiPgYR.js"),__vite__mapDeps([5,1,2]),import.meta.url)),E=l(()=>r(()=>import("./PageSwitcher-VX3h290t.js"),__vite__mapDeps([6,1,2]),import.meta.url)),D=l(()=>r(()=>import("./ConnectForm-BxcjsKB-.js"),__vite__mapDeps([7,1,2,8,9]),import.meta.url));I(async()=>{await $(),await c(1)});const e=O({view:[],companies:[],cities:[],contacts:[],page:1,prev:!1,next:!1,action:"",search:"",item:{}});async function $(){try{const n=await z.get(`${p}/connects`),{view:a,companies:s,cities:i}=n.data;Object.assign(e.value,{view:a,companies:s,cities:i})}catch(n){console.error(n)}}async function c(n){e.value.action="";try{const a=await w.get(`${p}/connect/${n}`,{params:{search:e.value.search}}),{contacts:s,has_prev:i,has_next:P}=a.data;Object.assign(e.value,{contacts:s,prev:i,next:P})}catch(a){a.request.status==401||a.request.status==403?T.push({name:"login"}):console.error(a)}}async function A(n){if(confirm("Вы действительно хотите удалить контакт?"))try{const a=await w.delete(`${p}/connect/${n}`);console.log(a.status),b.setAlert("alert-success",`Контакт с ID ${n} удален`),c(e.value.page)}catch(a){console.log(a),b.setAlert("alert-danger",`Ошибка при удалении контакта с ID ${n}`)}}const h=F(()=>{c(1)},500);return(n,a)=>(v(),_(f,null,[u(o(C),{"page-header":e.value.action?"Изменить/добавить контакт":"Контакты"},null,8,["page-header"]),e.value.action?(v(),L(o(D),{key:0,page:e.value.page,action:e.value.action,names:e.value.view,companies:e.value.companies,cities:e.value.cities,item:e.value.item,onGetContacts:c,onCancelEdit:a[0]||(a[0]=s=>e.value.action="")},null,8,["page","action","names","companies","cities","item"])):B("",!0),g(t("div",G,[g(t("input",{onInput:a[1]||(a[1]=S((...s)=>o(h)&&o(h)(...s),["prevent"])),class:"form-control mb-5",name:"search",id:"search",type:"text",placeholder:"Поиск по организации","onUpdate:modelValue":a[2]||(a[2]=s=>e.value.search=s)},null,544),[[N,e.value.search]]),u(o(k),{id:"modalConnect",title:e.value.item.fullname,size:"modal-md"},{default:m(()=>[u(o(x),{item:e.value.item},null,8,["item"])]),_:1},8,["title"]),u(o(y),{class:M({"table-hover":e.value.contacts.length>0})},q({caption:m(()=>[t("button",{class:"btn btn-link btn-sm",role:"button",onClick:a[3]||(a[3]=s=>e.value.action="create")}," Добавить контакт ")]),thead:m(()=>[H]),_:2},[e.value.contacts.length>0?{name:"tbody",fn:m(()=>[(v(!0),_(f,null,j(e.value.contacts,s=>(v(),_("tr",{key:s.id},[t("td",null,d(s.company),1),t("td",null,[t("a",{href:"#",title:"Посмотреть контакт","data-bs-target":"#modalConnect","data-bs-toggle":"modal",onClick:i=>e.value.item=s},d(s.fullname),9,U)]),t("td",null,d(s.phone),1),t("td",null,d(s.adding),1),t("td",null,d(s.mobile),1),t("td",null,[t("button",{class:"btn btn-link",type:"button",title:"Изменить контакт",onClick:i=>{e.value.action="edit",e.value.item=s}},K,8,W)]),t("td",Q,[t("a",{href:"#",title:"Удалить",onClick:i=>A(s.id)},Z,8,X)])]))),128))]),key:"0"}:void 0]),1032,["class"]),u(o(E),{has_prev:e.value.next,has_next:e.value.prev,switchPrev:e.value.page-1,switchNext:e.value.page+1,onSwitch:c},null,8,["has_prev","has_next","switchPrev","switchNext"])],512),[[R,!e.value.action]])],64))}});export{ne as default};
