const __vite__fileDeps=["assets/LabelSlot-C8Y-0GKw.js","assets/index-BhT_3F5B.js","assets/index-D3owuatg.css","assets/TextArea-BlZpyNHg.js","assets/InputElement-BRa9pb8S.js","assets/GroupContent-CBkEmxXT.js","assets/BtnGroup-CManQ3k2.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as E,U as V,o as b,c as A,b as t,w as m,u as o,z as I,e as i,f as l}from"./index-BhT_3F5B.js";const O=E({__name:"InvestigationForm",props:{investigation:{type:Object,default:{}}},emits:["submit","cancel"],setup(_,{emit:d}){const r=i(()=>l(()=>import("./LabelSlot-C8Y-0GKw.js"),__vite__mapDeps([0,1,2]))),p=i(()=>l(()=>import("./TextArea-BlZpyNHg.js"),__vite__mapDeps([3,1,2]))),f=i(()=>l(()=>import("./InputElement-BRa9pb8S.js"),__vite__mapDeps([4,1,2]))),v=i(()=>l(()=>import("./GroupContent-CBkEmxXT.js"),__vite__mapDeps([5,1,2]))),c=i(()=>l(()=>import("./BtnGroup-CManQ3k2.js"),__vite__mapDeps([6,1,2]))),u=d,a=_,s=V(a.investigation);return(g,e)=>(b(),A("form",{onSubmit:e[3]||(e[3]=I(n=>u("submit",s.value),["prevent"])),class:"form form-check",role:"form"},[t(o(r),{label:"Тема проверки"},{default:m(()=>[t(o(f),{name:"theme",place:"Тема проверки",need:!0,modelValue:s.value.theme,"onUpdate:modelValue":e[0]||(e[0]=n=>s.value.theme=n)},null,8,["modelValue"])]),_:1}),t(o(r),{label:"Информация"},{default:m(()=>[t(o(p),{name:"info",place:"Информация",modelValue:a.investigation.info,"onUpdate:modelValue":e[1]||(e[1]=n=>a.investigation.info=n)},null,8,["modelValue"])]),_:1}),t(o(c),null,{default:m(()=>[t(o(v),{onCancel:e[2]||(e[2]=n=>u("cancel"))})]),_:1})],32))}});export{O as default};
