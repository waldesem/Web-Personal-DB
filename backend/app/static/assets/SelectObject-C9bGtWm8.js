import{d as u,P as d,Q as c,t as p,R as v,o as s,c as o,F as f,x as g,C as b}from"./index-BhT_3F5B.js";const M=["id","name"],S=["value"],x=u({__name:"SelectObject",props:d({name:String,select:{type:Object,default:{}}},{modelValue:{},modelModifiers:{}}),emits:d(["submit-data"],["update:modelValue"]),setup(l,{emit:i}){const n=c(l,"modelValue"),r=i,a=l;return(V,e)=>p((s(),o("select",{onChange:e[0]||(e[0]=t=>r("submit-data")),class:"form-select",id:a.name,name:a.name,"onUpdate:modelValue":e[1]||(e[1]=t=>n.value=t)},[(s(!0),o(f,null,g(a.select,(t,m)=>(s(),o("option",{key:m,value:m},b(t),9,S))),128))],40,M)),[[v,n.value,void 0,{lazy:!0}]])}});export{x as default};
