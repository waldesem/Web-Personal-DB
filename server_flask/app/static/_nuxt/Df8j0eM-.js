import{_ as U,a as Y}from"./F1l9jR7M.js";import{_ as k}from"./C5nlZ-H6.js";import{_ as D}from"./BhVxa_ul.js";import{_ as F}from"./DOviaxzH.js";import{d as M,r,u as g,a as y,w as $,c as A,b as o,e,f as t,g as _,o as B,i as d}from"./DfFwspTN.js";import{u as C}from"./Bg7MONkg.js";import{u as N}from"./CSnMaNkz.js";import{a as S}from"./CifMPHan.js";import"./BY5lPLn4.js";import"./DfMykkUP.js";const E={class:"my-8"},z={class:"flex grid grid-cols-12 gap-3 mt-8"},G={class:"col-span-2"},H={class:"col-span-2"},I={class:"px-3"},L={class:"col-span-2"},R={class:"px-3"},oe=M({__name:"info",async setup(T){let c,m;const h=C(),p=N(),s=r(p.value.region),a=r(g(y(),"YYYY-MM").value+"-01"),n=r(g(y(),"YYYY-MM-DD").value),f=r([]),{status:b}=([c,m]=$(async()=>S("stats",async()=>{f.value=await h("/api/information",{params:{start:a.value,end:n.value,region:s.value}})},{watch:[s,a,n]})),c=await c,m(),c);return(j,l)=>{const x=U,V=k,w=D,u=F,v=Y;return B(),A("div",null,[o(x,{div:"py-1",header:`Информация по региону ${e(s)} за период с ${e(a)} г. по ${e(n)} г.`},null,8,["header"]),t("div",E,[o(V,{loading:e(b)=="pending",progress:{color:"red",animation:"swing"},"empty-state":{icon:"i-heroicons-circle-stack-20-solid",label:"Статистика за указанный период отсутствует."},rows:e(f),columns:[{key:"conclusion",label:"Решение"},{key:"count",label:"Количество"}]},null,8,["loading","rows"]),t("div",z,[t("div",G,[o(u,{class:"mb-3",label:"Регион"},{default:_(()=>[o(w,{modelValue:e(s),"onUpdate:modelValue":l[0]||(l[0]=i=>d(s)?s.value=i:null),disabled:e(p).region!="Главный офис",options:["Главный офис","РЦ Юг","РЦ Запад","РЦ Урал","РЦ Восток"]},null,8,["modelValue","disabled"])]),_:1})]),t("div",H,[t("div",I,[o(u,{label:"Начало периода"},{default:_(()=>[o(v,{modelValue:e(a),"onUpdate:modelValue":l[1]||(l[1]=i=>d(a)?a.value=i:null),type:"date"},null,8,["modelValue"])]),_:1})])]),t("div",L,[t("div",R,[o(u,{label:"Конец периода"},{default:_(()=>[o(v,{modelValue:e(n),"onUpdate:modelValue":l[2]||(l[2]=i=>d(n)?n.value=i:null),type:"date"},null,8,["modelValue"])]),_:1})])])])])])}}});export{oe as default};
