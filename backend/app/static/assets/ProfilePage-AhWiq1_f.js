const __vite__fileDeps=["./HeaderDiv-DTm--MTY.js","./index-1yFXvMEA.js","./index-BqKjTnG4.css","./PhotoCard-BfylffXt.js","./state-QybiP1xm.js","./_plugin-vue_export-helper-DlAUqK2U.js","./PhotoCard-4hLLjYeA.css","./AnketaTab-D0Sax4i5.js","./CheckTab-BLfszZB1.js","./CheckTab-DLW5DEVI.css","./PoligrafTab-4hsU78gD.js","./PoligrafTab-fC1nE4A4.css","./InvestigateTab-CmCdOO-d.js","./InvestigateTab-BqdYbyMq.css","./InquiryTab-R2WJqu_O.js","./InquiryTab-CMdrJt6g.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as A,k as D,r as C,c as r,b,u as e,e as s,f as k,F as u,z as p,B as V,o as n,A as v,t as x,m as L,q as O,h as i,j as l}from"./index-1yFXvMEA.js";import{h as t,c as R,b as $,f as B,e as f}from"./state-QybiP1xm.js";import{_ as j}from"./_plugin-vue_export-helper-DlAUqK2U.js";const q={class:"row mb-3"},w={class:"col-md-10"},N={class:"col-md-2 d-flex justify-content-end d-print-none"},z={key:0,class:"position-relative text-end"},F=["disabled"],H=["title","disabled","href"],M={class:"nav nav-tabs nav-justified",role:"tablist"},S=["data-bs-target","onClick"],U={class:"tab-content"},G=["id"],J=A({__name:"ProfilePage",setup(K){const g=i(()=>l(()=>import("./HeaderDiv-DTm--MTY.js"),__vite__mapDeps([0,1,2]),import.meta.url)),h=i(()=>l(()=>import("./PhotoCard-BfylffXt.js"),__vite__mapDeps([3,1,2,4,5,6]),import.meta.url)),T=i(()=>l(()=>import("./AnketaTab-D0Sax4i5.js"),__vite__mapDeps([7,1,2,4]),import.meta.url)),E=i(()=>l(()=>import("./CheckTab-BLfszZB1.js"),__vite__mapDeps([8,1,2,4,5,9]),import.meta.url)),I=i(()=>l(()=>import("./PoligrafTab-4hsU78gD.js"),__vite__mapDeps([10,1,2,4,5,11]),import.meta.url)),P=i(()=>l(()=>import("./InvestigateTab-CmCdOO-d.js"),__vite__mapDeps([12,1,2,4,5,13]),import.meta.url)),y=i(()=>l(()=>import("./InquiryTab-R2WJqu_O.js"),__vite__mapDeps([14,1,2,4,5,15]),import.meta.url));D(async()=>{const m=V();t.share.candId=m.params.id;try{const d=await R.get(`${$}/profile/${t.share.candId}`);[t.anketa.persons,t.anketa.previous,t.anketa.staffs,t.anketa.documents,t.anketa.addresses,t.anketa.contacts,t.anketa.educations,t.anketa.workplaces,t.anketa.affilations,t.anketa.relations,t.anketa.checks,t.anketa.investigations,t.anketa.poligrafs,t.anketa.inquiries]=d.data}catch(d){B(d)}});const c=C("anketaTab"),_={anketaTab:["Взять анкету","Анкета",T],checkTab:["Добавить проверку","Проверки",E],poligrafTab:["Добавить полиграф","Полиграф",I],investigateTab:["Добавить расследования","Расследования",P],inquiryTab:["Добавить запрос","Запросы",y]};return(m,d)=>(n(),r(u,null,[b(e(h)),s("div",q,[s("div",w,[b(e(g),{cls:"text-danger py-3","page-header":`${e(t).anketa.persons.surname} ${e(t).anketa.persons.firstname} ${e(t).anketa.persons.patronymic?" "+e(t).anketa.persons.patronymic:""}`},null,8,["page-header"])]),s("div",N,[c.value==="anketaTab"?(n(),r("div",z,[s("button",{type:"button",class:"btn btn-lg btn-outline-danger",title:"Взять анкету",onClick:d[0]||(d[0]=o=>e(t).getItem("persons","self")),disabled:e(t).anketa.persons.user_id==e(f).userId}," ≡ ",8,F)])):k("",!0),(n(!0),r(u,null,p(Object.keys(_).slice(1),(o,a)=>(n(),r("div",{key:a,class:"position-relative text-end"},[c.value===o?(n(),r("button",{key:0,title:_[c.value][0],type:"button",class:"btn btn-lg btn-outline-danger",disabled:e(t).anketa.persons.user_id!=e(f).userId,"data-bs-toggle":"collapse",href:"#"+o.split("T")[0]}," ≡ ",8,H)):k("",!0)]))),128))])]),s("nav",M,[(n(),r(u,null,p(_,(o,a)=>s("button",{key:a,class:v(["nav-link",{active:a==="anketaTab"}]),"data-bs-target":"#"+a,"data-bs-toggle":"tab",type:"button",role:"tab",onClick:Q=>c.value=a},x(o[1]),11,S)),64))]),s("div",U,[(n(),r(u,null,p(_,(o,a)=>s("div",{key:a,id:a,class:v(["tab-pane show fade pt-3",{active:a=="anketaTab"}]),role:"tabpanel"},[(n(),L(O(o[2])))],10,G)),64))])],64))}}),Z=j(J,[["__scopeId","data-v-66917351"]]);export{Z as default};
