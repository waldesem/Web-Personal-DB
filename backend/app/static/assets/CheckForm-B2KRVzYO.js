const __vite__fileDeps=["./TextArea-CVZzD21U.js","./index-Cj2pYzZu.js","./index-BqKjTnG4.css","./LabelSlot-CFQC1Hbj.js","./_plugin-vue_export-helper-DlAUqK2U.js","./LabelSlot-BKRWK_aH.css","./SelectDiv-DGHNFSzc.js","./SwitchBox-C4Dx5rtd.js","./BtnGroup-CTOwoHSI.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as _,D as E,n as w,L as y,o as A,c as O,g as v,a as o,w as n,u as a,s as C,b as r,e as s}from"./index-Cj2pYzZu.js";import{s as D,c as I}from"./state-Kc3gs5o9.js";import"./utilities-BY8xKrXT.js";const L={class:"p-3"},P={class:"form form-check",role:"form"},g=_({__name:"CheckForm",props:{check:{type:Object,default:{}}},emits:["cancel"],setup(f,{emit:b}){const d=r(()=>s(()=>import("./TextArea-CVZzD21U.js"),__vite__mapDeps([0,1,2]),import.meta.url)),t=r(()=>s(()=>import("./LabelSlot-CFQC1Hbj.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),c=r(()=>s(()=>import("./SelectDiv-DGHNFSzc.js"),__vite__mapDeps([6,1,2]),import.meta.url)),i=r(()=>s(()=>import("./SwitchBox-C4Dx5rtd.js"),__vite__mapDeps([7,1,2]),import.meta.url)),k=r(()=>s(()=>import("./BtnGroup-CTOwoHSI.js"),__vite__mapDeps([8,1,2]),import.meta.url)),p=b,e=E(f.check),m=w(!1);function U(){I.updateItem("checks",e.value),m.value=!1,p("cancel"),Object.keys(e.value).forEach(V=>delete e.value[V])}return y(m,()=>{m.value&&Object.assign(e.value,{workplace:"Негатива по местам работы не обнаружено",document:"Среди недействительных документов не обнаружен",inn:"ИНН соответствует паспорту",debt:"Задолженности не обнаружены",bankruptcy:"Решений о признании банкротом не имеется",bki:"Кредитная история не положительная",courts:"Судебные дела не обнаружены",affilation:"Аффилированность не выявлена",terrorist:"В списке террористов не обнаружен",mvd:"В розыск не объявлен",internet:"В открытых источниках негатив не обнаружен",cronos:"В Кронос негатив не выявлен",cros:"В Крос негатив не выявлен",addition:"Дополнительная информация отсутствует"})}),(V,l)=>(A(),O("div",L,[v("form",P,[o(a(t),{label:"Негатива нет"},{default:n(()=>[o(a(i),{name:"noNegative",place:"Негатива нет",modelValue:m.value,"onUpdate:modelValue":l[0]||(l[0]=u=>m.value=u)},null,8,["modelValue"])]),_:1})]),v("form",{onSubmit:C(U,["prevent"]),class:"form form-check",role:"form",id:"checkFormId"},[o(a(t),{label:"Проверка по местам работы"},{default:n(()=>[o(a(d),{name:"workplace",place:"Проверка по местам работы",modelValue:e.value.workplace,"onUpdate:modelValue":l[1]||(l[1]=u=>e.value.workplace=u)},null,8,["modelValue"])]),_:1}),o(a(t),{label:"Проверка документов"},{default:n(()=>[o(a(d),{name:"document",place:"Проверка документов",modelValue:e.value.document,"onUpdate:modelValue":l[2]||(l[2]=u=>e.value.document=u)},null,8,["modelValue"])]),_:1}),o(a(t),{label:"Проверка ИНН"},{default:n(()=>[o(a(d),{name:"inn",place:"Проверка ИНН",modelValue:e.value.inn,"onUpdate:modelValue":l[3]||(l[3]=u=>e.value.inn=u)},null,8,["modelValue"])]),_:1}),o(a(t),{label:"Проверка задолженностей"},{default:n(()=>[o(a(d),{name:"debt",place:"Проверка задолженностей",modelValue:e.value.debt,"onUpdate:modelValue":l[4]||(l[4]=u=>e.value.debt=u)},null,8,["modelValue"])]),_:1}),o(a(t),{label:"Проверка решений о признании банкротом"},{default:n(()=>[o(a(d),{name:"bankruptcy",place:"Проверка решений о признании банкротом",modelValue:e.value.bankruptcy,"onUpdate:modelValue":l[5]||(l[5]=u=>e.value.bankruptcy=u)},null,8,["modelValue"])]),_:1}),o(a(t),{label:"Проверка кредитной истории"},{default:n(()=>[o(a(d),{name:"bki",place:"Проверка кредитной истории",modelValue:e.value.bki,"onUpdate:modelValue":l[6]||(l[6]=u=>e.value.bki=u)},null,8,["modelValue"])]),_:1}),o(a(t),{label:"Проверка судебных дел"},{default:n(()=>[o(a(d),{name:"courts",place:"Проверка судебных дел",modelValue:e.value.courts,"onUpdate:modelValue":l[7]||(l[7]=u=>e.value.courts=u)},null,8,["modelValue"])]),_:1}),o(a(t),{label:"Проверка аффилированности"},{default:n(()=>[o(a(d),{name:"affilation",place:"Проверка аффилированности",modelValue:e.value.affilation,"onUpdate:modelValue":l[8]||(l[8]=u=>e.value.affilation=u)},null,8,["modelValue"])]),_:1}),o(a(t),{label:"Проверка в списке террористов"},{default:n(()=>[o(a(d),{name:"terrorist",place:"Проверка в списке террористов",modelValue:e.value.terrorist,"onUpdate:modelValue":l[9]||(l[9]=u=>e.value.terrorist=u)},null,8,["modelValue"])]),_:1}),o(a(t),{label:"Проверка в розыск"},{default:n(()=>[o(a(d),{name:"mvd",place:"Проверка в розыск",modelValue:e.value.mvd,"onUpdate:modelValue":l[10]||(l[10]=u=>e.value.mvd=u)},null,8,["modelValue"])]),_:1}),o(a(t),{label:"Проверка в открытых источниках"},{default:n(()=>[o(a(d),{name:"internet",place:"Проверка в открытых источниках",modelValue:e.value.internet,"onUpdate:modelValue":l[11]||(l[11]=u=>e.value.internet=u)},null,8,["modelValue"])]),_:1}),o(a(t),{label:"Проверка в Кронос"},{default:n(()=>[o(a(d),{name:"cronos",place:"Проверка в Кронос",modelValue:e.value.cronos,"onUpdate:modelValue":l[12]||(l[12]=u=>e.value.cronos=u)},null,8,["modelValue"])]),_:1}),o(a(t),{label:"Проверка в Крос"},{default:n(()=>[o(a(d),{name:"cros",place:"Проверка в Крос",modelValue:e.value.cros,"onUpdate:modelValue":l[13]||(l[13]=u=>e.value.cros=u)},null,8,["modelValue"])]),_:1}),o(a(t),{label:"Дополнительная информация"},{default:n(()=>[o(a(d),{name:"addition",place:"Дополнительная информация",modelValue:e.value.addition,"onUpdate:modelValue":l[14]||(l[14]=u=>e.value.addition=u)},null,8,["modelValue"])]),_:1}),o(a(t),{label:"Результат"},{default:n(()=>[o(a(c),{name:"conclusion",need:!0,select:a(D).conclusions,modelValue:e.value.conclusion,"onUpdate:modelValue":l[15]||(l[15]=u=>e.value.conclusion=u)},null,8,["select","modelValue"])]),_:1}),o(a(t),{label:"Комментарий"},{default:n(()=>[o(a(d),{name:"comments",place:"Комментарий",modelValue:e.value.comment,"onUpdate:modelValue":l[16]||(l[16]=u=>e.value.comment=u)},null,8,["modelValue"])]),_:1}),o(a(t),{label:"Полиграф"},{default:n(()=>[o(a(i),{name:"pfo",place:"Полиграф",modelValue:e.value.pfo,"onUpdate:modelValue":l[17]||(l[17]=u=>e.value.pfo=u)},null,8,["modelValue"])]),_:1}),o(a(k),{onCancel:l[18]||(l[18]=u=>p("cancel"))})],32)]))}});export{g as default};
