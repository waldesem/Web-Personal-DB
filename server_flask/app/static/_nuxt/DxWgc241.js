import{_ as y,a as w,b as x}from"./Cvx2MeBc.js";import{_ as V}from"./CLLHl9q7.js";import{_ as D}from"./_xYR8GxD.js";import{_ as S}from"./mt7KvKuW.js";import{a as U,s as C,b as k,u as $}from"./B_evGm4m.js";import{g as F,r as L,h as z,i as B,w as r,o as I,b as o,j as t,a}from"./DqpPj892.js";import"./08JNKZsB.js";import"./D06j80tp.js";import"./B-3zbiFr.js";const O={class:"my-8"},j={class:"flex grid grid-cols-12 gap-3 mt-8"},A={class:"col-span-2"},M={class:"col-span-2"},N={class:"px-3"},E={class:"col-span-2"},G={class:"px-3"},X=F({__name:"info",async setup(H){let _,d;const u=U(),m=C(),i=new Date,e=L({region:m.user.value.region,checks:[],start:new Date(i.getFullYear(),i.getMonth(),1).toISOString().slice(0,10),end:i.toISOString().slice(0,10)});async function l(){const p=$();e.value.checks=await p(`${k}/information`,{params:{start:e.value.start,end:e.value.end,region:e.value.region}})}return[_,d]=z(()=>l()),await _,d(),(p,s)=>{const f=y,v=V,h=D,c=w,g=x,b=S;return I(),B(b,null,{default:r(()=>[o(f,{div:"py-1",header:`Информация по региону ${t(e).region.toLocaleUpperCase()} за период с ${new Date(t(e).start).toLocaleDateString()} г. по ${new Date(t(e).end).toLocaleDateString()} г.`},null,8,["header"]),a("div",O,[o(v,{rows:t(e).checks,columns:[{key:"conclusion",label:"Решение"},{key:"count",label:"Количество"}]},null,8,["rows"]),a("div",j,[a("div",A,[o(c,{class:"mb-3",size:"md",label:"Регион"},{default:r(()=>[o(h,{modelValue:t(e).region,"onUpdate:modelValue":s[0]||(s[0]=n=>t(e).region=n),disable:t(m).user.value.region!=t(u).classes.value.regions.main,options:Object.values(t(u).classes.value.regions),onChange:l},null,8,["modelValue","disable","options"])]),_:1})]),a("div",M,[a("div",N,[o(c,{size:"md",label:"Начало периода"},{default:r(()=>[o(g,{modelValue:t(e).start,"onUpdate:modelValue":s[1]||(s[1]=n=>t(e).start=n),type:"date",onChange:l},null,8,["modelValue"])]),_:1})])]),a("div",E,[a("div",G,[o(c,{size:"md",label:"Конец периода"},{default:r(()=>[o(g,{modelValue:t(e).end,"onUpdate:modelValue":s[2]||(s[2]=n=>t(e).end=n),type:"date",onChange:l},null,8,["modelValue"])]),_:1})])])])])]),_:1})}}});export{X as default};
