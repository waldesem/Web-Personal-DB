const __vite__fileDeps=["./DropDownHead-DsL4Ax-r.js","./index-Cj2pYzZu.js","./index-BqKjTnG4.css","./ActionIcons-Bke58fUs.js","./_plugin-vue_export-helper-DlAUqK2U.js","./ActionIcons-Ns2nW-Me.css","./RelationForm-DoM8lafH.js","./state-Kc3gs5o9.js","./utilities-BY8xKrXT.js","./LabelSlot-CFQC1Hbj.js","./LabelSlot-BKRWK_aH.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as E,n as b,j as w,o as a,c as i,a as n,u as t,g,F as f,x as V,i as x,w as l,q as B,B as C,k,t as A,b as d,e as c}from"./index-Cj2pYzZu.js";import{c as m}from"./state-Kc3gs5o9.js";import{_ as L}from"./_plugin-vue_export-helper-DlAUqK2U.js";import"./utilities-BY8xKrXT.js";const R={class:"collapse card card-body",id:"relation"},S={key:0},O={key:1},P={key:1},T=E({__name:"RelationDiv",setup($){const D=d(()=>c(()=>import("./DropDownHead-DsL4Ax-r.js"),__vite__mapDeps([0,1,2]),import.meta.url)),I=d(()=>c(()=>import("./ActionIcons-Bke58fUs.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),p=d(()=>c(()=>import("./RelationForm-DoM8lafH.js"),__vite__mapDeps([6,1,2,7,8]),import.meta.url)),_=d(()=>c(()=>import("./LabelSlot-CFQC1Hbj.js"),__vite__mapDeps([9,1,2,4,10]),import.meta.url)),e=b({itemId:"",item:{},showActions:!1});function v(){e.value.itemId="",Object.keys(e.value.item).forEach(r=>delete e.value.item[r]);const s=document.getElementById("relation");s==null||s.setAttribute("class","collapse card card-body")}return(s,r)=>{const h=w("router-link");return a(),i(f,null,[n(t(D),{id:"relation",header:"Связи"}),g("div",R,[n(t(p),{onCancel:v})]),t(m).anketa.relations.length?(a(),i("div",S,[(a(!0),i(f,null,V(t(m).anketa.relations,(o,y)=>(a(),i("div",{key:y,class:"card card-body mb-3",onMouseover:r[0]||(r[0]=u=>e.value.showActions=!0),onMouseout:r[1]||(r[1]=u=>e.value.showActions=!1)},[e.value.itemId===o.id.toString()?(a(),x(t(p),{key:0,relation:e.value.item,onCancel:v},null,8,["relation"])):(a(),i("div",O,[n(t(_),null,{default:l(()=>[B(n(t(I),{hide:!0,onDelete:u=>t(m).deleteItem(o.id.toString(),"relations"),onUpdate:u=>{e.value.item=o,e.value.itemId=o.id.toString()}},null,8,["onDelete","onUpdate"]),[[C,e.value.showActions]])]),_:2},1024),n(t(_),{label:"Тип"},{default:l(()=>[k(A(o.relation),1)]),_:2},1024),n(t(_),{label:"Связь"},{default:l(()=>[n(h,{to:{name:"profile",params:{id:o.relation_id}}},{default:l(()=>[k(" ID #"+A(o.relation_id),1)]),_:2},1032,["to"])]),_:2},1024)]))],32))),128))])):(a(),i("p",P,"Данные отсутствуют"))],64)}}}),U=L(T,[["__scopeId","data-v-0c280fd2"]]);export{U as default};
