const __vite__fileDeps=["./InputElement-DVfPlSFZ.js","./index-Dx3HiUnq.js","./index-6fGrG267.css","./LabelSlot-DWQlJd1k.js","./_plugin-vue_export-helper-DlAUqK2U.js","./LabelSlot-BKRWK_aH.css","./SelectDiv-CjQJfLJg.js","./GroupContent-CqaLL0q_.js","./BtnGroup-CsUEiw5q.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as c,E,o as V,c as b,b as o,w as m,u as t,s as A,e as s,f as a}from"./index-Dx3HiUnq.js";import{b as w}from"./state-s_e9P3m1.js";import"./utilities-BVKB9Dez.js";const P=c({__name:"AddressForm",props:{addrs:{type:Object,default:{}}},emits:["submit","cancel"],setup(u,{emit:i}){const p=s(()=>a(()=>import("./InputElement-DVfPlSFZ.js"),__vite__mapDeps([0,1,2]),import.meta.url)),n=s(()=>a(()=>import("./LabelSlot-DWQlJd1k.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),_=s(()=>a(()=>import("./SelectDiv-CjQJfLJg.js"),__vite__mapDeps([6,1,2]),import.meta.url)),f=s(()=>a(()=>import("./GroupContent-CqaLL0q_.js"),__vite__mapDeps([7,1,2]),import.meta.url)),v=s(()=>a(()=>import("./BtnGroup-CsUEiw5q.js"),__vite__mapDeps([8,1,2]),import.meta.url)),d=i,r=E(u.addrs);return(D,e)=>(V(),b("form",{onSubmit:e[3]||(e[3]=A(l=>d("submit",r.value),["prevent"])),class:"form form-check",role:"form"},[o(t(n),{label:"Вид адреса"},{default:m(()=>[o(t(_),{name:"view",select:t(w).addresses,modelValue:r.value.view,"onUpdate:modelValue":e[0]||(e[0]=l=>r.value.view=l)},null,8,["select","modelValue"])]),_:1}),o(t(n),{label:"Адрес"},{default:m(()=>[o(t(p),{name:"address",place:"Адрес",need:!0,modelValue:r.value.address,"onUpdate:modelValue":e[1]||(e[1]=l=>r.value.address=l)},null,8,["modelValue"])]),_:1}),o(t(v),null,{default:m(()=>[o(t(f),{onCancel:e[2]||(e[2]=l=>d("cancel"))})]),_:1})],32))}});export{P as default};
