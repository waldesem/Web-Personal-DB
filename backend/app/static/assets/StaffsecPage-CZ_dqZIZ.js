const __vite__fileDeps=["./AlertMessage-CVZBkBai.js","./state-u74uZLPD.js","./index-D1U1a8b2.js","./index-BqKjTnG4.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as x,k as w,i as m,c as b,e as s,b as r,l as a,u as _,m as u,f as y,t as S,n as f,o as l,p as d,q as C,s as I,x as A,h as B,j as P}from"./index-D1U1a8b2.js";import{c as V,b as E,d as e,e as c}from"./state-u74uZLPD.js";import{_ as N}from"./_plugin-vue_export-helper-DlAUqK2U.js";const o=i=>(I("data-v-a60b39d0"),i=i(),A(),i),T={class:"container-fluid row px-3"},D={class:"col-2 d-print-none"},M={class:"navbar navbar-expand sticky-top fs-5 p-3"},F={class:"nav flex-column"},L=o(()=>s("a",{class:"nav-link text-danger fs-3 fw-bold"},"STAFFSEC - MTS Bank",-1)),$=o(()=>s("hr",{class:"text-info"},null,-1)),j=o(()=>s("hr",{class:"text-info"},null,-1)),q=o(()=>s("hr",{class:"text-info"},null,-1)),O=o(()=>s("hr",{class:"text-info"},null,-1)),R={class:"col-9",id:"staffsec"},U={class:"sticky-top bg-white d-print-none p-3"},z={class:"row"},G={class:"col-10 text-center"},H={class:"col-2 text-end"},J={class:"dropdown"},K={class:"btn btn-link btn-lg dropdown-toggle",style:{"text-decoration":"none"},role:"button","data-bs-toggle":"dropdown"},Q=o(()=>s("div",{class:"col-1 d-print-none"},null,-1)),W=x({__name:"StaffsecPage",setup(i){const h=B(()=>P(()=>import("./AlertMessage-CVZBkBai.js"),__vite__mapDeps([0,1,2,3]),import.meta.url));w(async()=>{try{const n=await V.get(`${E}/classes`);[e.regions,e.standing,e.conclusions,e.relations,e.affilations,e.educations,e.addresses,e.contacts,e.documents,e.poligrafs]=n.data;const p=localStorage.getItem("user_token"),t=window.atob(p).split(":");c.userId=t[1],c.username=t[2],c.hasAdmin=t[3]=="1",m.push({name:"persons"})}catch(n){console.error(n)}});async function v(){localStorage.removeItem("user_token"),m.push({name:"login"})}return(n,p)=>{const t=f("router-link"),k=f("router-view");return l(),b("div",T,[s("div",D,[s("div",M,[s("div",F,[L,$,r(t,{to:{name:"persons"},class:"nav-link active"},{default:a(()=>[d(" Кандидаты ")]),_:1}),j,r(t,{to:{name:"resume"},class:"nav-link active"},{default:a(()=>[d(" Создать ")]),_:1}),q,r(t,{to:{name:"information"},class:"nav-link active"},{default:a(()=>[d(" Информация ")]),_:1}),O,_(c).hasAdmin?(l(),u(t,{key:0,to:{name:"users"},class:"nav-link active"},{default:a(()=>[d(" Пользователи ")]),_:1})):y("",!0)])])]),s("div",R,[s("div",U,[s("div",z,[s("div",G,[r(_(h))]),s("div",H,[s("div",J,[s("button",K," ✪ "+S(_(c).username),1),s("ul",{class:"dropdown-menu"},[s("li",{class:"dropdown-item"},[s("a",{class:"link-opacity-50-hover",href:"#",onClick:v}," Выход ")])])])])])]),(l(),u(k,{key:n.$route.fullPath},{default:a(({Component:g})=>[(l(),u(C(g)))]),_:1}))]),Q])}}}),ss=N(W,[["__scopeId","data-v-a60b39d0"]]);export{ss as default};
