const __vite__fileDeps=["./DropDownHead-B7f3Pb2S.js","./index-8uvu1PmF.js","./index-BqKjTnG4.css","./ActionIcons-C-QsqxbB.js","./_plugin-vue_export-helper-DlAUqK2U.js","./ActionIcons-B4kU7i0h.css","./WorkplaceForm-lU0hNg74.js","./state-BEsVv8Mv.js","./utilities-Dq58mqGZ.js","./LabelSlot-BRgWJkXq.js","./LabelSlot-BKRWK_aH.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as I,l as E,o as a,c as i,a as l,u as e,g,F as y,s as L,h as _,w as n,m as S,B as V,q as s,t as d,y as v,b as p,e as m}from"./index-8uvu1PmF.js";import{c as w}from"./state-BEsVv8Mv.js";import{_ as B}from"./_plugin-vue_export-helper-DlAUqK2U.js";import"./utilities-Dq58mqGZ.js";const C={class:"collapse card card-body mb-3",id:"work"},R={key:0},x={key:1},O={key:1},P=I({__name:"WorkplaceDiv",setup(T){const D=p(()=>m(()=>import("./DropDownHead-B7f3Pb2S.js"),__vite__mapDeps([0,1,2]),import.meta.url)),h=p(()=>m(()=>import("./ActionIcons-C-QsqxbB.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),f=p(()=>m(()=>import("./WorkplaceForm-lU0hNg74.js"),__vite__mapDeps([6,1,2,7,8]),import.meta.url)),r=p(()=>m(()=>import("./LabelSlot-BRgWJkXq.js"),__vite__mapDeps([9,1,2,4,10]),import.meta.url)),o=E({itemId:"",item:{},showActions:!1});function b(){o.value.itemId="",Object.keys(o.value.item).forEach(c=>delete o.value.item[c]);const u=document.getElementById("work");u==null||u.setAttribute("class","collapse card card-body mb-3")}return(u,c)=>(a(),i(y,null,[l(e(D),{id:"work",header:"Работа"}),g("div",C,[l(e(f),{onCancel:b})]),e(w).anketa.workplaces.length?(a(),i("div",R,[(a(!0),i(y,null,L(e(w).anketa.workplaces,(t,A)=>(a(),i("div",{key:A,onMouseover:c[0]||(c[0]=k=>o.value.showActions=!0),onMouseout:c[1]||(c[1]=k=>o.value.showActions=!1),class:"card card-body mb-3"},[o.value.itemId===t.id.toString()?(a(),_(e(f),{key:0,work:o.value.item,onCancel:b},null,8,["work"])):(a(),i("div",x,[l(e(r),null,{default:n(()=>[S(l(e(h),{onDelete:k=>e(w).deleteItem(t.id.toString(),"workplaces"),onUpdate:k=>{o.value.item=t,o.value.itemId=t.id.toString()},hide:!0},null,8,["onDelete","onUpdate"]),[[V,o.value.showActions]])]),_:2},1024),t.now_work?(a(),_(e(r),{key:0,label:"Текущая работа"},{default:n(()=>[s(d(t.now_work?"Да":"Нет"),1)]),_:2},1024)):v("",!0),l(e(r),{label:"Начало работы"},{default:n(()=>[s(d(new Date(t.started).toLocaleDateString("ru-RU")),1)]),_:2},1024),t.now_work?v("",!0):(a(),_(e(r),{key:1,label:"Окончание работы"},{default:n(()=>[s(d(new Date(t.finished).toLocaleDateString("ru-RU")),1)]),_:2},1024)),l(e(r),{label:"Место работы"},{default:n(()=>[s(d(t.workplace),1)]),_:2},1024),l(e(r),{label:"Адрес"},{default:n(()=>[s(d(t.address),1)]),_:2},1024),l(e(r),{label:"Должность"},{default:n(()=>[s(d(t.position),1)]),_:2},1024),t.reason?(a(),_(e(r),{key:2,label:"Причина увольнения"},{default:n(()=>[s(d(t.reason),1)]),_:2},1024)):v("",!0)]))],32))),128))])):(a(),i("p",O,"Данные отсутствуют"))],64))}}),M=B(P,[["__scopeId","data-v-35dfead8"]]);export{M as default};
