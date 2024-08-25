import{P as j,r as V,ax as ie,x as r,a2 as te,ay as re,_ as J,m as K,k as $,g as L,s as U,v as T,K as se,o as u,c as d,a as F,B as g,A as b,aq as S,D as z,F as B,d as w,t as N,C,az as oe,aA as ue,l as H,au as de,$ as ge,L as fe,y as ce,z as O,b as W,ag as me}from"./BPBLQG6i.js";const ve={wrapper:"",inner:"",label:{wrapper:"flex content-center items-center justify-between",base:"block font-medium text-gray-700 dark:text-gray-200",required:"after:content-['*'] after:ms-0.5 after:text-red-500 dark:after:text-red-400"},size:{"2xs":"text-xs",xs:"text-xs",sm:"text-sm",md:"text-sm",lg:"text-sm",xl:"text-base"},container:"mt-1 relative",description:"text-gray-500 dark:text-gray-400",hint:"text-gray-500 dark:text-gray-400",help:"mt-2 text-gray-500 dark:text-gray-400",error:"mt-2 text-red-500 dark:text-red-400",default:{size:"sm"}},ye=(e,l)=>{const i=j("form-events",void 0),a=j("form-group",void 0),f=j("form-inputs",void 0);a&&(e!=null&&e.id&&(a.inputId.value=e==null?void 0:e.id),f&&(f.value[a.name.value]=a.inputId.value));const c=V(!1);function o(n,v){i&&i.emit({type:n,path:v})}function s(){o("blur",a==null?void 0:a.name.value),c.value=!0}function m(){o("change",a==null?void 0:a.name.value)}const h=ie(()=>{(c.value||a!=null&&a.eagerValidation.value)&&o("input",a==null?void 0:a.name.value)},300);return{inputId:r(()=>(e==null?void 0:e.id)??(a==null?void 0:a.inputId.value)),name:r(()=>(e==null?void 0:e.name)??(a==null?void 0:a.name.value)),size:r(()=>{var v;const n=l.size[a==null?void 0:a.size.value]?a==null?void 0:a.size.value:null;return(e==null?void 0:e.size)??n??((v=l.default)==null?void 0:v.size)}),color:r(()=>{var n;return(n=a==null?void 0:a.error)!=null&&n.value?"red":e==null?void 0:e.color}),emitFormBlur:s,emitFormInput:h,emitFormChange:m}},be=Symbol.for("nuxt:client-only"),he="data-n-ids",Ie="-";function pe(e){var f,c,o,s,m,h;if(typeof e!="string")throw new TypeError("[nuxt] [useId] key must be a string.");e=`n${e.slice(1)}`;const l=te(),i=re();if(!i)throw new TypeError("[nuxt] `useId` must be called within a component setup function.");l._id||(l._id=0),i._nuxtIdIndex||(i._nuxtIdIndex={}),(f=i._nuxtIdIndex)[e]||(f[e]=0);const a=e+Ie+i._nuxtIdIndex[e]++;if(l.payload.serverRendered&&l.isHydrating&&!j(be,!1)){const n=((c=i.vnode.el)==null?void 0:c.nodeType)===8&&((s=(o=i.vnode.el)==null?void 0:o.nextElementSibling)!=null&&s.getAttribute)?(m=i.vnode.el)==null?void 0:m.nextElementSibling:i.vnode.el,v=JSON.parse(((h=n==null?void 0:n.getAttribute)==null?void 0:h.call(n,he))||"{}");if(v[a])return v[a]}return e+"_"+l._id++}const q=K($.ui.strategy,$.ui.formGroup,ve),ze=L({inheritAttrs:!1,props:{name:{type:String,default:null},size:{type:String,default:null,validator(e){return Object.keys(q.size).includes(e)}},label:{type:String,default:null},description:{type:String,default:null},required:{type:Boolean,default:!1},help:{type:String,default:null},error:{type:[String,Boolean],default:null},hint:{type:String,default:null},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})},eagerValidation:{type:Boolean,default:!1}},setup(e){const{ui:l,attrs:i}=U("formGroup",T(e,"ui"),q,T(e,"class")),a=j("form-errors",null),f=r(()=>{var s,m;return e.error&&typeof e.error=="string"||typeof e.error=="boolean"?e.error:(m=(s=a==null?void 0:a.value)==null?void 0:s.find(h=>h.path===e.name))==null?void 0:m.message}),c=r(()=>l.value.size[e.size??q.default.size]),o=V(pe("$K7dDJpdOWE"));return se("form-group",{error:f,inputId:o,name:r(()=>e.name),size:r(()=>e.size),eagerValidation:r(()=>e.eagerValidation)}),{ui:l,attrs:i,inputId:o,size:c,error:f}}}),$e=["for"];function Se(e,l,i,a,f,c){return u(),d("div",z({class:e.ui.wrapper},e.attrs),[F("div",{class:g(e.ui.inner)},[e.label||e.$slots.label?(u(),d("div",{key:0,class:g([e.ui.label.wrapper,e.size])},[F("label",{for:e.inputId,class:g([e.ui.label.base,e.required?e.ui.label.required:""])},[e.$slots.label?b(e.$slots,"label",S(z({key:0},{error:e.error,label:e.label,name:e.name,hint:e.hint,description:e.description,help:e.help}))):(u(),d(B,{key:1},[w(N(e.label),1)],64))],10,$e),e.hint||e.$slots.hint?(u(),d("span",{key:0,class:g([e.ui.hint])},[e.$slots.hint?b(e.$slots,"hint",S(z({key:0},{error:e.error,label:e.label,name:e.name,hint:e.hint,description:e.description,help:e.help}))):(u(),d(B,{key:1},[w(N(e.hint),1)],64))],2)):C("",!0)],2)):C("",!0),e.description||e.$slots.description?(u(),d("p",{key:1,class:g([e.ui.description,e.size])},[e.$slots.description?b(e.$slots,"description",S(z({key:0},{error:e.error,label:e.label,name:e.name,hint:e.hint,description:e.description,help:e.help}))):(u(),d(B,{key:1},[w(N(e.description),1)],64))],2)):C("",!0)],2),F("div",{class:g([e.label?e.ui.container:""])},[b(e.$slots,"default",S(oe({error:e.error}))),typeof e.error=="string"&&e.error?(u(),d("p",{key:0,class:g([e.ui.error,e.size])},[e.$slots.error?b(e.$slots,"error",S(z({key:0},{error:e.error,label:e.label,name:e.name,hint:e.hint,description:e.description,help:e.help}))):(u(),d(B,{key:1},[w(N(e.error),1)],64))],2)):e.help||e.$slots.help?(u(),d("p",{key:1,class:g([e.ui.help,e.size])},[e.$slots.help?b(e.$slots,"help",S(z({key:0},{error:e.error,label:e.label,name:e.name,hint:e.hint,description:e.description,help:e.help}))):(u(),d(B,{key:1},[w(N(e.help),1)],64))],2)):C("",!0)],2)],16)}const Ne=J(ze,[["render",Se]]),y=K($.ui.strategy,$.ui.input,ue),Ce=L({components:{UIcon:H},inheritAttrs:!1,props:{modelValue:{type:[String,Number],default:""},type:{type:String,default:"text"},id:{type:String,default:null},name:{type:String,default:null},placeholder:{type:String,default:null},required:{type:Boolean,default:!1},disabled:{type:Boolean,default:!1},autofocus:{type:Boolean,default:!1},autofocusDelay:{type:Number,default:100},icon:{type:String,default:null},loadingIcon:{type:String,default:()=>y.default.loadingIcon},leadingIcon:{type:String,default:null},trailingIcon:{type:String,default:null},trailing:{type:Boolean,default:!1},leading:{type:Boolean,default:!1},loading:{type:Boolean,default:!1},padded:{type:Boolean,default:!0},size:{type:String,default:null,validator(e){return Object.keys(y.size).includes(e)}},color:{type:String,default:()=>y.default.color,validator(e){return[...$.ui.colors,...Object.keys(y.color)].includes(e)}},variant:{type:String,default:()=>y.default.variant,validator(e){return[...Object.keys(y.variant),...Object.values(y.color).flatMap(l=>Object.keys(l))].includes(e)}},inputClass:{type:String,default:null},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})},modelModifiers:{type:Object,default:()=>({})}},emits:["update:modelValue","blur","change"],setup(e,{emit:l,slots:i}){const{ui:a,attrs:f}=U("input",T(e,"ui"),y,T(e,"class")),{size:c,rounded:o}=de({ui:a,props:e}),{emitFormBlur:s,emitFormInput:m,size:h,color:n,inputId:v,name:Y}=ye(e,y),I=r(()=>c.value??h.value),k=V(ge({},e.modelModifiers,{trim:!1,lazy:!1,number:!1})),E=V(null),Q=()=>{var t;e.autofocus&&((t=E.value)==null||t.focus())},D=t=>{k.value.trim&&(t=t.trim()),(k.value.number||e.type==="number")&&(t=me(t)),l("update:modelValue",t),m()},X=t=>{k.value.lazy||D(t.target.value)},Z=t=>{if(e.type==="file"){const p=t.target.files;l("change",p)}else{const p=t.target.value;l("change",p),k.value.lazy&&D(p),k.value.trim&&(t.target.value=p.trim())}},G=t=>{s(),l("blur",t)};fe(()=>{setTimeout(()=>{Q()},e.autofocusDelay)});const P=r(()=>{var p,R;const t=((R=(p=a.value.color)==null?void 0:p[n.value])==null?void 0:R[e.variant])||a.value.variant[e.variant];return ce(O(a.value.base,a.value.form,o.value,a.value.placeholder,e.type==="file"&&a.value.file.base,a.value.size[I.value],e.padded?a.value.padding[I.value]:"p-0",t==null?void 0:t.replaceAll("{color}",n.value),(A.value||i.leading)&&a.value.leading.padding[I.value],(M.value||i.trailing)&&a.value.trailing.padding[I.value]),e.inputClass)}),A=r(()=>e.icon&&e.leading||e.icon&&!e.trailing||e.loading&&!e.trailing||e.leadingIcon),M=r(()=>e.icon&&e.trailing||e.loading&&e.trailing||e.trailingIcon),x=r(()=>e.loading?e.loadingIcon:e.leadingIcon||e.icon),_=r(()=>e.loading&&!A.value?e.loadingIcon:e.trailingIcon||e.icon),ee=r(()=>O(a.value.icon.leading.wrapper,a.value.icon.leading.pointer,a.value.icon.leading.padding[I.value])),ae=r(()=>O(a.value.icon.base,n.value&&$.ui.colors.includes(n.value)&&a.value.icon.color.replaceAll("{color}",n.value),a.value.icon.size[I.value],e.loading&&a.value.icon.loading)),le=r(()=>O(a.value.icon.trailing.wrapper,a.value.icon.trailing.pointer,a.value.icon.trailing.padding[I.value])),ne=r(()=>O(a.value.icon.base,n.value&&$.ui.colors.includes(n.value)&&a.value.icon.color.replaceAll("{color}",n.value),a.value.icon.size[I.value],e.loading&&!A.value&&a.value.icon.loading));return{ui:a,attrs:f,name:Y,inputId:v,input:E,isLeading:A,isTrailing:M,inputClass:P,leadingIconName:x,leadingIconClass:ae,leadingWrapperIconClass:ee,trailingIconName:_,trailingIconClass:ne,trailingWrapperIconClass:le,onInput:X,onChange:Z,onBlur:G}}}),ke=["id","name","value","type","required","placeholder","disabled"];function Be(e,l,i,a,f,c){const o=H;return u(),d("div",{class:g(e.type==="hidden"?"hidden":e.ui.wrapper)},[F("input",z({id:e.inputId,ref:"input",name:e.name,value:e.modelValue,type:e.type,required:e.required,placeholder:e.placeholder,disabled:e.disabled,class:e.inputClass},e.attrs,{onInput:l[0]||(l[0]=(...s)=>e.onInput&&e.onInput(...s)),onBlur:l[1]||(l[1]=(...s)=>e.onBlur&&e.onBlur(...s)),onChange:l[2]||(l[2]=(...s)=>e.onChange&&e.onChange(...s))}),null,16,ke),b(e.$slots,"default"),e.isLeading&&e.leadingIconName||e.$slots.leading?(u(),d("span",{key:0,class:g(e.leadingWrapperIconClass)},[b(e.$slots,"leading",{disabled:e.disabled,loading:e.loading},()=>[W(o,{name:e.leadingIconName,class:g(e.leadingIconClass)},null,8,["name","class"])])],2)):C("",!0),e.isTrailing&&e.trailingIconName||e.$slots.trailing?(u(),d("span",{key:1,class:g(e.trailingWrapperIconClass)},[b(e.$slots,"trailing",{disabled:e.disabled,loading:e.loading},()=>[W(o,{name:e.trailingIconName,class:g(e.trailingIconClass)},null,8,["name","class"])])],2)):C("",!0)],2)}const Oe=J(Ce,[["render",Be]]);export{Ne as _,Oe as a,ye as b,pe as u};
