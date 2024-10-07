import{u as K,a as L}from"./B0poOYeU.js";import{_ as P}from"./8sbBbPEZ.js";import{m as I,ao as Q,h as V,_ as F,d as w,l as q,t as B,r as O,K as W,$ as j,N as X,ak as Z,q as D,s as N,v as T,o as v,c as S,f as x,B as G,x as ee,z as ae,ap as te,y as C,g as c,b as l,k as le,u as oe,e as s,G as ne,aq as se,F as re,E as ue}from"./lgINOUnl.js";import{_ as ie}from"./C10ojqVm.js";import{_ as de}from"./4cJSv5k2.js";import{a as me}from"./sZSTzJ3f.js";const pe={base:"animate-pulse",background:"bg-gray-100 dark:bg-gray-800",rounded:"rounded-md"},g=I(V.ui.strategy,V.ui.textarea,Q),ce=w({inheritAttrs:!1,props:{modelValue:{type:[String,Number],default:""},id:{type:String,default:null},name:{type:String,default:null},placeholder:{type:String,default:null},required:{type:Boolean,default:!1},disabled:{type:Boolean,default:!1},rows:{type:Number,default:3},maxrows:{type:Number,default:0},autoresize:{type:Boolean,default:!1},autofocus:{type:Boolean,default:!1},autofocusDelay:{type:Number,default:100},resize:{type:Boolean,default:!1},padded:{type:Boolean,default:!0},size:{type:String,default:null,validator(e){return Object.keys(g.size).includes(e)}},color:{type:String,default:()=>g.default.color,validator(e){return[...V.ui.colors,...Object.keys(g.color)].includes(e)}},variant:{type:String,default:()=>g.default.variant,validator(e){return[...Object.keys(g.variant),...Object.values(g.color).flatMap(o=>Object.keys(o))].includes(e)}},textareaClass:{type:String,default:null},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})},modelModifiers:{type:Object,default:()=>({})}},emits:["update:modelValue","blur","change"],setup(e,{emit:o}){const{ui:i,attrs:y}=q("textarea",B(e,"ui"),g,B(e,"class")),{emitFormBlur:a,emitFormInput:f,inputId:m,color:_,size:$,name:d}=K(e,g),t=O(W({},e.modelModifiers,{trim:!1,lazy:!1,number:!1})),r=O(null),p=()=>{var u;e.autofocus&&((u=r.value)==null||u.focus())},h=()=>{if(e.autoresize){if(!r.value)return;r.value.rows=e.rows;const u=r.value.style.overflow;r.value.style.overflow="hidden";const b=window.getComputedStyle(r.value),k=parseInt(b.paddingTop),E=parseInt(b.paddingBottom),Y=k+E,H=parseInt(b.lineHeight),{scrollHeight:J}=r.value,U=(J-Y)/H;U>e.rows&&(r.value.rows=e.maxrows?Math.min(U,e.maxrows):U),r.value.style.overflow=u}},z=u=>{t.value.trim&&(u=u.trim()),t.value.number&&(u=te(u)),o("update:modelValue",u),f()},M=u=>{h(),t.value.lazy||z(u.target.value)},n=u=>{const b=u.target.value;o("change",b),t.value.lazy&&z(b),t.value.trim&&(u.target.value=b.trim())},A=u=>{o("blur",u),a()};j(()=>{setTimeout(()=>{p()},e.autofocusDelay)}),X(()=>e.modelValue,()=>{Z(h)}),j(()=>{setTimeout(()=>{p(),h()},100)});const R=D(()=>{var b,k;const u=((k=(b=i.value.color)==null?void 0:b[_.value])==null?void 0:k[e.variant])||i.value.variant[e.variant];return N(T(i.value.base,i.value.form,i.value.rounded,i.value.placeholder,i.value.size[$.value],e.padded?i.value.padding[$.value]:"p-0",u==null?void 0:u.replaceAll("{color}",_.value),!e.resize&&"resize-none"),e.textareaClass)});return{ui:i,attrs:y,name:d,inputId:m,textarea:r,textareaClass:R,onInput:M,onChange:n,onBlur:A}}}),fe=["id","value","name","rows","required","disabled","placeholder"];function be(e,o,i,y,a,f){return v(),S("div",{class:ae(e.ui.wrapper)},[x("textarea",G({id:e.inputId,ref:"textarea",value:e.modelValue,name:e.name,rows:e.rows,required:e.required,disabled:e.disabled,placeholder:e.placeholder,class:e.textareaClass},e.attrs,{onInput:o[0]||(o[0]=(...m)=>e.onInput&&e.onInput(...m)),onBlur:o[1]||(o[1]=(...m)=>e.onBlur&&e.onBlur(...m)),onChange:o[2]||(o[2]=(...m)=>e.onChange&&e.onChange(...m))}),null,16,fe),ee(e.$slots,"default")],2)}const ye=F(ce,[["render",be]]),ge=w({__name:"BtnGroup",emits:["cancel"],setup(e,{emit:o}){const i=o;return(y,a)=>{const f=le,m=ie;return v(),C(m,{class:"mt-3",size:"md",orientation:"horizontal"},{default:c(()=>[l(f,{label:"Принять",color:"green",variant:"outline",type:"submit"}),l(f,{label:"Отмена",color:"red",variant:"outline",onClick:a[0]||(a[0]=_=>i("cancel"))})]),_:1})}}}),Se=w({__name:"ResumeForm",props:{resume:{type:Object,default:{}}},emits:["cancel","update"],setup(e,{emit:o}){const i=o,a=B(e.resume);a.value.birthday=a.value.birthday?oe(a.value.birthday,"YYYY-MM-DD").value:"";function f(){i("cancel"),m()}function m(){Object.assign(a.value,{surname:"",firstname:"",patronymic:"",birthday:"",birthplace:"",citizenship:"",dual:"",inn:"",snils:"",marital:"",addition:""})}const _=d=>{const t=[];return d.surname&&!d.surname.match(/^[а-яёЁА-Я-\s]+$/)&&t.push({path:"surname",message:"Поле должно содержать только русские буквы"}),d.firstname&&!d.firstname.match(/^[а-яёЁА-Я-\s]+$/)&&t.push({path:"firstname",message:"Поле должно содержать только русские буквы"}),d.patronymic&&!d.patronymic.match(/^[а-яёЁА-Я-\s]+$/)&&t.push({path:"patronymic",message:"Поле должно содержать только русские буквы"}),Object.prototype.toString.call(d.birthday)||(console.log(d.birthday),t.push({path:"birthday",message:"Поле должно содержать дату"})),new Date(d.birthday)>new Date&&(console.log(d.birthday),t.push({path:"birthday",message:"Поле должно содержать корректную дату"})),d.snils&&!d.snils.match(/^[0-9]{11}$/)&&t.push({path:"snils",message:"Поле должно содержать 11 цифр"}),d.inn&&!d.inn.match(/^[0-9]{12}$/)&&t.push({path:"inn",message:"Поле должно содержать 12 цифр"}),t};async function $(){i("update",a.value),m()}return(d,t)=>{const r=L,p=P,h=ye,z=ge,M=de;return v(),C(M,{state:s(a),validate:_,onSubmit:ne($,["prevent"])},{default:c(()=>[l(p,{class:"mb-3",label:"Фамилия",name:"surname"},{default:c(()=>[l(r,{modelValue:s(a).surname,"onUpdate:modelValue":t[0]||(t[0]=n=>s(a).surname=n),modelModifiers:{trim:!0},required:"",placeholder:"Фамилия"},null,8,["modelValue"])]),_:1}),l(p,{class:"mb-3",label:"Имя",name:"firstname"},{default:c(()=>[l(r,{modelValue:s(a).firstname,"onUpdate:modelValue":t[1]||(t[1]=n=>s(a).firstname=n),modelModifiers:{trim:!0},required:"",placeholder:"Имя"},null,8,["modelValue"])]),_:1}),l(p,{class:"mb-3",label:"Отчество",name:"patronymic"},{default:c(()=>[l(r,{modelValue:s(a).patronymic,"onUpdate:modelValue":t[2]||(t[2]=n=>s(a).patronymic=n),modelModifiers:{trim:!0},placeholder:"Отчество"},null,8,["modelValue"])]),_:1}),l(p,{class:"mb-3",label:"Дата рождения",name:"birthday"},{default:c(()=>[l(r,{modelValue:s(a).birthday,"onUpdate:modelValue":t[3]||(t[3]=n=>s(a).birthday=n),required:"",type:"date"},null,8,["modelValue"])]),_:1}),l(p,{class:"mb-3",label:"Место рождения"},{default:c(()=>[l(r,{modelValue:s(a).birthplace,"onUpdate:modelValue":t[4]||(t[4]=n=>s(a).birthplace=n),modelModifiers:{trim:!0,lazy:!0},placeholder:"Место рождения"},null,8,["modelValue"])]),_:1}),l(p,{class:"mb-3",label:"Гражданство",name:"citizenship"},{default:c(()=>[l(r,{modelValue:s(a).citizenship,"onUpdate:modelValue":t[5]||(t[5]=n=>s(a).citizenship=n),modelModifiers:{trim:!0},placeholder:"Гражданство"},null,8,["modelValue"])]),_:1}),l(p,{class:"mb-3",label:"Двойное гражданство",name:"dual"},{default:c(()=>[l(r,{modelValue:s(a).dual,"onUpdate:modelValue":t[6]||(t[6]=n=>s(a).dual=n),modelModifiers:{trim:!0},placeholder:"Двойное гражданство"},null,8,["modelValue"])]),_:1}),l(p,{class:"mb-3",label:"СНИЛС",name:"snils"},{default:c(()=>[l(r,{modelValue:s(a).snils,"onUpdate:modelValue":t[7]||(t[7]=n=>s(a).snils=n),modelModifiers:{trim:!0,lazy:!0},placeholder:"СНИЛС"},null,8,["modelValue"])]),_:1}),l(p,{class:"mb-3",label:"ИНН",name:"inn"},{default:c(()=>[l(r,{modelValue:s(a).inn,"onUpdate:modelValue":t[8]||(t[8]=n=>s(a).inn=n),modelModifiers:{trim:!0,lazy:!0},placeholder:"ИНН"},null,8,["modelValue"])]),_:1}),l(p,{class:"mb-3",label:"Семейное положение",name:"marital"},{default:c(()=>[l(r,{modelValue:s(a).marital,"onUpdate:modelValue":t[9]||(t[9]=n=>s(a).marital=n),modelModifiers:{trim:!0,lazy:!0},placeholder:"Семейное положение"},null,8,["modelValue"])]),_:1}),l(p,{class:"mb-3",label:"Дополнительно"},{default:c(()=>[l(h,{modelValue:s(a).addition,"onUpdate:modelValue":t[10]||(t[10]=n=>s(a).addition=n),modelModifiers:{trim:!0,lazy:!0},placeholder:"Дополнительно"},null,8,["modelValue"])]),_:1}),l(z,{onCancel:f})]),_:1},8,["state"])}}}),ve=I(V.ui.strategy,V.ui.skeleton,pe),_e=w({inheritAttrs:!1,props:{as:{type:String,default:"div"},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})}},setup(e){const{ui:o,attrs:i}=q("skeleton",B(e,"ui"),ve),y=D(()=>N(T(o.value.base,o.value.background,o.value.rounded),e.class));return{ui:o,attrs:i,skeletonClass:y}}});function he(e,o,i,y,a,f){return v(),C(se(e.as),G({class:e.skeletonClass},e.attrs),null,16,["class"])}const Ve=F(_e,[["render",he]]),we={class:"col-span-1"},$e={class:"col-span-5"},xe=w({__name:"SkeletonDiv",props:{rows:{type:Number,default:3}},setup(e){const o=e;return(i,y)=>{const a=Ve,f=me;return v(),C(f,null,{default:c(()=>[(v(!0),S(re,null,ue(o.rows,m=>(v(),S("div",{key:m,class:"flex grid grid-cols-6 gap-3 mb-3"},[x("div",we,[l(a,{class:"h-4"})]),x("div",$e,[l(a,{class:"h-4 w-[300px]"})])]))),128))]),_:1})}}});export{Se as _,xe as a,ge as b,ye as c};