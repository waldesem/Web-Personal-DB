const __vite__fileDeps=["./LabelSlot-RdSfBjzZ.js","./index-D1U1a8b2.js","./index-BqKjTnG4.css","./_plugin-vue_export-helper-DlAUqK2U.js","./LabelSlot-BKRWK_aH.css","./TextArea-COCR6DJ9.js","./InputElement-CpP_zLuD.js","./BtnGroup-DCfcNJ97.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as E,I as V,o as I,c as b,b as o,l as s,u as n,w as y,h as a,j as l}from"./index-D1U1a8b2.js";import{g as A}from"./state-u74uZLPD.js";const L=E({__name:"InquiryForm",props:{inquiry:{type:Object,default:{}}},emits:["cancel"],setup(p,{emit:d}){const i=a(()=>l(()=>import("./LabelSlot-RdSfBjzZ.js"),__vite__mapDeps([0,1,2,3,4]),import.meta.url)),_=a(()=>l(()=>import("./TextArea-COCR6DJ9.js"),__vite__mapDeps([5,1,2]),import.meta.url)),c=a(()=>l(()=>import("./InputElement-CpP_zLuD.js"),__vite__mapDeps([6,1,2]),import.meta.url)),f=a(()=>l(()=>import("./BtnGroup-DCfcNJ97.js"),__vite__mapDeps([7,1,2]),import.meta.url)),u=d,e=V(p.inquiry);function v(){A.updateItem("inquiries",e.value),u("cancel"),Object.keys(e.value).forEach(m=>delete e.value[m])}return(m,t)=>(I(),b("form",{onSubmit:y(v,["prevent"]),class:"form form-check p-3",role:"form"},[o(n(i),{label:"Информация"},{default:s(()=>[o(n(_),{name:"info",place:"Информация",modelValue:e.value.info,"onUpdate:modelValue":t[0]||(t[0]=r=>e.value.info=r)},null,8,["modelValue"])]),_:1}),o(n(i),{label:"Инициатор"},{default:s(()=>[o(n(c),{name:"origins",place:"Инициатор",modelValue:e.value.origins,"onUpdate:modelValue":t[1]||(t[1]=r=>e.value.origins=r)},null,8,["modelValue"])]),_:1}),o(n(f),{onCancel:t[2]||(t[2]=r=>u("cancel"))})],32))}});export{L as default};
