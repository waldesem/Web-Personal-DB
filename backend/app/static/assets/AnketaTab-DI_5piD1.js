const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=["./PrevDiv-EqJhy6_G.js","./index-D-dL7D6l.js","./index-BqKjTnG4.css","./state-aOZCxFm5.js","./_plugin-vue_export-helper-DlAUqK2U.js","./PrevDiv-BdR9qNBc.css","./EducateDiv-DhCf2Piz.js","./EducateDiv-De-RMDFL.css","./StaffDiv-CTUtpFRw.js","./StaffDiv-D5boCRCx.css","./DocumDiv-D-w7Qvvf.js","./DocumDiv-C_j8sXc0.css","./AddressDiv-CWl5E_Ek.js","./AddressDiv-DWQ00uE8.css","./ContactDiv-BAOClgBF.js","./ContactDiv-Be9msH-k.css","./RelateDiv-C1ZTz5EK.js","./RelateDiv-BTrRPvtx.css","./WorkDiv-CF3eM6WZ.js","./WorkDiv-B4DLFT8m.css","./AffilDiv-B57dZ723.js","./AffilDiv-Bv0iXI5f.css","./ActionIcons-HH4Thdt8.js","./ActionIcons-CukUJdTR.css","./SelectDiv-CIb5_sD0.js","./FileForm-DSFlukZz.js","./ResumeForm-BCPHvF0p.js","./LabelSlot-UyefIB2q.js","./LabelSlot-BMshfUVW.css"])))=>i.map(i=>d[i]);
import{d as C,r as F,o as m,c as p,b as a,u as e,l as o,g as v,v as c,p as r,t as i,m as f,f as U,F as k,A as $,q as x,h as l,j as u}from"./index-D-dL7D6l.js";import{e as t,c as D,g as B}from"./state-aOZCxFm5.js";const N={key:0,class:"card card-body mb-3"},z=C({__name:"AnketaTab",setup(M){const E=l(()=>u(()=>import("./PrevDiv-EqJhy6_G.js"),__vite__mapDeps([0,1,2,3,4,5]),import.meta.url)),b=l(()=>u(()=>import("./EducateDiv-DhCf2Piz.js"),__vite__mapDeps([6,1,2,3,4,7]),import.meta.url)),A=l(()=>u(()=>import("./StaffDiv-CTUtpFRw.js"),__vite__mapDeps([8,1,2,3,4,9]),import.meta.url)),I=l(()=>u(()=>import("./DocumDiv-D-w7Qvvf.js"),__vite__mapDeps([10,1,2,3,4,11]),import.meta.url)),R=l(()=>u(()=>import("./AddressDiv-CWl5E_Ek.js"),__vite__mapDeps([12,1,2,3,4,13]),import.meta.url)),V=l(()=>u(()=>import("./ContactDiv-BAOClgBF.js"),__vite__mapDeps([14,1,2,3,4,15]),import.meta.url)),L=l(()=>u(()=>import("./RelateDiv-C1ZTz5EK.js"),__vite__mapDeps([16,1,2,3,4,17]),import.meta.url)),T=l(()=>u(()=>import("./WorkDiv-CF3eM6WZ.js"),__vite__mapDeps([18,1,2,3,4,19]),import.meta.url)),g=l(()=>u(()=>import("./AffilDiv-B57dZ723.js"),__vite__mapDeps([20,1,2,3,4,21]),import.meta.url)),P=l(()=>u(()=>import("./ActionIcons-HH4Thdt8.js"),__vite__mapDeps([22,1,2,4,23]),import.meta.url)),O=l(()=>u(()=>import("./SelectDiv-CIb5_sD0.js"),__vite__mapDeps([24,1,2]),import.meta.url)),y=l(()=>u(()=>import("./FileForm-DSFlukZz.js"),__vite__mapDeps([25,1,2]),import.meta.url)),w=l(()=>u(()=>import("./ResumeForm-BCPHvF0p.js"),__vite__mapDeps([26,1,2,3]),import.meta.url)),n=l(()=>u(()=>import("./LabelSlot-UyefIB2q.js"),__vite__mapDeps([27,1,2,4,28]),import.meta.url)),d=F({action:"",form:{},showActions:!1});return(h,s)=>(m(),p(k,null,[d.value.action?(m(),p("div",N,[a(e(w),{action:d.value.action,resume:e(t).anketa.persons,onCancel:s[0]||(s[0]=_=>{d.value.action="",e(t).getItem("persons")})},null,8,["action","resume"])])):(m(),p("div",{key:1,class:"card card-body mb-3",onMouseover:s[6]||(s[6]=_=>d.value.showActions=!0),onMouseout:s[7]||(s[7]=_=>d.value.showActions=!1)},[a(e(n),null,{default:o(()=>[v(a(e(P),{onDelete:s[2]||(s[2]=_=>e(t).deleteItem(e(t).anketa.persons.id,"persons")),onUpdate:s[3]||(s[3]=_=>d.value.action="update"),"for-input":"persons-file"},{default:o(()=>[v(a(e(y),{"name-id":"persons-file",accept:"*",onSubmit:s[1]||(s[1]=_=>e(t).submitFile(_,"anketa",e(t).share.candId))},null,512),[[c,d.value.showActions]])]),_:1},512),[[c,d.value.showActions&&e(t).anketa.persons.user_id==e(D).user.userId&&e(t).anketa.persons.standing]])]),_:1}),a(e(n),{label:"Регион"},{default:o(()=>[a(e(O),{width:"20%",name:"region",disable:e(D).user.userId!=e(t).anketa.persons.user_id||!e(t).anketa.persons.standing,select:e(B).classes.regions,modelValue:e(t).anketa.persons.region,"onUpdate:modelValue":s[4]||(s[4]=_=>e(t).anketa.persons.region=_),onSubmitData:s[5]||(s[5]=_=>e(t).changeRegion())},null,8,["disable","select","modelValue"])]),_:1}),a(e(n),{label:"Фамилия"},{default:o(()=>[r(i(e(t).anketa.persons.surname),1)]),_:1}),a(e(n),{label:"Имя"},{default:o(()=>[r(i(e(t).anketa.persons.firstname),1)]),_:1}),a(e(n),{label:"Отчество"},{default:o(()=>[r(i(e(t).anketa.persons.patronymic),1)]),_:1}),a(e(n),{label:"Дата рождения"},{default:o(()=>[r(i(new Date(String(e(t).anketa.persons.birthday)).toLocaleDateString("ru-RU")),1)]),_:1}),a(e(n),{label:"Место рождения"},{default:o(()=>[r(i(e(t).anketa.persons.birthplace),1)]),_:1}),a(e(n),{label:"Гражданство"},{default:o(()=>[r(i(e(t).anketa.persons.citizenship),1)]),_:1}),e(t).anketa.persons.dual?(m(),f(e(n),{key:0,label:"Двойное гражданство"},{default:o(()=>[r(i(e(t).anketa.persons.dual),1)]),_:1})):U("",!0),a(e(n),{label:"СНИЛС"},{default:o(()=>[r(i(e(t).anketa.persons.snils),1)]),_:1}),a(e(n),{label:"ИНН"},{default:o(()=>[r(i(e(t).anketa.persons.inn),1)]),_:1}),a(e(n),{label:"Семейное положение"},{default:o(()=>[r(i(e(t).anketa.persons.marital),1)]),_:1}),a(e(n),{label:"Дата записи"},{default:o(()=>[r(i(e(t).anketa.persons.created?new Date(e(t).anketa.persons.created+" UTC").toLocaleString("ru-RU"):""),1)]),_:1}),a(e(n),{label:"Пользователь"},{default:o(()=>[r(i(e(t).anketa.persons.username?e(t).anketa.persons.username:""),1)]),_:1}),a(e(n),{label:"Материалы"},{default:o(()=>[r(i(e(t).anketa.persons.destination),1)]),_:1}),a(e(n),{label:"Дополнительная информация"},{default:o(()=>[r(i(e(t).anketa.persons.addition?e(t).anketa.persons.addition:"-"),1)]),_:1})],32)),(m(!0),p(k,null,$([e(A),e(b),e(T),e(I),e(R),e(V),e(g),e(E),e(L)],(_,S)=>(m(),p("div",{key:S},[(m(),f(x(_)))]))),128))],64))}});export{z as default};
