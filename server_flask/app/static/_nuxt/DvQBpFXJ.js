import{g as N,z as A,h as F,i as R,w as n,o as b,A as a,c as k,a as m,b as o,J as G,G as x,H as w,I as P,d as l,t as r,L as j,B as E,e as H,D as J,K as M}from"./B_4c7bjE.js";import{b as K,a as O,_ as q}from"./B8ZzhQbn.js";import{d as Q,_ as W}from"./CyAbWRfo.js";import{_ as X}from"./C6Jsogy6.js";import{_ as Y}from"./Ckh4YSd5.js";import{_ as Z}from"./B_ysnhc0.js";import{u as ee}from"./Cias7xHV.js";import{s as te,a as ae,b as $,c as ne}from"./DupJrylg.js";import"./CyEoj2gn.js";import"./B-pH45DD.js";import"./HQhQkk_r.js";const oe={key:0,class:"relative"},se={class:"my-6"},ie={class:"caption-bottom text-left"},le={key:1,class:"grid place-items-center py-8"},ve=N({__name:"persons",async setup(re){let c,f;const g=ne(),D=te(),U=ae(),t=A({candidates:[],page:1,prev:!1,next:!0,search:"",updated:`${new Date().toLocaleDateString("ru-RU")} в ${new Date().toLocaleTimeString("ru-RU")}`}),{refresh:d,status:y}=([c,f]=F(async()=>ee("candidates",async()=>{if(t.value.page<1){t.value.page=1;return}const i=await g(`${$}/index/${t.value.page}`,{params:{search:t.value.search}});[t.value.candidates,t.value.next,t.value.prev]=i,t.value.updated=`${new Date().toLocaleDateString("ru-RU")} в ${new Date().toLocaleTimeString("ru-RU")}`})),c=await c,f(),c),C=Q(async()=>{await d()},500),v=async(i=1)=>{t.value.page=i,await d()};async function S(i){const s=j();if(!i.length){s.add({icon:"i-heroicons-exclamation-triangle",title:"Внимание",description:"Файлы не выбраны",color:"red"});return}const p=new FormData;for(const _ of i)p.append("file",_);const u=await g(`${$}/file/persons/0`,{method:"POST",body:p});console.log(u),s.add({icon:"i-heroicons-check-circle",title:"Информация",description:"Файлы успешно загружены",color:"green"}),await d()}return(i,s)=>{const p=E,u=K,_=O,L=q,B=H,V=W,h=J,z=X,T=Y,I=Z;return b(),R(I,null,{default:n(()=>[a(U).role==a(D).classes.value.roles.user?(b(),k("div",oe,[m("div",{class:x(["absolute inset-y-0 right-0",{"animate-pulse":a(y)=="pending"}]),title:"Загрузить json"},[o(_,{class:"mb-3",size:"md"},{label:n(()=>[o(p,{name:"i-heroicons-cloud-arrow-up",class:"w-8 h-8",style:{cursor:"pointer",color:"dodgerblue"}})]),default:n(()=>[G(o(u,{type:"file",accept:".json",multiple:"",onChange:s[0]||(s[0]=e=>S(e))},null,512),[[M,!1]])]),_:1})],2)])):w("",!0),o(L,{header:"КАНДИДАТЫ"}),m("div",se,[o(u,{modelValue:a(t).search,"onUpdate:modelValue":s[1]||(s[1]=e=>a(t).search=e),placeholder:"поиск по фамилии, имени, отчеству, дате рождения или инн",size:"lg",onInput:P(a(C),["prevent"])},null,8,["modelValue","onInput"])]),o(z,{loading:a(y)=="pending",progress:{color:"red",animation:"swing"},"empty-state":{icon:"i-heroicons-circle-stack-20-solid",label:"Ничего не найдено."},columns:[{key:"id",label:"#"},{key:"region",label:"Регион"},{key:"surname",label:"Фамилия Имя Отчество"},{key:"birthday",label:"Дата рождения"},{key:"inn",label:"ИНН"},{key:"snils",label:"СНИЛС"},{key:"created",label:"Обновлено"},{key:"username",label:"Сотрудник"},{key:"editable",label:"Статус"}],rows:a(t).candidates},{"id-data":n(({row:e})=>[l(r(e.id),1)]),"region-data":n(({row:e})=>[l(r(e.region),1)]),"surname-data":n(({row:e})=>[o(B,{to:`/profile/${e.id}`},{default:n(()=>[l(r(`${e.surname} ${e.firstname} ${e.patronymic?e.patronymic:""}`),1)]),_:2},1032,["to"])]),"birthday-data":n(({row:e})=>[l(r(new Date(e.birthday).toLocaleDateString()),1)]),"birthplace-data":n(({row:e})=>[l(r(e.birthplace?e.birthplace:""),1)]),"created-data":n(({row:e})=>[l(r(new Date(e.created).toLocaleDateString()),1)]),"username-data":n(({row:e})=>[l(r(e.username?e.username.toString().split(" ")[0]:""),1)]),"editable-data":n(({row:e})=>[m("div",{class:x(["text-center me-12",e.editable?"animate-pulse":""])},[o(V,{size:"2xl",color:e.editable?"red":"green"},null,8,["color"])],2)]),caption:n(()=>[m("caption",ie,[o(h,{variant:"link",icon:"i-heroicons-arrow-path",label:`Обновлено: ${a(t).updated}`,onClick:a(d)},null,8,["label","onClick"])])]),_:1},8,["loading","rows"]),a(t).prev||a(t).next?(b(),k("div",le,[o(T,{orientation:"horizontal"},{default:n(()=>[o(h,{disabled:!a(t).prev,label:"Назад",variant:"link",icon:"i-heroicons-chevron-double-left",onClick:s[2]||(s[2]=e=>v(a(t).page-1))},null,8,["disabled"]),o(h,{disabled:!a(t).next,label:"Вперед",variant:"link",trailing:"",icon:"i-heroicons-chevron-double-right",onClick:s[3]||(s[3]=e=>v(a(t).page+1))},null,8,["disabled"])]),_:1})])):w("",!0)]),_:1})}}});export{ve as default};
