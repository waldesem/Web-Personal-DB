const __vite__fileDeps=["./ActionHeader-B5rljA6q.js","./index-BCJo_gEN.js","./index-6fGrG267.css","./ActionIcons-Dw34qmV0.js","./AffilationForm-Ck7Jzfid.js","./utilities-B_ayHb2j.js","./state-CDYnk2KN.js","./LabelSlot-CvGLSY44.js","./_plugin-vue_export-helper-DlAUqK2U.js","./LabelSlot-BKRWK_aH.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as k,i as S,n as y,o as i,c as u,b as n,u as t,g as I,B as E,F as b,r as L,w as s,q as V,z as $,x as r,t as d,e as c,f as m}from"./index-BCJo_gEN.js";import{s as f}from"./state-CDYnk2KN.js";import"./utilities-B_ayHb2j.js";const C={key:1,class:"collapse show",id:"affilation"},R={key:1},x={key:2},F=k({__name:"AffilationDiv",setup(B){const w=c(()=>m(()=>import("./ActionHeader-B5rljA6q.js"),__vite__mapDeps([0,1,2]),import.meta.url)),D=c(()=>m(()=>import("./ActionIcons-Dw34qmV0.js"),__vite__mapDeps([3,1,2]),import.meta.url)),_=c(()=>m(()=>import("./AffilationForm-Ck7Jzfid.js"),__vite__mapDeps([4,1,2,5,6]),import.meta.url)),l=c(()=>m(()=>import("./LabelSlot-CvGLSY44.js"),__vite__mapDeps([7,1,2,8,9]),import.meta.url));S(async()=>{await f.getItem("affilations")});const e=y({action:"",itemId:"",item:{},showActions:!1});function p(A){f.updateItem(e.value.action,"affilations",e.value.itemId,A),e.value.action="",e.value.itemId=""}return(A,o)=>(i(),u(b,null,[n(t(w),{header:"Аффилированность",action:e.value.action,onAction:o[0]||(o[0]=a=>e.value.action=e.value.action?"":"create")},null,8,["action"]),e.value.action==="create"?(i(),I(t(_),{key:0,affils:e.value.item,onSubmit:p,onCancel:o[1]||(o[1]=a=>{e.value.action="",e.value.itemId=""})},null,8,["affils"])):E("",!0),t(f).anketa.affilations.length?(i(),u("div",C,[(i(!0),u(b,null,L(t(f).anketa.affilations,(a,g)=>(i(),u("div",{key:g,onMouseover:o[3]||(o[3]=v=>e.value.showActions=!0),onMouseout:o[4]||(o[4]=v=>e.value.showActions=!1),class:"card card-body mb-3"},[e.value.action==="update"&&e.value.itemId===a.id.toString()?(i(),I(t(_),{key:0,affils:e.value.item,onSubmit:p,onCancel:o[2]||(o[2]=v=>{e.value.action="",e.value.itemId=""})},null,8,["affils"])):(i(),u("div",R,[n(t(l),null,{default:s(()=>[V(n(t(D),{onDelete:v=>t(f).deleteItem(a.id.toString(),"affilations"),onUpdate:v=>{e.value.action="update",e.value.item=a,e.value.itemId=a.id.toString()}},null,8,["onDelete","onUpdate"]),[[$,e.value.showActions]])]),_:2},1024),n(t(l),{label:"Тип участия"},{default:s(()=>[r(d(a.view),1)]),_:2},1024),n(t(l),{label:"Организация"},{default:s(()=>[r(d(a.name),1)]),_:2},1024),n(t(l),{label:"ИНН"},{default:s(()=>[r(d(a.inn),1)]),_:2},1024),n(t(l),{label:"Должность"},{default:s(()=>[r(d(a.position),1)]),_:2},1024),n(t(l),{label:"Дата создания"},{default:s(()=>[r(d(new Date(String(a.created)).toLocaleDateString("ru-RU")),1)]),_:2},1024),n(t(l),{label:"Дата изменения"},{default:s(()=>[r(d(new Date(String(a.updated)).toLocaleDateString("ru-RU")),1)]),_:2},1024)]))],32))),128))])):(i(),u("p",x,"Данные отсутствуют"))],64))}});export{F as default};
