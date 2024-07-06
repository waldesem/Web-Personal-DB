const __vite__fileDeps=["./LabelSlot-RdSfBjzZ.js","./index-D1U1a8b2.js","./index-BqKjTnG4.css","./_plugin-vue_export-helper-DlAUqK2U.js","./LabelSlot-BKRWK_aH.css","./SelectDiv-CcT-1QKJ.js","./InputElement-CpP_zLuD.js","./TextArea-COCR6DJ9.js","./BtnGroup-DCfcNJ97.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as E,I as A,o as U,c as g,b as o,l as n,u as t,w as I,h as r,j as d,i as R}from"./index-D1U1a8b2.js";import{d as O,c as x,b as D,g as L,s as V}from"./state-u74uZLPD.js";const k=E({__name:"ResumeForm",props:{action:{type:String,default:"create"},resume:{type:Object,default:{}}},emits:["cancel"],setup(v,{emit:f}){const u=r(()=>d(()=>import("./LabelSlot-RdSfBjzZ.js"),__vite__mapDeps([0,1,2,3,4]),import.meta.url)),b=r(()=>d(()=>import("./SelectDiv-CcT-1QKJ.js"),__vite__mapDeps([5,1,2]),import.meta.url)),m=r(()=>d(()=>import("./InputElement-CpP_zLuD.js"),__vite__mapDeps([6,1,2]),import.meta.url)),_=r(()=>d(()=>import("./TextArea-COCR6DJ9.js"),__vite__mapDeps([7,1,2]),import.meta.url)),c=r(()=>d(()=>import("./BtnGroup-DCfcNJ97.js"),__vite__mapDeps([8,1,2]),import.meta.url)),i=f,p=v,l=A(p.resume);async function y(){try{const s=await x.post(`${D}/persons`,l.value),{person_id:e}=s.data;Object.keys(l.value).forEach(a=>delete l.value[a]),p.action==="create"?R.push({name:"profile",params:{id:e}}):(i("cancel"),L.getItem("persons")),V.setAlert("alert-success","Данные успешно обновлены")}catch(s){V.setAlert("alert-danger",`Возникла ошибка ${s}`)}}return(s,e)=>(U(),g("form",{onSubmit:I(y,["prevent"]),class:"form form-check",role:"form"},[o(t(u),{label:"Регион"},{default:n(()=>[o(t(b),{name:"region_id",select:t(O).regions,modelValue:l.value.region,"onUpdate:modelValue":e[0]||(e[0]=a=>l.value.region=a)},null,8,["select","modelValue"])]),_:1}),o(t(u),{label:"Фамилия"},{default:n(()=>[o(t(m),{need:!0,name:"surname",place:"Фамилия*",pattern:"[А-Яа-яЁё\\-'\\s]+",modelValue:l.value.surname,"onUpdate:modelValue":e[1]||(e[1]=a=>l.value.surname=a)},null,8,["modelValue"])]),_:1}),o(t(u),{label:"Имя"},{default:n(()=>[o(t(m),{need:!0,name:"firstname",place:"Имя*",pattern:"[А-Яа-яЁё\\-'\\s]+",modelValue:l.value.firstname,"onUpdate:modelValue":e[2]||(e[2]=a=>l.value.firstname=a)},null,8,["modelValue"])]),_:1}),o(t(u),{label:"Отчество"},{default:n(()=>[o(t(m),{name:"patronymic",place:"Отчество",modelValue:l.value.patronymic,"onUpdate:modelValue":e[3]||(e[3]=a=>l.value.patronymic=a)},null,8,["modelValue"])]),_:1}),o(t(u),{label:"Дата рождения*"},{default:n(()=>[o(t(m),{need:!0,name:"birthday",place:"Дата рождения*",typeof:"date",modelValue:l.value.birthday,"onUpdate:modelValue":e[4]||(e[4]=a=>l.value.birthday=a)},null,8,["modelValue"])]),_:1}),o(t(u),{label:"Место рождения"},{default:n(()=>[o(t(m),{name:"birthplace",place:"Место рождения",modelValue:l.value.birthplace,"onUpdate:modelValue":e[5]||(e[5]=a=>l.value.birthplace=a)},null,8,["modelValue"])]),_:1}),o(t(u),{label:"Гражданство"},{default:n(()=>[o(t(m),{name:"citizenship",place:"Гражданство",modelValue:l.value.citizenship,"onUpdate:modelValue":e[6]||(e[6]=a=>l.value.citizenship=a)},null,8,["modelValue"])]),_:1}),o(t(u),{label:"Двойное гражданство"},{default:n(()=>[o(t(m),{name:"dual",place:"Двойное гражданство",modelValue:l.value.dual,"onUpdate:modelValue":e[7]||(e[7]=a=>l.value.dual=a)},null,8,["modelValue"])]),_:1}),o(t(u),{label:"СНИЛС"},{default:n(()=>[o(t(m),{name:"snils",place:"СНИЛС",pattern:"[0-9]{11}",modelValue:l.value.snils,"onUpdate:modelValue":e[8]||(e[8]=a=>l.value.snils=a)},null,8,["modelValue"])]),_:1}),o(t(u),{label:"ИНН"},{default:n(()=>[o(t(m),{name:"inn",place:"ИНН",max:"12",pattern:"[0-9]{12}",modelValue:l.value.inn,"onUpdate:modelValue":e[9]||(e[9]=a=>l.value.inn=a)},null,8,["modelValue"])]),_:1}),o(t(u),{label:"Семейное положение"},{default:n(()=>[o(t(m),{name:"marital",place:"Семейное положение",modelValue:l.value.marital,"onUpdate:modelValue":e[10]||(e[10]=a=>l.value.marital=a)},null,8,["modelValue"])]),_:1}),o(t(u),{label:"Дополнительно"},{default:n(()=>[o(t(_),{name:"addition",place:"Дополнительно",modelValue:l.value.addition,"onUpdate:modelValue":e[11]||(e[11]=a=>l.value.addition=a)},null,8,["modelValue"])]),_:1}),o(t(c),{onCancel:e[12]||(e[12]=a=>i("cancel"))})],32))}});export{k as default};
