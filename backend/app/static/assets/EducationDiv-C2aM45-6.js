const __vite__fileDeps=["./DropDownHead-B7f3Pb2S.js","./index-8uvu1PmF.js","./index-BqKjTnG4.css","./ActionIcons-C-QsqxbB.js","./_plugin-vue_export-helper-DlAUqK2U.js","./ActionIcons-B4kU7i0h.css","./EducationForm-DdPMjXG-.js","./state-BEsVv8Mv.js","./utilities-Dq58mqGZ.js","./LabelSlot-BRgWJkXq.js","./LabelSlot-BKRWK_aH.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as k,l as D,o as n,c as i,a,u as e,g as I,F as h,s as w,h as g,w as l,m as V,B,q as c,t as u,b as _,e as m}from"./index-8uvu1PmF.js";import{c as p}from"./state-BEsVv8Mv.js";import{_ as L}from"./_plugin-vue_export-helper-DlAUqK2U.js";import"./utilities-Dq58mqGZ.js";const S={class:"collapse card card-body mb-3",id:"education"},x={key:0},C={key:1},O={key:1},T=k({__name:"EducationDiv",setup(P){const E=_(()=>m(()=>import("./DropDownHead-B7f3Pb2S.js"),__vite__mapDeps([0,1,2]),import.meta.url)),y=_(()=>m(()=>import("./ActionIcons-C-QsqxbB.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),f=_(()=>m(()=>import("./EducationForm-DdPMjXG-.js"),__vite__mapDeps([6,1,2,7,8]),import.meta.url)),d=_(()=>m(()=>import("./LabelSlot-BRgWJkXq.js"),__vite__mapDeps([9,1,2,4,10]),import.meta.url)),t=D({itemId:"",item:{},showActions:!1});function b(){t.value.itemId="",Object.keys(t.value.item).forEach(s=>delete t.value.item[s]);const r=document.getElementById("education");r==null||r.setAttribute("class","collapse card card-body mb-3")}return(r,s)=>(n(),i(h,null,[a(e(E),{id:"education",header:"Образование"}),I("div",S,[a(e(f),{onCancel:b})]),e(p).anketa.educations.length?(n(),i("div",x,[(n(!0),i(h,null,w(e(p).anketa.educations,(o,A)=>(n(),i("div",{key:A,onMouseover:s[0]||(s[0]=v=>t.value.showActions=!0),onMouseout:s[1]||(s[1]=v=>t.value.showActions=!1),class:"card card-body mb-3"},[t.value.itemId===o.id.toString()?(n(),g(e(f),{key:0,education:t.value.item,onCancel:b},null,8,["education"])):(n(),i("div",C,[a(e(d),null,{default:l(()=>[V(a(e(y),{onDelete:v=>e(p).deleteItem(o.id.toString(),"educations"),onUpdate:v=>{t.value.item=o,t.value.itemId=o.id.toString()},hide:!0},null,8,["onDelete","onUpdate"]),[[B,t.value.showActions]])]),_:2},1024),a(e(d),{label:"Уровень образования"},{default:l(()=>[c(u(o.view),1)]),_:2},1024),a(e(d),{label:"Название учебного заведения"},{default:l(()=>[c(u(o.name),1)]),_:2},1024),a(e(d),{label:"Год окончания"},{default:l(()=>[c(u(o.finished),1)]),_:2},1024),a(e(d),{label:"Специальность"},{default:l(()=>[c(u(o.speciality),1)]),_:2},1024)]))],32))),128))])):(n(),i("p",O,"Данные отсутствуют"))],64))}}),M=L(T,[["__scopeId","data-v-333148e1"]]);export{M as default};
