const __vite__fileDeps=["./ActionIcons-BCE4-2Qs.js","./index-Dx3HiUnq.js","./index-6fGrG267.css","./PoligrafForm-BlpxiZVj.js","./state-s_e9P3m1.js","./utilities-BVKB9Dez.js","./FileForm-CVXWBM0I.js","./_plugin-vue_export-helper-DlAUqK2U.js","./FileForm-By8_2B11.css","./LabelSlot-DWQlJd1k.js","./LabelSlot-BKRWK_aH.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as h,n as L,o as a,g as v,u as t,c as r,F as x,r as V,b as i,w as l,q as S,z as I,x as c,t as d,e as m,f}from"./index-Dx3HiUnq.js";import{s as _,c as C}from"./state-s_e9P3m1.js";import"./utilities-BVKB9Dez.js";const R={key:1,class:"py-3"},$={key:1},O={key:0,class:"spinner-border-sm text-primary"},B={key:2},q=h({__name:"PoligrafTab",props:{tabAction:{type:String,default:""},currentTab:{type:String,default:""}},emits:["cancel"],setup(w,{emit:D}){const E=m(()=>f(()=>import("./ActionIcons-BCE4-2Qs.js"),__vite__mapDeps([0,1,2]),import.meta.url)),g=m(()=>f(()=>import("./PoligrafForm-BlpxiZVj.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),P=m(()=>f(()=>import("./FileForm-CVXWBM0I.js"),__vite__mapDeps([6,1,2,7,8]),import.meta.url)),s=m(()=>f(()=>import("./LabelSlot-DWQlJd1k.js"),__vite__mapDeps([9,1,2,7,10]),import.meta.url)),b=D,y=w,e=L({itemId:"",item:{},showActions:!1,spinner:!1});function A(){e.value.itemId="",e.value.item={},b("cancel")}function k(p){_.updateItem("poligrafs",p),A()}function T(p){e.value.spinner=!0,C(p,"poligrafs"),e.value.spinner=!1}return(p,n)=>y.tabAction==="create"&&y.currentTab==="PoligrafTab"?(a(),v(t(g),{key:0,onSubmit:k,onCancel:n[0]||(n[0]=o=>b("cancel"))})):t(_).anketa.poligrafs.length?(a(),r("div",R,[(a(!0),r(x,null,V(t(_).anketa.poligrafs,(o,F)=>(a(),r("div",{key:F,onMouseover:n[2]||(n[2]=u=>e.value.showActions=!0),onMouseout:n[3]||(n[3]=u=>e.value.showActions=!1),class:"card card-body mb-3"},[e.value.itemId===o.id.toString()?(a(),v(t(g),{key:0,poligraf:e.value.item,onSubmit:k,onCancel:A},null,8,["poligraf"])):(a(),r("div",$,[i(t(s),null,{default:l(()=>[S(i(t(E),{onDelete:u=>t(_).deleteItem(o.id.toString(),"poligrafs"),onUpdate:u=>{e.value.item=o,e.value.itemId=o.id.toString()},"for-input":"poligrafs-file"},{default:l(()=>[e.value.spinner?(a(),r("span",O)):S((a(),v(t(P),{key:1,"name-id":"poligrafs-file",accept:"*",onSubmit:n[1]||(n[1]=u=>T(u))},null,512)),[[I,e.value.showActions]])]),_:2},1032,["onDelete","onUpdate"]),[[I,e.value.showActions]])]),_:2},1024),i(t(s),{label:"Тема проверки"},{default:l(()=>[c(d(o.theme),1)]),_:2},1024),i(t(s),{label:"Результат"},{default:l(()=>[c(d(o.results),1)]),_:2},1024),i(t(s),{label:"Сотрудник"},{default:l(()=>[c(d(o.user),1)]),_:2},1024),i(t(s),{label:"Дата записи"},{default:l(()=>[c(d(new Date(String(o.created)).toLocaleDateString("ru-RU")),1)]),_:2},1024)]))],32))),128))])):(a(),r("p",B,"Данные отсутствуют"))}});export{q as default};
