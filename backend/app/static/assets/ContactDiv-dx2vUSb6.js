const __vite__fileDeps=["./ActionHeader-B5rljA6q.js","./index-BCJo_gEN.js","./index-6fGrG267.css","./ActionIcons-Dw34qmV0.js","./ContactForm-Dz08PZGL.js","./utilities-B_ayHb2j.js","./state-CDYnk2KN.js","./LabelSlot-CvGLSY44.js","./_plugin-vue_export-helper-DlAUqK2U.js","./LabelSlot-BKRWK_aH.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as S,i as y,n as E,o as n,c as i,b as l,u as e,g as f,B as w,F as A,r as L,w as s,q as C,z as V,x as u,t as d,e as v,f as m}from"./index-BCJo_gEN.js";import{s as c}from"./state-CDYnk2KN.js";import"./utilities-B_ayHb2j.js";const R={key:1,class:"collapse show",id:"contact"},$={key:2},T=S({__name:"ContactDiv",setup(h){const D=v(()=>m(()=>import("./ActionHeader-B5rljA6q.js"),__vite__mapDeps([0,1,2]),import.meta.url)),I=v(()=>m(()=>import("./ActionIcons-Dw34qmV0.js"),__vite__mapDeps([3,1,2]),import.meta.url)),g=v(()=>m(()=>import("./ContactForm-Dz08PZGL.js"),__vite__mapDeps([4,1,2,5,6]),import.meta.url)),r=v(()=>m(()=>import("./LabelSlot-CvGLSY44.js"),__vite__mapDeps([7,1,2,8,9]),import.meta.url));y(async()=>{await c.getItem("contacts")});const t=E({action:"",itemId:"",item:{},showActions:!1});function k(p){c.updateItem(t.value.action,"contacts",t.value.itemId,p),t.value.action="",t.value.itemId=""}return(p,o)=>(n(),i(A,null,[l(e(D),{id:"contact",header:"Контакты",action:t.value.action,onAction:o[0]||(o[0]=a=>t.value.action=t.value.action?"":"create")},null,8,["action"]),t.value.action==="create"?(n(),f(e(g),{key:0,contact:t.value.item,onSubmit:k,onCancel:o[1]||(o[1]=a=>t.value.action="")},null,8,["contact"])):w("",!0),e(c).anketa.contacts.length?(n(),i("div",R,[(n(!0),i(A,null,L(e(c).anketa.contacts,(a,b)=>(n(),i("div",{key:b,onMouseover:o[2]||(o[2]=_=>t.value.showActions=!0),onMouseout:o[3]||(o[3]=_=>t.value.showActions=!1),class:"card card-body mb-3"},[l(e(r),null,{default:s(()=>[C(l(e(I),{onDelete:_=>e(c).deleteItem(a.id.toString(),"contacts"),onUpdate:_=>{t.value.action="update",t.value.item=a,t.value.itemId=a.id.toString()}},null,8,["onDelete","onUpdate"]),[[V,t.value.showActions]])]),_:2},1024),l(e(r),{label:"Вид"},{default:s(()=>[u(d(a.view),1)]),_:2},1024),l(e(r),{label:"Контакт"},{default:s(()=>[u(d(a.contact),1)]),_:2},1024),l(e(r),{label:"Дата"},{default:s(()=>[u(d(new Date(String(a.created)).toLocaleDateString("ru-RU")),1)]),_:2},1024),a.updated?(n(),f(e(r),{key:0,label:"Обновлено"},{default:s(()=>[u(d(new Date(String(a.updated)).toLocaleDateString("ru-RU")),1)]),_:2},1024)):w("",!0)],32))),128))])):(n(),i("p",$,"Данные отсутствуют"))],64))}});export{T as default};
