import{_ as f}from"./D0Q5Al_0.js";import{_ as d}from"./CIkW37UV.js";import{e as l}from"./BNoJJA1K.js";import{_ as h}from"./Bf7Arzfu.js";import{a as b}from"./Cthp-bJU.js";import{f as v,I as x,h as C,w as n,o as F,b as o,n as s}from"./BL57t9pv.js";import"./A1NmxWM6.js";import"./Yo-9r0Kq.js";const P=v({__name:"resume",setup(k){const r=x(),a=b();function c(){return s("/persons")}async function m(e){const{person_id:t}=await a("/api/resume",{method:"POST",body:e});return r.add({icon:"i-heroicons-check-circle",title:"Успешно",description:"Информация добавлена",color:"green"}),s("/profile/"+t)}return(e,t)=>{const i=f,_=d,p=l,u=h;return F(),C(u,null,{default:n(()=>[o(i,{div:"mb-6",header:"НОВАЯ АНКЕТА"}),o(p,null,{default:n(()=>[o(_,{onCancel:c,onUpdate:m})]),_:1})]),_:1})}}});export{P as default};
