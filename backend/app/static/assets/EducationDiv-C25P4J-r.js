const __vite__fileDeps=["./ActionHeader-CPtlKGZ4.js","./index-DRtVOEFB.js","./index-6fGrG267.css","./ActionIcons-DZ7YM6Q8.js","./EducationForm-B33VNli7.js","./state-Skb32c17.js","./utilities-BFRXa8zy.js","./LabelSlot-Bx6cFhlr.js","./_plugin-vue_export-helper-DlAUqK2U.js","./LabelSlot-BKRWK_aH.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as I,n as b,o,c as l,a as n,u as t,g as k,C as D,F as E,r as g,w as u,q as C,z as V,x as r,t as c,b as d,e as v}from"./index-DRtVOEFB.js";import{s as m}from"./state-Skb32c17.js";import"./utilities-BFRXa8zy.js";const L={key:1,class:"collapse show",id:"education"},S={key:1},x={key:2},R=I({__name:"EducationDiv",setup(O){const h=d(()=>v(()=>import("./ActionHeader-CPtlKGZ4.js"),__vite__mapDeps([0,1,2]),import.meta.url)),y=d(()=>v(()=>import("./ActionIcons-DZ7YM6Q8.js"),__vite__mapDeps([3,1,2]),import.meta.url)),p=d(()=>v(()=>import("./EducationForm-B33VNli7.js"),__vite__mapDeps([4,1,2,5,6]),import.meta.url)),s=d(()=>v(()=>import("./LabelSlot-Bx6cFhlr.js"),__vite__mapDeps([7,1,2,8,9]),import.meta.url)),e=b({action:"",itemId:"",item:{},showActions:!1});function f(){e.value.action="",e.value.itemId="",Object.keys(e.value.item).forEach(A=>delete e.value.item[A])}return(A,i)=>(o(),l(E,null,[n(t(h),{id:"education",header:"Образование",action:e.value.action,onAction:i[0]||(i[0]=a=>e.value.action=e.value.action?"":"create")},null,8,["action"]),e.value.action==="create"?(o(),k(t(p),{key:0,onCancel:f})):D("",!0),t(m).anketa.educations.length?(o(),l("div",L,[(o(!0),l(E,null,g(t(m).anketa.educations,(a,w)=>(o(),l("div",{key:w,onMouseover:i[1]||(i[1]=_=>e.value.showActions=!0),onMouseout:i[2]||(i[2]=_=>e.value.showActions=!1),class:"card card-body mb-3"},[e.value.action==="update"&&e.value.itemId===a.id.toString()?(o(),k(t(p),{key:0,education:e.value.item,onCancel:f},null,8,["education"])):(o(),l("div",S,[n(t(s),null,{default:u(()=>[C(n(t(y),{onDelete:_=>t(m).deleteItem(a.id.toString(),"educations"),onUpdate:_=>{e.value.action="update",e.value.item=a,e.value.itemId=a.id.toString()},hide:!0},null,8,["onDelete","onUpdate"]),[[V,e.value.showActions]])]),_:2},1024),n(t(s),{label:"Вид образования"},{default:u(()=>[r(c(a.view),1)]),_:2},1024),n(t(s),{label:"Название учебного заведения"},{default:u(()=>[r(c(a.name),1)]),_:2},1024),n(t(s),{label:"Год окончания"},{default:u(()=>[r(c(a.finished),1)]),_:2},1024),n(t(s),{label:"Специальность"},{default:u(()=>[r(c(a.speciality),1)]),_:2},1024)]))],32))),128))])):(o(),l("p",x,"Данные отсутствуют"))],64))}});export{R as default};
