const __vite__fileDeps=["./DropDownHead-DWPQPqzh.js","./index-D2OLA4OR.js","./index-BqKjTnG4.css","./ActionIcons-B__oqcU7.js","./_plugin-vue_export-helper-DlAUqK2U.js","./ActionIcons-CukUJdTR.css","./AffilationForm-C2DTtrvs.js","./state-BHhWPIxB.js","./LabelSlot-Dfq8r-re.js","./LabelSlot-BKRWK_aH.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as V,r as u,o,c as n,b as a,u as e,e as L,F as g,A as S,m as w,l,g as x,v as B,p as f,t as _,h as c,j as v}from"./index-D2OLA4OR.js";import{f as i,e as P}from"./state-BHhWPIxB.js";import{_ as T}from"./_plugin-vue_export-helper-DlAUqK2U.js";const C={class:"collapse card card-body mb-3",id:"affilationer"},O={key:0},R={key:1},$={key:1},F=V({__name:"AffilationDiv",setup(N){const E=c(()=>v(()=>import("./DropDownHead-DWPQPqzh.js"),__vite__mapDeps([0,1,2]),import.meta.url)),I=c(()=>v(()=>import("./ActionIcons-B__oqcU7.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),A=c(()=>v(()=>import("./AffilationForm-C2DTtrvs.js"),__vite__mapDeps([6,1,2,7]),import.meta.url)),s=c(()=>v(()=>import("./LabelSlot-Dfq8r-re.js"),__vite__mapDeps([8,1,2,4,9]),import.meta.url)),p=u(!1),m=u(!1),b=u(""),D=u({});function y(){m.value=!1,b.value="";const r=document.getElementById("affilationer");r==null||r.setAttribute("class","collapse card card-body mb-3")}return(r,d)=>(o(),n(g,null,[a(e(E),{id:"affilationer",header:"Аффилированность"}),L("div",C,[a(e(A),{onCancel:y})]),e(i).anketa.affilations.length?(o(),n("div",O,[(o(!0),n(g,null,S(e(i).anketa.affilations,(t,h)=>(o(),n("div",{key:h,onMouseover:d[0]||(d[0]=k=>p.value=!0),onMouseout:d[1]||(d[1]=k=>p.value=!1),class:"card card-body mb-3"},[m.value&&b.value==t.id.toString()?(o(),w(e(A),{key:0,affils:D.value,onCancel:y},null,8,["affils"])):(o(),n("div",R,[a(e(s),null,{default:l(()=>[x(a(e(I),{onDelete:k=>e(i).deleteItem(t.id.toString(),"affilations"),onUpdate:k=>{D.value=t,b.value=t.id.toString(),m.value=!0},hide:!0},null,8,["onDelete","onUpdate"]),[[B,p.value&&e(i).anketa.persons.user_id==e(P).userId&&e(i).anketa.persons.standing]])]),_:2},1024),a(e(s),{label:"Тип участия"},{default:l(()=>[f(_(t.view),1)]),_:2},1024),a(e(s),{label:"Организация"},{default:l(()=>[f(_(t.organization),1)]),_:2},1024),a(e(s),{label:"ИНН"},{default:l(()=>[f(_(t.inn),1)]),_:2},1024),a(e(s),{label:"Должность"},{default:l(()=>[f(_(t.position),1)]),_:2},1024)]))],32))),128))])):(o(),n("p",$,"Данные отсутствуют"))],64))}}),z=T(F,[["__scopeId","data-v-ab47d5f5"]]);export{z as default};