import{_ as h}from"./CLw5YCjI.js";import{_ as x}from"./BqwW0LnQ.js";import{_ as S,a as y}from"./B7F370T9.js";import{_ as V}from"./jOVDlQnc.js";import{a as w,s as D,b as U,u as k}from"./C7PE2IGf.js";import{g as $,r as C,h as F,i as z,w as l,o as B,a as o,b as s,t as I,j as e}from"./BPBLQG6i.js";import"./DgIFj23g.js";import"./7ab4JJky.js";import"./C85h92ts.js";const O={class:"my-14"},j={class:"text-left"},A={class:"flex grid grid-cols-12 gap-3 mt-4"},M={class:"col-span-2"},N={class:"flex col-span-2"},G={class:"px-3"},L={class:"px-3"},W=$({__name:"info",async setup(T){let _,m;const u=w(),d=D(),r=new Date,t=C({region:d.user.value.region,checks:[],start:new Date(r.getFullYear(),r.getMonth(),1).toISOString().slice(0,10),end:r.toISOString().slice(0,10)});async function i(){const p=k();t.value.checks=await p(`${U}/information`,{params:{start:t.value.start,end:t.value.end,region:t.value.region}})}return[_,m]=F(()=>i()),await _,m(),(p,a)=>{const g=h,v=x,c=S,f=y,b=V;return B(),z(b,null,{default:l(()=>[o("div",O,[s(g,{rows:e(t).checks,columns:["Решение","Количество"]},{caption:l(()=>[o("caption",j,I(`Информация по региону ${e(t).region} 
            за период c ${e(t).start} по ${e(t).end} г.`),1)]),_:1},8,["rows"]),o("div",A,[o("div",M,[s(c,{class:"mb-3",size:"md",label:"Регион"},{default:l(()=>[s(v,{modelValue:e(t).region,"onUpdate:modelValue":a[0]||(a[0]=n=>e(t).region=n),disable:e(d).user.value.region!=e(u).classes.value.regions.main,options:Object.values(e(u).classes.value.regions),onSubmitData:i},null,8,["modelValue","disable","options"])]),_:1})]),o("div",N,[o("div",G,[s(c,{size:"md",label:"Начало периода"},{default:l(()=>[s(f,{modelValue:e(t).start,"onUpdate:modelValue":a[1]||(a[1]=n=>e(t).start=n),type:"date",onSubmitData:i},null,8,["modelValue"])]),_:1})]),o("div",L,[s(c,{size:"md",label:"Конец периода"},{default:l(()=>[s(f,{modelValue:e(t).end,"onUpdate:modelValue":a[2]||(a[2]=n=>e(t).end=n),type:"date",onSubmitData:i},null,8,["modelValue"])]),_:1})])])])])]),_:1})}}});export{W as default};
