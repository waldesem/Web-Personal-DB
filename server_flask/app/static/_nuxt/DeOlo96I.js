import{f as i,o as m,c as l,m as r,s as c,a as p,n as f}from"./BLczYTEp.js";const d=["id","name","accept"],_=i({__name:"FileForm",props:{accept:String,nameId:{type:String,default:"file"},display:{type:Boolean,default:!1}},emits:["submit"],setup(a,{emit:s}){const e=a,o=s;return(u,t)=>(m(),l("form",{class:"form form-check",onChange:t[0]||(t[0]=n=>o("submit",n)),enctype:"multipart/form-data"},[r(p("input",{class:f(["form-control form-control-sm",e.display?"visible":"hidden"]),id:e.nameId,name:e.nameId,type:"file",accept:e.accept,ref:"file",multiple:""},null,10,d),[[c,e.display]])],32))}});export{_};
