const __vite__fileDeps=["./SwitchBox-myEhDfyv.js","./index-2fGtmyHu.js","./index-BGNnvclF.css","./LabelSlot-CNcRoBCi.js","./_plugin-vue_export-helper-DlAUqK2U.js","./LabelSlot-BKRWK_aH.css","./InputElement-frsqUg0l.js","./BtnGroup-BM3JjHhl.js","./GroupContent-6Vhm430s.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as w,E,o as i,c as b,a,w as u,u as o,i as A,n as I,s as O,b as d,e as m}from"./index-2fGtmyHu.js";import{c as U}from"./state-BI0Epm2O.js";import"./utilities-DjwPzg-5.js";const P=w({__name:"WorkplaceForm",props:{work:{type:Object,default:{}}},emits:["cancel"],setup(_,{emit:f}){const V=d(()=>m(()=>import("./SwitchBox-myEhDfyv.js"),__vite__mapDeps([0,1,2]),import.meta.url)),n=d(()=>m(()=>import("./LabelSlot-CNcRoBCi.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),r=d(()=>m(()=>import("./InputElement-frsqUg0l.js"),__vite__mapDeps([6,1,2]),import.meta.url)),v=d(()=>m(()=>import("./BtnGroup-BM3JjHhl.js"),__vite__mapDeps([7,1,2]),import.meta.url)),k=d(()=>m(()=>import("./GroupContent-6Vhm430s.js"),__vite__mapDeps([8,1,2]),import.meta.url)),p=f,e=E(_.work);function c(){U.updateItem("workplaces",e.value),p("cancel"),Object.keys(e.value).forEach(s=>delete e.value[s])}return(s,l)=>(i(),b("form",{onSubmit:O(c,["prevent"]),class:"form form-check",role:"form"},[a(o(n),{label:"Текущая работа"},{default:u(()=>[a(o(V),{name:"now_work",place:"Текущая работа",modelValue:e.value.now_work,"onUpdate:modelValue":l[0]||(l[0]=t=>e.value.now_work=t)},null,8,["modelValue"])]),_:1}),a(o(n),{label:"Начало работы"},{default:u(()=>[a(o(r),{name:"start_date",need:!0,place:"Начало работы",typeof:"date",modelValue:e.value.started,"onUpdate:modelValue":l[1]||(l[1]=t=>e.value.started=t)},null,8,["modelValue"])]),_:1}),e.value.now_work?I("",!0):(i(),A(o(n),{key:0,label:"Окончание работы"},{default:u(()=>[a(o(r),{name:"end_date",place:"Окончание работы",typeof:"date",modelValue:e.value.finished,"onUpdate:modelValue":l[2]||(l[2]=t=>e.value.finished=t)},null,8,["modelValue"])]),_:1})),a(o(n),{label:"Место работы"},{default:u(()=>[a(o(r),{name:"workplace",place:"Место работы",need:!0,modelValue:e.value.workplace,"onUpdate:modelValue":l[3]||(l[3]=t=>e.value.workplace=t)},null,8,["modelValue"])]),_:1}),a(o(n),{label:"Должность"},{default:u(()=>[a(o(r),{name:"position",place:"Должность",need:!0,modelValue:e.value.position,"onUpdate:modelValue":l[4]||(l[4]=t=>e.value.position=t)},null,8,["modelValue"])]),_:1}),a(o(n),{label:"Адрес организации"},{default:u(()=>[a(o(r),{name:"address",place:"Адрес организации",modelValue:e.value.address,"onUpdate:modelValue":l[5]||(l[5]=t=>e.value.address=t)},null,8,["modelValue"])]),_:1}),a(o(n),{label:"Причина увольнения"},{default:u(()=>[a(o(r),{name:"reason",place:"Причина увольнения",modelValue:e.value.reason,"onUpdate:modelValue":l[6]||(l[6]=t=>e.value.reason=t)},null,8,["modelValue"])]),_:1}),a(o(v),null,{default:u(()=>[a(o(k),{onCancel:l[7]||(l[7]=t=>p("cancel"))})]),_:1})],32))}});export{P as default};
