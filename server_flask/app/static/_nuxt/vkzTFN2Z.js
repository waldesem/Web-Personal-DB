import{m as F,k as b,_ as O,g as I,s as V,v as h,x as s,z as t,o,c as u,A as z,B as d,Y as D,a as C,t as v,C as m,ay as E,D as f,F as P,E as J,d as L}from"./IZgRZ49_.js";const R={wrapper:"w-full flex flex-col gap-2",indicator:{container:{base:"flex flex-row justify-end",width:"min-w-fit",transition:"transition-all"},align:"text-end",width:"w-fit",color:"text-gray-400 dark:text-gray-500",size:{"2xs":"text-xs",xs:"text-xs",sm:"text-sm",md:"text-sm",lg:"text-sm",xl:"text-base","2xl":"text-base"}},progress:{base:"block appearance-none border-none overflow-hidden",width:"w-full [&::-webkit-progress-bar]:w-full",size:{"2xs":"h-px",xs:"h-0.5",sm:"h-1",md:"h-2",lg:"h-3",xl:"h-4","2xl":"h-5"},rounded:"rounded-full [&::-webkit-progress-bar]:rounded-full",track:"[&::-webkit-progress-bar]:bg-gray-200 [&::-webkit-progress-bar]:dark:bg-gray-700 [@supports(selector(&::-moz-progress-bar))]:bg-gray-200 [@supports(selector(&::-moz-progress-bar))]:dark:bg-gray-700",bar:"[&::-webkit-progress-value]:rounded-full [&::-webkit-progress-value]:transition-all [&::-webkit-progress-value]:ease-in-out [&::-moz-progress-bar]:rounded-full",color:"text-{color}-500 dark:text-{color}-400",background:"[&::-webkit-progress-value]:bg-current [&::-moz-progress-bar]:bg-current",indeterminate:{base:"indeterminate:relative",rounded:"indeterminate:after:rounded-full [&:indeterminate::-webkit-progress-value]:rounded-full [&:indeterminate::-moz-progress-bar]:rounded-full"}},steps:{base:"grid grid-cols-1",color:"text-{color}-500 dark:text-{color}-400",size:{"2xs":"text-xs",xs:"text-xs",sm:"text-sm",md:"text-sm",lg:"text-sm",xl:"text-base","2xl":"text-base"}},step:{base:"transition-all opacity-0 truncate row-start-1 col-start-1",align:"text-end",active:"opacity-100",first:"text-gray-500 dark:text-gray-400"},animation:{carousel:"bar-animation-carousel","carousel-inverse":"bar-animation-carousel-inverse",swing:"bar-animation-swing",elastic:"bar-animation-elastic"},default:{color:"primary",size:"md",animation:"carousel"}},i=F(b.ui.strategy,b.ui.progress,R),T=I({inheritAttrs:!1,props:{value:{type:Number,default:null},max:{type:[Number,Array],default:100},indicator:{type:Boolean,default:!1},animation:{type:String,default:()=>i.default.animation,validator(e){return Object.keys(i.animation).includes(e)}},size:{type:String,default:()=>i.default.size,validator(e){return Object.keys(i.progress.size).includes(e)}},color:{type:String,default:()=>i.default.color,validator(e){return b.ui.colors.includes(e)}},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})}},setup(e){const{ui:r,attrs:y}=V("progress",h(e,"ui"),i,h(e,"class")),x=s(()=>t(r.value.indicator.container.base,r.value.indicator.container.width,r.value.indicator.container.transition)),w=s(()=>t(r.value.indicator.align,r.value.indicator.width,r.value.indicator.color,r.value.indicator.size[e.size])),k=s(()=>{var n;const a=[r.value.progress.base,r.value.progress.width,r.value.progress.size[e.size],r.value.progress.rounded,r.value.progress.track,r.value.progress.bar,(n=r.value.progress.color)==null?void 0:n.replaceAll("{color}",e.color),r.value.progress.background,r.value.progress.indeterminate.base,r.value.progress.indeterminate.rounded];return g.value&&a.push(r.value.animation[e.animation]),t(...a)}),c=s(()=>{var a;return t(r.value.steps.base,(a=r.value.steps.color)==null?void 0:a.replaceAll("{color}",e.color),r.value.steps.size[e.size])}),l=s(()=>t(r.value.step.base,r.value.step.align)),A=s(()=>t(r.value.step.active)),S=s(()=>t(r.value.step.first));function $(a){return a===Number(e.value)}function N(a){return a===0}function j(a){a=Number(a);const n=[l.value];return N(a)&&n.push(S.value),$(a)&&n.push(A.value),n.join(" ")}const g=s(()=>e.value===void 0||e.value===null),B=s(()=>Array.isArray(e.max)),p=s(()=>g.value?null:Array.isArray(e.max)?e.max.length-1:Number(e.max)),M=s(()=>{if(!g.value)switch(!0){case e.value<0:return 0;case e.value>p.value:return 100;default:return e.value/p.value*100}});return{ui:r,attrs:y,indicatorContainerClass:x,indicatorClass:w,progressClass:k,stepsClass:c,stepClasses:j,isIndeterminate:g,isSteps:B,realMax:p,percent:M}}}),U=["aria-valuemax","aria-valuenow"];function Y(e,r,y,x,w,k){return o(),u("div",{class:d(e.ui.wrapper),role:"progressbar"},[e.indicator||e.$slots.indicator?z(e.$slots,"indicator",E(f({key:0},{percent:e.percent})),()=>[e.isSteps?m("",!0):(o(),u("div",{key:0,class:d(e.indicatorContainerClass),style:D({width:`${e.percent}%`})},[C("div",{class:d(e.indicatorClass)},v(Math.round(e.percent))+"% ",3)],6))],!0):m("",!0),C("progress",f({"aria-valuemax":e.realMax,"aria-valuenow":e.value,class:e.progressClass},{value:e.value,max:e.realMax,...e.attrs}),v(e.percent!==void 0?`${Math.round(e.percent)}%`:void 0),17,U),e.isSteps?(o(),u("div",{key:1,class:d(e.stepsClass)},[(o(!0),u(P,null,J(e.max,(c,l)=>(o(),u("div",{key:l,class:d(e.stepClasses(l))},[z(e.$slots,`step-${l}`,f({ref_for:!0},{step:c}),()=>[L(v(c),1)],!0)],2))),128))],2)):m("",!0)],2)}const G=O(T,[["render",Y],["__scopeId","data-v-69c6813f"]]);export{G as _};