const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=["./LabelSlot-B0m-81OP.js","./index-C2-iPJTr.js","./index-BqKjTnG4.css","./_plugin-vue_export-helper-DlAUqK2U.js","./LabelSlot-BKRWK_aH.css","./TextArea-D_a4J1Ct.js","./InputElement-i7upPvzI.js","./BtnGroup--g1E1sM-.js"])))=>i.map(i=>d[i]);
import{d as E,I as V,o as I,c as b,b as o,l as u,u as a,w as A,h as l,j as i}from"./index-C2-iPJTr.js";import{e as g}from"./state-HF1or3d1.js";const P=E({__name:"InvestigationForm",props:{investigation:{type:Object,default:{}}},emits:["cancel"],setup(p,{emit:d}){const m=l(()=>i(()=>import("./LabelSlot-B0m-81OP.js"),__vite__mapDeps([0,1,2,3,4]),import.meta.url)),_=l(()=>i(()=>import("./TextArea-D_a4J1Ct.js"),__vite__mapDeps([5,1,2]),import.meta.url)),c=l(()=>i(()=>import("./InputElement-i7upPvzI.js"),__vite__mapDeps([6,1,2]),import.meta.url)),f=l(()=>i(()=>import("./BtnGroup--g1E1sM-.js"),__vite__mapDeps([7,1,2]),import.meta.url)),r=d,e=V(p.investigation);function v(){g.updateItem("investigations",e.value),r("cancel"),Object.keys(e.value).forEach(s=>delete e.value[s])}return(s,t)=>(I(),b("form",{onSubmit:A(v,["prevent"]),class:"form form-check p-3",role:"form"},[o(a(m),{label:"Тема проверки"},{default:u(()=>[o(a(c),{name:"theme",place:"Тема проверки",need:!0,modelValue:e.value.theme,"onUpdate:modelValue":t[0]||(t[0]=n=>e.value.theme=n)},null,8,["modelValue"])]),_:1}),o(a(m),{label:"Информация"},{default:u(()=>[o(a(_),{name:"info",place:"Информация",modelValue:e.value.info,"onUpdate:modelValue":t[1]||(t[1]=n=>e.value.info=n)},null,8,["modelValue"])]),_:1}),o(a(f),{onCancel:t[2]||(t[2]=n=>r("cancel"))})],32))}});export{P as default};