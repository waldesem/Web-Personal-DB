const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=["./DropDownHead-DaJRNVph.js","./index-D-dL7D6l.js","./index-BqKjTnG4.css","./ActionIcons-HH4Thdt8.js","./_plugin-vue_export-helper-DlAUqK2U.js","./ActionIcons-CukUJdTR.css","./RelationForm-B8R2M1vj.js","./state-aOZCxFm5.js","./LabelSlot-UyefIB2q.js","./LabelSlot-BMshfUVW.css"])))=>i.map(i=>d[i]);
import{d as C,r as u,n as L,o,c as r,b as a,u as e,e as R,F as b,A as S,m as x,l as _,g as B,v as P,p as y,t as I,h as c,j as v}from"./index-D-dL7D6l.js";import{e as l,c as T}from"./state-aOZCxFm5.js";import{_ as $}from"./_plugin-vue_export-helper-DlAUqK2U.js";const w={class:"collapse card card-body mb-3",id:"relationer"},O={key:0},F={key:1},N={key:1},U=C({__name:"RelateDiv",setup(M){const A=c(()=>v(()=>import("./DropDownHead-DaJRNVph.js"),__vite__mapDeps([0,1,2]),import.meta.url)),E=c(()=>v(()=>import("./ActionIcons-HH4Thdt8.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),k=c(()=>v(()=>import("./RelationForm-B8R2M1vj.js"),__vite__mapDeps([6,1,2,7]),import.meta.url)),p=c(()=>v(()=>import("./LabelSlot-UyefIB2q.js"),__vite__mapDeps([8,1,2,4,9]),import.meta.url)),m=u(!1),s=u(!1),f=u(""),D=u({});function g(){s.value=!1,f.value="";const i=document.getElementById("relationer");i==null||i.setAttribute("class","collapse card card-body mb-3")}return(i,n)=>{const V=L("router-link");return o(),r(b,null,[a(e(A),{id:"relationer",header:"Связи"}),R("div",w,[a(e(k),{onCancel:g})]),e(l).anketa.relations.length?(o(),r("div",O,[(o(!0),r(b,null,S(e(l).anketa.relations,(t,h)=>(o(),r("div",{key:h,class:"card card-body mb-3",onMouseover:n[1]||(n[1]=d=>m.value=!0),onMouseout:n[2]||(n[2]=d=>m.value=!1)},[s.value&&f.value==t.id.toString()?(o(),x(e(k),{key:0,relation:D.value,onCancel:n[0]||(n[0]=d=>s.value=!s.value)},null,8,["relation"])):(o(),r("div",F,[a(e(p),null,{default:_(()=>[B(a(e(E),{onDelete:d=>e(l).deleteItem(t.id.toString(),"relations"),onUpdate:d=>{D.value=t,f.value=t.id.toString(),s.value=!0},hide:!0},null,8,["onDelete","onUpdate"]),[[P,m.value&&e(l).anketa.persons.user_id==e(T).user.userId&&e(l).anketa.persons.standing]])]),_:2},1024),a(e(p),{label:"Тип"},{default:_(()=>[y(I(t.relation),1)]),_:2},1024),a(e(p),{label:"Связь"},{default:_(()=>[a(V,{to:{name:"profile",params:{id:t.relation_id}}},{default:_(()=>[y(" ID #"+I(t.relation_id),1)]),_:2},1032,["to"])]),_:2},1024)]))],32))),128))])):(o(),r("p",N,"Данные отсутствуют"))],64)}}}),z=$(U,[["__scopeId","data-v-c624d83a"]]);export{z as default};
