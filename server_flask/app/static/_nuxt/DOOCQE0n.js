import{b as y,_ as C,e as $,a as b}from"./BXUL-ZmB.js";import{_ as x}from"./BxRuhaE2.js";import{d as g,N as w,r as i,c as B,e,z as r,B as E,b as m,g as F,o as n,n as _}from"./DWkXyvYO.js";import{u as T}from"./DNvdZEfF.js";import"./Ck1huEKZ.js";import"./C05_pIlN.js";import"./CW3WTNyl.js";import"./b7Pa5xvB.js";const H=g({__name:"resume",setup(D){const c=w(),p=T(),o=i(!1),t=i({}),l=()=>_("/persons");async function u(s){t.value=s,o.value=!0;const{person_id:a}=await p("/api/resume",{method:"POST",body:s});if(c.add({icon:"i-heroicons-check-circle",title:"Успешно",description:"Информация добавлена",color:"green"}),o.value=!1,a)return _("/profile/"+a);c.add({icon:"i-heroicons-information-circle",title:"Внимание",description:"Невозможно выполнить действие",color:"red"})}return(s,a)=>{const d=$,f=x,h=b,v=C,k=y;return n(),B("div",null,[e(o)?(n(),r(d,{key:0,class:"h-44 w-44"})):E("",!0),m(f,{div:"mb-6",header:e(o)?`${e(t).surname} ${e(t).firstname} ${e(t).patronymic}`.toUpperCase():"НОВАЯ АНКЕТА"},null,8,["header"]),e(o)?(n(),r(h,{key:1,rows:16})):(n(),r(k,{key:2},{default:F(()=>[m(v,{onCancel:l,onUpdate:u})]),_:1}))])}}});export{H as default};
