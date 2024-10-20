import{d as D,o as B,c as S,f as T,E as G,A as f,y as h,a0 as j,r as F,s as t,as as _,m as p,at as x,h as C,_ as P,j as W,q as ee,t as M,an as ae,L as le,Y as ne,v as ie,x as b,C as te,b as q,B as w,ac as ue}from"./DWkXyvYO.js";const ge=D({__name:"HeaderDiv",props:{div:{type:String,default:"py-1"},cls:{type:String,default:"text-xl text-red-800"},header:{type:String,default:""}},setup(e){const n=e;return(g,l)=>(B(),S("div",{class:f(n.div)},[T("h3",{class:f(["font-bold",n.cls])},G(n.header),3),h(g.$slots,"default")],2))}}),de=(e,n,g=!0)=>{const l=j("form-events",void 0),a=j("form-group",void 0),y=j("form-inputs",void 0);a&&(!g||e!=null&&e.legend?a.inputId.value=void 0:e!=null&&e.id&&(a.inputId.value=e==null?void 0:e.id),y&&(y.value[a.name.value]=a.inputId.value));const v=F(!1);function u(s,m){l&&l.emit({type:s,path:m})}function N(){u("blur",a==null?void 0:a.name.value),v.value=!0}function $(){u("change",a==null?void 0:a.name.value)}const d=_(()=>{(v.value||a!=null&&a.eagerValidation.value)&&u("input",a==null?void 0:a.name.value)},300);return{inputId:t(()=>(e==null?void 0:e.id)??(a==null?void 0:a.inputId.value)),name:t(()=>(e==null?void 0:e.name)??(a==null?void 0:a.name.value)),size:t(()=>{var m;const s=n.size[a==null?void 0:a.size.value]?a==null?void 0:a.size.value:null;return(e==null?void 0:e.size)??s??((m=n.default)==null?void 0:m.size)}),color:t(()=>{var s;return(s=a==null?void 0:a.error)!=null&&s.value?"red":e==null?void 0:e.color}),emitFormBlur:N,emitFormInput:d,emitFormChange:$}},o=p(C.ui.strategy,C.ui.input,x),oe=D({components:{UIcon:W},inheritAttrs:!1,props:{modelValue:{type:[String,Number],default:""},type:{type:String,default:"text"},id:{type:String,default:null},name:{type:String,default:null},placeholder:{type:String,default:null},required:{type:Boolean,default:!1},disabled:{type:Boolean,default:!1},autofocus:{type:Boolean,default:!1},autofocusDelay:{type:Number,default:100},icon:{type:String,default:null},loadingIcon:{type:String,default:()=>o.default.loadingIcon},leadingIcon:{type:String,default:null},trailingIcon:{type:String,default:null},trailing:{type:Boolean,default:!1},leading:{type:Boolean,default:!1},loading:{type:Boolean,default:!1},padded:{type:Boolean,default:!0},size:{type:String,default:null,validator(e){return Object.keys(o.size).includes(e)}},color:{type:String,default:()=>o.default.color,validator(e){return[...C.ui.colors,...Object.keys(o.color)].includes(e)}},variant:{type:String,default:()=>o.default.variant,validator(e){return[...Object.keys(o.variant),...Object.values(o.color).flatMap(n=>Object.keys(n))].includes(e)}},inputClass:{type:String,default:null},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})},modelModifiers:{type:Object,default:()=>({})}},emits:["update:modelValue","blur","change"],setup(e,{emit:n,slots:g}){const{ui:l,attrs:a}=ee("input",M(e,"ui"),o,M(e,"class")),{size:y,rounded:v}=ae({ui:l,props:e}),{emitFormBlur:u,emitFormInput:N,size:$,color:d,inputId:s,name:m}=de(e,o),r=t(()=>y.value??$.value),I=F(le({},e.modelModifiers,{trim:!1,lazy:!1,number:!1})),k=F(null),E=()=>{var i;e.autofocus&&((i=k.value)==null||i.focus())},O=i=>{I.value.trim&&(i=i.trim()),(I.value.number||e.type==="number")&&(i=ue(i)),n("update:modelValue",i),N()},L=i=>{I.value.lazy||O(i.target.value)},U=i=>{if(e.type==="file"){const c=i.target.files;n("change",c)}else{const c=i.target.value;n("change",c),I.value.lazy&&O(c),I.value.trim&&(i.target.value=c.trim())}},H=i=>{u(),n("blur",i)};ne(()=>{setTimeout(()=>{E()},e.autofocusDelay)});const J=t(()=>{var c,A;const i=((A=(c=l.value.color)==null?void 0:c[d.value])==null?void 0:A[e.variant])||l.value.variant[e.variant];return ie(b(l.value.base,l.value.form,v.value,l.value.placeholder,e.type==="file"&&l.value.file.base,l.value.size[r.value],e.padded?l.value.padding[r.value]:"p-0",i==null?void 0:i.replaceAll("{color}",d.value),(z.value||g.leading)&&l.value.leading.padding[r.value],(V.value||g.trailing)&&l.value.trailing.padding[r.value]),e.inputClass)}),z=t(()=>e.icon&&e.leading||e.icon&&!e.trailing||e.loading&&!e.trailing||e.leadingIcon),V=t(()=>e.icon&&e.trailing||e.loading&&e.trailing||e.trailingIcon),R=t(()=>e.loading?e.loadingIcon:e.leadingIcon||e.icon),Y=t(()=>e.loading&&!z.value?e.loadingIcon:e.trailingIcon||e.icon),K=t(()=>b(l.value.icon.leading.wrapper,l.value.icon.leading.pointer,l.value.icon.leading.padding[r.value])),Q=t(()=>b(l.value.icon.base,d.value&&C.ui.colors.includes(d.value)&&l.value.icon.color.replaceAll("{color}",d.value),l.value.icon.size[r.value],e.loading&&l.value.icon.loading)),X=t(()=>b(l.value.icon.trailing.wrapper,l.value.icon.trailing.pointer,l.value.icon.trailing.padding[r.value])),Z=t(()=>b(l.value.icon.base,d.value&&C.ui.colors.includes(d.value)&&l.value.icon.color.replaceAll("{color}",d.value),l.value.icon.size[r.value],e.loading&&!z.value&&l.value.icon.loading));return{ui:l,attrs:a,name:m,inputId:s,input:k,isLeading:z,isTrailing:V,inputClass:J,leadingIconName:R,leadingIconClass:Q,leadingWrapperIconClass:K,trailingIconName:Y,trailingIconClass:Z,trailingWrapperIconClass:X,onInput:L,onChange:U,onBlur:H}}}),se=["id","name","type","required","placeholder","disabled"];function re(e,n,g,l,a,y){const v=W;return B(),S("div",{class:f(e.type==="hidden"?"hidden":e.ui.wrapper)},[T("input",te({id:e.inputId,ref:"input",name:e.name,type:e.type,required:e.required,placeholder:e.placeholder,disabled:e.disabled,class:e.inputClass},e.type==="file"?e.attrs:{...e.attrs,value:e.modelValue},{onInput:n[0]||(n[0]=(...u)=>e.onInput&&e.onInput(...u)),onBlur:n[1]||(n[1]=(...u)=>e.onBlur&&e.onBlur(...u)),onChange:n[2]||(n[2]=(...u)=>e.onChange&&e.onChange(...u))}),null,16,se),h(e.$slots,"default"),e.isLeading&&e.leadingIconName||e.$slots.leading?(B(),S("span",{key:0,class:f(e.leadingWrapperIconClass)},[h(e.$slots,"leading",{disabled:e.disabled,loading:e.loading},()=>[q(v,{name:e.leadingIconName,class:f(e.leadingIconClass)},null,8,["name","class"])])],2)):w("",!0),e.isTrailing&&e.trailingIconName||e.$slots.trailing?(B(),S("span",{key:1,class:f(e.trailingWrapperIconClass)},[h(e.$slots,"trailing",{disabled:e.disabled,loading:e.loading},()=>[q(v,{name:e.trailingIconName,class:f(e.trailingIconClass)},null,8,["name","class"])])],2)):w("",!0)],2)}const ve=P(oe,[["render",re]]);export{ge as _,ve as a,de as u};
