const __vite__fileDeps=["./DropDownHead-DJv7dHS3.js","./index-1yFXvMEA.js","./index-BqKjTnG4.css","./ActionIcons-D1xqXEN-.js","./_plugin-vue_export-helper-DlAUqK2U.js","./ActionIcons-Ns2nW-Me.css","./PreviousForm-D-LG5oZW.js","./state-QybiP1xm.js","./LabelSlot-DmfbviAy.js","./LabelSlot-BKRWK_aH.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as I,r as E,o as a,c as n,b as i,u as e,e as w,F as D,z as S,m as _,l,g as V,v as L,p as u,t as d,f,h as v,j as p}from"./index-1yFXvMEA.js";import{h as y}from"./state-QybiP1xm.js";import{_ as P}from"./_plugin-vue_export-helper-DlAUqK2U.js";const C={class:"collapse card card-body",id:"previous"},x={key:0},B={key:1},O={key:1},R=I({__name:"PreviousDiv",setup(T){const A=v(()=>p(()=>import("./DropDownHead-DJv7dHS3.js"),__vite__mapDeps([0,1,2]),import.meta.url)),b=v(()=>p(()=>import("./ActionIcons-D1xqXEN-.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),h=v(()=>p(()=>import("./PreviousForm-D-LG5oZW.js"),__vite__mapDeps([6,1,2,7]),import.meta.url)),r=v(()=>p(()=>import("./LabelSlot-DmfbviAy.js"),__vite__mapDeps([8,1,2,4,9]),import.meta.url)),o=E({itemId:"",item:{},showActions:!1});function k(){o.value.itemId="",Object.keys(o.value.item).forEach(s=>delete o.value.item[s]);const c=document.getElementById("previous");c==null||c.setAttribute("class","collapse card card-body")}return(c,s)=>(a(),n(D,null,[i(e(A),{id:"previous",header:"Изменение имени"}),w("div",C,[i(e(h),{onCancel:k})]),e(y).anketa.previous.length?(a(),n("div",x,[(a(!0),n(D,null,S(e(y).anketa.previous,(t,g)=>(a(),n("div",{key:g,onMouseover:s[0]||(s[0]=m=>o.value.showActions=!0),onMouseout:s[1]||(s[1]=m=>o.value.showActions=!1),class:"card card-body"},[o.value.itemId===t.id.toString()?(a(),_(e(h),{key:0,previous:o.value.item,onCancel:k},null,8,["previous"])):(a(),n("div",B,[i(e(r),null,{default:l(()=>[V(i(e(b),{onDelete:m=>e(y).deleteItem(t.id.toString(),"previous"),onUpdate:m=>{o.value.item=t,o.value.itemId=t.id.toString()},hide:!0},null,8,["onDelete","onUpdate"]),[[L,o.value.showActions]])]),_:2},1024),i(e(r),{label:"Фамилия"},{default:l(()=>[u(d(t.surname),1)]),_:2},1024),i(e(r),{label:"Имя"},{default:l(()=>[u(d(t.firstname),1)]),_:2},1024),t.patronymic?(a(),_(e(r),{key:0,label:"Отчество"},{default:l(()=>[u(d(t.patronymic),1)]),_:2},1024)):f("",!0),t.changed?(a(),_(e(r),{key:1,label:"Дата изменения"},{default:l(()=>[u(d(new Date(String(t.changed)).toLocaleDateString("ru-RU")),1)]),_:2},1024)):f("",!0),t.reason?(a(),_(e(r),{key:2,label:"Причина"},{default:l(()=>[u(d(t.reason),1)]),_:2},1024)):f("",!0)]))],32))),128))])):(a(),n("p",O,"Данные отсутствуют"))],64))}}),U=P(R,[["__scopeId","data-v-02256d05"]]);export{U as default};
