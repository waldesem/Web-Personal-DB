const __vite__fileDeps=["./HeaderDiv-CE5d1A68.js","./index-D1GedQkO.js","./index-BqKjTnG4.css","./SelectDiv-tCS8aW-8.js","./InputElement-BVvBog7z.js","./TableSlots-vNQWibgY.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as E,r as S,k as I,c,b as s,u as o,m,A as k,e as t,F as g,o as _,q as A,t as p,B as w,h as i,j as d}from"./index-D1GedQkO.js";import{e as b,c as O,b as P,d as f}from"./state-z_tMSp-o.js";const T=t("tr",null,[t("th",{width:"45%"},"Решение"),t("th",null,"Количество")],-1),x={class:"row mb-3"},B=t("label",{class:"col-form-label col-md-1",for:"region"}," Регион: ",-1),C={class:"col-md-3"},L=t("label",{class:"col-form-label col-md-1",for:"start"}," Период: ",-1),R={class:"col-md-2"},U={class:"col-md-2"},M=E({__name:"InfoPage",setup($){const h=i(()=>d(()=>import("./HeaderDiv-CE5d1A68.js"),__vite__mapDeps([0,1,2]),import.meta.url)),V=i(()=>d(()=>import("./SelectDiv-tCS8aW-8.js"),__vite__mapDeps([3,1,2]),import.meta.url)),v=i(()=>d(()=>import("./InputElement-BVvBog7z.js"),__vite__mapDeps([4,1,2]),import.meta.url)),D=i(()=>d(()=>import("./TableSlots-vNQWibgY.js"),__vite__mapDeps([5,1,2]),import.meta.url)),u=new Date,e=S({region:b.region,checks:{},start:new Date(u.getFullYear(),u.getMonth(),1).toISOString().slice(0,10),end:u.toISOString().slice(0,10)});async function n(){try{const r=await O.get(`${P}/information`,{params:{start:e.value.start,end:e.value.end,region:e.value.region}});e.value.checks=r.data}catch(r){console.error(r)}}return I(async()=>{await n()}),(r,l)=>(_(),c(g,null,[s(o(h),{"page-header":`Статистика по региону ${e.value.region} 
            за период c ${e.value.start} по ${e.value.end} г.`},null,8,["page-header"]),s(o(D),{class:k("table table-hover table-responsive align-middle py-3")},{caption:m(()=>[A(p("Решения по кандидатам"))]),thead:m(()=>[T]),tbody:m(()=>[(_(!0),c(g,null,w(e.value.checks,(a,y)=>(_(),c("tr",{key:y},[t("td",null,p(a.conclusion),1),t("td",null,p(a.count),1)]))),128))]),_:1}),t("div",x,[B,t("div",C,[s(o(V),{place:"Регион",name:"region",select:o(f).regions,disable:o(b).region!=o(f).regions.main,modelValue:e.value.region,"onUpdate:modelValue":l[0]||(l[0]=a=>e.value.region=a),onSubmitData:n},null,8,["select","disable","modelValue"])]),L,t("div",R,[s(o(v),{name:"start",typeof:"date",modelValue:e.value.start,"onUpdate:modelValue":l[1]||(l[1]=a=>e.value.start=a),onSubmitData:n},null,8,["modelValue"])]),t("div",U,[s(o(v),{name:"end",typeof:"date",modelValue:e.value.end,"onUpdate:modelValue":l[2]||(l[2]=a=>e.value.end=a),onSubmitData:n},null,8,["modelValue"])])])],64))}});export{M as default};
