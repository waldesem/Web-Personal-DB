const __vite__fileDeps=["./HeaderDiv-DQMckfaw.js","./index-2fGtmyHu.js","./index-BGNnvclF.css","./PhotoCard-zUu9z_Wc.js","./state-BI0Epm2O.js","./utilities-DjwPzg-5.js","./_plugin-vue_export-helper-DlAUqK2U.js","./PhotoCard-4hLLjYeA.css","./AnketaTab-ChgE2Qb6.js","./CheckTab-CEdZHnYN.js","./CheckTab-BkNKSSNB.css","./PoligrafTab-FDVM1BUc.js","./PoligrafTab-ra3YAlfb.css","./InvestigateTab-LOCId6Fg.js","./InvestigateTab-ySyL4tIK.css","./InquiryTab-DEbg0_4w.js","./InquiryTab-CJkHK5BE.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as D,f as $,r as C,m as V,c as d,a as b,u as e,h as s,q as f,A as k,F as _,y as p,B as w,o as c,z as v,x,i as L,k as R,b as i,e as l}from"./index-2fGtmyHu.js";import{c as t,d as O,s as g}from"./state-BI0Epm2O.js";import{b as q,s as B}from"./utilities-DjwPzg-5.js";import{_ as j}from"./_plugin-vue_export-helper-DlAUqK2U.js";const z={class:"row mb-3"},F={class:"col-md-10"},N={class:"col-md-2 d-flex justify-content-end d-print-none"},S={class:"position-relative text-end flex-grow-1"},H=["disabled"],M=["title","disabled","href"],U={class:"nav nav-tabs nav-justified",role:"tablist"},G=["data-bs-target","onClick"],J={class:"tab-content"},K=["id"],Q=D({__name:"ProfilePage",setup(W){const h=i(()=>l(()=>import("./HeaderDiv-DQMckfaw.js"),__vite__mapDeps([0,1,2]),import.meta.url)),T=i(()=>l(()=>import("./PhotoCard-zUu9z_Wc.js"),__vite__mapDeps([3,1,2,4,5,6,7]),import.meta.url)),y=i(()=>l(()=>import("./AnketaTab-ChgE2Qb6.js"),__vite__mapDeps([8,1,2,4,5]),import.meta.url)),E=i(()=>l(()=>import("./CheckTab-CEdZHnYN.js"),__vite__mapDeps([9,1,2,4,5,6,10]),import.meta.url)),I=i(()=>l(()=>import("./PoligrafTab-FDVM1BUc.js"),__vite__mapDeps([11,1,2,4,5,6,12]),import.meta.url)),A=i(()=>l(()=>import("./InvestigateTab-LOCId6Fg.js"),__vite__mapDeps([13,1,2,4,5,6,14]),import.meta.url)),P=i(()=>l(()=>import("./InquiryTab-DEbg0_4w.js"),__vite__mapDeps([15,1,2,4,5,6,16]),import.meta.url));$(async()=>{const m=w();t.share.candId=m.params.id;try{const n=await q.get(`${B}/profile/${t.share.candId}`);[t.anketa.persons,t.anketa.previous,t.anketa.staffs,t.anketa.documents,t.anketa.addresses,t.anketa.contacts,t.anketa.educations,t.anketa.workplaces,t.anketa.affilations,t.anketa.relations,t.anketa.checks,t.anketa.investigations,t.anketa.poligrafs,t.anketa.inquiries]=n.data}catch(n){n.request.status==401||n.request.status==403?C.push({name:"login"}):(console.error(n),O.setAlert("alert-danger",`Ошибка: ${n}`))}});const u=V("anketaTab"),o=[["anketa","Взять анкету","Анкета",y],["check","Добавить проверку","Проверки",E],["poligraf","Добавить полиграф","Полиграф",I],["investigate","Добавить расследования","Расследования",A],["inquiry","Добавить запрос","Запросы",P]];return(m,n)=>(c(),d(_,null,[b(e(T)),s("div",z,[s("div",F,[b(e(h),{cls:"text-info py-3","page-header":`${e(t).anketa.persons.surname} ${e(t).anketa.persons.firstname} ${e(t).anketa.persons.patronymic?" "+e(t).anketa.persons.patronymic:""}`},null,8,["page-header"])]),s("div",N,[f(s("div",S,[s("button",{type:"button",class:"btn btn-lg btn-outline-info",title:"Взять анкету",onClick:n[0]||(n[0]=a=>e(t).getItem("persons","self")),disabled:e(t).anketa.persons.user_id==e(g).userId}," ≡ ",8,H)],512),[[k,u.value==o[0][0]+"Tab"]]),(c(!0),d(_,null,p(o.slice(1),(a,r)=>f((c(),d("div",{key:r,class:"position-relative text-end flex-grow-1"},[s("button",{title:a[1],type:"button",class:"btn btn-lg btn-outline-info",disabled:e(t).anketa.persons.user_id!=e(g).userId,"data-bs-toggle":"collapse",href:`#${a[0]}`}," ≡ ",8,M)])),[[k,u.value==a[0]+"Tab"]])),128))])]),s("nav",U,[(c(),d(_,null,p(o,(a,r)=>s("button",{key:r,class:v(["nav-link",{active:a[0]==o[0][0]}]),"data-bs-target":`#${o[r][0]}Tab`,"data-bs-toggle":"tab",type:"button",role:"tab",onClick:X=>u.value=o[r][0]+"Tab"},x(a[2]),11,G)),64))]),s("div",J,[(c(),d(_,null,p(o,(a,r)=>s("div",{key:r,id:o[r][0]+"Tab",class:v(["tab-pane show fade pt-3",{active:a[0]==o[0][0]}]),role:"tabpanel"},[(c(),L(R(a[4])))],10,K)),64))])],64))}}),at=j(Q,[["__scopeId","data-v-dfd0af82"]]);export{at as default};
