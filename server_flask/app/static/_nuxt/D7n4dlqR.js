import{m as u,k as o,_ as c,g as m,s as f,v as n,x as d,z as x,o as i,c as l,A as p,B as g,d as h,t as y,C as b,D as w}from"./DqpPj892.js";const k={wrapper:"relative inline-flex items-center justify-center flex-shrink-0",base:"absolute rounded-full ring-1 ring-white dark:ring-gray-900 flex items-center justify-center text-white dark:text-gray-900 font-medium whitespace-nowrap",background:"bg-{color}-500 dark:bg-{color}-400",position:{"top-right":"top-0 right-0","bottom-right":"bottom-0 right-0","top-left":"top-0 left-0","bottom-left":"bottom-0 left-0"},translate:{"top-right":"-translate-y-1/2 translate-x-1/2 transform","bottom-right":"translate-y-1/2 translate-x-1/2 transform","top-left":"-translate-y-1/2 -translate-x-1/2 transform","bottom-left":"translate-y-1/2 -translate-x-1/2 transform"},size:{"3xs":"h-[4px] min-w-[4px] text-[4px] p-px","2xs":"h-[5px] min-w-[5px] text-[5px] p-px",xs:"h-1.5 min-w-[0.375rem] text-[6px] p-px",sm:"h-2 min-w-[0.5rem] text-[7px] p-0.5",md:"h-2.5 min-w-[0.625rem] text-[8px] p-0.5",lg:"h-3 min-w-[0.75rem] text-[10px] p-0.5",xl:"h-3.5 min-w-[0.875rem] text-[11px] p-1","2xl":"h-4 min-w-[1rem] text-[12px] p-1","3xl":"h-5 min-w-[1.25rem] text-[14px] p-1"},default:{size:"sm",color:"primary",position:"top-right",inset:!1}},a=u(o.ui.strategy,o.ui.chip,k),v=m({inheritAttrs:!1,props:{size:{type:String,default:()=>a.default.size,validator(t){return Object.keys(a.size).includes(t)}},color:{type:String,default:()=>a.default.color,validator(t){return["gray",...o.ui.colors].includes(t)}},position:{type:String,default:()=>a.default.position,validator(t){return Object.keys(a.position).includes(t)}},text:{type:[String,Number],default:null},inset:{type:Boolean,default:()=>a.default.inset},show:{type:Boolean,default:!0},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})}},setup(t){const{ui:e,attrs:r}=f("chip",n(t,"ui"),a,n(t,"class")),s=d(()=>x(e.value.base,e.value.size[t.size],e.value.position[t.position],t.inset?null:e.value.translate[t.position],e.value.background.replaceAll("{color}",t.color)));return{ui:e,attrs:r,chipClass:s}}});function z(t,e,r,s,C,S){return i(),l("div",w({class:t.ui.wrapper},t.attrs),[p(t.$slots,"default"),t.show?(i(),l("span",{key:0,class:g(t.chipClass)},[p(t.$slots,"content",{},()=>[h(y(t.text),1)])],2)):b("",!0)],16)}const j=c(v,[["render",z]]);function $(t,e){let r;return function(...s){r&&clearTimeout(r),r=setTimeout(()=>{t.apply(this,s),r=void 0},e)}}export{j as _,$ as d};
