import{d as c,o as i,c as n,y as a}from"./index-BCJo_gEN.js";import{_ as d}from"./_plugin-vue_export-helper-DlAUqK2U.js";const l=["title"],p=c({__name:"AscDesc",props:{sort:{type:String,default:"id"},order:{type:String,default:"desc"}},emits:["sort-candidates"],setup(s,{emit:o}){const r=o,e=s;return(m,t)=>(i(),n("i",{onClick:t[0]||(t[0]=_=>r("sort-candidates",e.sort,e.order)),title:e.order==="desc"?"Сортировка по убыванию":"Сортировка по возрастанию",class:a(["bi",e.order==="desc"?"bi-caret-down-fill":"bi-caret-up-fill"])},null,10,l))}}),b=d(p,[["__scopeId","data-v-e9d78873"]]);export{b as default};
