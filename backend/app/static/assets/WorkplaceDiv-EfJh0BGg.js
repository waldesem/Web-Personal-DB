const __vite__fileDeps=["./ActionHeader-BqcdmkJM.js","./index-BhwzwnLH.js","./index-6fGrG267.css","./ActionIcons-BkvQs5mF.js","./WorkplaceForm-DgjD61QP.js","./utilities-DuY9392d.js","./LabelSlot-DtLQ-bg4.js","./_plugin-vue_export-helper-DlAUqK2U.js","./LabelSlot-BKRWK_aH.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as g,i as S,n as E,o as n,c as d,b as r,u as o,g as _,q as k,F as b,r as L,w as s,s as V,A as $,y as i,t as u,e as p,f as m}from"./index-BhwzwnLH.js";import{s as c}from"./state-BY_Xl-td.js";import"./utilities-DuY9392d.js";const C={key:1,class:"collapse show",id:"work"},R={key:1},h={key:2},F=g({__name:"WorkplaceDiv",setup(P){const A=p(()=>m(()=>import("./ActionHeader-BqcdmkJM.js"),__vite__mapDeps([0,1,2]),import.meta.url)),D=p(()=>m(()=>import("./ActionIcons-BkvQs5mF.js"),__vite__mapDeps([3,1,2]),import.meta.url)),w=p(()=>m(()=>import("./WorkplaceForm-DgjD61QP.js"),__vite__mapDeps([4,1,2,5]),import.meta.url)),l=p(()=>m(()=>import("./LabelSlot-DtLQ-bg4.js"),__vite__mapDeps([6,1,2,7,8]),import.meta.url));S(()=>{c.getItem("workplaces")});const e=E({action:"",itemId:"",item:{},showActions:!1});function f(I){c.updateItem(e.value.action,"workplaces",e.value.itemId,I),e.value.action="",e.value.itemId=""}return(I,a)=>(n(),d(b,null,[r(o(A),{id:"work",header:"Работа",action:e.value.action,onAction:a[0]||(a[0]=t=>e.value.action=e.value.action?"":"create")},null,8,["action"]),e.value.action==="create"?(n(),_(o(w),{key:0,onSubmit:f,onCancel:a[1]||(a[1]=t=>{e.value.action="",e.value.itemId=""})})):k("",!0),o(c).anketa.workplaces.length?(n(),d("div",C,[(n(!0),d(b,null,L(o(c).anketa.workplaces,(t,y)=>(n(),d("div",{key:y,onMouseover:a[3]||(a[3]=v=>e.value.showActions=!0),onMouseout:a[4]||(a[4]=v=>e.value.showActions=!1),class:"card card-body mb-3"},[e.value.action==="update"&&e.value.itemId===t.id.toString()?(n(),_(o(w),{key:0,work:e.value.item,onSubmit:f,onCancel:a[2]||(a[2]=v=>{e.value.action="",e.value.itemId=""})},null,8,["work"])):(n(),d("div",R,[r(o(l),null,{default:s(()=>[V(r(o(D),{onDelete:v=>o(c).deleteItem(t.id.toString(),"workplaces"),onUpdate:v=>{e.value.action="update",e.value.item=t,e.value.itemId=t.id.toString()}},null,8,["onDelete","onUpdate"]),[[$,e.value.showActions]])]),_:2},1024),t.now_work?(n(),_(o(l),{key:0,label:"Текущая работа"},{default:s(()=>[i(u(t.now_work?"Да":"Нет"),1)]),_:2},1024)):k("",!0),r(o(l),{label:"Начало работы"},{default:s(()=>[i(u(new Date(t.started).toLocaleDateString("ru-RU")),1)]),_:2},1024),t.now_work?k("",!0):(n(),_(o(l),{key:1,label:"Окончание работы"},{default:s(()=>[i(u(new Date(t.finished).toLocaleDateString("ru-RU")),1)]),_:2},1024)),r(o(l),{label:"Место работы"},{default:s(()=>[i(u(t.workplace),1)]),_:2},1024),r(o(l),{label:"Адрес"},{default:s(()=>[i(u(t.address),1)]),_:2},1024),r(o(l),{label:"Должность"},{default:s(()=>[i(u(t.position),1)]),_:2},1024),r(o(l),{label:"Причина увольнения"},{default:s(()=>[i(u(t.reason),1)]),_:2},1024)]))],32))),128))])):(n(),d("p",h,"Данные отсутствуют"))],64))}});export{F as default};