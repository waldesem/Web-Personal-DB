const __vite__fileDeps=["./LabelSlot-CcnVWBIm.js","./index-K0Y79g34.js","./index-6fGrG267.css","./_plugin-vue_export-helper-DlAUqK2U.js","./LabelSlot-BKRWK_aH.css","./TextArea-BBimklz7.js","./InputElement-BU5buE4z.js","./GroupContent-C7Qhptof.js","./BtnGroup-D4b48yKH.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as v,E,o as V,c as b,b as t,w as a,u as o,s as A,e as l,f as i}from"./index-K0Y79g34.js";const O=v({__name:"InquiryForm",props:{inquiry:{type:Object,default:{}}},emits:["submit","cancel"],setup(s,{emit:p}){const u=l(()=>i(()=>import("./LabelSlot-CcnVWBIm.js"),__vite__mapDeps([0,1,2,3,4]),import.meta.url)),_=l(()=>i(()=>import("./TextArea-BBimklz7.js"),__vite__mapDeps([5,1,2]),import.meta.url)),d=l(()=>i(()=>import("./InputElement-BU5buE4z.js"),__vite__mapDeps([6,1,2]),import.meta.url)),f=l(()=>i(()=>import("./GroupContent-C7Qhptof.js"),__vite__mapDeps([7,1,2]),import.meta.url)),c=l(()=>i(()=>import("./BtnGroup-D4b48yKH.js"),__vite__mapDeps([8,1,2]),import.meta.url)),m=p,n=E(s.inquiry);return(y,e)=>(V(),b("form",{onSubmit:e[3]||(e[3]=A(r=>m("submit",n.value),["prevent"])),class:"form form-check p-3",role:"form"},[t(o(u),{label:"Информация"},{default:a(()=>[t(o(_),{name:"info",place:"Информация",modelValue:n.value.info,"onUpdate:modelValue":e[0]||(e[0]=r=>n.value.info=r)},null,8,["modelValue"])]),_:1}),t(o(u),{label:"Инициатор"},{default:a(()=>[t(o(d),{name:"initiator",place:"Инициатор",modelValue:n.value.initiator,"onUpdate:modelValue":e[1]||(e[1]=r=>n.value.initiator=r)},null,8,["modelValue"])]),_:1}),t(o(c),null,{default:a(()=>[t(o(f),{onCancel:e[2]||(e[2]=r=>m("cancel"))})]),_:1})],32))}});export{O as default};
