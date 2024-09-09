import{g as E,o,c as u,a as j,t as C,B as d,O as A,r as V,aF as te,x as r,a7 as ie,am as re,m as J,k as $,_ as K,s as L,v as T,K as se,A as b,ay as S,D as z,F as O,d as w,C as k,aG as oe,aH as ue,l as U,aC as de,a4 as ge,L as ce,y as fe,z as N,b as H,aq as me}from"./IZgRZ49_.js";const ve={wrapper:"",inner:"",label:{wrapper:"flex content-center items-center justify-between",base:"block font-medium text-gray-700 dark:text-gray-200",required:"after:content-['*'] after:ms-0.5 after:text-red-500 dark:after:text-red-400"},size:{"2xs":"text-xs",xs:"text-xs",sm:"text-sm",md:"text-sm",lg:"text-sm",xl:"text-base"},container:"mt-1 relative",description:"text-gray-500 dark:text-gray-400",hint:"text-gray-500 dark:text-gray-400",help:"mt-2 text-gray-500 dark:text-gray-400",error:"mt-2 text-red-500 dark:text-red-400",default:{size:"sm"}},we=E({__name:"HeaderDiv",props:{div:{type:String,default:"py-1"},cls:{type:String,default:"text-2xl text-red-800"},header:{type:String,default:""}},setup(e){const l=e;return(n,a)=>(o(),u("div",{class:d(l.div)},[j("h3",{class:d(["font-bold",l.cls])},C(l.header),3)],2))}}),ye=(e,l)=>{const n=A("form-events",void 0),a=A("form-group",void 0),c=A("form-inputs",void 0);a&&(e!=null&&e.id&&(a.inputId.value=e==null?void 0:e.id),c&&(c.value[a.name.value]=a.inputId.value));const f=V(!1);function g(t,v){n&&n.emit({type:t,path:v})}function s(){g("blur",a==null?void 0:a.name.value),f.value=!0}function m(){g("change",a==null?void 0:a.name.value)}const h=te(()=>{(f.value||a!=null&&a.eagerValidation.value)&&g("input",a==null?void 0:a.name.value)},300);return{inputId:r(()=>(e==null?void 0:e.id)??(a==null?void 0:a.inputId.value)),name:r(()=>(e==null?void 0:e.name)??(a==null?void 0:a.name.value)),size:r(()=>{var v;const t=l.size[a==null?void 0:a.size.value]?a==null?void 0:a.size.value:null;return(e==null?void 0:e.size)??t??((v=l.default)==null?void 0:v.size)}),color:r(()=>{var t;return(t=a==null?void 0:a.error)!=null&&t.value?"red":e==null?void 0:e.color}),emitFormBlur:s,emitFormInput:h,emitFormChange:m}},be=Symbol.for("nuxt:client-only"),he="data-n-ids",pe="-";function Ie(e){var c,f,g,s,m,h;if(typeof e!="string")throw new TypeError("[nuxt] [useId] key must be a string.");e=`n${e.slice(1)}`;const l=ie(),n=re();if(!n)throw new TypeError("[nuxt] `useId` must be called within a component setup function.");l._id||(l._id=0),n._nuxtIdIndex||(n._nuxtIdIndex={}),(c=n._nuxtIdIndex)[e]||(c[e]=0);const a=e+pe+n._nuxtIdIndex[e]++;if(l.payload.serverRendered&&l.isHydrating&&!A(be,!1)){const t=((f=n.vnode.el)==null?void 0:f.nodeType)===8&&((s=(g=n.vnode.el)==null?void 0:g.nextElementSibling)!=null&&s.getAttribute)?(m=n.vnode.el)==null?void 0:m.nextElementSibling:n.vnode.el,v=JSON.parse(((h=t==null?void 0:t.getAttribute)==null?void 0:h.call(t,he))||"{}");if(v[a])return v[a]}return e+"_"+l._id++}const q=J($.ui.strategy,$.ui.formGroup,ve),ze=E({inheritAttrs:!1,props:{name:{type:String,default:null},size:{type:String,default:null,validator(e){return Object.keys(q.size).includes(e)}},label:{type:String,default:null},description:{type:String,default:null},required:{type:Boolean,default:!1},help:{type:String,default:null},error:{type:[String,Boolean],default:null},hint:{type:String,default:null},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})},eagerValidation:{type:Boolean,default:!1}},setup(e){const{ui:l,attrs:n}=L("formGroup",T(e,"ui"),q,T(e,"class")),a=A("form-errors",null),c=r(()=>{var s,m;return e.error&&typeof e.error=="string"||typeof e.error=="boolean"?e.error:(m=(s=a==null?void 0:a.value)==null?void 0:s.find(h=>h.path===e.name))==null?void 0:m.message}),f=r(()=>l.value.size[e.size??q.default.size]),g=V(Ie("$K7dDJpdOWE"));return se("form-group",{error:c,inputId:g,name:r(()=>e.name),size:r(()=>e.size),eagerValidation:r(()=>e.eagerValidation)}),{ui:l,attrs:n,inputId:g,size:f,error:c}}}),$e=["for"];function Se(e,l,n,a,c,f){return o(),u("div",z({class:e.ui.wrapper},e.attrs),[j("div",{class:d(e.ui.inner)},[e.label||e.$slots.label?(o(),u("div",{key:0,class:d([e.ui.label.wrapper,e.size])},[j("label",{for:e.inputId,class:d([e.ui.label.base,e.required?e.ui.label.required:""])},[e.$slots.label?b(e.$slots,"label",S(z({key:0},{error:e.error,label:e.label,name:e.name,hint:e.hint,description:e.description,help:e.help}))):(o(),u(O,{key:1},[w(C(e.label),1)],64))],10,$e),e.hint||e.$slots.hint?(o(),u("span",{key:0,class:d([e.ui.hint])},[e.$slots.hint?b(e.$slots,"hint",S(z({key:0},{error:e.error,label:e.label,name:e.name,hint:e.hint,description:e.description,help:e.help}))):(o(),u(O,{key:1},[w(C(e.hint),1)],64))],2)):k("",!0)],2)):k("",!0),e.description||e.$slots.description?(o(),u("p",{key:1,class:d([e.ui.description,e.size])},[e.$slots.description?b(e.$slots,"description",S(z({key:0},{error:e.error,label:e.label,name:e.name,hint:e.hint,description:e.description,help:e.help}))):(o(),u(O,{key:1},[w(C(e.description),1)],64))],2)):k("",!0)],2),j("div",{class:d([e.label?e.ui.container:""])},[b(e.$slots,"default",S(oe({error:e.error}))),typeof e.error=="string"&&e.error?(o(),u("p",{key:0,class:d([e.ui.error,e.size])},[e.$slots.error?b(e.$slots,"error",S(z({key:0},{error:e.error,label:e.label,name:e.name,hint:e.hint,description:e.description,help:e.help}))):(o(),u(O,{key:1},[w(C(e.error),1)],64))],2)):e.help||e.$slots.help?(o(),u("p",{key:1,class:d([e.ui.help,e.size])},[e.$slots.help?b(e.$slots,"help",S(z({key:0},{error:e.error,label:e.label,name:e.name,hint:e.hint,description:e.description,help:e.help}))):(o(),u(O,{key:1},[w(C(e.help),1)],64))],2)):k("",!0)],2)],16)}const Ne=K(ze,[["render",Se]]),y=J($.ui.strategy,$.ui.input,ue),Ce=E({components:{UIcon:U},inheritAttrs:!1,props:{modelValue:{type:[String,Number],default:""},type:{type:String,default:"text"},id:{type:String,default:null},name:{type:String,default:null},placeholder:{type:String,default:null},required:{type:Boolean,default:!1},disabled:{type:Boolean,default:!1},autofocus:{type:Boolean,default:!1},autofocusDelay:{type:Number,default:100},icon:{type:String,default:null},loadingIcon:{type:String,default:()=>y.default.loadingIcon},leadingIcon:{type:String,default:null},trailingIcon:{type:String,default:null},trailing:{type:Boolean,default:!1},leading:{type:Boolean,default:!1},loading:{type:Boolean,default:!1},padded:{type:Boolean,default:!0},size:{type:String,default:null,validator(e){return Object.keys(y.size).includes(e)}},color:{type:String,default:()=>y.default.color,validator(e){return[...$.ui.colors,...Object.keys(y.color)].includes(e)}},variant:{type:String,default:()=>y.default.variant,validator(e){return[...Object.keys(y.variant),...Object.values(y.color).flatMap(l=>Object.keys(l))].includes(e)}},inputClass:{type:String,default:null},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})},modelModifiers:{type:Object,default:()=>({})}},emits:["update:modelValue","blur","change"],setup(e,{emit:l,slots:n}){const{ui:a,attrs:c}=L("input",T(e,"ui"),y,T(e,"class")),{size:f,rounded:g}=de({ui:a,props:e}),{emitFormBlur:s,emitFormInput:m,size:h,color:t,inputId:v,name:Y}=ye(e,y),p=r(()=>f.value??h.value),B=V(ge({},e.modelModifiers,{trim:!1,lazy:!1,number:!1})),D=V(null),Q=()=>{var i;e.autofocus&&((i=D.value)==null||i.focus())},M=i=>{B.value.trim&&(i=i.trim()),(B.value.number||e.type==="number")&&(i=me(i)),l("update:modelValue",i),m()},X=i=>{B.value.lazy||M(i.target.value)},Z=i=>{if(e.type==="file"){const I=i.target.files;l("change",I)}else{const I=i.target.value;l("change",I),B.value.lazy&&M(I),B.value.trim&&(i.target.value=I.trim())}},G=i=>{s(),l("blur",i)};ce(()=>{setTimeout(()=>{Q()},e.autofocusDelay)});const P=r(()=>{var I,W;const i=((W=(I=a.value.color)==null?void 0:I[t.value])==null?void 0:W[e.variant])||a.value.variant[e.variant];return fe(N(a.value.base,a.value.form,g.value,a.value.placeholder,e.type==="file"&&a.value.file.base,a.value.size[p.value],e.padded?a.value.padding[p.value]:"p-0",i==null?void 0:i.replaceAll("{color}",t.value),(F.value||n.leading)&&a.value.leading.padding[p.value],(R.value||n.trailing)&&a.value.trailing.padding[p.value]),e.inputClass)}),F=r(()=>e.icon&&e.leading||e.icon&&!e.trailing||e.loading&&!e.trailing||e.leadingIcon),R=r(()=>e.icon&&e.trailing||e.loading&&e.trailing||e.trailingIcon),x=r(()=>e.loading?e.loadingIcon:e.leadingIcon||e.icon),_=r(()=>e.loading&&!F.value?e.loadingIcon:e.trailingIcon||e.icon),ee=r(()=>N(a.value.icon.leading.wrapper,a.value.icon.leading.pointer,a.value.icon.leading.padding[p.value])),ae=r(()=>N(a.value.icon.base,t.value&&$.ui.colors.includes(t.value)&&a.value.icon.color.replaceAll("{color}",t.value),a.value.icon.size[p.value],e.loading&&a.value.icon.loading)),le=r(()=>N(a.value.icon.trailing.wrapper,a.value.icon.trailing.pointer,a.value.icon.trailing.padding[p.value])),ne=r(()=>N(a.value.icon.base,t.value&&$.ui.colors.includes(t.value)&&a.value.icon.color.replaceAll("{color}",t.value),a.value.icon.size[p.value],e.loading&&!F.value&&a.value.icon.loading));return{ui:a,attrs:c,name:Y,inputId:v,input:D,isLeading:F,isTrailing:R,inputClass:P,leadingIconName:x,leadingIconClass:ae,leadingWrapperIconClass:ee,trailingIconName:_,trailingIconClass:ne,trailingWrapperIconClass:le,onInput:X,onChange:Z,onBlur:G}}}),ke=["id","name","value","type","required","placeholder","disabled"];function Be(e,l,n,a,c,f){const g=U;return o(),u("div",{class:d(e.type==="hidden"?"hidden":e.ui.wrapper)},[j("input",z({id:e.inputId,ref:"input",name:e.name,value:e.modelValue,type:e.type,required:e.required,placeholder:e.placeholder,disabled:e.disabled,class:e.inputClass},e.attrs,{onInput:l[0]||(l[0]=(...s)=>e.onInput&&e.onInput(...s)),onBlur:l[1]||(l[1]=(...s)=>e.onBlur&&e.onBlur(...s)),onChange:l[2]||(l[2]=(...s)=>e.onChange&&e.onChange(...s))}),null,16,ke),b(e.$slots,"default"),e.isLeading&&e.leadingIconName||e.$slots.leading?(o(),u("span",{key:0,class:d(e.leadingWrapperIconClass)},[b(e.$slots,"leading",{disabled:e.disabled,loading:e.loading},()=>[H(g,{name:e.leadingIconName,class:d(e.leadingIconClass)},null,8,["name","class"])])],2)):k("",!0),e.isTrailing&&e.trailingIconName||e.$slots.trailing?(o(),u("span",{key:1,class:d(e.trailingWrapperIconClass)},[b(e.$slots,"trailing",{disabled:e.disabled,loading:e.loading},()=>[H(g,{name:e.trailingIconName,class:d(e.trailingIconClass)},null,8,["name","class"])])],2)):k("",!0)],2)}const je=K(Ce,[["render",Be]]);export{we as _,Ne as a,je as b,ye as c,Ie as u};