const __vite__fileDeps=["./ActionIcons-D1xqXEN-.js","./index-1yFXvMEA.js","./index-BqKjTnG4.css","./_plugin-vue_export-helper-DlAUqK2U.js","./ActionIcons-Ns2nW-Me.css","./LabelSlot-DmfbviAy.js","./LabelSlot-BKRWK_aH.css","./FileForm-DvW3KssW.js","./FileForm-By8_2B11.css","./CheckForm-ByPU7JGc.js","./state-QybiP1xm.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as g,r as D,o as d,c as u,e as h,b as a,u as e,F as y,z as C,m as S,l,g as A,v as I,t as s,p as n,h as f,j as p}from"./index-1yFXvMEA.js";import{h as b,g as T}from"./state-QybiP1xm.js";import{_ as L}from"./_plugin-vue_export-helper-DlAUqK2U.js";const V={class:"collapse card card-body",id:"check"},F={key:0},x={key:1},B={class:"fs-5 fw-medium text-primary p-1"},O={key:1,class:"p-3"},P=g({__name:"CheckTab",setup(R){const w=f(()=>p(()=>import("./ActionIcons-D1xqXEN-.js"),__vite__mapDeps([0,1,2,3,4]),import.meta.url)),o=f(()=>p(()=>import("./LabelSlot-DmfbviAy.js"),__vite__mapDeps([5,1,2,3,6]),import.meta.url)),E=f(()=>p(()=>import("./FileForm-DvW3KssW.js"),__vite__mapDeps([7,1,2,3,8]),import.meta.url)),v=f(()=>p(()=>import("./CheckForm-ByPU7JGc.js"),__vite__mapDeps([9,1,2,10]),import.meta.url)),c=D({itemId:"",item:{},showActions:!1});function k(){c.value.itemId="",Object.keys(c.value.item).forEach(r=>delete c.value.item[r]);const i=document.getElementById("check");i==null||i.setAttribute("class","collapse card card-body")}return(i,r)=>(d(),u(y,null,[h("div",V,[a(e(v),{onCancel:k})]),e(b).anketa.checks.length?(d(),u("div",F,[(d(!0),u(y,null,C(e(b).anketa.checks,(t,m)=>(d(),u("div",{class:"card card-body",key:m,onMouseover:r[1]||(r[1]=_=>c.value.showActions=!0),onMouseout:r[2]||(r[2]=_=>c.value.showActions=!1)},[c.value.itemId===t.id.toString()?(d(),S(e(v),{key:0,check:c.value.item,onCancel:k},null,8,["check"])):(d(),u("div",x,[a(e(o),null,{default:l(()=>[A(a(e(w),{onDelete:_=>e(b).deleteItem(t.id.toString(),"checks"),onUpdate:_=>{c.value.item=t,c.value.itemId=t.id.toString()},"for-input":"check-file"},{default:l(()=>[A(a(e(E),{"name-id":"check-file",accept:"*",onSubmit:r[0]||(r[0]=_=>e(T)(_,"checks"))},null,512),[[I,c.value.showActions]])]),_:2},1032,["onDelete","onUpdate"]),[[I,c.value.showActions]])]),_:2},1024),h("p",B,s("Проверка кандидата #"+(m+1)),1),a(e(o),{label:"Проверка по местам работы"},{default:l(()=>[n(s(t.workplace),1)]),_:2},1024),a(e(o),{label:"Проверка паспорта"},{default:l(()=>[n(s(t.document),1)]),_:2},1024),a(e(o),{label:"Проверка ИНН"},{default:l(()=>[n(s(t.inn),1)]),_:2},1024),a(e(o),{label:"Проверка ФССП"},{default:l(()=>[n(s(t.debt),1)]),_:2},1024),a(e(o),{label:"Проверка банкротства"},{default:l(()=>[n(s(t.bankruptcy),1)]),_:2},1024),a(e(o),{label:"Проверка БКИ"},{default:l(()=>[n(s(t.bki),1)]),_:2},1024),a(e(o),{label:"Проверка судебных решений"},{default:l(()=>[n(s(t.courts),1)]),_:2},1024),a(e(o),{label:"Проверка аффилированности"},{default:l(()=>[n(s(t.affilation),1)]),_:2},1024),a(e(o),{label:"Проверка по списку террористов"},{default:l(()=>[n(s(t.terrorist),1)]),_:2},1024),a(e(o),{label:"Проверка в розыск"},{default:l(()=>[n(s(t.mvd),1)]),_:2},1024),a(e(o),{label:"Проверка в открытых источниках"},{default:l(()=>[n(s(t.internet),1)]),_:2},1024),a(e(o),{label:"Проверка в Кронос"},{default:l(()=>[n(s(t.cronos),1)]),_:2},1024),a(e(o),{label:"Проверка в Крос"},{default:l(()=>[n(s(t.cros),1)]),_:2},1024),a(e(o),{label:"Дополнительная информация"},{default:l(()=>[n(s(t.addition),1)]),_:2},1024),a(e(o),{label:"ПФО"},{default:l(()=>[n(s(t.pfo?"Да":"Нет"),1)]),_:2},1024),a(e(o),{label:"Комментарии"},{default:l(()=>[n(s(t.comment?t.comment:"-"),1)]),_:2},1024),a(e(o),{label:"Результат"},{default:l(()=>[n(s(t.conclusion),1)]),_:2},1024),a(e(o),{label:"Сотрудник"},{default:l(()=>[n(s(t.user),1)]),_:2},1024),a(e(o),{label:"Дата записи"},{default:l(()=>[n(s(new Date(t.created+" UTC").toLocaleString("ru-RU")),1)]),_:2},1024)]))],32))),128))])):(d(),u("p",O,"Проверка кандидата отсутствует"))],64))}}),j=L(P,[["__scopeId","data-v-b7907836"]]);export{j as default};
