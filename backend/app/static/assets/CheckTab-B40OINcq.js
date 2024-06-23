const __vite__fileDeps=["./ActionIcons-BCE4-2Qs.js","./index-Dx3HiUnq.js","./index-6fGrG267.css","./LabelSlot-DWQlJd1k.js","./_plugin-vue_export-helper-DlAUqK2U.js","./LabelSlot-BKRWK_aH.css","./FileForm-CVXWBM0I.js","./FileForm-By8_2B11.css","./CheckForm-D74vdR_f.js","./state-s_e9P3m1.js","./utilities-BVKB9Dez.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as F,n as L,o as u,g as A,u as e,c as i,F as V,r as x,b as a,w as l,q as S,C as P,z as g,x as o,t as s,e as f,f as p}from"./index-Dx3HiUnq.js";import{s as b,c as R}from"./state-s_e9P3m1.js";import"./utilities-BVKB9Dez.js";const $={key:1,class:"py-3"},O={key:1},B={key:0,class:"spinner-border-sm text-primary"},N={key:2},z=F({__name:"CheckTab",props:{tabAction:{type:String,default:""},currentTab:{type:String,default:""}},emits:["cancel"],setup(w,{emit:C}){const I=f(()=>p(()=>import("./ActionIcons-BCE4-2Qs.js"),__vite__mapDeps([0,1,2]),import.meta.url)),n=f(()=>p(()=>import("./LabelSlot-DWQlJd1k.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),D=f(()=>p(()=>import("./FileForm-CVXWBM0I.js"),__vite__mapDeps([6,1,2,4,7]),import.meta.url)),m=f(()=>p(()=>import("./CheckForm-D74vdR_f.js"),__vite__mapDeps([8,1,2,9,10]),import.meta.url)),k=C,v=w,r=L({itemId:"",item:{},showActions:!1,spinner:!1});function h(){r.value.itemId="",r.value.item={},k("cancel")}function y(_){b.updateItem("checks",_),h()}function E(_){r.value.spinner=!0,R(_,"checks"),r.value.spinner=!1}return(_,c)=>v.tabAction==="create"&&v.currentTab==="CheckTab"?(u(),A(e(m),{key:0,onCancel:c[0]||(c[0]=t=>k("cancel")),onSubmit:y})):e(b).anketa.checks.length?(u(),i("div",$,[(u(!0),i(V,null,x(e(b).anketa.checks,(t,T)=>(u(),i("div",{key:T,onMouseover:c[2]||(c[2]=d=>r.value.showActions=!0),onMouseout:c[3]||(c[3]=d=>r.value.showActions=!1),class:"card card-body mb-3"},[r.value.itemId===t.id.toString()?(u(),A(e(m),{key:0,check:r.value.item,onSubmit:y,onCancel:h},null,8,["check"])):(u(),i("div",O,[a(e(n),null,{default:l(()=>[S(a(e(I),{onDelete:d=>e(b).deleteItem(t.id.toString(),"checks"),onUpdate:d=>{r.value.item=t,r.value.itemId=t.id.toString()},"for-input":"check-file"},{default:l(()=>[r.value.spinner?(u(),i("span",B)):P("",!0),S(a(e(D),{"name-id":"check-file",accept:"*",onSubmit:c[1]||(c[1]=d=>E(d))},null,512),[[g,r.value.showActions]])]),_:2},1032,["onDelete","onUpdate"]),[[g,r.value.showActions]])]),_:2},1024),a(e(n),{label:"Проверка по местам работы"},{default:l(()=>[o(s(t.workplace),1)]),_:2},1024),a(e(n),{label:"Проверка паспорта"},{default:l(()=>[o(s(t.document),1)]),_:2},1024),a(e(n),{label:"Проверка ИНН"},{default:l(()=>[o(s(t.inn),1)]),_:2},1024),a(e(n),{label:"Проверка ФССП"},{default:l(()=>[o(s(t.debt),1)]),_:2},1024),a(e(n),{label:"Проверка банкротства"},{default:l(()=>[o(s(t.bankruptcy),1)]),_:2},1024),a(e(n),{label:"Проверка БКИ"},{default:l(()=>[o(s(t.bki),1)]),_:2},1024),a(e(n),{label:"Проверка судебных решений"},{default:l(()=>[o(s(t.courts),1)]),_:2},1024),a(e(n),{label:"Проверка аффилированности"},{default:l(()=>[o(s(t.affilation),1)]),_:2},1024),a(e(n),{label:"Проверка по списку террористов"},{default:l(()=>[o(s(t.terrorist),1)]),_:2},1024),a(e(n),{label:"Проверка в розыск"},{default:l(()=>[o(s(t.mvd),1)]),_:2},1024),a(e(n),{label:"Проверка в открытых источниках"},{default:l(()=>[o(s(t.internet),1)]),_:2},1024),a(e(n),{label:"Проверка в Кронос"},{default:l(()=>[o(s(t.cronos),1)]),_:2},1024),a(e(n),{label:"Проверка в Крос"},{default:l(()=>[o(s(t.cros),1)]),_:2},1024),a(e(n),{label:"Дополнительная информация"},{default:l(()=>[o(s(t.addition),1)]),_:2},1024),a(e(n),{label:"ПФО"},{default:l(()=>[o(s(t.pfo?"Да":"Нет"),1)]),_:2},1024),a(e(n),{label:"Комментарии"},{default:l(()=>[o(s(t.comment?t.comment:"-"),1)]),_:2},1024),a(e(n),{label:"Результат"},{default:l(()=>[o(s(t.conclusion),1)]),_:2},1024),a(e(n),{label:"Сотрудник"},{default:l(()=>[o(s(t.user),1)]),_:2},1024),a(e(n),{label:"Дата записи"},{default:l(()=>[o(s(new Date(String(t.created)).toLocaleDateString("ru-RU")),1)]),_:2},1024)]))],32))),128))])):(u(),i("p",N,"Данные отсутствуют"))}});export{z as default};
