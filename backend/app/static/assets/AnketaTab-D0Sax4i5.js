const __vite__fileDeps=["./ActionIcons-D1xqXEN-.js","./index-1yFXvMEA.js","./index-BqKjTnG4.css","./_plugin-vue_export-helper-DlAUqK2U.js","./ActionIcons-Ns2nW-Me.css","./FileForm-DvW3KssW.js","./FileForm-By8_2B11.css","./ResumeForm-CWKd7x48.js","./state-QybiP1xm.js","./PreviousDiv-PgQHAOm7.js","./PreviousDiv-bkNbdR_A.css","./EducationDiv-BAvDSkJ4.js","./EducationDiv--yooqeoF.css","./StaffDiv-BlVypY8N.js","./StaffDiv-DE59AevV.css","./DocumentDiv-Bxjj-oQ8.js","./DocumentDiv-DlhRruGm.css","./AddressDiv-Del2x0Wj.js","./AddressDiv-D1oEIbjp.css","./ContactDiv-C-Ya_Xt5.js","./ContactDiv-DoLNqn01.css","./RelationDiv-DvxQKoww.js","./RelationDiv-DtvekvSv.css","./WorkplaceDiv-C9tp5C2U.js","./WorkplaceDiv-agfIBb1X.css","./AffilationDiv-CzXNLFHu.js","./AffilationDiv-C4Vj8Mma.css","./LabelSlot-DmfbviAy.js","./LabelSlot-BKRWK_aH.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as C,r as S,o as p,c as d,b as a,u as e,l as o,g as v,v as c,p as r,t as s,m as f,f as g,F as k,z as F,q as $,h as i,j as l}from"./index-1yFXvMEA.js";import{h as t,g as h}from"./state-QybiP1xm.js";const x={key:0,class:"card card-body"},M=C({__name:"AnketaTab",setup(U){const D=i(()=>l(()=>import("./ActionIcons-D1xqXEN-.js"),__vite__mapDeps([0,1,2,3,4]),import.meta.url)),E=i(()=>l(()=>import("./FileForm-DvW3KssW.js"),__vite__mapDeps([5,1,2,3,6]),import.meta.url)),b=i(()=>l(()=>import("./ResumeForm-CWKd7x48.js"),__vite__mapDeps([7,1,2,8]),import.meta.url)),A=i(()=>l(()=>import("./PreviousDiv-PgQHAOm7.js"),__vite__mapDeps([9,1,2,8,3,10]),import.meta.url)),R=i(()=>l(()=>import("./EducationDiv-BAvDSkJ4.js"),__vite__mapDeps([11,1,2,8,3,12]),import.meta.url)),L=i(()=>l(()=>import("./StaffDiv-BlVypY8N.js"),__vite__mapDeps([13,1,2,8,3,14]),import.meta.url)),T=i(()=>l(()=>import("./DocumentDiv-Bxjj-oQ8.js"),__vite__mapDeps([15,1,2,8,3,16]),import.meta.url)),V=i(()=>l(()=>import("./AddressDiv-Del2x0Wj.js"),__vite__mapDeps([17,1,2,8,3,18]),import.meta.url)),I=i(()=>l(()=>import("./ContactDiv-C-Ya_Xt5.js"),__vite__mapDeps([19,1,2,8,3,20]),import.meta.url)),P=i(()=>l(()=>import("./RelationDiv-DvxQKoww.js"),__vite__mapDeps([21,1,2,8,3,22]),import.meta.url)),O=i(()=>l(()=>import("./WorkplaceDiv-C9tp5C2U.js"),__vite__mapDeps([23,1,2,8,3,24]),import.meta.url)),y=i(()=>l(()=>import("./AffilationDiv-CzXNLFHu.js"),__vite__mapDeps([25,1,2,8,3,26]),import.meta.url)),n=i(()=>l(()=>import("./LabelSlot-DmfbviAy.js"),__vite__mapDeps([27,1,2,3,28]),import.meta.url)),_=S({action:"",form:{},showActions:!1});return(B,u)=>(p(),d(k,null,[_.value.action?(p(),d("div",x,[a(e(b),{action:_.value.action,resume:e(t).anketa.persons,onCancel:u[0]||(u[0]=m=>_.value.action="")},null,8,["action","resume"])])):(p(),d("div",{key:1,class:"card card-body",onMouseover:u[4]||(u[4]=m=>_.value.showActions=!0),onMouseout:u[5]||(u[5]=m=>_.value.showActions=!1)},[a(e(n),null,{default:o(()=>[v(a(e(D),{onDelete:u[2]||(u[2]=m=>e(t).deleteItem(e(t).anketa.persons.id,"persons")),onUpdate:u[3]||(u[3]=m=>_.value.action="update"),"for-input":"persons-file"},{default:o(()=>[v(a(e(E),{"name-id":"persons-file",accept:"*",onSubmit:u[1]||(u[1]=m=>e(h)(m,"persons"))},null,512),[[c,_.value.showActions]])]),_:1},512),[[c,_.value.showActions]])]),_:1}),a(e(n),{label:"Фамилия"},{default:o(()=>[r(s(e(t).anketa.persons.surname),1)]),_:1}),a(e(n),{label:"Имя"},{default:o(()=>[r(s(e(t).anketa.persons.firstname),1)]),_:1}),a(e(n),{label:"Отчество"},{default:o(()=>[r(s(e(t).anketa.persons.patronymic),1)]),_:1}),a(e(n),{label:"Дата рождения"},{default:o(()=>[r(s(new Date(String(e(t).anketa.persons.birthday)).toLocaleDateString("ru-RU")),1)]),_:1}),a(e(n),{label:"Место рождения"},{default:o(()=>[r(s(e(t).anketa.persons.birthplace),1)]),_:1}),a(e(n),{label:"Гражданство"},{default:o(()=>[r(s(e(t).anketa.persons.citizenship),1)]),_:1}),e(t).anketa.persons.dual?(p(),f(e(n),{key:0,label:"Двойное гражданство"},{default:o(()=>[r(s(e(t).anketa.persons.dual),1)]),_:1})):g("",!0),a(e(n),{label:"СНИЛС"},{default:o(()=>[r(s(e(t).anketa.persons.snils),1)]),_:1}),a(e(n),{label:"ИНН"},{default:o(()=>[r(s(e(t).anketa.persons.inn),1)]),_:1}),a(e(n),{label:"Семейное положение"},{default:o(()=>[r(s(e(t).anketa.persons.marital),1)]),_:1}),a(e(n),{label:"Статус"},{default:o(()=>[r(s(e(t).anketa.persons.status),1)]),_:1}),a(e(n),{label:"Дата записи"},{default:o(()=>[r(s(e(t).anketa.persons.created?new Date(e(t).anketa.persons.created+" UTC").toLocaleString("ru-RU"):""),1)]),_:1}),a(e(n),{label:"Пользователь"},{default:o(()=>[r(s(e(t).anketa.persons.username?e(t).anketa.persons.username:""),1)]),_:1}),a(e(n),{label:"Материалы"},{default:o(()=>[r(s(e(t).anketa.persons.path),1)]),_:1}),a(e(n),{label:"Дополнительная информация"},{default:o(()=>[r(s(e(t).anketa.persons.addition?e(t).anketa.persons.addition:"-"),1)]),_:1})],32)),(p(!0),d(k,null,F([e(L),e(R),e(O),e(T),e(V),e(I),e(y),e(A),e(P)],(m,w)=>(p(),d("div",{key:w},[(p(),f($(m)))]))),128))],64))}});export{M as default};