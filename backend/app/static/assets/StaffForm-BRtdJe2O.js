const __vite__fileDeps=["./LabelSlot-Bx6cFhlr.js","./index-DRtVOEFB.js","./index-6fGrG267.css","./_plugin-vue_export-helper-DlAUqK2U.js","./LabelSlot-BKRWK_aH.css","./InputElement-3Vud0B9L.js","./BtnGroup-BbOWQw1q.js","./GroupContent-5M-iCxnF.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as E,E as V,o as b,c as A,a as o,w as m,u as a,s as I,b as n,e as r}from"./index-DRtVOEFB.js";import{s as O}from"./state-Skb32c17.js";import"./utilities-BFRXa8zy.js";const R=E({__name:"StaffForm",props:{staff:{type:Object,default:{}}},emits:["cancel"],setup(f,{emit:d}){const s=n(()=>r(()=>import("./LabelSlot-Bx6cFhlr.js"),__vite__mapDeps([0,1,2,3,4]),import.meta.url)),u=n(()=>r(()=>import("./InputElement-3Vud0B9L.js"),__vite__mapDeps([5,1,2]),import.meta.url)),_=n(()=>r(()=>import("./BtnGroup-BbOWQw1q.js"),__vite__mapDeps([6,1,2]),import.meta.url)),c=n(()=>r(()=>import("./GroupContent-5M-iCxnF.js"),__vite__mapDeps([7,1,2]),import.meta.url)),p=d,e=V(f.staff);function v(){O.updateItem("staffs",e.value),p("cancel"),Object.keys(e.value).forEach(i=>delete e.value[i])}return(i,t)=>(b(),A("form",{onSubmit:I(v,["prevent"]),class:"form form-check",role:"form"},[o(a(s),{label:"Должность"},{default:m(()=>[o(a(u),{name:"position",place:"Должность",need:!0,modelValue:e.value.position,"onUpdate:modelValue":t[0]||(t[0]=l=>e.value.position=l)},null,8,["modelValue"])]),_:1}),o(a(s),{label:"Подразделение"},{default:m(()=>[o(a(u),{name:"department",place:"Подразделение",modelValue:e.value.department,"onUpdate:modelValue":t[1]||(t[1]=l=>e.value.department=l)},null,8,["modelValue"])]),_:1}),o(a(_),null,{default:m(()=>[o(a(c),{onCancel:t[2]||(t[2]=l=>p("cancel"))})]),_:1})],32))}});export{R as default};
