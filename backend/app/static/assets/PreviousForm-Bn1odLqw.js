const __vite__fileDeps=["./LabelSlot-Bx6cFhlr.js","./index-DRtVOEFB.js","./index-6fGrG267.css","./_plugin-vue_export-helper-DlAUqK2U.js","./LabelSlot-BKRWK_aH.css","./InputElement-3Vud0B9L.js","./BtnGroup-BbOWQw1q.js","./GroupContent-5M-iCxnF.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as c,E,o as b,c as P,a,w as n,u as t,s as y,b as m,e as s}from"./index-DRtVOEFB.js";import{s as A}from"./state-Skb32c17.js";import"./utilities-BFRXa8zy.js";const L=c({__name:"PreviousForm",props:{previous:{type:Object,default:{}}},emits:["cancel"],setup(i,{emit:v}){const u=m(()=>s(()=>import("./LabelSlot-Bx6cFhlr.js"),__vite__mapDeps([0,1,2,3,4]),import.meta.url)),r=m(()=>s(()=>import("./InputElement-3Vud0B9L.js"),__vite__mapDeps([5,1,2]),import.meta.url)),f=m(()=>s(()=>import("./BtnGroup-BbOWQw1q.js"),__vite__mapDeps([6,1,2]),import.meta.url)),_=m(()=>s(()=>import("./GroupContent-5M-iCxnF.js"),__vite__mapDeps([7,1,2]),import.meta.url)),p=v,e=E(i.previous);function V(){A.updateItem("previous",e.value),p("cancel"),Object.keys(e.value).forEach(d=>delete e.value[d])}return(d,l)=>(b(),P("form",{onSubmit:y(V,["prevent"]),class:"form form-check",role:"form"},[a(t(u),{label:"Фамилия"},{default:n(()=>[a(t(r),{need:!0,name:"surname",place:"Фамилия*",pattern:"[А-Яа-яЁё\\-'\\s]+",modelValue:e.value.surname,"onUpdate:modelValue":l[0]||(l[0]=o=>e.value.surname=o)},null,8,["modelValue"])]),_:1}),a(t(u),{label:"Имя"},{default:n(()=>[a(t(r),{need:!0,name:"firstname",place:"Имя*",pattern:"[А-Яа-яЁё\\-'\\s]+",modelValue:e.value.firstname,"onUpdate:modelValue":l[1]||(l[1]=o=>e.value.firstname=o)},null,8,["modelValue"])]),_:1}),a(t(u),{label:"Отчество"},{default:n(()=>[a(t(r),{name:"patronymic",place:"Отчество",modelValue:e.value.patronymic,"onUpdate:modelValue":l[2]||(l[2]=o=>e.value.patronymic=o)},null,8,["modelValue"])]),_:1}),a(t(u),{label:"Дата изменения"},{default:n(()=>[a(t(r),{name:"date_change",place:"Год изменения",modelValue:e.value.changed,"onUpdate:modelValue":l[3]||(l[3]=o=>e.value.changed=o)},null,8,["modelValue"])]),_:1}),a(t(u),{label:"Причина изменения"},{default:n(()=>[a(t(r),{name:"reason",place:"Причина изменения",modelValue:e.value.reason,"onUpdate:modelValue":l[4]||(l[4]=o=>e.value.reason=o)},null,8,["modelValue"])]),_:1}),a(t(f),null,{default:n(()=>[a(t(_),{onCancel:l[5]||(l[5]=o=>p("cancel"))})]),_:1})],32))}});export{L as default};
