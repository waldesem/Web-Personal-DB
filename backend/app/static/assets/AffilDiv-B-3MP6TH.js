const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=["./DropDownHead-D_3exLLE.js","./index-CuxALIEa.js","./index-QNw51pzy.css","./ActionIcons-nL13gtqs.js","./_plugin-vue_export-helper-DlAUqK2U.js","./ActionIcons-CukUJdTR.css","./AffilationForm-CEuTmcoC.js","./state-Dl_2yBjS.js","./LabelSlot-D4bqwlze.js","./LabelSlot-BMshfUVW.css"])))=>i.map(i=>d[i]);
import{d as V,r as d,o as a,c as n,b as o,u as e,e as L,F as g,z as S,m as w,l as u,g as x,v as B,p as b,t as k,h as c,j as f}from"./index-CuxALIEa.js";import{e as s,c as P}from"./state-Dl_2yBjS.js";import{_ as T}from"./_plugin-vue_export-helper-DlAUqK2U.js";const C={class:"collapse card card-body mb-3",id:"affilationer"},O={key:0},R={key:1},$={key:1},F=V({__name:"AffilDiv",setup(N){const E=c(()=>f(()=>import("./DropDownHead-D_3exLLE.js"),__vite__mapDeps([0,1,2]),import.meta.url)),I=c(()=>f(()=>import("./ActionIcons-nL13gtqs.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),A=c(()=>f(()=>import("./AffilationForm-CEuTmcoC.js"),__vite__mapDeps([6,1,2,7]),import.meta.url)),l=c(()=>f(()=>import("./LabelSlot-D4bqwlze.js"),__vite__mapDeps([8,1,2,4,9]),import.meta.url)),_=d(!1),v=d(!1),p=d(""),D=d({});function y(){v.value=!1,p.value="";const r=document.getElementById("affilationer");r==null||r.setAttribute("class","collapse card card-body mb-3")}return(r,i)=>(a(),n(g,null,[o(e(E),{id:"affilationer",header:"Аффилированность"}),L("div",C,[o(e(A),{onCancel:y})]),e(s).anketa.affilations.length?(a(),n("div",O,[(a(!0),n(g,null,S(e(s).anketa.affilations,(t,h)=>(a(),n("div",{key:h,onMouseover:i[0]||(i[0]=m=>_.value=!0),onMouseout:i[1]||(i[1]=m=>_.value=!1),class:"card card-body mb-3"},[v.value&&p.value==t.id.toString()?(a(),w(e(A),{key:0,affils:D.value,onCancel:y},null,8,["affils"])):(a(),n("div",R,[o(e(l),null,{default:u(()=>[x(o(e(I),{onDelete:m=>e(s).deleteItem(t.id.toString(),"affilations"),onUpdate:m=>{D.value=t,p.value=t.id.toString(),v.value=!0},hide:!0},null,8,["onDelete","onUpdate"]),[[B,_.value&&e(s).anketa.persons.user_id==e(P).user.userId&&e(s).anketa.persons.standing]])]),_:2},1024),o(e(l),{label:"Тип участия"},{default:u(()=>[b(k(t.view),1)]),_:2},1024),o(e(l),{label:"Организация"},{default:u(()=>[b(k(t.organization),1)]),_:2},1024),o(e(l),{label:"ИНН"},{default:u(()=>[b(k(t.inn),1)]),_:2},1024)]))],32))),128))])):(a(),n("p",$,"Данные отсутствуют"))],64))}}),j=T(F,[["__scopeId","data-v-2f1b14c0"]]);export{j as default};