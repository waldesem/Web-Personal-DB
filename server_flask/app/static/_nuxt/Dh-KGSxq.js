import{_ as D,a as S,b as x}from"./BaLSyn9W.js";import{_ as w}from"./CewLIM-l.js";import{_ as y}from"./CVAfITsI.js";import{_ as V}from"./C65ECaZ4.js";import{a as U,s as $,b as k,u as C}from"./CfpFGIXT.js";import{g as F,r as L,h as z,i as B,w as r,o as I,b as a,j as t,a as s}from"./BrjdBAS6.js";import"./DjPh29BU.js";import"./Cb9qdVfj.js";import"./8q6nTwcG.js";const O={class:"my-8"},j={class:"flex grid grid-cols-12 gap-3 mt-8"},A={class:"col-span-2"},M={class:"flex col-span-2"},N={class:"px-3"},E={class:"px-3"},W=F({__name:"info",async setup(G){let _,m;const u=U(),d=$(),i=new Date,e=L({region:d.user.value.region,checks:[],start:new Date(i.getFullYear(),i.getMonth(),1).toISOString().slice(0,10),end:i.toISOString().slice(0,10)});async function l(){const p=C();e.value.checks=await p(`${k}/information`,{params:{start:e.value.start,end:e.value.end,region:e.value.region}})}return[_,m]=z(()=>l()),await _,m(),(p,o)=>{const g=D,v=w,b=y,c=S,f=x,h=V;return I(),B(h,null,{default:r(()=>[a(g,{div:"py-1",header:`Информация по региону ${t(e).region.toLocaleUpperCase()} за период с ${new Date(t(e).start).toLocaleDateString()} г. по ${new Date(t(e).end).toLocaleDateString()} г.`},null,8,["header"]),s("div",O,[a(v,{rows:t(e).checks,columns:["Решение","Количество"]},null,8,["rows"]),s("div",j,[s("div",A,[a(c,{class:"mb-3",size:"md",label:"Регион"},{default:r(()=>[a(b,{modelValue:t(e).region,"onUpdate:modelValue":o[0]||(o[0]=n=>t(e).region=n),disable:t(d).user.value.region!=t(u).classes.value.regions.main,options:Object.values(t(u).classes.value.regions),onSubmitData:l},null,8,["modelValue","disable","options"])]),_:1})]),s("div",M,[s("div",N,[a(c,{size:"md",label:"Начало периода"},{default:r(()=>[a(f,{modelValue:t(e).start,"onUpdate:modelValue":o[1]||(o[1]=n=>t(e).start=n),type:"date",onSubmitData:l},null,8,["modelValue"])]),_:1})]),s("div",E,[a(c,{size:"md",label:"Конец периода"},{default:r(()=>[a(f,{modelValue:t(e).end,"onUpdate:modelValue":o[2]||(o[2]=n=>t(e).end=n),type:"date",onSubmitData:l},null,8,["modelValue"])]),_:1})])])])])]),_:1})}}});export{W as default};
