const __vite__fileDeps=["./ActionIcons-CxAFntL3.js","./index-D1U1a8b2.js","./index-BqKjTnG4.css","./_plugin-vue_export-helper-DlAUqK2U.js","./ActionIcons-CukUJdTR.css","./FileForm-B3mS3pEf.js","./FileForm-By8_2B11.css","./ResumeForm-DJ9mJwu5.js","./state-u74uZLPD.js","./PreviousDiv-D8umxd9E.js","./PreviousDiv-B95jUJqM.css","./EducationDiv-Czzrg8PH.js","./EducationDiv-Bb9B8WnN.css","./StaffDiv-BYyeppec.js","./StaffDiv-jMs7GQTq.css","./DocumentDiv-BfK615yn.js","./DocumentDiv-CiIxhqs0.css","./AddressDiv-QAVRfGys.js","./AddressDiv-B7XMfByo.css","./ContactDiv-0lksuNrz.js","./ContactDiv-BCuLm8oN.css","./RelationDiv-Dtr2-uJv.js","./RelationDiv-BNz6er3T.css","./WorkplaceDiv-C8LcfgTA.js","./WorkplaceDiv-Bi7opNap.css","./AffilationDiv-VJAWFJCM.js","./AffilationDiv-Cun-kTID.css","./LabelSlot-RdSfBjzZ.js","./LabelSlot-BKRWK_aH.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as g,r as C,o as p,c as d,b as a,u as e,l as o,g as v,v as c,p as r,t as s,m as f,f as S,F as k,z as F,q as U,h as i,j as l}from"./index-D1U1a8b2.js";import{g as t,f as $,e as x}from"./state-u74uZLPD.js";const B={key:0,class:"card card-body mb-3"},j=g({__name:"AnketaTab",setup(N){const D=i(()=>l(()=>import("./ActionIcons-CxAFntL3.js"),__vite__mapDeps([0,1,2,3,4]),import.meta.url)),E=i(()=>l(()=>import("./FileForm-B3mS3pEf.js"),__vite__mapDeps([5,1,2,3,6]),import.meta.url)),b=i(()=>l(()=>import("./ResumeForm-DJ9mJwu5.js"),__vite__mapDeps([7,1,2,8]),import.meta.url)),A=i(()=>l(()=>import("./PreviousDiv-D8umxd9E.js"),__vite__mapDeps([9,1,2,8,3,10]),import.meta.url)),R=i(()=>l(()=>import("./EducationDiv-Czzrg8PH.js"),__vite__mapDeps([11,1,2,8,3,12]),import.meta.url)),L=i(()=>l(()=>import("./StaffDiv-BYyeppec.js"),__vite__mapDeps([13,1,2,8,3,14]),import.meta.url)),I=i(()=>l(()=>import("./DocumentDiv-BfK615yn.js"),__vite__mapDeps([15,1,2,8,3,16]),import.meta.url)),T=i(()=>l(()=>import("./AddressDiv-QAVRfGys.js"),__vite__mapDeps([17,1,2,8,3,18]),import.meta.url)),V=i(()=>l(()=>import("./ContactDiv-0lksuNrz.js"),__vite__mapDeps([19,1,2,8,3,20]),import.meta.url)),P=i(()=>l(()=>import("./RelationDiv-Dtr2-uJv.js"),__vite__mapDeps([21,1,2,8,3,22]),import.meta.url)),O=i(()=>l(()=>import("./WorkplaceDiv-C8LcfgTA.js"),__vite__mapDeps([23,1,2,8,3,24]),import.meta.url)),y=i(()=>l(()=>import("./AffilationDiv-VJAWFJCM.js"),__vite__mapDeps([25,1,2,8,3,26]),import.meta.url)),n=i(()=>l(()=>import("./LabelSlot-RdSfBjzZ.js"),__vite__mapDeps([27,1,2,3,28]),import.meta.url)),_=C({action:"",form:{},showActions:!1});return(h,u)=>(p(),d(k,null,[_.value.action?(p(),d("div",B,[a(e(b),{action:_.value.action,resume:e(t).anketa.persons,onCancel:u[0]||(u[0]=m=>_.value.action="")},null,8,["action","resume"])])):(p(),d("div",{key:1,class:"card card-body mb-3",onMouseover:u[4]||(u[4]=m=>_.value.showActions=!0),onMouseout:u[5]||(u[5]=m=>_.value.showActions=!1)},[a(e(n),null,{default:o(()=>[v(a(e(D),{onDelete:u[2]||(u[2]=m=>e(t).deleteItem(e(t).anketa.persons.id,"persons")),onUpdate:u[3]||(u[3]=m=>_.value.action="update"),"for-input":"persons-file"},{default:o(()=>[v(a(e(E),{"name-id":"persons-file",accept:"*",onSubmit:u[1]||(u[1]=m=>e($)(m,"persons"))},null,512),[[c,_.value.showActions]])]),_:1},512),[[c,_.value.showActions&&e(t).anketa.persons.user_id==e(x).userId]])]),_:1}),a(e(n),{label:"Фамилия"},{default:o(()=>[r(s(e(t).anketa.persons.surname),1)]),_:1}),a(e(n),{label:"Имя"},{default:o(()=>[r(s(e(t).anketa.persons.firstname),1)]),_:1}),a(e(n),{label:"Отчество"},{default:o(()=>[r(s(e(t).anketa.persons.patronymic),1)]),_:1}),a(e(n),{label:"Дата рождения"},{default:o(()=>[r(s(new Date(String(e(t).anketa.persons.birthday)).toLocaleDateString("ru-RU")),1)]),_:1}),a(e(n),{label:"Место рождения"},{default:o(()=>[r(s(e(t).anketa.persons.birthplace),1)]),_:1}),a(e(n),{label:"Гражданство"},{default:o(()=>[r(s(e(t).anketa.persons.citizenship),1)]),_:1}),e(t).anketa.persons.dual?(p(),f(e(n),{key:0,label:"Двойное гражданство"},{default:o(()=>[r(s(e(t).anketa.persons.dual),1)]),_:1})):S("",!0),a(e(n),{label:"СНИЛС"},{default:o(()=>[r(s(e(t).anketa.persons.snils),1)]),_:1}),a(e(n),{label:"ИНН"},{default:o(()=>[r(s(e(t).anketa.persons.inn),1)]),_:1}),a(e(n),{label:"Семейное положение"},{default:o(()=>[r(s(e(t).anketa.persons.marital),1)]),_:1}),a(e(n),{label:"Статус"},{default:o(()=>[r(s(e(t).anketa.persons.standing),1)]),_:1}),a(e(n),{label:"Дата записи"},{default:o(()=>[r(s(e(t).anketa.persons.created?new Date(e(t).anketa.persons.created+" UTC").toLocaleString("ru-RU"):""),1)]),_:1}),a(e(n),{label:"Пользователь"},{default:o(()=>[r(s(e(t).anketa.persons.username?e(t).anketa.persons.username:""),1)]),_:1}),a(e(n),{label:"Материалы"},{default:o(()=>[r(s(e(t).anketa.persons.destination),1)]),_:1}),a(e(n),{label:"Дополнительная информация"},{default:o(()=>[r(s(e(t).anketa.persons.addition?e(t).anketa.persons.addition:"-"),1)]),_:1})],32)),(p(!0),d(k,null,F([e(L),e(R),e(O),e(I),e(T),e(V),e(y),e(A),e(P)],(m,w)=>(p(),d("div",{key:w},[(p(),f(U(m)))]))),128))],64))}});export{j as default};
