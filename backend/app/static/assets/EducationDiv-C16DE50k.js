const __vite__fileDeps=["./ActionHeader-BqcdmkJM.js","./index-BhwzwnLH.js","./index-6fGrG267.css","./ActionIcons-BkvQs5mF.js","./EducationForm-BKXNgyNW.js","./utilities-DuY9392d.js","./state-BY_Xl-td.js","./LabelSlot-DtLQ-bg4.js","./_plugin-vue_export-helper-DlAUqK2U.js","./LabelSlot-BKRWK_aH.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as E,i as D,n as g,o as n,c as u,b as i,u as t,g as A,q as S,F as k,r as V,w as s,s as $,A as C,y as c,t as v,e as m,f as _}from"./index-BhwzwnLH.js";import{s as d}from"./state-BY_Xl-td.js";import"./utilities-DuY9392d.js";const L={key:1,class:"collapse show",id:"education"},h={key:1},P={key:2},O=E({__name:"EducationDiv",setup(T){const y=m(()=>_(()=>import("./ActionHeader-BqcdmkJM.js"),__vite__mapDeps([0,1,2]),import.meta.url)),b=m(()=>_(()=>import("./ActionIcons-BkvQs5mF.js"),__vite__mapDeps([3,1,2]),import.meta.url)),p=m(()=>_(()=>import("./EducationForm-BKXNgyNW.js"),__vite__mapDeps([4,1,2,5,6]),import.meta.url)),l=m(()=>_(()=>import("./LabelSlot-DtLQ-bg4.js"),__vite__mapDeps([7,1,2,8,9]),import.meta.url));D(async()=>{await d.getItem("educations")});const e=g({action:"",itemId:"",item:{},showActions:!1});function f(I){d.updateItem(e.value.action,"educations",e.value.itemId,I),e.value.action="",e.value.itemId=""}return(I,o)=>(n(),u(k,null,[i(t(y),{id:"education",header:"Образование",action:e.value.action,onAction:o[0]||(o[0]=a=>e.value.action=e.value.action?"":"create")},null,8,["action"]),e.value.action==="create"?(n(),A(t(p),{key:0,onSubmit:f,onCancel:o[1]||(o[1]=a=>{e.value.action="",e.value.itemId=""})})):S("",!0),t(d).anketa.educations.length?(n(),u("div",L,[(n(!0),u(k,null,V(t(d).anketa.educations,(a,w)=>(n(),u("div",{key:w,onMouseover:o[3]||(o[3]=r=>e.value.showActions=!0),onMouseout:o[4]||(o[4]=r=>e.value.showActions=!1),class:"card card-body mb-3"},[e.value.action==="update"&&e.value.itemId===a.id.toString()?(n(),A(t(p),{key:0,education:e.value.item,onSubmit:f,onCancel:o[2]||(o[2]=r=>{e.value.action="",e.value.itemId=""})},null,8,["education"])):(n(),u("div",h,[i(t(l),null,{default:s(()=>[$(i(t(b),{onDelete:r=>t(d).deleteItem(a.id.toString(),"educations"),onUpdate:r=>{e.value.action="update",e.value.item=a,e.value.itemId=a.id.toString()}},null,8,["onDelete","onUpdate"]),[[C,e.value.showActions]])]),_:2},1024),i(t(l),{label:"Вид образования"},{default:s(()=>[c(v(a.view),1)]),_:2},1024),i(t(l),{label:"Название учебного заведения"},{default:s(()=>[c(v(a.name),1)]),_:2},1024),i(t(l),{label:"Год окончания"},{default:s(()=>[c(v(a.finished),1)]),_:2},1024),i(t(l),{label:"Специальность"},{default:s(()=>[c(v(a.speciality),1)]),_:2},1024)]))],32))),128))])):(n(),u("p",P,"Данные отсутствуют"))],64))}});export{O as default};