import{d,o as c,c as r,a as t,D as p}from"./index-K0Y79g34.js";const _={class:"position-relative d-print-none"},u={class:"position-absolute top-0 end-0"},b=t("i",{class:"bi bi-pencil-square"},null,-1),f=[b],h=t("i",{class:"bi bi-trash"},null,-1),m=[h],k=["for","hidden"],v=t("a",{class:"btn btn-link",title:"Загрузить"},[t("i",{class:"bi bi-cloud-arrow-up-fill"})],-1),B=[v],I=d({__name:"ActionIcons",props:{hide:{type:Boolean,default:!1},forInput:{type:String,default:"file"}},emits:["delete","update"],setup(n,{emit:i}){const s=i,o=n;return(l,e)=>(c(),r("div",_,[t("div",u,[t("a",{class:"btn btn-link",title:"Изменить",onClick:e[0]||(e[0]=a=>s("update"))},f),t("a",{class:"btn btn-link",title:"Удалить",onClick:e[1]||(e[1]=a=>s("delete"))},m),t("label",{for:o.forInput,hidden:o.hide},B,8,k),p(l.$slots,"default")])]))}});export{I as default};
