import{d as u,E as n,G as c,q as p,H as f,o as s,c as l,F as b,r as v,t as g}from"./index-BCJo_gEN.js";const y=["disabled","required","id","name"],B=["value"],V=u({__name:"SelectDiv",props:n({name:String,need:{type:Boolean,default:!1},disable:{type:Boolean,default:!1},select:{type:Object,default:{}}},{modelValue:{},modelModifiers:{}}),emits:n(["submit-data"],["update:modelValue"]),setup(o,{emit:i}){const d=c(o,"modelValue"),r=i,e=o;return(M,a)=>p((s(),l("select",{onChange:a[0]||(a[0]=t=>r("submit-data")),class:"form-select",disabled:e.disable,required:e.need,id:e.name,name:e.name,"onUpdate:modelValue":a[1]||(a[1]=t=>d.value=t)},[(s(!0),l(b,null,v(e.select,(t,m)=>(s(),l("option",{key:m,value:t},g(t),9,B))),128))],40,y)),[[f,d.value,void 0,{lazy:!0}]])}});export{V as default};
