const __vite__fileDeps=["./DropDownHead-amleYETa.js","./index-DCiFGIcJ.js","./index-BqKjTnG4.css","./ActionIcons-drW2QoDS.js","./_plugin-vue_export-helper-DlAUqK2U.js","./ActionIcons-B4kU7i0h.css","./PreviousForm-DvsJgjlj.js","./state-Kk6UeE2d.js","./utilities-DksN3XFX.js","./LabelSlot-BomMvJ3C.js","./LabelSlot-BKRWK_aH.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as g,m as E,o as a,c as n,a as i,u as e,h as w,F as k,y as S,i as _,w as l,q as V,C,t as u,x as d,n as f,b as v,e as p}from"./index-DCiFGIcJ.js";import{c as y}from"./state-Kk6UeE2d.js";import{_ as L}from"./_plugin-vue_export-helper-DlAUqK2U.js";import"./utilities-DksN3XFX.js";const P={class:"collapse card card-body mb-3",id:"previous"},x={key:0},B={key:1},O={key:1},R=g({__name:"PreviousDiv",setup(T){const D=v(()=>p(()=>import("./DropDownHead-amleYETa.js"),__vite__mapDeps([0,1,2]),import.meta.url)),A=v(()=>p(()=>import("./ActionIcons-drW2QoDS.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),b=v(()=>p(()=>import("./PreviousForm-DvsJgjlj.js"),__vite__mapDeps([6,1,2,7,8]),import.meta.url)),r=v(()=>p(()=>import("./LabelSlot-BomMvJ3C.js"),__vite__mapDeps([9,1,2,4,10]),import.meta.url)),o=E({itemId:"",item:{},showActions:!1});function h(){o.value.itemId="",Object.keys(o.value.item).forEach(s=>delete o.value.item[s]);const c=document.getElementById("previous");c==null||c.setAttribute("class","collapse card card-body mb-3")}return(c,s)=>(a(),n(k,null,[i(e(D),{id:"previous",header:"Изменение имени"}),w("div",P,[i(e(b),{onCancel:h})]),e(y).anketa.previous.length?(a(),n("div",x,[(a(!0),n(k,null,S(e(y).anketa.previous,(t,I)=>(a(),n("div",{key:I,onMouseover:s[0]||(s[0]=m=>o.value.showActions=!0),onMouseout:s[1]||(s[1]=m=>o.value.showActions=!1),class:"card card-body mb-3"},[o.value.itemId===t.id.toString()?(a(),_(e(b),{key:0,previous:o.value.item,onCancel:h},null,8,["previous"])):(a(),n("div",B,[i(e(r),null,{default:l(()=>[V(i(e(A),{onDelete:m=>e(y).deleteItem(t.id.toString(),"previous"),onUpdate:m=>{o.value.item=t,o.value.itemId=t.id.toString()},hide:!0},null,8,["onDelete","onUpdate"]),[[C,o.value.showActions]])]),_:2},1024),i(e(r),{label:"Фамилия"},{default:l(()=>[u(d(t.surname),1)]),_:2},1024),i(e(r),{label:"Имя"},{default:l(()=>[u(d(t.firstname),1)]),_:2},1024),t.patronymic?(a(),_(e(r),{key:0,label:"Отчество"},{default:l(()=>[u(d(t.patronymic),1)]),_:2},1024)):f("",!0),t.changed?(a(),_(e(r),{key:1,label:"Дата изменения"},{default:l(()=>[u(d(new Date(String(t.changed)).toLocaleDateString("ru-RU")),1)]),_:2},1024)):f("",!0),t.reason?(a(),_(e(r),{key:2,label:"Причина"},{default:l(()=>[u(d(t.reason),1)]),_:2},1024)):f("",!0)]))],32))),128))])):(a(),n("p",O,"Данные отсутствуют"))],64))}}),M=L(R,[["__scopeId","data-v-9ff10445"]]);export{M as default};
