const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=["./ActionIcons-D-fKbOWt.js","./index-C1r4f5TB.js","./index-BqKjTnG4.css","./_plugin-vue_export-helper-DlAUqK2U.js","./ActionIcons-CukUJdTR.css","./SelectDiv-CIic7RDs.js","./FileForm-CPEIJme2.js","./ResumeForm-BjgzWBWg.js","./state-BGY6iYIz.js","./PreviousDiv-CPJwKH_F.js","./PreviousDiv-DveST6cc.css","./EducationDiv-CyLzctUy.js","./EducationDiv-CxDAMEtZ.css","./StaffDiv-CnY_pV4S.js","./StaffDiv-D5boCRCx.css","./DocumentDiv-K_DLaAAZ.js","./DocumentDiv-Ba0h98Ti.css","./AddressDiv-CVkCnBFe.js","./AddressDiv-DWQ00uE8.css","./ContactDiv-RfvBt3bt.js","./ContactDiv-Be9msH-k.css","./RelationDiv-Bo8bjYxC.js","./RelationDiv-CBM61PeA.css","./WorkplaceDiv-Bo8QpNrs.js","./WorkplaceDiv-BWag6gxg.css","./AffilationDiv-Bik4dobt.js","./AffilationDiv-XPg7ieOZ.css","./LabelSlot-B9jKJnYD.js","./LabelSlot-BMshfUVW.css"])))=>i.map(i=>d[i]);
import{d as C,r as F,o as m,c as p,b as a,u as e,l as o,g as v,v as c,p as r,t as i,m as f,f as U,F as k,A as $,q as x,h as l,j as u}from"./index-C1r4f5TB.js";import{e as t,c as D,g as B}from"./state-BGY6iYIz.js";const N={key:0,class:"card card-body mb-3"},z=C({__name:"AnketaTab",setup(M){const E=l(()=>u(()=>import("./ActionIcons-D-fKbOWt.js"),__vite__mapDeps([0,1,2,3,4]),import.meta.url)),b=l(()=>u(()=>import("./SelectDiv-CIic7RDs.js"),__vite__mapDeps([5,1,2]),import.meta.url)),A=l(()=>u(()=>import("./FileForm-CPEIJme2.js"),__vite__mapDeps([6,1,2]),import.meta.url)),I=l(()=>u(()=>import("./ResumeForm-BjgzWBWg.js"),__vite__mapDeps([7,1,2,8]),import.meta.url)),R=l(()=>u(()=>import("./PreviousDiv-CPJwKH_F.js"),__vite__mapDeps([9,1,2,8,3,10]),import.meta.url)),V=l(()=>u(()=>import("./EducationDiv-CyLzctUy.js"),__vite__mapDeps([11,1,2,8,3,12]),import.meta.url)),L=l(()=>u(()=>import("./StaffDiv-CnY_pV4S.js"),__vite__mapDeps([13,1,2,8,3,14]),import.meta.url)),T=l(()=>u(()=>import("./DocumentDiv-K_DLaAAZ.js"),__vite__mapDeps([15,1,2,8,3,16]),import.meta.url)),g=l(()=>u(()=>import("./AddressDiv-CVkCnBFe.js"),__vite__mapDeps([17,1,2,8,3,18]),import.meta.url)),P=l(()=>u(()=>import("./ContactDiv-RfvBt3bt.js"),__vite__mapDeps([19,1,2,8,3,20]),import.meta.url)),O=l(()=>u(()=>import("./RelationDiv-Bo8bjYxC.js"),__vite__mapDeps([21,1,2,8,3,22]),import.meta.url)),y=l(()=>u(()=>import("./WorkplaceDiv-Bo8QpNrs.js"),__vite__mapDeps([23,1,2,8,3,24]),import.meta.url)),w=l(()=>u(()=>import("./AffilationDiv-Bik4dobt.js"),__vite__mapDeps([25,1,2,8,3,26]),import.meta.url)),n=l(()=>u(()=>import("./LabelSlot-B9jKJnYD.js"),__vite__mapDeps([27,1,2,3,28]),import.meta.url)),d=F({action:"",form:{},showActions:!1});return(h,s)=>(m(),p(k,null,[d.value.action?(m(),p("div",N,[a(e(I),{action:d.value.action,resume:e(t).anketa.persons,onCancel:s[0]||(s[0]=_=>{d.value.action="",e(t).getItem("persons")})},null,8,["action","resume"])])):(m(),p("div",{key:1,class:"card card-body mb-3",onMouseover:s[6]||(s[6]=_=>d.value.showActions=!0),onMouseout:s[7]||(s[7]=_=>d.value.showActions=!1)},[a(e(n),null,{default:o(()=>[v(a(e(E),{onDelete:s[2]||(s[2]=_=>e(t).deleteItem(e(t).anketa.persons.id,"persons")),onUpdate:s[3]||(s[3]=_=>d.value.action="update"),"for-input":"persons-file"},{default:o(()=>[v(a(e(A),{"name-id":"persons-file",accept:"*",onSubmit:s[1]||(s[1]=_=>e(t).submitFile(_,"anketa",e(t).share.candId))},null,512),[[c,d.value.showActions]])]),_:1},512),[[c,d.value.showActions&&e(t).anketa.persons.user_id==e(D).user.userId&&e(t).anketa.persons.standing]])]),_:1}),a(e(n),{label:"Регион"},{default:o(()=>[a(e(b),{width:"20%",name:"region",disable:e(D).user.userId!=e(t).anketa.persons.user_id||!e(t).anketa.persons.standing,select:e(B).classes.regions,modelValue:e(t).anketa.persons.region,"onUpdate:modelValue":s[4]||(s[4]=_=>e(t).anketa.persons.region=_),onSubmitData:s[5]||(s[5]=_=>e(t).changeRegion())},null,8,["disable","select","modelValue"])]),_:1}),a(e(n),{label:"Фамилия"},{default:o(()=>[r(i(e(t).anketa.persons.surname),1)]),_:1}),a(e(n),{label:"Имя"},{default:o(()=>[r(i(e(t).anketa.persons.firstname),1)]),_:1}),a(e(n),{label:"Отчество"},{default:o(()=>[r(i(e(t).anketa.persons.patronymic),1)]),_:1}),a(e(n),{label:"Дата рождения"},{default:o(()=>[r(i(new Date(String(e(t).anketa.persons.birthday)).toLocaleDateString("ru-RU")),1)]),_:1}),a(e(n),{label:"Место рождения"},{default:o(()=>[r(i(e(t).anketa.persons.birthplace),1)]),_:1}),a(e(n),{label:"Гражданство"},{default:o(()=>[r(i(e(t).anketa.persons.citizenship),1)]),_:1}),e(t).anketa.persons.dual?(m(),f(e(n),{key:0,label:"Двойное гражданство"},{default:o(()=>[r(i(e(t).anketa.persons.dual),1)]),_:1})):U("",!0),a(e(n),{label:"СНИЛС"},{default:o(()=>[r(i(e(t).anketa.persons.snils),1)]),_:1}),a(e(n),{label:"ИНН"},{default:o(()=>[r(i(e(t).anketa.persons.inn),1)]),_:1}),a(e(n),{label:"Семейное положение"},{default:o(()=>[r(i(e(t).anketa.persons.marital),1)]),_:1}),a(e(n),{label:"Дата записи"},{default:o(()=>[r(i(e(t).anketa.persons.created?new Date(e(t).anketa.persons.created+" UTC").toLocaleString("ru-RU"):""),1)]),_:1}),a(e(n),{label:"Пользователь"},{default:o(()=>[r(i(e(t).anketa.persons.username?e(t).anketa.persons.username:""),1)]),_:1}),a(e(n),{label:"Материалы"},{default:o(()=>[r(i(e(t).anketa.persons.destination),1)]),_:1}),a(e(n),{label:"Дополнительная информация"},{default:o(()=>[r(i(e(t).anketa.persons.addition?e(t).anketa.persons.addition:"-"),1)]),_:1})],32)),(m(!0),p(k,null,$([e(L),e(V),e(y),e(T),e(g),e(P),e(w),e(R),e(O)],(_,S)=>(m(),p("div",{key:S},[(m(),f(x(_)))]))),128))],64))}});export{z as default};