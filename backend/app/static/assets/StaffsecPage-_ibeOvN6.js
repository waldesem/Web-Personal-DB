const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=["./AlertMessage-kcm9e62j.js","./index-CuxALIEa.js","./index-QNw51pzy.css","./state-Dl_2yBjS.js"])))=>i.map(i=>d[i]);
import{d as v,k,c as b,e as t,b as a,l as s,u as l,m as r,f as g,t as x,F as w,i as y,n as _,o as c,p as i,q as C,s as S,x as F,h as I,j as E}from"./index-CuxALIEa.js";import{c as d}from"./state-Dl_2yBjS.js";import{_ as A}from"./_plugin-vue_export-helper-DlAUqK2U.js";const e=o=>(S("data-v-06bf083b"),o=o(),F(),o),N={class:"container-fluid row ps-3"},T={class:"col-2 d-print-none"},B={class:"navbar navbar-expand sticky-top fs-5 p-3"},P={class:"nav flex-column"},V=e(()=>t("a",{class:"nav-link text-danger fs-3 fw-bold"},"STAFFSEC FINTECH",-1)),D=e(()=>t("hr",{class:"text-info"},null,-1)),j=e(()=>t("hr",{class:"text-info"},null,-1)),H=e(()=>t("hr",{class:"text-info"},null,-1)),L=e(()=>t("hr",{class:"text-info"},null,-1)),M={class:"col-10",id:"staffsec"},U={class:"col-11"},q={class:"sticky-top bg-white d-print-none p-3"},O={class:"row"},R={class:"col-10 text-center"},$={class:"col-2 text-end"},z={class:"dropdown"},G={class:"btn btn-link btn-lg dropdown-toggle",style:{"text-decoration":"none"},role:"button","data-bs-toggle":"dropdown"},J=e(()=>t("div",{class:"col-1 d-print-none"},null,-1)),K=e(()=>t("footer",{id:"footer",class:"d-flex justify-content-center border-top bg-white d-print-none"},[t("p",{class:"text-muted mt-2"},"© 2024 STAFFSEC FINTECH")],-1)),Q=v({__name:"StaffsecPage",setup(o){const u=I(()=>E(()=>import("./AlertMessage-kcm9e62j.js"),__vite__mapDeps([0,1,2,3]),import.meta.url));k(async()=>{await d.getCurrentUser()});async function p(){localStorage.removeItem("user_token"),y.push({name:"login"})}return(f,W)=>{const n=_("router-link"),m=_("router-view");return c(),b(w,null,[t("div",N,[t("div",T,[t("div",B,[t("div",P,[V,D,a(n,{to:{name:"persons"},class:"nav-link active"},{default:s(()=>[i(" Кандидаты ")]),_:1}),j,a(n,{to:{name:"resume"},class:"nav-link active"},{default:s(()=>[i(" Создать ")]),_:1}),H,a(n,{to:{name:"information"},class:"nav-link active"},{default:s(()=>[i(" Информация ")]),_:1}),L,l(d).user.hasAdmin?(c(),r(n,{key:0,to:{name:"users"},class:"nav-link active"},{default:s(()=>[i(" Пользователи ")]),_:1})):g("",!0)])])]),t("div",M,[t("div",U,[t("div",q,[t("div",O,[t("div",R,[a(l(u))]),t("div",$,[t("div",z,[t("button",G," ✪ "+x(l(d).user.username),1),t("ul",{class:"dropdown-menu"},[t("li",{class:"dropdown-item"},[t("a",{class:"link-opacity-50-hover",href:"#",onClick:p}," Выход ")])])])])])]),(c(),r(m,{key:f.$route.fullPath},{default:s(({Component:h})=>[(c(),r(C(h)))]),_:1}))]),J])]),K],64)}}}),tt=A(Q,[["__scopeId","data-v-06bf083b"]]);export{tt as default};