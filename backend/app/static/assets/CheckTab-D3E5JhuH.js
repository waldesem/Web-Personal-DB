const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=["./ActionIcons-HH4Thdt8.js","./index-D-dL7D6l.js","./index-BqKjTnG4.css","./_plugin-vue_export-helper-DlAUqK2U.js","./ActionIcons-CukUJdTR.css","./LabelSlot-UyefIB2q.js","./LabelSlot-BMshfUVW.css","./FileForm-DSFlukZz.js","./CheckForm-Bs4D8I18.js","./state-aOZCxFm5.js"])))=>i.map(i=>d[i]);
import{d as D,r as T,o as i,c as _,e as p,b as a,u as e,F as g,A as C,m as $,l,g as x,v as E,t as n,p as s,h as m,j as k}from"./index-D-dL7D6l.js";import{e as f,c as F}from"./state-aOZCxFm5.js";import{_ as V}from"./_plugin-vue_export-helper-DlAUqK2U.js";const w={class:"collapse card card-body mb-3",id:"clps_check"},O={key:0},B={key:1},M={class:"fs-5 fw-medium text-primary p-1"},P={class:"collapse card card-body",id:"clps_additional"},R=["innerHTML"],U={key:1,class:"form-label text-primary text-decoration-underline",for:"xml-file",style:{cursor:"pointer"}},j={key:1,class:"p-3"},N=D({__name:"CheckTab",setup(H){const L=m(()=>k(()=>import("./ActionIcons-HH4Thdt8.js"),__vite__mapDeps([0,1,2,3,4]),import.meta.url)),o=m(()=>k(()=>import("./LabelSlot-UyefIB2q.js"),__vite__mapDeps([5,1,2,3,6]),import.meta.url)),h=m(()=>k(()=>import("./FileForm-DSFlukZz.js"),__vite__mapDeps([7,1,2]),import.meta.url)),y=m(()=>k(()=>import("./CheckForm-Bs4D8I18.js"),__vite__mapDeps([8,1,2,9]),import.meta.url)),d=T({actions:!1,edit:!1,itemId:"",isAddition:!1,check:{}});function A(){d.value.edit=!1,d.value.itemId="";const u=document.getElementById("clps_check");u==null||u.setAttribute("class","collapse card card-body mb-3")}function I(u){let r="";for(let t of u){let b="";for(const[c,v]of Object.entries(t))b+=`<tr><td>${c}</td>`+(typeof v=="string"?`<td>${v}</td>`:`<td>${I(v)}</td>`)+"</tr>";r+=b}return`<table class="table table-sm table-striped text-break">${r}</table>`}const S=u=>{try{const r=JSON.parse(u);return I(r)}catch(r){return console.error(r),null}};return(u,r)=>(i(),_(g,null,[p("div",w,[a(e(y),{onCancel:A})]),e(f).anketa.checks.length?(i(),_("div",O,[(i(!0),_(g,null,C(e(f).anketa.checks,(t,b)=>(i(),_("div",{class:"card card-body mb-3",key:b,onMouseover:r[2]||(r[2]=c=>d.value.actions=!0),onMouseout:r[3]||(r[3]=c=>d.value.actions=!1)},[d.value.edit&&d.value.itemId==t.id.toString()?(i(),$(e(y),{key:0,check:d.value.check,onCancel:A},null,8,["check"])):(i(),_("div",B,[a(e(o),null,{default:l(()=>[x(a(e(L),{onDelete:c=>e(f).deleteItem(t.id.toString(),"checks"),onUpdate:c=>{d.value.check=t,d.value.itemId=t.id.toString(),d.value.edit=!0},"for-input":"check-file"},{default:l(()=>[x(a(e(h),{"name-id":"check-file",accept:"*",onSubmit:r[0]||(r[0]=c=>e(f).submitFile(c,"checks",e(f).share.candId))},null,512),[[E,d.value.actions]])]),_:2},1032,["onDelete","onUpdate"]),[[E,d.value.actions&&e(f).anketa.persons.user_id==e(F).user.userId&&e(f).anketa.persons.standing]])]),_:2},1024),p("p",M,n("Проверка кандидата #"+(b+1)),1),a(e(o),{label:"Проверка по местам работы"},{default:l(()=>[s(n(t.workplace),1)]),_:2},1024),a(e(o),{label:"Проверка паспорта"},{default:l(()=>[s(n(t.document),1)]),_:2},1024),a(e(o),{label:"Проверка ИНН"},{default:l(()=>[s(n(t.inn),1)]),_:2},1024),a(e(o),{label:"Проверка ФССП"},{default:l(()=>[s(n(t.debt),1)]),_:2},1024),a(e(o),{label:"Проверка банкротства"},{default:l(()=>[s(n(t.bankruptcy),1)]),_:2},1024),a(e(o),{label:"Проверка БКИ"},{default:l(()=>[s(n(t.bki),1)]),_:2},1024),a(e(o),{label:"Проверка судебных решений"},{default:l(()=>[s(n(t.courts),1)]),_:2},1024),a(e(o),{label:"Проверка аффилированности"},{default:l(()=>[s(n(t.affilation),1)]),_:2},1024),a(e(o),{label:"Проверка по списку террористов"},{default:l(()=>[s(n(t.terrorist),1)]),_:2},1024),a(e(o),{label:"Проверка в розыск"},{default:l(()=>[s(n(t.mvd),1)]),_:2},1024),a(e(o),{label:"Проверка в открытых источниках"},{default:l(()=>[s(n(t.internet),1)]),_:2},1024),a(e(o),{label:"Проверка в Кронос"},{default:l(()=>[s(n(t.cronos),1)]),_:2},1024),a(e(o),{label:"Проверка в Крос"},{default:l(()=>[s(n(t.cros),1)]),_:2},1024),a(e(o),{label:"Комментарии"},{default:l(()=>[s(n(t.comment?t.comment:"-"),1)]),_:2},1024),a(e(o),{label:"Результат"},{default:l(()=>[s(n(t.conclusion),1)]),_:2},1024),a(e(o),{label:"Сотрудник"},{default:l(()=>[s(n(t.username),1)]),_:2},1024),a(e(o),{label:"Дата записи"},{default:l(()=>[s(n(new Date(t.created+" UTC").toLocaleString("ru-RU")),1)]),_:2},1024),a(e(o),{class:"d-print-none",label:"Дополнительная информация"},{default:l(()=>[p("button",{type:"button",class:"btn btn-link","data-bs-toggle":"collapse",href:"#clps_additional",role:"button",onClick:r[1]||(r[1]=c=>d.value.isAddition=!d.value.isAddition)},n(d.value.isAddition?"Скрыть":"Показать"),1)]),_:1}),p("div",P,[t.addition?(i(),_("div",{key:0,innerHTML:S(t.addition)},null,8,R)):(i(),_("label",U,[s(" Загрузить XML "),a(e(h),{style:{display:"none"},accept:".xml","name-id":"xml-file",onSubmit:c=>e(f).submitFile(c,"xml",t.id)},null,8,["onSubmit"])]))])]))],32))),128))])):(i(),_("p",j,"Проверка кандидата отсутствует"))],64))}}),z=V(N,[["__scopeId","data-v-61935f4c"]]);export{z as default};
