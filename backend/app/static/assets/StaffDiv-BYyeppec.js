const __vite__fileDeps=["./DropDownHead-BEOHNMQq.js","./index-D1U1a8b2.js","./index-BqKjTnG4.css","./ActionIcons-CxAFntL3.js","./_plugin-vue_export-helper-DlAUqK2U.js","./ActionIcons-CukUJdTR.css","./StaffForm-JckUVYQ4.js","./state-u74uZLPD.js","./LabelSlot-RdSfBjzZ.js","./LabelSlot-BKRWK_aH.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as S,r as l,o as t,c as o,b as s,u as e,e as V,F as y,z as L,m as x,l as m,g as B,v as C,p as E,t as g,h as d,j as i}from"./index-D1U1a8b2.js";import{g as p}from"./state-u74uZLPD.js";import{_ as P}from"./_plugin-vue_export-helper-DlAUqK2U.js";const T={class:"collapse card card-body mb-3",id:"staffer"},w={key:0},O={key:1},R={key:1},$=S({__name:"StaffDiv",setup(F){const A=d(()=>i(()=>import("./DropDownHead-BEOHNMQq.js"),__vite__mapDeps([0,1,2]),import.meta.url)),I=d(()=>i(()=>import("./ActionIcons-CxAFntL3.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),b=d(()=>i(()=>import("./StaffForm-JckUVYQ4.js"),__vite__mapDeps([6,1,2,7]),import.meta.url)),c=d(()=>i(()=>import("./LabelSlot-RdSfBjzZ.js"),__vite__mapDeps([8,1,2,4,9]),import.meta.url)),u=l(!1),_=l(!1),f=l(""),D=l({});function k(){_.value=!1,f.value="";const n=document.getElementById("staffer");n==null||n.setAttribute("class","collapse card card-body mb-3")}return(n,r)=>(t(),o(y,null,[s(e(A),{id:"staffer",header:"Должности"}),V("div",T,[s(e(b),{onCancel:k})]),e(p).anketa.staffs.length?(t(),o("div",w,[(t(!0),o(y,null,L(e(p).anketa.staffs,(a,h)=>(t(),o("div",{key:h,onMouseover:r[0]||(r[0]=v=>u.value=!0),onMouseout:r[1]||(r[1]=v=>u.value=!1),class:"card card-body mb-3"},[_.value&&f.value==a.id.toString()?(t(),x(e(b),{key:0,staff:D.value,onCancel:k},null,8,["staff"])):(t(),o("div",O,[s(e(c),null,{default:m(()=>[B(s(e(I),{onDelete:v=>e(p).deleteItem(a.id.toString(),"staffs"),onUpdate:v=>{D.value=a,_.value=!0,f.value=a.id.toString()},hide:!0},null,8,["onDelete","onUpdate"]),[[C,u.value]])]),_:2},1024),s(e(c),{label:"Должность"},{default:m(()=>[E(g(a.position),1)]),_:2},1024),s(e(c),{label:"Департамент"},{default:m(()=>[E(g(a.department),1)]),_:2},1024)]))],32))),128))])):(t(),o("p",R,"Данные отсутствуют"))],64))}}),j=P($,[["__scopeId","data-v-435c580b"]]);export{j as default};
