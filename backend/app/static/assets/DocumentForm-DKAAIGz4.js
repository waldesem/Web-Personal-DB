const __vite__fileDeps=["./InputElement-CpP_zLuD.js","./index-D1U1a8b2.js","./index-BqKjTnG4.css","./LabelSlot-RdSfBjzZ.js","./_plugin-vue_export-helper-DlAUqK2U.js","./LabelSlot-BKRWK_aH.css","./SelectDiv-CcT-1QKJ.js","./BtnGroup-DCfcNJ97.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as V,I as b,o as E,c as y,b as a,l as n,u as t,w as D,h as s,j as d}from"./index-D1U1a8b2.js";import{d as I,g}from"./state-u74uZLPD.js";const k=V({__name:"DocumentForm",props:{docs:{type:Object,default:{}}},emits:["cancel"],setup(p,{emit:c}){const m=s(()=>d(()=>import("./InputElement-CpP_zLuD.js"),__vite__mapDeps([0,1,2]),import.meta.url)),u=s(()=>d(()=>import("./LabelSlot-RdSfBjzZ.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),v=s(()=>d(()=>import("./SelectDiv-CcT-1QKJ.js"),__vite__mapDeps([6,1,2]),import.meta.url)),f=s(()=>d(()=>import("./BtnGroup-DCfcNJ97.js"),__vite__mapDeps([7,1,2]),import.meta.url)),r=c,e=b(p.docs);function _(){g.updateItem("documents",e.value),r("cancel"),Object.keys(e.value).forEach(i=>delete e.value[i])}return(i,l)=>(E(),y("form",{onSubmit:D(_,["prevent"]),class:"form form-check",role:"form"},[a(t(u),{label:"Вид документа"},{default:n(()=>[a(t(v),{name:"view",need:!0,select:t(I).documents,modelValue:e.value.view,"onUpdate:modelValue":l[0]||(l[0]=o=>e.value.view=o)},null,8,["select","modelValue"])]),_:1}),a(t(u),{label:"Серия документа"},{default:n(()=>[a(t(m),{name:"series",place:"Серия документа",modelValue:e.value.series,"onUpdate:modelValue":l[1]||(l[1]=o=>e.value.series=o)},null,8,["modelValue"])]),_:1}),a(t(u),{label:"Номер документа"},{default:n(()=>[a(t(m),{name:"number",place:"Номер документа",need:!0,modelValue:e.value.digits,"onUpdate:modelValue":l[2]||(l[2]=o=>e.value.digits=o)},null,8,["modelValue"])]),_:1}),a(t(u),{label:"Кем выдан"},{default:n(()=>[a(t(m),{name:"agency",place:"Орган выдавший",modelValue:e.value.agency,"onUpdate:modelValue":l[3]||(l[3]=o=>e.value.agency=o)},null,8,["modelValue"])]),_:1}),a(t(u),{label:"Дата выдачи"},{default:n(()=>[a(t(m),{name:"issue",place:"Дата выдачи",typeof:"date",modelValue:e.value.issue,"onUpdate:modelValue":l[4]||(l[4]=o=>e.value.issue=o)},null,8,["modelValue"])]),_:1}),a(t(f),{onCancel:l[5]||(l[5]=o=>r("cancel"))})],32))}});export{k as default};
