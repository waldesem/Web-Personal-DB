const __vite__fileDeps=["./ActionHeader-BMAkxzmt.js","./index-K0Y79g34.js","./index-6fGrG267.css","./ActionIcons-D1_KH3vh.js","./AffilationForm-a_UWGuSy.js","./state-CXEVWkFn.js","./LabelSlot-CcnVWBIm.js","./_plugin-vue_export-helper-DlAUqK2U.js","./LabelSlot-BKRWK_aH.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as D,n as E,o,c as l,b as n,u as t,g as b,C as S,F as I,r as g,w as u,q as C,z as V,x as r,t as c,e as d,f}from"./index-K0Y79g34.js";import{s as m}from"./state-CXEVWkFn.js";const L={key:1,class:"collapse show",id:"affilation"},x={key:1},P={key:2},O=D({__name:"AffilationDiv",setup(T){const w=d(()=>f(()=>import("./ActionHeader-BMAkxzmt.js"),__vite__mapDeps([0,1,2]),import.meta.url)),h=d(()=>f(()=>import("./ActionIcons-D1_KH3vh.js"),__vite__mapDeps([3,1,2]),import.meta.url)),p=d(()=>f(()=>import("./AffilationForm-a_UWGuSy.js"),__vite__mapDeps([4,1,2,5]),import.meta.url)),s=d(()=>f(()=>import("./LabelSlot-CcnVWBIm.js"),__vite__mapDeps([6,1,2,7,8]),import.meta.url)),e=E({action:"",itemId:"",item:{},showActions:!1});function v(){e.value.action="",e.value.itemId="",e.value.item={}}function A(k){m.updateItem("affilations",k),v()}return(k,i)=>(o(),l(I,null,[n(t(w),{header:"Аффилированность",action:e.value.action,onAction:i[0]||(i[0]=a=>e.value.action=e.value.action?"":"create")},null,8,["action"]),e.value.action==="create"?(o(),b(t(p),{key:0,affils:e.value.item,onSubmit:A,onCancel:v},null,8,["affils"])):S("",!0),t(m).anketa.affilations.length?(o(),l("div",L,[(o(!0),l(I,null,g(t(m).anketa.affilations,(a,y)=>(o(),l("div",{key:y,onMouseover:i[1]||(i[1]=_=>e.value.showActions=!0),onMouseout:i[2]||(i[2]=_=>e.value.showActions=!1),class:"card card-body mb-3"},[e.value.action==="update"&&e.value.itemId===a.id.toString()?(o(),b(t(p),{key:0,affils:e.value.item,onSubmit:A,onCancel:v},null,8,["affils"])):(o(),l("div",x,[n(t(s),null,{default:u(()=>[C(n(t(h),{onDelete:_=>t(m).deleteItem(a.id.toString(),"affilations"),onUpdate:_=>{e.value.action="update",e.value.item=a,e.value.itemId=a.id.toString()},hide:!0},null,8,["onDelete","onUpdate"]),[[V,e.value.showActions]])]),_:2},1024),n(t(s),{label:"Тип участия"},{default:u(()=>[r(c(a.view),1)]),_:2},1024),n(t(s),{label:"Организация"},{default:u(()=>[r(c(a.name),1)]),_:2},1024),n(t(s),{label:"ИНН"},{default:u(()=>[r(c(a.inn),1)]),_:2},1024),n(t(s),{label:"Должность"},{default:u(()=>[r(c(a.position),1)]),_:2},1024)]))],32))),128))])):(o(),l("p",P,"Данные отсутствуют"))],64))}});export{O as default};
