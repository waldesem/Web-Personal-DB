const __vite__fileDeps=["./DropDownHead-DsL4Ax-r.js","./index-Cj2pYzZu.js","./index-BqKjTnG4.css","./ActionIcons-Bke58fUs.js","./_plugin-vue_export-helper-DlAUqK2U.js","./ActionIcons-Ns2nW-Me.css","./ContactForm-DhD_QldJ.js","./state-Kc3gs5o9.js","./utilities-BY8xKrXT.js","./LabelSlot-CFQC1Hbj.js","./LabelSlot-BKRWK_aH.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as I,n as E,o,c as s,a as c,u as e,g as b,F as f,x as w,i as g,w as _,q as C,B as V,k,t as A,b as i,e as l}from"./index-Cj2pYzZu.js";import{c as m}from"./state-Kc3gs5o9.js";import{_ as x}from"./_plugin-vue_export-helper-DlAUqK2U.js";import"./utilities-BY8xKrXT.js";const B={class:"collapse card card-body",id:"contact"},L={key:0},S={key:1},O={key:1},P=I({__name:"ContactDiv",setup(T){const h=i(()=>l(()=>import("./DropDownHead-DsL4Ax-r.js"),__vite__mapDeps([0,1,2]),import.meta.url)),y=i(()=>l(()=>import("./ActionIcons-Bke58fUs.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),v=i(()=>l(()=>import("./ContactForm-DhD_QldJ.js"),__vite__mapDeps([6,1,2,7,8]),import.meta.url)),d=i(()=>l(()=>import("./LabelSlot-CFQC1Hbj.js"),__vite__mapDeps([9,1,2,4,10]),import.meta.url)),t=E({itemId:"",item:{},showActions:!1});function p(){t.value.itemId="",Object.keys(t.value.item).forEach(a=>delete t.value.item[a]);const r=document.getElementById("contact");r==null||r.setAttribute("class","collapse card card-body")}return(r,a)=>(o(),s(f,null,[c(e(h),{id:"contact",header:"Контакты"}),b("div",B,[c(e(v),{onCancel:p})]),e(m).anketa.contacts.length?(o(),s("div",L,[(o(!0),s(f,null,w(e(m).anketa.contacts,(n,D)=>(o(),s("div",{key:D,onMouseover:a[0]||(a[0]=u=>t.value.showActions=!0),onMouseout:a[1]||(a[1]=u=>t.value.showActions=!1),class:"card card-body mb-3"},[t.value.itemId===n.id.toString()?(o(),g(e(v),{key:0,contact:t.value.item,onCancel:p},null,8,["contact"])):(o(),s("div",S,[c(e(d),null,{default:_(()=>[C(c(e(y),{onDelete:u=>e(m).deleteItem(n.id.toString(),"contacts"),onUpdate:u=>{t.value.item=n,t.value.itemId=n.id.toString()},hide:!0},null,8,["onDelete","onUpdate"]),[[V,t.value.showActions]])]),_:2},1024),c(e(d),{label:"Вид"},{default:_(()=>[k(A(n.view),1)]),_:2},1024),c(e(d),{label:"Контакт"},{default:_(()=>[k(A(n.contact),1)]),_:2},1024)]))],32))),128))])):(o(),s("p",O,"Данные отсутствуют"))],64))}}),M=x(P,[["__scopeId","data-v-411878ea"]]);export{M as default};
