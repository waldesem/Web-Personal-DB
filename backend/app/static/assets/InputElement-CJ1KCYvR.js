import{d as m,E as r,G as p,o as n,c as s,q as c,L as f,a as y,F as d,r as g,B as v}from"./index-BCJo_gEN.js";const S=["id","name","type","max","required","disabled","pattern","placeholder","list"],b=["id"],x=["value"],h=m({__name:"InputElement",props:r({name:String,place:String,lst:{type:String,default:""},selects:{type:Array,default:[]},typeof:{type:String,default:"text"},need:{type:Boolean,default:!1},disable:{type:Boolean,default:!1},max:{type:[String,Number],default:t=>t.typeof==="date"?new Date().toISOString().split("T")[0]:"255"},pattern:{type:String,default:".*"}},{modelValue:{},modelModifiers:{}}),emits:r(["submit-data"],["update:modelValue"]),setup(t,{emit:i}){const u=i,o=p(t,"modelValue"),e=t;return(B,a)=>(n(),s(d,null,[c(y("input",{class:"form-control",id:e.name,name:e.name,type:e.typeof,max:e.max,required:e.need,disabled:e.disable,pattern:e.pattern,placeholder:e.place,list:e.lst,"onUpdate:modelValue":a[0]||(a[0]=l=>o.value=l),onChange:a[1]||(a[1]=l=>u("submit-data"))},null,40,S),[[f,o.value,void 0,{trim:!0,lazy:!0}]]),e.lst?(n(),s("datalist",{key:0,id:e.lst},[(n(!0),s(d,null,g(t.selects,l=>(n(),s("option",{value:l},null,8,x))),256))],8,b)):v("",!0)],64))}});export{h as default};
