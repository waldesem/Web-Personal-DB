const __vite__fileDeps=["assets/ActionHeader--2fnFKkH.js","assets/index-BhT_3F5B.js","assets/index-D3owuatg.css","assets/ActionIcons-Bi7YhEuM.js","assets/DocumentForm-BqGEln98.js","assets/LabelSlot-C8Y-0GKw.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as y,n as E,J as u,q as S,o as n,c as i,b as l,u as t,k as b,K as C,E as k,F as A,x as L,w as d,t as P,v as V,B as r,C as c,e as m,f as _}from"./index-BhT_3F5B.js";const $={key:1},h={key:2},R=y({__name:"DocumentDiv",setup(x){const D=m(()=>_(()=>import("./ActionHeader--2fnFKkH.js"),__vite__mapDeps([0,1,2]))),g=m(()=>_(()=>import("./ActionIcons-Bi7YhEuM.js"),__vite__mapDeps([3,1,2]))),p=m(()=>_(()=>import("./DocumentForm-BqGEln98.js"),__vite__mapDeps([4,1,2]))),s=m(()=>_(()=>import("./LabelSlot-C8Y-0GKw.js"),__vite__mapDeps([5,1,2])));E(async()=>{await u.getItem("document")});const e=S({action:"",itemId:"",item:{},showActions:!1});function f(I){u.updateItem(e.value.action,"document",e.value.itemId,I),e.value.action="",e.value.itemId=""}return(I,a)=>(n(),i(A,null,[l(t(D),{id:"document",header:"Документы",action:e.value.action,onAction:a[0]||(a[0]=o=>e.value.action=e.value.action?"":"create")},null,8,["action"]),e.value.action==="create"?(n(),b(t(p),{key:0,docs:e.value.item,onSubmit:f,onCancel:a[1]||(a[1]=o=>{e.value.action="",e.value.itemId=""})},null,8,["docs"])):C("",!0),t(u).anketa.document.length?(n(),i("div",{key:1,class:k({"collapse show":!t(u).share.printPage}),id:"document"},[(n(!0),i(A,null,L(t(u).anketa.document,(o,w)=>(n(),i("div",{class:k(["mb-3",{"card card-body":!t(u).share.printPage}]),key:w,onMouseover:a[3]||(a[3]=v=>e.value.showActions=!0),onMouseout:a[4]||(a[4]=v=>e.value.showActions=!1)},[e.value.action==="update"&&e.value.itemId===o.id.toString()?(n(),b(t(p),{key:0,docs:e.value.item,onSubmit:f,onCancel:a[2]||(a[2]=v=>{e.value.action="",e.value.itemId=""})},null,8,["docs"])):(n(),i("div",$,[l(t(s),null,{default:d(()=>[P(l(t(g),{onDelete:v=>t(u).deleteItem(o.id.toString(),"document"),onUpdate:v=>{e.value.action="update",e.value.item=o,e.value.itemId=o.id.toString()}},null,8,["onDelete","onUpdate"]),[[V,e.value.showActions]])]),_:2},1024),l(t(s),{label:"Вид документа"},{default:d(()=>[r(c(o.view),1)]),_:2},1024),l(t(s),{label:"Номер документа"},{default:d(()=>[r(c(o.number),1)]),_:2},1024),l(t(s),{label:"Серия документа"},{default:d(()=>[r(c(o.series),1)]),_:2},1024),l(t(s),{label:"Кем выдан"},{default:d(()=>[r(c(o.agency),1)]),_:2},1024),l(t(s),{label:"Дата выдачи"},{default:d(()=>[r(c(new Date(String(o.issue)).toLocaleDateString("ru-RU")),1)]),_:2},1024)]))],34))),128))],2)):(n(),i("p",h,"Данные отсутствуют"))],64))}});export{R as default};
