const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=["./ActionIcons-nL13gtqs.js","./index-CuxALIEa.js","./index-QNw51pzy.css","./_plugin-vue_export-helper-DlAUqK2U.js","./ActionIcons-CukUJdTR.css","./InquiryForm-BqFeWVXr.js","./state-Dl_2yBjS.js","./LabelSlot-D4bqwlze.js","./LabelSlot-BMshfUVW.css"])))=>i.map(i=>d[i]);
import{d as E,r as c,o as a,c as n,e as h,b as s,u as e,F as A,z as S,m as T,l as r,g as C,v as L,t as l,p as _,h as b,j as k}from"./index-CuxALIEa.js";import{e as i,c as V}from"./state-Dl_2yBjS.js";import{_ as w}from"./_plugin-vue_export-helper-DlAUqK2U.js";const B={class:"collapse card card-body mb-3",id:"clps_inquiry"},U={key:0},x={key:1},P={class:"fs-5 fw-medium text-primary p-1"},R={key:1,class:"p-3"},$=E({__name:"InquiryTab",setup(F){const D=b(()=>k(()=>import("./ActionIcons-nL13gtqs.js"),__vite__mapDeps([0,1,2,3,4]),import.meta.url)),g=b(()=>k(()=>import("./InquiryForm-BqFeWVXr.js"),__vite__mapDeps([5,1,2,6]),import.meta.url)),o=b(()=>k(()=>import("./LabelSlot-D4bqwlze.js"),__vite__mapDeps([7,1,2,3,8]),import.meta.url)),p=c(!1),v=c(!1),m=c(""),I=c({});function q(){v.value=!1,m.value="";const u=document.getElementById("clps_inquiry");u==null||u.setAttribute("class","collapse card card-body mb-3")}return(u,d)=>(a(),n(A,null,[h("div",B,[s(e(g),{onCancel:q})]),e(i).anketa.inquiries.length?(a(),n("div",U,[(a(!0),n(A,null,S(e(i).anketa.inquiries,(t,f)=>(a(),n("div",{class:"card card-body mb-3",key:f,onMouseover:d[0]||(d[0]=y=>p.value=!0),onMouseout:d[1]||(d[1]=y=>p.value=!1)},[v.value&&m.value==t.id.toString()?(a(),T(e(g),{key:0,inquiry:I.value,onCancel:q},null,8,["inquiry"])):(a(),n("div",x,[s(e(o),null,{default:r(()=>[C(s(e(D),{onDelete:y=>e(i).deleteItem(t.id.toString(),"inquiries"),onUpdate:y=>{I.value=t,m.value=t.id.toString(),v.value=!0},hide:!0},null,8,["onDelete","onUpdate"]),[[L,p.value&&f&&e(i).anketa.persons.user_id==e(V).user.userId&&e(i).anketa.persons.standing]])]),_:2},1024),h("p",P,l("Запросы о сотруднике #"+(f+1)),1),s(e(o),{label:"Информация"},{default:r(()=>[_(l(t.info),1)]),_:2},1024),s(e(o),{label:"Иннициатор"},{default:r(()=>[_(l(t.origins),1)]),_:2},1024),s(e(o),{label:"Сотрудник"},{default:r(()=>[_(l(t.username),1)]),_:2},1024),s(e(o),{label:"Дата записи"},{default:r(()=>[_(l(new Date(t.created+" UTC").toLocaleString("ru-RU")),1)]),_:2},1024)]))],32))),128))])):(a(),n("p",R,"Запросы о сотруднике не поступали"))],64))}}),j=w($,[["__scopeId","data-v-0fa8ff5b"]]);export{j as default};