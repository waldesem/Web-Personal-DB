const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=["./DropDownHead-D_3exLLE.js","./index-CuxALIEa.js","./index-QNw51pzy.css","./ActionIcons-nL13gtqs.js","./_plugin-vue_export-helper-DlAUqK2U.js","./ActionIcons-CukUJdTR.css","./EducationForm-BybF9Hr1.js","./state-Dl_2yBjS.js","./LabelSlot-D4bqwlze.js","./LabelSlot-BMshfUVW.css"])))=>i.map(i=>d[i]);
import{d as V,r as u,o,c as n,b as a,u as e,e as L,F as I,z as S,m as w,l as r,g as x,v as B,p as c,t as _,h as v,j as p}from"./index-CuxALIEa.js";import{e as d,c as C}from"./state-Dl_2yBjS.js";import{_ as T}from"./_plugin-vue_export-helper-DlAUqK2U.js";const O={class:"collapse card card-body mb-3",id:"educationer"},P={key:0},R={key:1},$={key:1},F=V({__name:"EducateDiv",setup(N){const g=v(()=>p(()=>import("./DropDownHead-D_3exLLE.js"),__vite__mapDeps([0,1,2]),import.meta.url)),h=v(()=>p(()=>import("./ActionIcons-nL13gtqs.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),E=v(()=>p(()=>import("./EducationForm-BybF9Hr1.js"),__vite__mapDeps([6,1,2,7]),import.meta.url)),s=v(()=>p(()=>import("./LabelSlot-D4bqwlze.js"),__vite__mapDeps([8,1,2,4,9]),import.meta.url)),m=u(!1),f=u(""),b=u(!1),y=u({});function D(){b.value=!1,f.value="";const l=document.getElementById("educationer");l==null||l.setAttribute("class","collapse card card-body mb-3")}return(l,i)=>(o(),n(I,null,[a(e(g),{id:"educationer",header:"Образование"}),L("div",O,[a(e(E),{onCancel:D})]),e(d).anketa.educations.length?(o(),n("div",P,[(o(!0),n(I,null,S(e(d).anketa.educations,(t,A)=>(o(),n("div",{key:A,onMouseover:i[0]||(i[0]=k=>m.value=!0),onMouseout:i[1]||(i[1]=k=>m.value=!1),class:"card card-body mb-3"},[b.value&&f.value==t.id.toString()?(o(),w(e(E),{key:0,education:y.value,onCancel:D},null,8,["education"])):(o(),n("div",R,[a(e(s),null,{default:r(()=>[x(a(e(h),{onDelete:k=>e(d).deleteItem(t.id.toString(),"educations"),onUpdate:k=>{y.value=t,f.value=t.id.toString(),b.value=!0},hide:!0},null,8,["onDelete","onUpdate"]),[[B,m.value&&e(d).anketa.persons.user_id==e(C).user.userId&&e(d).anketa.persons.standing]])]),_:2},1024),a(e(s),{label:"Уровень образования"},{default:r(()=>[c(_(t.view),1)]),_:2},1024),a(e(s),{label:"Название учебного заведения"},{default:r(()=>[c(_(t.institution),1)]),_:2},1024),a(e(s),{label:"Год окончания"},{default:r(()=>[c(_(t.finished),1)]),_:2},1024),a(e(s),{label:"Специальность"},{default:r(()=>[c(_(t.specialty),1)]),_:2},1024)]))],32))),128))])):(o(),n("p",$,"Данные отсутствуют"))],64))}}),z=T(F,[["__scopeId","data-v-8561892c"]]);export{z as default};