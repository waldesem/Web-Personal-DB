const __vite__fileDeps=["./NavBar-DFfWRzGm.js","./_plugin-vue_export-helper-DlAUqK2U.js","./index-K0Y79g34.js","./index-6fGrG267.css","./MenuBar-ChwybZ5R.js","./state-CXEVWkFn.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as g,i as w,j as i,k as I,c as k,a as t,b as n,u as d,g as l,w as _,l as y,o as r,h as B,T as C,p as P,m as S,e as p,f as u}from"./index-K0Y79g34.js";import{a as c,b as x,c as E,d as e}from"./state-CXEVWkFn.js";import{_ as A}from"./_plugin-vue_export-helper-DlAUqK2U.js";const T=o=>(P("data-v-0cc285ad"),o=o(),S(),o),V={class:"container-fluid row px-3"},b={class:"col-2"},D={class:"col-9"},M=T(()=>t("div",{class:"col-1"},null,-1)),N=g({__name:"StaffsecPage",setup(o){const m=p(()=>u(()=>import("./NavBar-DFfWRzGm.js"),__vite__mapDeps([0,1,2,3]),import.meta.url)),f=p(()=>u(()=>import("./MenuBar-ChwybZ5R.js"),__vite__mapDeps([4,2,3,5]),import.meta.url));return w(()=>{const s=localStorage.getItem("user_token");s||i.push({name:"login"});const a=decodeURIComponent(escape(window.atob(s))).split(":");c.userId=a[1],c.username=a[2],c.hasAdmin=a[3]==="1"}),I(async()=>{try{const s=await x.get(`${E}/classes`);[e.regions,e.status,e.conclusions,e.relations,e.affilations,e.educations,e.addresses,e.contacts,e.documents,e.poligrafs]=s.data}catch(s){console.error(s)}i.push({name:"persons"})}),(s,a)=>{const v=y("router-view");return r(),k("div",V,[t("div",b,[n(d(m))]),t("div",D,[n(d(f)),(r(),l(v,{key:s.$route.fullPath},{default:_(({Component:h})=>[n(C,{name:"fade"},{default:_(()=>[t("div",null,[(r(),l(B(h)))])]),_:2},1024)]),_:1}))]),M])}}}),U=A(N,[["__scopeId","data-v-0cc285ad"]]);export{U as default};
