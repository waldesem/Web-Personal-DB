import{m as X,au as Y,f,_ as Z,d as _,g as F,j as x,t as O,av as ee,k as i,l as ae,q as v,o,c as d,b as le,F as z,C as j,B as N,z as ne,x as b,s as p,a as W,y as q,as as w}from"./B8dkklNN.js";import{u as te}from"./DvJ7HPBa.js";const u=X(f.ui.strategy,f.ui.select,Y),ie=_({components:{UIcon:F},inheritAttrs:!1,props:{modelValue:{type:[String,Number,Object],default:""},id:{type:String,default:null},name:{type:String,default:null},placeholder:{type:String,default:null},required:{type:Boolean,default:!1},disabled:{type:Boolean,default:!1},icon:{type:String,default:null},loadingIcon:{type:String,default:()=>u.default.loadingIcon},leadingIcon:{type:String,default:null},trailingIcon:{type:String,default:()=>u.default.trailingIcon},trailing:{type:Boolean,default:!1},leading:{type:Boolean,default:!1},loading:{type:Boolean,default:!1},padded:{type:Boolean,default:!0},options:{type:Array,default:()=>[]},size:{type:String,default:null,validator(e){return Object.keys(u.size).includes(e)}},color:{type:String,default:()=>u.default.color,validator(e){return[...f.ui.colors,...Object.keys(u.color)].includes(e)}},variant:{type:String,default:()=>u.default.variant,validator(e){return[...Object.keys(u.variant),...Object.values(u.color).flatMap(r=>Object.keys(r))].includes(e)}},optionAttribute:{type:String,default:"label"},valueAttribute:{type:String,default:"value"},selectClass:{type:String,default:null},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})}},emits:["update:modelValue","change"],setup(e,{emit:r,slots:A}){const{ui:a,attrs:h}=x("select",O(e,"ui"),u,O(e,"class")),{size:S,rounded:m}=ee({ui:a,props:e}),{emitFormChange:n,inputId:c,color:t,size:C,name:G}=te(e,u),s=i(()=>S.value??C.value),L=l=>{r("update:modelValue",l.target.value)},M=l=>{r("change",l.target.value),n()},P=l=>w(l,e.valueAttribute,""),T=l=>w(l,e.optionAttribute,""),$=l=>["string","number","boolean"].includes(typeof l)?{[e.valueAttribute]:l,[e.optionAttribute]:l}:{...l,[e.valueAttribute]:P(l),[e.optionAttribute]:T(l)},V=i(()=>e.options.map(l=>$(l))),k=i(()=>e.placeholder?[{[e.valueAttribute]:"",[e.optionAttribute]:e.placeholder,disabled:!0},...V.value]:V.value),U=i(()=>{const l=$(e.modelValue),g=k.value.find(I=>I[e.valueAttribute]===l[e.valueAttribute]);return g?g[e.valueAttribute]:""}),D=i(()=>{var g,I;const l=((I=(g=a.value.color)==null?void 0:g[t.value])==null?void 0:I[e.variant])||a.value.variant[e.variant];return ae(v(a.value.base,a.value.form,m.value,a.value.size[s.value],e.padded?a.value.padding[s.value]:"p-0",l==null?void 0:l.replaceAll("{color}",t.value),(y.value||A.leading)&&a.value.leading.padding[s.value],(B.value||A.trailing)&&a.value.trailing.padding[s.value]),e.placeholder&&!e.modelValue&&a.value.placeholder,e.selectClass)}),y=i(()=>e.icon&&e.leading||e.icon&&!e.trailing||e.loading&&!e.trailing||e.leadingIcon),B=i(()=>e.icon&&e.trailing||e.loading&&e.trailing||e.trailingIcon),E=i(()=>e.loading?e.loadingIcon:e.leadingIcon||e.icon),J=i(()=>e.loading&&!y.value?e.loadingIcon:e.trailingIcon||e.icon),R=i(()=>v(a.value.icon.leading.wrapper,a.value.icon.leading.pointer,a.value.icon.leading.padding[s.value])),H=i(()=>v(a.value.icon.base,t.value&&f.ui.colors.includes(t.value)&&a.value.icon.color.replaceAll("{color}",t.value),a.value.icon.size[s.value],e.loading&&a.value.icon.loading)),K=i(()=>v(a.value.icon.trailing.wrapper,a.value.icon.trailing.pointer,a.value.icon.trailing.padding[s.value])),Q=i(()=>v(a.value.icon.base,t.value&&f.ui.colors.includes(t.value)&&a.value.icon.color.replaceAll("{color}",t.value),a.value.icon.size[s.value],e.loading&&!y.value&&a.value.icon.loading));return{ui:a,attrs:h,name:G,inputId:c,normalizedOptionsWithPlaceholder:k,normalizedValue:U,isLeading:y,isTrailing:B,selectClass:D,leadingIconName:E,leadingIconClass:H,leadingWrapperIconClass:R,trailingIconName:J,trailingIconClass:Q,trailingWrapperIconClass:K,onInput:L,onChange:M}}}),ue=["id","name","value","required","disabled"],re=["value","label"],oe=["value","selected","disabled","textContent"],de=["value","selected","disabled","textContent"];function se(e,r,A,a,h,S){const m=F;return o(),d("div",{class:b(e.ui.wrapper)},[le("select",ne({id:e.inputId,name:e.name,value:e.modelValue,required:e.required,disabled:e.disabled,class:e.selectClass},e.attrs,{onInput:r[0]||(r[0]=(...n)=>e.onInput&&e.onInput(...n)),onChange:r[1]||(r[1]=(...n)=>e.onChange&&e.onChange(...n))}),[(o(!0),d(z,null,j(e.normalizedOptionsWithPlaceholder,(n,c)=>(o(),d(z,null,[n.children?(o(),d("optgroup",{key:`${n[e.valueAttribute]}-optgroup-${c}`,value:n[e.valueAttribute],label:n[e.optionAttribute]},[(o(!0),d(z,null,j(n.children,(t,C)=>(o(),d("option",{key:`${t[e.valueAttribute]}-${c}-${C}`,value:t[e.valueAttribute],selected:t[e.valueAttribute]===e.normalizedValue,disabled:t.disabled,textContent:N(t[e.optionAttribute])},null,8,oe))),128))],8,re)):(o(),d("option",{key:`${n[e.valueAttribute]}-${c}`,value:n[e.valueAttribute],selected:n[e.valueAttribute]===e.normalizedValue,disabled:n.disabled,textContent:N(n[e.optionAttribute])},null,8,de))],64))),256))],16,ue),e.isLeading&&e.leadingIconName||e.$slots.leading?(o(),d("span",{key:0,class:b(e.leadingWrapperIconClass)},[p(e.$slots,"leading",{disabled:e.disabled,loading:e.loading},()=>[W(m,{name:e.leadingIconName,class:b(e.leadingIconClass)},null,8,["name","class"])],!0)],2)):q("",!0),e.isTrailing&&e.trailingIconName||e.$slots.trailing?(o(),d("span",{key:1,class:b(e.trailingWrapperIconClass)},[p(e.$slots,"trailing",{disabled:e.disabled,loading:e.loading},()=>[W(m,{name:e.trailingIconName,class:b(e.trailingIconClass),"aria-hidden":"true"},null,8,["name","class"])],!0)],2)):q("",!0)],2)}const ve=Z(ie,[["render",se],["__scopeId","data-v-9f80dc9e"]]);export{ve as _};
