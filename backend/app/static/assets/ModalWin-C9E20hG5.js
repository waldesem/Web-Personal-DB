import{d as o,o as d,c as l,a as s,t as i,E as n,z as c}from"./index-BhwzwnLH.js";const r=["id"],m={class:"modal-content"},_={class:"modal-header"},b={class:"modal-title fs-5"},p=s("button",{type:"button",class:"btn-close","data-bs-dismiss":"modal","aria-label":"Close"},null,-1),f={class:"modal-body"},g=o({__name:"ModalWin",props:{id:String,title:String,size:{type:String,default:"modal-xl"}},setup(t){const a=t;return(e,u)=>(d(),l("div",{class:"modal fade","data-bs-backdrop":"static","data-bs-keyboard":"false",id:a.id,tabindex:"-1"},[s("div",{class:c(["modal-dialog modal-dialog-centered",a.size]),"data-bs-keyboard":"false",role:"document"},[s("div",m,[s("div",_,[s("h1",b,i(a.title),1),p]),s("div",f,[n(e.$slots,"default")])])],2)],8,r))}});export{g as default};