const __vite__fileDeps=["./ActionIcons-B__oqcU7.js","./index-D2OLA4OR.js","./index-BqKjTnG4.css","./_plugin-vue_export-helper-DlAUqK2U.js","./ActionIcons-CukUJdTR.css","./FileForm-CFD10zx8.js","./FileForm-By8_2B11.css","./ResumeForm-B0kj5Tnj.js","./state-BHhWPIxB.js","./PreviousDiv-DD5Rojvu.js","./PreviousDiv-WXF32BgB.css","./EducationDiv-vUzN8Q21.js","./EducationDiv-D7RRw2ks.css","./StaffDiv-CazI4OAK.js","./StaffDiv-BIYzME-J.css","./DocumentDiv-CsAop55q.js","./DocumentDiv-B9bwHpEN.css","./AddressDiv-vmFjvpkw.js","./AddressDiv-Cs0vB29R.css","./ContactDiv-_68Og0D_.js","./ContactDiv-CQM2s3jM.css","./RelationDiv-BTAPQcRg.js","./RelationDiv-DV668zst.css","./WorkplaceDiv-B8AmZx3k.js","./WorkplaceDiv-Bh7TbgoK.css","./AffilationDiv-X2sy9eSg.js","./AffilationDiv-BjHgk6_s.css","./LabelSlot-Dfq8r-re.js","./LabelSlot-BKRWK_aH.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as C,r as S,o as d,c as p,b as a,u as e,l as o,g as v,v as c,p as r,t as s,m as f,f as g,F as k,A as F,q as U,h as i,j as l}from"./index-D2OLA4OR.js";import{f as t,e as $}from"./state-BHhWPIxB.js";const x={key:0,class:"card card-body mb-3"},j=C({__name:"AnketaTab",setup(h){const D=i(()=>l(()=>import("./ActionIcons-B__oqcU7.js"),__vite__mapDeps([0,1,2,3,4]),import.meta.url)),E=i(()=>l(()=>import("./FileForm-CFD10zx8.js"),__vite__mapDeps([5,1,2,3,6]),import.meta.url)),b=i(()=>l(()=>import("./ResumeForm-B0kj5Tnj.js"),__vite__mapDeps([7,1,2,8]),import.meta.url)),A=i(()=>l(()=>import("./PreviousDiv-DD5Rojvu.js"),__vite__mapDeps([9,1,2,8,3,10]),import.meta.url)),R=i(()=>l(()=>import("./EducationDiv-vUzN8Q21.js"),__vite__mapDeps([11,1,2,8,3,12]),import.meta.url)),I=i(()=>l(()=>import("./StaffDiv-CazI4OAK.js"),__vite__mapDeps([13,1,2,8,3,14]),import.meta.url)),L=i(()=>l(()=>import("./DocumentDiv-CsAop55q.js"),__vite__mapDeps([15,1,2,8,3,16]),import.meta.url)),T=i(()=>l(()=>import("./AddressDiv-vmFjvpkw.js"),__vite__mapDeps([17,1,2,8,3,18]),import.meta.url)),V=i(()=>l(()=>import("./ContactDiv-_68Og0D_.js"),__vite__mapDeps([19,1,2,8,3,20]),import.meta.url)),P=i(()=>l(()=>import("./RelationDiv-BTAPQcRg.js"),__vite__mapDeps([21,1,2,8,3,22]),import.meta.url)),O=i(()=>l(()=>import("./WorkplaceDiv-B8AmZx3k.js"),__vite__mapDeps([23,1,2,8,3,24]),import.meta.url)),y=i(()=>l(()=>import("./AffilationDiv-X2sy9eSg.js"),__vite__mapDeps([25,1,2,8,3,26]),import.meta.url)),n=i(()=>l(()=>import("./LabelSlot-Dfq8r-re.js"),__vite__mapDeps([27,1,2,3,28]),import.meta.url)),_=S({action:"",form:{},showActions:!1});return(B,u)=>(d(),p(k,null,[_.value.action?(d(),p("div",x,[a(e(b),{action:_.value.action,resume:e(t).anketa.persons,onCancel:u[0]||(u[0]=m=>_.value.action="")},null,8,["action","resume"])])):(d(),p("div",{key:1,class:"card card-body mb-3",onMouseover:u[4]||(u[4]=m=>_.value.showActions=!0),onMouseout:u[5]||(u[5]=m=>_.value.showActions=!1)},[a(e(n),null,{default:o(()=>[v(a(e(D),{onDelete:u[2]||(u[2]=m=>e(t).deleteItem(e(t).anketa.persons.id,"persons")),onUpdate:u[3]||(u[3]=m=>_.value.action="update"),"for-input":"persons-file"},{default:o(()=>[v(a(e(E),{"name-id":"persons-file",accept:"*",onSubmit:u[1]||(u[1]=m=>e(t).submitFile(m,"anketa",e(t).share.candId))},null,512),[[c,_.value.showActions]])]),_:1},512),[[c,_.value.showActions&&e(t).anketa.persons.user_id==e($).userId&&e(t).anketa.persons.standing]])]),_:1}),a(e(n),{label:"Фамилия"},{default:o(()=>[r(s(e(t).anketa.persons.surname),1)]),_:1}),a(e(n),{label:"Имя"},{default:o(()=>[r(s(e(t).anketa.persons.firstname),1)]),_:1}),a(e(n),{label:"Отчество"},{default:o(()=>[r(s(e(t).anketa.persons.patronymic),1)]),_:1}),a(e(n),{label:"Дата рождения"},{default:o(()=>[r(s(new Date(String(e(t).anketa.persons.birthday)).toLocaleDateString("ru-RU")),1)]),_:1}),a(e(n),{label:"Место рождения"},{default:o(()=>[r(s(e(t).anketa.persons.birthplace),1)]),_:1}),a(e(n),{label:"Гражданство"},{default:o(()=>[r(s(e(t).anketa.persons.citizenship),1)]),_:1}),e(t).anketa.persons.dual?(d(),f(e(n),{key:0,label:"Двойное гражданство"},{default:o(()=>[r(s(e(t).anketa.persons.dual),1)]),_:1})):g("",!0),a(e(n),{label:"СНИЛС"},{default:o(()=>[r(s(e(t).anketa.persons.snils),1)]),_:1}),a(e(n),{label:"ИНН"},{default:o(()=>[r(s(e(t).anketa.persons.inn),1)]),_:1}),a(e(n),{label:"Семейное положение"},{default:o(()=>[r(s(e(t).anketa.persons.marital),1)]),_:1}),a(e(n),{label:"Дата записи"},{default:o(()=>[r(s(e(t).anketa.persons.created?new Date(e(t).anketa.persons.created+" UTC").toLocaleString("ru-RU"):""),1)]),_:1}),a(e(n),{label:"Пользователь"},{default:o(()=>[r(s(e(t).anketa.persons.username?e(t).anketa.persons.username:""),1)]),_:1}),a(e(n),{label:"Материалы"},{default:o(()=>[r(s(e(t).anketa.persons.destination),1)]),_:1}),a(e(n),{label:"Дополнительная информация"},{default:o(()=>[r(s(e(t).anketa.persons.addition?e(t).anketa.persons.addition:"-"),1)]),_:1})],32)),(d(!0),p(k,null,F([e(I),e(R),e(O),e(L),e(T),e(V),e(y),e(A),e(P)],(m,w)=>(d(),p("div",{key:w},[(d(),f(U(m)))]))),128))],64))}});export{j as default};
