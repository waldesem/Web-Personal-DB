import{d as u,P as r,Q as c,t as p,R as f,o as s,c as o,F as v,x as y,C as g}from"./index-BhT_3F5B.js";const M=["id","name"],S=["value"],k=u({__name:"SelectArray",props:r({name:String,select:{type:Array,default:[]}},{modelValue:{},modelModifiers:{}}),emits:r(["submit-data"],["update:modelValue"]),setup(l,{emit:m}){const n=c(l,"modelValue"),d=m,a=l;return(V,t)=>p((s(),o("select",{onChange:t[0]||(t[0]=e=>d("submit-data")),class:"form-select",id:a.name,name:a.name,"onUpdate:modelValue":t[1]||(t[1]=e=>n.value=e)},[(s(!0),o(v,null,y(a.select,(e,i)=>(s(),o("option",{key:i,value:e},g(e),9,S))),128))],40,M)),[[f,n.value,void 0,{lazy:!0}]])}});export{k as default};
