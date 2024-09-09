import{m as M,k as h,_ as D,g as z,l as C,n as U,s as L,v as x,x as m,y as T,z as _,o as s,c as l,a as n,B as g,F as O,A as p,t as E,i as c,D as v,C as d,ad as I,ae as K,E as V,b as w,w as F,d as q,U as G,ao as R,j as N,q as W,ag as Q}from"./IZgRZ49_.js";import{_ as P}from"./CNnCnols.js";import{a as X,s as Y,c as Z}from"./BGhzAh6M.js";const ee={base:"mx-auto",padding:"px-4 sm:px-6 lg:px-8",constrained:"max-w-7xl"},ae={wrapper:{base:"flex items-center align-center text-center",horizontal:"w-full flex-row",vertical:"flex-col"},container:{base:"font-medium text-gray-700 dark:text-gray-200 flex",horizontal:"mx-3 whitespace-nowrap",vertical:"my-2"},border:{base:"flex border-gray-200 dark:border-gray-800",horizontal:"w-full",vertical:"h-full",size:{horizontal:{"2xs":"border-t",xs:"border-t-[2px]",sm:"border-t-[3px]",md:"border-t-[4px]",lg:"border-t-[5px]",xl:"border-t-[6px]"},vertical:{"2xs":"border-s",xs:"border-s-[2px]",sm:"border-s-[3px]",md:"border-s-[4px]",lg:"border-s-[5px]",xl:"border-s-[6px]"}},type:{solid:"border-solid",dotted:"border-dotted",dashed:"border-dashed"}},icon:{base:"flex-shrink-0 w-5 h-5"},avatar:{base:"flex-shrink-0",size:"2xs"},label:"text-sm",default:{size:"2xs"}},re={wrapper:"relative",base:"group relative flex items-center gap-1.5 focus:outline-none focus-visible:outline-none dark:focus-visible:outline-none focus-visible:before:ring-inset focus-visible:before:ring-1 focus-visible:before:ring-primary-500 dark:focus-visible:before:ring-primary-400 before:absolute before:inset-px before:rounded-md disabled:cursor-not-allowed disabled:opacity-75",ring:"focus-visible:ring-inset focus-visible:ring-2 focus-visible:ring-primary-500 dark:focus-visible:ring-primary-400",padding:"px-2.5 py-1.5",width:"w-full",rounded:"rounded-md",font:"font-medium",size:"text-sm",active:"text-gray-900 dark:text-white before:bg-gray-100 dark:before:bg-gray-800",inactive:"text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:before:bg-gray-50 dark:hover:before:bg-gray-800/50",label:"truncate relative",icon:{base:"flex-shrink-0 w-5 h-5 relative",active:"text-gray-700 dark:text-gray-200",inactive:"text-gray-400 dark:text-gray-500 group-hover:text-gray-700 dark:group-hover:text-gray-200"},avatar:{base:"flex-shrink-0",size:"2xs"},badge:{base:"flex-shrink-0 ml-auto relative rounded",color:"gray",variant:"solid",size:"xs"},divider:{wrapper:{base:"p-2"}}},$=M(h.ui.strategy,h.ui.divider,ae),se=z({components:{UIcon:C,UAvatar:U},inheritAttrs:!1,props:{label:{type:String,default:null},icon:{type:String,default:null},avatar:{type:Object,default:null},size:{type:String,default:()=>$.default.size,validator(e){return Object.keys($.border.size.horizontal).includes(e)||Object.keys($.border.size.vertical).includes(e)}},orientation:{type:String,default:"horizontal",validator:e=>["horizontal","vertical"].includes(e)},type:{type:String,default:"solid",validator:e=>["solid","dotted","dashed"].includes(e)},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})}},setup(e){const{ui:a,attrs:o}=L("divider",x(e,"ui"),$),i=m(()=>T(_(a.value.wrapper.base,a.value.wrapper[e.orientation]),e.class)),u=m(()=>_(a.value.container.base,a.value.container[e.orientation])),y=m(()=>_(a.value.border.base,a.value.border[e.orientation],a.value.border.size[e.orientation][e.size],a.value.border.type[e.type]));return{ui:a,attrs:o,wrapperClass:i,containerClass:u,borderClass:y}}});function te(e,a,o,i,u,y){const t=C,b=U;return s(),l("div",v({class:e.wrapperClass},e.attrs),[n("div",{class:g(e.borderClass)},null,2),e.label||e.icon||e.avatar||e.$slots.default?(s(),l(O,{key:0},[n("div",{class:g(e.containerClass)},[p(e.$slots,"default",{},()=>[e.label?(s(),l("span",{key:0,class:g(e.ui.label)},E(e.label),3)):e.icon?(s(),c(t,{key:1,name:e.icon,class:g(e.ui.icon.base)},null,8,["name","class"])):e.avatar?(s(),c(b,v({key:2},{size:e.ui.avatar.size,...e.avatar},{class:e.ui.avatar.base}),null,16,["class"])):d("",!0)])],2),n("div",{class:g(e.borderClass)},null,2)],64)):d("",!0)],16)}const H=D(se,[["render",te]]),oe=M(h.ui.strategy,h.ui.verticalNavigation,re),ne=z({components:{UIcon:C,UAvatar:U,UBadge:P,ULink:I,UDivider:H},inheritAttrs:!1,props:{links:{type:Array,default:()=>[]},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})}},setup(e){const{ui:a,attrs:o}=L("verticalNavigation",x(e,"ui"),oe,x(e,"class")),i=m(()=>Array.isArray(e.links[0])?e.links:[e.links]);return{ui:a,attrs:o,sections:i,getULinkProps:K,twMerge:T,twJoin:_}}}),ie={key:0,class:"sr-only"};function le(e,a,o,i,u,y){const t=U,b=C,k=P,A=I,S=H;return s(),l("nav",v({class:e.ui.wrapper},e.attrs),[(s(!0),l(O,null,V(e.sections,(j,B)=>(s(),l("ul",{key:`section${B}`},[(s(!0),l(O,null,V(j,(r,J)=>(s(),l("li",{key:`section${B}-${J}`},[w(A,v({ref_for:!0},e.getULinkProps(r),{class:[e.ui.base,e.ui.padding,e.ui.width,e.ui.ring,e.ui.rounded,e.ui.font,e.ui.size],"active-class":e.ui.active,"inactive-class":e.ui.inactive,onClick:r.click,onKeyup:a[0]||(a[0]=G(f=>f.target.blur(),["enter"]))}),{default:F(({isActive:f})=>[p(e.$slots,"avatar",{link:r,isActive:f},()=>[r.avatar?(s(),c(t,v({key:0,ref_for:!0},{size:e.ui.avatar.size,...r.avatar},{class:[e.ui.avatar.base]}),null,16,["class"])):d("",!0)]),p(e.$slots,"icon",{link:r,isActive:f},()=>[r.icon?(s(),c(b,{key:0,name:r.icon,class:g(e.twMerge(e.twJoin(e.ui.icon.base,f?e.ui.icon.active:e.ui.icon.inactive),r.iconClass))},null,8,["name","class"])):d("",!0)]),p(e.$slots,"default",{link:r,isActive:f},()=>[r.label?(s(),l("span",{key:0,class:g(e.twMerge(e.ui.label,r.labelClass))},[f?(s(),l("span",ie," Current page: ")):d("",!0),q(" "+E(r.label),1)],2)):d("",!0)]),p(e.$slots,"badge",{link:r,isActive:f},()=>[r.badge?(s(),c(k,v({key:0,ref_for:!0},{size:e.ui.badge.size,color:e.ui.badge.color,variant:e.ui.badge.variant,...typeof r.badge=="string"||typeof r.badge=="number"?{label:r.badge}:r.badge},{class:e.ui.badge.base}),null,16,["class"])):d("",!0)])]),_:2},1040,["class","active-class","inactive-class","onClick"])]))),128)),B<e.sections.length-1?(s(),c(S,{key:0,ui:e.ui.divider},null,8,["ui"])):d("",!0)]))),128))],16)}const ue=D(ne,[["render",le]]),de=M(h.ui.strategy,h.ui.container,ee),ce=z({inheritAttrs:!1,props:{as:{type:String,default:"div"},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})}},setup(e){const{ui:a,attrs:o}=L("container",x(e,"ui"),de),i=m(()=>T(_(a.value.base,a.value.padding,a.value.constrained),e.class));return{ui:a,attrs:o,containerClass:i}}});function be(e,a,o,i,u,y){return s(),c(R(e.as),v({class:e.containerClass},e.attrs),{default:F(()=>[p(e.$slots,"default")]),_:3},16,["class"])}const fe=D(ce,[["render",be]]),ge={class:"flex flex-col h-screen"},pe={class:"sticky py-8"},ve={class:"flex justify-between grid grid-cols-12 gap-3"},ye=n("div",{class:"col-span-2"},[n("h3",{class:"text-2xl text-red-800 font-bold"},"STAFFSEC FINTECH")],-1),me={class:"col-span-10 relative"},he={class:"flex flex-grow flex-col grid grid-cols-12 gap-3",style:{"padding-bottom":"5vh"}},ke={class:"col-span-2 py-3"},_e={class:"col-span-10 py-8"},$e=n("footer",{class:"flex justify-center py-3 bg-white border-t dark:bg-gray-800 dark:border-gray-700"},[n("a",{class:"text-gray-500",href:"https://github.com/waldesem/Web-Personal-DB",target:"_blank"},"GitHub")],-1),Ce=z({__name:"menu",setup(e){const a=X(),o=Y();async function i(){confirm("Вы действительно хотите выйти?")&&(Q("/login"),Z.value="")}const u=[[{label:"Кандидаты",to:"/persons"}],[{label:"Создать",to:"/resume"}],[{label:"Информация",to:"/info"}],[{label:"Пользователи",to:"/users"}],[{label:"Выход",to:"/login",click:()=>i()}]],y=m(()=>o.user.value.role!==a.classes.value.roles.user?u.filter(t=>t[0].to!=="/resume"):o.user.value.role!==a.classes.value.roles.admin?u.filter(t=>t[0].to!=="/users"):o.user.value.role!==a.classes.value.roles.guest?u.filter(t=>t[0].to!=="/users"&&t[0].to!=="/resume"):u);return(t,b)=>{const k=W,A=ue,S=fe;return s(),c(S,{ui:{constrained:"max-w-none",padding:"px-4 sm:px-6 lg:px-12"}},{default:F(()=>[n("div",ge,[n("header",pe,[n("div",ve,[ye,n("div",me,[w(k,{class:"absolute top-0 right-0",icon:"i-heroicons-moon",variant:t.$colorMode.preference=="dark"?"soft":"ghost",onClick:b[0]||(b[0]=j=>t.$colorMode.preference="dark")},null,8,["variant"]),w(k,{class:"absolute top-0 right-12",icon:"i-heroicons-sun",variant:t.$colorMode.preference=="light"?"soft":"ghost",onClick:b[1]||(b[1]=j=>t.$colorMode.preference="light")},null,8,["variant"]),N(o).user.value.username?(s(),c(k,{key:0,class:"absolute top-0 right-24",icon:"i-heroicons-user",variant:"ghost",title:N(o).user.value.username},null,8,["title"])):d("",!0)])])]),n("div",he,[n("div",ke,[w(A,{links:N(y),ui:{active:"text-red-900 dark:text-white before:bg-gray-0 dark:before:bg-gray-0",inactive:"text-gray-500 dark:text-gray-400 hover:text-red-600 dark:hover:text-white hover:before:bg-gray-0 dark:hover:before:bg-gray-800/50",size:"text-xl text-primary mt-4"}},null,8,["links"])]),n("div",_e,[p(t.$slots,"default")])]),$e])]),_:3})}}});export{Ce as _};