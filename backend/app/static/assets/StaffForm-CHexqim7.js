const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=["./LabelSlot-B0m-81OP.js","./index-C2-iPJTr.js","./index-BqKjTnG4.css","./_plugin-vue_export-helper-DlAUqK2U.js","./LabelSlot-BKRWK_aH.css","./InputElement-i7upPvzI.js","./BtnGroup--g1E1sM-.js"])))=>i.map(i=>d[i]);
import{d as v,I as V,o as E,c as b,b as o,l as i,u as a,w as I,h as n,j as r}from"./index-C2-iPJTr.js";import{e as k}from"./state-HF1or3d1.js";const L=v({__name:"StaffForm",props:{staff:{type:Object,default:{}}},emits:["cancel"],setup(f,{emit:d}){const m=n(()=>r(()=>import("./LabelSlot-B0m-81OP.js"),__vite__mapDeps([0,1,2,3,4]),import.meta.url)),s=n(()=>r(()=>import("./InputElement-i7upPvzI.js"),__vite__mapDeps([5,1,2]),import.meta.url)),c=n(()=>r(()=>import("./BtnGroup--g1E1sM-.js"),__vite__mapDeps([6,1,2]),import.meta.url)),u=d,e=V(f.staff);function _(){k.updateItem("staffs",e.value),u("cancel"),Object.keys(e.value).forEach(p=>delete e.value[p])}return(p,t)=>(E(),b("form",{onSubmit:I(_,["prevent"]),class:"form form-check",role:"form"},[o(a(m),{label:"Должность"},{default:i(()=>[o(a(s),{name:"position",place:"Должность",need:!0,modelValue:e.value.position,"onUpdate:modelValue":t[0]||(t[0]=l=>e.value.position=l)},null,8,["modelValue"])]),_:1}),o(a(m),{label:"Подразделение"},{default:i(()=>[o(a(s),{name:"department",place:"Подразделение",modelValue:e.value.department,"onUpdate:modelValue":t[1]||(t[1]=l=>e.value.department=l)},null,8,["modelValue"])]),_:1}),o(a(c),{onCancel:t[2]||(t[2]=l=>u("cancel"))})],32))}});export{L as default};