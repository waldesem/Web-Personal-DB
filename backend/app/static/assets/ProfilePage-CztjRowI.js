const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=["./HeaderDiv-ClbpCabr.js","./index-BZDug3Gw.js","./index-BqKjTnG4.css","./PhotoCard-Cxjemae2.js","./state-Cwn6w3yA.js","./_plugin-vue_export-helper-DlAUqK2U.js","./PhotoCard-BGhN6_01.css","./AnketaTab-Yz-54NCf.js","./CheckTab-5iaTnyPd.js","./CheckTab-CbxqQTAA.css","./PoligrafTab-BHZJ0BWZ.js","./PoligrafTab-BX_LjGnk.css","./InvestigateTab-CCDRBzzk.js","./InvestigateTab-BtSqIIwH.css","./InquiryTab-BlBTWiVG.js","./InquiryTab-BHA1DXWu.css"])))=>i.map(i=>d[i]);
import{d as D,k as V,r as O,c as r,b as h,u as s,e as n,F as u,A as b,z as v,B as w,o,f as L,t as R,m as x,q as B,h as c,j as l}from"./index-BZDug3Gw.js";import{e as t,d as $,b as j,c as N}from"./state-Cwn6w3yA.js";const q={class:"row mb-3"},z={class:"col-md-10"},F={class:"col-md-2 d-flex justify-content-end d-print-none"},S=["title","href"],H={class:"position-relative px-3"},K=["title"],M={key:0,class:"spinner-grow text-danger",role:"status"},U={key:1},G={class:"nav nav-tabs nav-justified d-print-none",role:"tablist"},J=["data-bs-target","onClick"],Q={class:"tab-content"},W=["id"],tt=D({__name:"ProfilePage",setup(X){const k=c(()=>l(()=>import("./HeaderDiv-ClbpCabr.js"),__vite__mapDeps([0,1,2]),import.meta.url)),f=c(()=>l(()=>import("./PhotoCard-Cxjemae2.js"),__vite__mapDeps([3,1,2,4,5,6]),import.meta.url)),T=c(()=>l(()=>import("./AnketaTab-Yz-54NCf.js"),__vite__mapDeps([7,1,2,4]),import.meta.url)),y=c(()=>l(()=>import("./CheckTab-5iaTnyPd.js"),__vite__mapDeps([8,1,2,4,5,9]),import.meta.url)),E=c(()=>l(()=>import("./PoligrafTab-BHZJ0BWZ.js"),__vite__mapDeps([10,1,2,4,5,11]),import.meta.url)),A=c(()=>l(()=>import("./InvestigateTab-CCDRBzzk.js"),__vite__mapDeps([12,1,2,4,5,13]),import.meta.url)),C=c(()=>l(()=>import("./InquiryTab-BlBTWiVG.js"),__vite__mapDeps([14,1,2,4,5,15]),import.meta.url));V(async()=>{const i=w();t.share.candId=i.params.id;try{const a=(await $.get(`${j}/profile/${t.share.candId}`)).data,e=Object.keys(t.anketa);for(let _=0;_<e.length;_++)t.anketa[e[_]]=a[_]}catch(d){console.error(d)}});const m=O("anketaTab"),p={anketaTab:["Взять анкету","Анкета",T],checkTab:["Добавить проверку","Проверки",y],poligrafTab:["Добавить полиграф","Полиграф",E],investigateTab:["Добавить расследования","Расследования",A],inquiryTab:["Добавить запрос","Запросы",C]};async function g(){var d;const i=document.getElementsByClassName("collapse");for(let a=0;a<i.length;a++)(d=i[a])==null||d.setAttribute("class","collapse card card-body mb-3")}async function I(){await g(),t.getItem("persons","self")}async function P(i){await g(),m.value=i}return(i,d)=>(o(),r(u,null,[h(s(f)),n("div",q,[n("div",z,[h(s(k),{cls:"text-danger py-3","page-header":`${s(t).anketa.persons.surname} ${s(t).anketa.persons.firstname} ${s(t).anketa.persons.patronymic?" "+s(t).anketa.persons.patronymic:""}`},null,8,["page-header"])]),n("div",F,[(o(!0),r(u,null,b(Object.keys(p).slice(1),(a,e)=>(o(),r("div",{key:e,class:"position-relative"},[m.value==a&&s(t).anketa.persons.user_id==s(N).user.userId&&s(t).anketa.persons.standing?(o(),r("button",{key:0,title:p[m.value][0],type:"button",class:"btn btn-lg btn-outline-danger","data-bs-toggle":"collapse",href:"#clps_"+a.split("T")[0]}," ≡ ",8,S)):L("",!0)]))),128)),n("div",H,[n("button",{type:"button",class:v(s(t).anketa.persons.standing?"btn btn-link":"btn btn-lg btn-outline-primary"),title:s(t).anketa.persons.standing?"Отключить режим проверки":"Включить режим проверки",onClick:I},[s(t).anketa.persons.standing?(o(),r("span",M)):(o(),r("div",U,"≡"))],10,K)])])]),n("nav",G,[(o(),r(u,null,b(p,(a,e)=>n("button",{key:e,class:v(["nav-link",{active:e==="anketaTab"}]),"data-bs-target":"#"+e,"data-bs-toggle":"tab",type:"button",role:"tab",onClick:_=>P(e)},R(a[1]),11,J)),64))]),n("div",Q,[(o(),r(u,null,b(p,(a,e)=>n("div",{key:e,id:e,class:v(["tab-pane show fade pt-3",{active:e=="anketaTab"}]),role:"tabpanel"},[(o(),x(B(a[2])))],10,W)),64))])],64))}});export{tt as default};
