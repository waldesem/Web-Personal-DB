const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=["./ActionIcons-D-fKbOWt.js","./index-C1r4f5TB.js","./index-BqKjTnG4.css","./_plugin-vue_export-helper-DlAUqK2U.js","./ActionIcons-CukUJdTR.css","./LabelSlot-B9jKJnYD.js","./LabelSlot-BMshfUVW.css","./FileForm-CPEIJme2.js","./CheckForm-BiOch_Lu.js","./state-BGY6iYIz.js"])))=>i.map(i=>d[i]);
import{d as T,r as C,o as i,c as _,e as v,b as a,u as e,F as x,A as $,m as w,l,g as A,v as E,t as s,p as n,h as m,j as k,s as F,x as V}from"./index-C1r4f5TB.js";import{e as p,c as O}from"./state-BGY6iYIz.js";import{_ as B}from"./_plugin-vue_export-helper-DlAUqK2U.js";const M=f=>(F("data-v-a9924031"),f=f(),V(),f),P={class:"collapse card card-body mb-3",id:"clps_check"},R={key:0},U={key:1},j={class:"fs-5 fw-medium text-primary p-1"},N=M(()=>v("button",{type:"button",class:"btn btn-link","data-bs-toggle":"collapse",href:"#clps_additional",role:"button"}," Показать ",-1)),H={class:"collapse card card-body mb-3",id:"clps_additional"},J=["innerHTML"],X={key:1,class:"form-label text-primary text-decoration-underline",for:"xml-file",style:{cursor:"pointer"}},q={key:1,class:"p-3"},z=T({__name:"CheckTab",setup(f){const L=m(()=>k(()=>import("./ActionIcons-D-fKbOWt.js"),__vite__mapDeps([0,1,2,3,4]),import.meta.url)),o=m(()=>k(()=>import("./LabelSlot-B9jKJnYD.js"),__vite__mapDeps([5,1,2,3,6]),import.meta.url)),y=m(()=>k(()=>import("./FileForm-CPEIJme2.js"),__vite__mapDeps([7,1,2]),import.meta.url)),I=m(()=>k(()=>import("./CheckForm-BiOch_Lu.js"),__vite__mapDeps([8,1,2,9]),import.meta.url)),r=C({actions:!1,edit:!1,itemId:"",check:{}});function S(){r.value.edit=!1,r.value.itemId="";const u=document.getElementById("clps_check");u==null||u.setAttribute("class","collapse card card-body mb-3")}function g(u){let c="";for(let t of u){let b="";for(const[d,h]of Object.entries(t))b+=`<tr><td>${d}</td>`+(typeof h=="string"?`<td>${h}</td>`:`<td>${g(h)}</td>`)+"</tr>";c+=b}return`<table class="table table-sm table-responsive table-striped">${c}</table>`}const D=u=>{try{const c=JSON.parse(u);return g(c)}catch(c){return console.error(c),null}};return(u,c)=>(i(),_(x,null,[v("div",P,[a(e(I),{onCancel:S})]),e(p).anketa.checks.length?(i(),_("div",R,[(i(!0),_(x,null,$(e(p).anketa.checks,(t,b)=>(i(),_("div",{class:"card card-body mb-3",key:b,onMouseover:c[1]||(c[1]=d=>r.value.actions=!0),onMouseout:c[2]||(c[2]=d=>r.value.actions=!1)},[r.value.edit&&r.value.itemId==t.id.toString()?(i(),w(e(I),{key:0,check:r.value.check,onCancel:S},null,8,["check"])):(i(),_("div",U,[a(e(o),null,{default:l(()=>[A(a(e(L),{onDelete:d=>e(p).deleteItem(t.id.toString(),"checks"),onUpdate:d=>{r.value.check=t,r.value.itemId=t.id.toString(),r.value.edit=!0},"for-input":"check-file"},{default:l(()=>[A(a(e(y),{"name-id":"check-file",accept:"*",onSubmit:c[0]||(c[0]=d=>e(p).submitFile(d,"checks",e(p).share.candId))},null,512),[[E,r.value.actions]])]),_:2},1032,["onDelete","onUpdate"]),[[E,r.value.actions&&e(p).anketa.persons.user_id==e(O).user.userId&&e(p).anketa.persons.standing]])]),_:2},1024),v("p",j,s("Проверка кандидата #"+(b+1)),1),a(e(o),{label:"Проверка по местам работы"},{default:l(()=>[n(s(t.workplace),1)]),_:2},1024),a(e(o),{label:"Проверка паспорта"},{default:l(()=>[n(s(t.document),1)]),_:2},1024),a(e(o),{label:"Проверка ИНН"},{default:l(()=>[n(s(t.inn),1)]),_:2},1024),a(e(o),{label:"Проверка ФССП"},{default:l(()=>[n(s(t.debt),1)]),_:2},1024),a(e(o),{label:"Проверка банкротства"},{default:l(()=>[n(s(t.bankruptcy),1)]),_:2},1024),a(e(o),{label:"Проверка БКИ"},{default:l(()=>[n(s(t.bki),1)]),_:2},1024),a(e(o),{label:"Проверка судебных решений"},{default:l(()=>[n(s(t.courts),1)]),_:2},1024),a(e(o),{label:"Проверка аффилированности"},{default:l(()=>[n(s(t.affilation),1)]),_:2},1024),a(e(o),{label:"Проверка по списку террористов"},{default:l(()=>[n(s(t.terrorist),1)]),_:2},1024),a(e(o),{label:"Проверка в розыск"},{default:l(()=>[n(s(t.mvd),1)]),_:2},1024),a(e(o),{label:"Проверка в открытых источниках"},{default:l(()=>[n(s(t.internet),1)]),_:2},1024),a(e(o),{label:"Проверка в Кронос"},{default:l(()=>[n(s(t.cronos),1)]),_:2},1024),a(e(o),{label:"Проверка в Крос"},{default:l(()=>[n(s(t.cros),1)]),_:2},1024),a(e(o),{label:"Комментарии"},{default:l(()=>[n(s(t.comment?t.comment:"-"),1)]),_:2},1024),a(e(o),{label:"Результат"},{default:l(()=>[n(s(t.conclusion),1)]),_:2},1024),a(e(o),{label:"Сотрудник"},{default:l(()=>[n(s(t.username),1)]),_:2},1024),a(e(o),{label:"Дата записи"},{default:l(()=>[n(s(new Date(t.created+" UTC").toLocaleString("ru-RU")),1)]),_:2},1024),a(e(o),{class:"d-print-none",label:"Дополнительная информация"},{default:l(()=>[N]),_:1}),v("div",H,[t.addition?(i(),_("div",{key:0,innerHTML:D(t.addition)},null,8,J)):(i(),_("label",X,[n(" Загрузить XML "),a(e(y),{accept:".xml","name-id":"xml-file",onSubmit:d=>e(p).submitFile(d,"xml",t.id)},null,8,["onSubmit"])]))])]))],32))),128))])):(i(),_("p",q,"Проверка кандидата отсутствует"))],64))}}),W=B(z,[["__scopeId","data-v-a9924031"]]);export{W as default};
