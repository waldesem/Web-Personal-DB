const __vite__fileDeps=["./InputElement-DaxrQ1UY.js","./index-Cj2pYzZu.js","./index-BqKjTnG4.css","./LabelSlot-CFQC1Hbj.js","./_plugin-vue_export-helper-DlAUqK2U.js","./LabelSlot-BKRWK_aH.css","./SelectDiv-DGHNFSzc.js","./BtnGroup-CTOwoHSI.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as V,D as E,o as b,c as y,a,w as u,u as l,s as A,b as m,e as s}from"./index-Cj2pYzZu.js";import{s as D,c as I}from"./state-Kc3gs5o9.js";import"./utilities-BY8xKrXT.js";const L=V({__name:"EducationForm",props:{docs:{type:Object,default:{}}},emits:["cancel"],setup(p,{emit:c}){const i=m(()=>s(()=>import("./InputElement-DaxrQ1UY.js"),__vite__mapDeps([0,1,2]),import.meta.url)),n=m(()=>s(()=>import("./LabelSlot-CFQC1Hbj.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),f=m(()=>s(()=>import("./SelectDiv-DGHNFSzc.js"),__vite__mapDeps([6,1,2]),import.meta.url)),_=m(()=>s(()=>import("./BtnGroup-CTOwoHSI.js"),__vite__mapDeps([7,1,2]),import.meta.url)),r=c,e=E(p.docs);function v(){I.updateItem("educations",e.value),r("cancel"),Object.keys(e.value).forEach(d=>delete e.value[d])}return(d,t)=>(b(),y("form",{onSubmit:A(v,["prevent"]),class:"form form-check",role:"form"},[a(l(n),{label:"Уровень образования"},{default:u(()=>[a(l(f),{name:"type",need:!0,select:l(D).educations,modelValue:e.value.view,"onUpdate:modelValue":t[0]||(t[0]=o=>e.value.view=o)},null,8,["select","modelValue"])]),_:1}),a(l(n),{label:"Название учебного заведения"},{default:u(()=>[a(l(i),{name:"name",place:"Название учебного заведения",modelValue:e.value.name,"onUpdate:modelValue":t[1]||(t[1]=o=>e.value.name=o)},null,8,["modelValue"])]),_:1}),a(l(n),{label:"Год окончания"},{default:u(()=>[a(l(i),{name:"finish",place:"Год окончания",need:!0,modelValue:e.value.finished,"onUpdate:modelValue":t[2]||(t[2]=o=>e.value.finished=o)},null,8,["modelValue"])]),_:1}),a(l(n),{label:"Специальность"},{default:u(()=>[a(l(i),{name:"speciality",place:"Специальность",modelValue:e.value.speciality,"onUpdate:modelValue":t[3]||(t[3]=o=>e.value.speciality=o)},null,8,["modelValue"])]),_:1}),a(l(_),{onCancel:t[4]||(t[4]=o=>r("cancel"))})],32))}});export{L as default};
