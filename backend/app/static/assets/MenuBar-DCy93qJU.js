const __vite__fileDeps=["./AlertMessage-CXEiueLn.js","./state-s_e9P3m1.js","./utilities-BVKB9Dez.js","./index-Dx3HiUnq.js","./index-6fGrG267.css"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d,l as _,o as t,c as s,a as e,b as n,u as o,x as a,t as p,w as m,C as u,e as h,f,j as k}from"./index-Dx3HiUnq.js";import{a as r}from"./state-s_e9P3m1.js";import"./utilities-BVKB9Dez.js";const v={class:"d-print-none sticky-top bg-white p-3"},g={class:"row"},w={class:"col-10 text-center"},b={class:"col-2 text-end"},x={class:"dropdown"},y={class:"btn btn-link dropdown-toggle",role:"button","data-bs-toggle":"dropdown"},C=e("i",{class:"bi bi-person-circle fs-3"},null,-1),V={class:"dropdown-menu"},A={key:0,class:"dropdown-item"},M=d({__name:"MenuBar",setup(B){const c=h(()=>f(()=>import("./AlertMessage-CXEiueLn.js"),__vite__mapDeps([0,1,2,3,4]),import.meta.url));async function i(){localStorage.removeItem("user_token"),k.push({name:"login"})}return(N,E)=>{const l=_("router-link");return t(),s("div",v,[e("div",g,[e("div",w,[n(o(c))]),e("div",b,[e("div",x,[e("button",y,[a(p(o(r).username)+" ",1),C]),e("ul",V,[o(r).hasAdmin?(t(),s("li",A,[n(l,{to:{name:"users"},class:"link-opacity-50-hover"},{default:m(()=>[a(" Пользователи ")]),_:1})])):u("",!0),e("li",{class:"dropdown-item"},[e("a",{class:"link-opacity-50-hover",href:"#",onClick:i}," Выход ")])])])])])])}}});export{M as default};
