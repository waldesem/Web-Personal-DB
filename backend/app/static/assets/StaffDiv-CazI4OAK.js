const __vite__fileDeps=["./DropDownHead-DWPQPqzh.js","./index-D2OLA4OR.js","./index-BqKjTnG4.css","./ActionIcons-B__oqcU7.js","./_plugin-vue_export-helper-DlAUqK2U.js","./ActionIcons-CukUJdTR.css","./StaffForm-ZnUrQpBp.js","./state-BHhWPIxB.js","./LabelSlot-Dfq8r-re.js","./LabelSlot-BKRWK_aH.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as S,r as d,o as t,c as o,b as s,u as e,e as V,F as y,A as L,m as x,l as m,g as B,v as C,p as A,t as E,h as i,j as u}from"./index-D2OLA4OR.js";import{f as n,e as P}from"./state-BHhWPIxB.js";import{_ as T}from"./_plugin-vue_export-helper-DlAUqK2U.js";const w={class:"collapse card card-body mb-3",id:"staffer"},O={key:0},R={key:1},$={key:1},F=S({__name:"StaffDiv",setup(N){const I=i(()=>u(()=>import("./DropDownHead-DWPQPqzh.js"),__vite__mapDeps([0,1,2]),import.meta.url)),g=i(()=>u(()=>import("./ActionIcons-B__oqcU7.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),k=i(()=>u(()=>import("./StaffForm-ZnUrQpBp.js"),__vite__mapDeps([6,1,2,7]),import.meta.url)),c=i(()=>u(()=>import("./LabelSlot-Dfq8r-re.js"),__vite__mapDeps([8,1,2,4,9]),import.meta.url)),_=d(!1),f=d(!1),p=d(""),D=d({});function b(){f.value=!1,p.value="";const r=document.getElementById("staffer");r==null||r.setAttribute("class","collapse card card-body mb-3")}return(r,l)=>(t(),o(y,null,[s(e(I),{id:"staffer",header:"Должности"}),V("div",w,[s(e(k),{onCancel:b})]),e(n).anketa.staffs.length?(t(),o("div",O,[(t(!0),o(y,null,L(e(n).anketa.staffs,(a,h)=>(t(),o("div",{key:h,onMouseover:l[0]||(l[0]=v=>_.value=!0),onMouseout:l[1]||(l[1]=v=>_.value=!1),class:"card card-body mb-3"},[f.value&&p.value==a.id.toString()?(t(),x(e(k),{key:0,staff:D.value,onCancel:b},null,8,["staff"])):(t(),o("div",R,[s(e(c),null,{default:m(()=>[B(s(e(g),{onDelete:v=>e(n).deleteItem(a.id.toString(),"staffs"),onUpdate:v=>{D.value=a,f.value=!0,p.value=a.id.toString()},hide:!0},null,8,["onDelete","onUpdate"]),[[C,_.value&&e(n).anketa.persons.user_id==e(P).userId&&e(n).anketa.persons.standing]])]),_:2},1024),s(e(c),{label:"Должность"},{default:m(()=>[A(E(a.position),1)]),_:2},1024),s(e(c),{label:"Департамент"},{default:m(()=>[A(E(a.department),1)]),_:2},1024)]))],32))),128))])):(t(),o("p",$,"Данные отсутствуют"))],64))}}),H=T(F,[["__scopeId","data-v-7813ca9e"]]);export{H as default};