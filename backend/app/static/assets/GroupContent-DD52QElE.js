import{d as c,o as t,c as n,y as s,t as a,B as r,F as m}from"./index-BCJo_gEN.js";const b=c({__name:"GroupContent",props:{subclass:{type:String,default:"outline"},submitNeeds:{type:Boolean,default:!0},submitBtn:{type:String,default:"Принять"},resetNeeds:{type:Boolean,default:!0},resetBtn:{type:String,default:"Очистить"},cancelNeeds:{type:Boolean,default:!0},cancelBtn:{type:String,default:"Отмена"}},emits:["cancel"],setup(o,{emit:i}){const e=o;return(u,l)=>(t(),n(m,null,[e.submitNeeds?(t(),n("button",{key:0,class:s(["btn btn-md d-print-none",`btn-${e.subclass}-primary`]),name:"submit",type:"submit"},a(e.submitBtn),3)):r("",!0),e.resetNeeds?(t(),n("button",{key:1,class:s(["btn btn-md d-print-none",`btn-${e.subclass}-danger`]),name:"reset",type:"reset"},a(e.resetBtn),3)):r("",!0),e.cancelNeeds?(t(),n("button",{key:2,class:s(["btn btn-md d-print-none",`btn-${e.subclass}-secondary`]),name:"cancel",type:"button",onClick:l[0]||(l[0]=d=>u.$emit("cancel"))},a(e.cancelBtn),3)):r("",!0)],64))}});export{b as default};
