const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=["./DropDownHead-Dbxg8NWj.js","./index-BZDug3Gw.js","./index-BqKjTnG4.css","./ActionIcons-BnMunXz1.js","./_plugin-vue_export-helper-DlAUqK2U.js","./ActionIcons-CukUJdTR.css","./ContactForm-B35XW8BW.js","./state-Cwn6w3yA.js","./LabelSlot-CazHWzn8.js","./LabelSlot-BKRWK_aH.css"])))=>i.map(i=>d[i]);
import{d as C,r as l,o as t,c as o,b as n,u as e,e as V,F as y,A as L,m as S,l as f,g as w,v as x,p as A,t as E,h as d,j as i}from"./index-BZDug3Gw.js";import{e as s,c as B}from"./state-Cwn6w3yA.js";import{_ as P}from"./_plugin-vue_export-helper-DlAUqK2U.js";const T={class:"collapse card card-body mb-3",id:"contacter"},O={key:0},R={key:1},$={key:1},F=C({__name:"ContactDiv",setup(N){const I=d(()=>i(()=>import("./DropDownHead-Dbxg8NWj.js"),__vite__mapDeps([0,1,2]),import.meta.url)),g=d(()=>i(()=>import("./ActionIcons-BnMunXz1.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),k=d(()=>i(()=>import("./ContactForm-B35XW8BW.js"),__vite__mapDeps([6,1,2,7]),import.meta.url)),u=d(()=>i(()=>import("./LabelSlot-CazHWzn8.js"),__vite__mapDeps([8,1,2,4,9]),import.meta.url)),_=l(!1),v=l(""),p=l(!1),D=l({});function b(){p.value=!1,v.value="";const r=document.getElementById("contacter");r==null||r.setAttribute("class","collapse card card-body mb-3")}return(r,c)=>(t(),o(y,null,[n(e(I),{id:"contacter",header:"Контакты"}),V("div",T,[n(e(k),{onCancel:b})]),e(s).anketa.contacts.length?(t(),o("div",O,[(t(!0),o(y,null,L(e(s).anketa.contacts,(a,h)=>(t(),o("div",{key:h,onMouseover:c[0]||(c[0]=m=>_.value=!0),onMouseout:c[1]||(c[1]=m=>_.value=!1),class:"card card-body mb-3"},[p.value&&v.value==a.id.toString()?(t(),S(e(k),{key:0,contact:D.value,onCancel:b},null,8,["contact"])):(t(),o("div",R,[n(e(u),null,{default:f(()=>[w(n(e(g),{onDelete:m=>e(s).deleteItem(a.id.toString(),"contacts"),onUpdate:m=>{D.value=a,v.value=a.id.toString(),p.value=!0},hide:!0},null,8,["onDelete","onUpdate"]),[[x,_.value&&e(s).anketa.persons.user_id==e(B).user.userId&&e(s).anketa.persons.standing]])]),_:2},1024),n(e(u),{label:"Вид"},{default:f(()=>[A(E(a.view),1)]),_:2},1024),n(e(u),{label:"Контакт"},{default:f(()=>[A(E(a.contact),1)]),_:2},1024)]))],32))),128))])):(t(),o("p",$,"Данные отсутствуют"))],64))}}),H=P(F,[["__scopeId","data-v-f47d51fa"]]);export{H as default};
