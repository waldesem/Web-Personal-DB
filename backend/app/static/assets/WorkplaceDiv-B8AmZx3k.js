const __vite__fileDeps=["./DropDownHead-DWPQPqzh.js","./index-D2OLA4OR.js","./index-BqKjTnG4.css","./ActionIcons-B__oqcU7.js","./_plugin-vue_export-helper-DlAUqK2U.js","./ActionIcons-CukUJdTR.css","./WorkplaceForm-BOZCPDWC.js","./state-BHhWPIxB.js","./LabelSlot-Dfq8r-re.js","./LabelSlot-BKRWK_aH.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as S,r as i,o as a,c as d,b as r,u as e,e as V,F as E,A as C,m as p,l as s,g as R,v as x,p as n,t as l,f as D,h as k,j as v}from"./index-D2OLA4OR.js";import{f as c,e as B}from"./state-BHhWPIxB.js";import{_ as P}from"./_plugin-vue_export-helper-DlAUqK2U.js";const T={class:"collapse card card-body mb-3",id:"worker"},U={key:0},N={key:1},O={key:1},$=S({__name:"WorkplaceDiv",setup(F){const I=k(()=>v(()=>import("./DropDownHead-DWPQPqzh.js"),__vite__mapDeps([0,1,2]),import.meta.url)),h=k(()=>v(()=>import("./ActionIcons-B__oqcU7.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),y=k(()=>v(()=>import("./WorkplaceForm-BOZCPDWC.js"),__vite__mapDeps([6,1,2,7]),import.meta.url)),o=k(()=>v(()=>import("./LabelSlot-Dfq8r-re.js"),__vite__mapDeps([8,1,2,4,9]),import.meta.url)),f=i(!1),m=i(!1),w=i(""),g=i({});function A(){m.value=!1,w.value="";const u=document.getElementById("worker");u==null||u.setAttribute("class","collapse card card-body mb-3")}return(u,_)=>(a(),d(E,null,[r(e(I),{id:"worker",header:"Работа"}),V("div",T,[r(e(y),{onCancel:A})]),e(c).anketa.workplaces.length?(a(),d("div",U,[(a(!0),d(E,null,C(e(c).anketa.workplaces,(t,L)=>(a(),d("div",{key:L,onMouseover:_[0]||(_[0]=b=>f.value=!0),onMouseout:_[1]||(_[1]=b=>f.value=!1),class:"card card-body mb-3"},[m.value&&w.value==t.id.toString()?(a(),p(e(y),{key:0,work:g.value,onCancel:A},null,8,["work"])):(a(),d("div",N,[r(e(o),null,{default:s(()=>[R(r(e(h),{onDelete:b=>e(c).deleteItem(t.id.toString(),"workplaces"),onUpdate:b=>{g.value=t,w.value=t.id.toString(),m.value=!0},hide:!0},null,8,["onDelete","onUpdate"]),[[x,f.value&&e(c).anketa.persons.user_id==e(B).userId&&e(c).anketa.persons.standing]])]),_:2},1024),t.now_work?(a(),p(e(o),{key:0,label:"Текущая работа"},{default:s(()=>[n(l(t.now_work?"Да":"Нет"),1)]),_:2},1024)):D("",!0),r(e(o),{label:"Начало работы"},{default:s(()=>[n(l(new Date(t.starts).toLocaleDateString("ru-RU")),1)]),_:2},1024),t.now_work?D("",!0):(a(),p(e(o),{key:1,label:"Окончание работы"},{default:s(()=>[n(l(new Date(t.finished).toLocaleDateString("ru-RU")),1)]),_:2},1024)),r(e(o),{label:"Место работы"},{default:s(()=>[n(l(t.workplace),1)]),_:2},1024),r(e(o),{label:"Адрес"},{default:s(()=>[n(l(t.addresses),1)]),_:2},1024),r(e(o),{label:"Должность"},{default:s(()=>[n(l(t.position),1)]),_:2},1024),t.reason?(a(),p(e(o),{key:2,label:"Причина увольнения"},{default:s(()=>[n(l(t.reason),1)]),_:2},1024)):D("",!0)]))],32))),128))])):(a(),d("p",O,"Данные отсутствуют"))],64))}}),H=P($,[["__scopeId","data-v-9dc18c5c"]]);export{H as default};