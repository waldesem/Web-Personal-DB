import{a as De,_ as $e}from"./B0poOYeU.js";import{_ as Te}from"./DFqDBo_N.js";import{r as D,ac as me,d as B,q as C,aa as Ce,$ as fe,ab as Pe,ak as L,ad as Ae,m as ve,at as Re,h as H,_ as ge,i as be,j as he,l as ye,t as G,K as Fe,N as re,ag as Oe,au as Ee,s as Ne,v as _e,ai as W,o as I,y as U,g as _,b as k,z as P,x as Q,f as $,c as A,al as Ue,T as ke,B as z,A as j,F as te,E as ae,aq as Be,D as E,C as V,a9 as we,L as je,w as Ve,M as Le,e as h,k as ze,G as He,u as se}from"./lgINOUnl.js";import{_ as Ke}from"./8sbBbPEZ.js";import{_ as qe}from"./4cJSv5k2.js";import{_ as Ie}from"./CeWA6jVp.js";import{e as Ze,o as x,w as Je,j as We,t as Ge,u as Qe,a as X,A as Y,i as le,s as Xe,l as Ye,N as ue,b as S,v as et,g as ie,_ as Me,O as tt,h as at}from"./BB-zBTUB.js";import{w as nt}from"./veLHMktU.js";import{u as lt}from"./Cl7nKP5_.js";import{_ as ot}from"./DhNX-qHN.js";import{_ as rt}from"./B67Mu-OL.js";import{u as st}from"./Cx_alqFP.js";import{a as ut}from"./C4qOVT1x.js";import"./DibbOkmJ.js";import"./BbT3jp1P.js";const it={wrapper:"relative inline-flex items-center justify-center flex-shrink-0",base:"absolute rounded-full ring-1 ring-white dark:ring-gray-900 flex items-center justify-center text-white dark:text-gray-900 font-medium whitespace-nowrap",background:"bg-{color}-500 dark:bg-{color}-400",position:{"top-right":"top-0 right-0","bottom-right":"bottom-0 right-0","top-left":"top-0 left-0","bottom-left":"bottom-0 left-0"},translate:{"top-right":"-translate-y-1/2 translate-x-1/2 transform","bottom-right":"translate-y-1/2 translate-x-1/2 transform","top-left":"-translate-y-1/2 -translate-x-1/2 transform","bottom-left":"translate-y-1/2 -translate-x-1/2 transform"},size:{"3xs":"h-[4px] min-w-[4px] text-[4px] p-px","2xs":"h-[5px] min-w-[5px] text-[5px] p-px",xs:"h-1.5 min-w-[0.375rem] text-[6px] p-px",sm:"h-2 min-w-[0.5rem] text-[7px] p-0.5",md:"h-2.5 min-w-[0.625rem] text-[8px] p-0.5",lg:"h-3 min-w-[0.75rem] text-[10px] p-0.5",xl:"h-3.5 min-w-[0.875rem] text-[11px] p-1","2xl":"h-4 min-w-[1rem] text-[12px] p-1","3xl":"h-5 min-w-[1.25rem] text-[14px] p-1"},default:{size:"sm",color:"primary",position:"top-right",inset:!1}};function de(e){return[e.screenX,e.screenY]}function dt(){let e=D([-1,-1]);return{wasMoved(s){let o=de(s);return e.value[0]===o[0]&&e.value[1]===o[1]?!1:(e.value=o,!0)},update(s){e.value=de(s)}}}function ct({container:e,accept:s,walk:o,enabled:d}){me(()=>{let p=e.value;if(!p||d!==void 0&&!d.value)return;let t=Ze(e);if(!t)return;let a=Object.assign(f=>s(f),{acceptNode:s}),u=t.createTreeWalker(p,NodeFilter.SHOW_ELEMENT,a,!1);for(;u.nextNode();)o(u.currentNode)})}function pt(e){throw new Error("Unexpected object: "+e)}var T=(e=>(e[e.First=0]="First",e[e.Previous=1]="Previous",e[e.Next=2]="Next",e[e.Last=3]="Last",e[e.Specific=4]="Specific",e[e.Nothing=5]="Nothing",e))(T||{});function mt(e,s){let o=s.resolveItems();if(o.length<=0)return null;let d=s.resolveActiveIndex(),p=d??-1;switch(e.focus){case 0:{for(let t=0;t<o.length;++t)if(!s.resolveDisabled(o[t],t,o))return t;return d}case 1:{p===-1&&(p=o.length);for(let t=p-1;t>=0;--t)if(!s.resolveDisabled(o[t],t,o))return t;return d}case 2:{for(let t=p+1;t<o.length;++t)if(!s.resolveDisabled(o[t],t,o))return t;return d}case 3:{for(let t=o.length-1;t>=0;--t)if(!s.resolveDisabled(o[t],t,o))return t;return d}case 4:{for(let t=0;t<o.length;++t)if(s.resolveId(o[t],t,o)===e.id)return t;return d}case 5:return null;default:pt(e)}}let ce=/([\u2700-\u27BF]|[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDD10-\uDDFF])/g;function pe(e){var s,o;let d=(s=e.innerText)!=null?s:"",p=e.cloneNode(!0);if(!(p instanceof HTMLElement))return d;let t=!1;for(let u of p.querySelectorAll('[hidden],[aria-hidden],[role="img"]'))u.remove(),t=!0;let a=t?(o=p.innerText)!=null?o:"":d;return ce.test(a)&&(a=a.replace(ce,"")),a}function ft(e){let s=e.getAttribute("aria-label");if(typeof s=="string")return s.trim();let o=e.getAttribute("aria-labelledby");if(o){let d=o.split(" ").map(p=>{let t=document.getElementById(p);if(t){let a=t.getAttribute("aria-label");return typeof a=="string"?a.trim():pe(t).trim()}return null}).filter(Boolean);if(d.length>0)return d.join(", ")}return pe(e).trim()}function vt(e){let s=D(""),o=D("");return()=>{let d=x(e);if(!d)return"";let p=d.innerText;if(s.value===p)return o.value;let t=ft(d).trim().toLowerCase();return s.value=p,o.value=t,t}}var gt=(e=>(e[e.Open=0]="Open",e[e.Closed=1]="Closed",e))(gt||{}),bt=(e=>(e[e.Pointer=0]="Pointer",e[e.Other=1]="Other",e))(bt||{});function ht(e){requestAnimationFrame(()=>requestAnimationFrame(e))}let Se=Symbol("MenuContext");function ee(e){let s=Ae(Se,null);if(s===null){let o=new Error(`<${e} /> is missing a parent <Menu /> component.`);throw Error.captureStackTrace&&Error.captureStackTrace(o,ee),o}return s}let yt=B({name:"Menu",props:{as:{type:[Object,String],default:"template"}},setup(e,{slots:s,attrs:o}){let d=D(1),p=D(null),t=D(null),a=D([]),u=D(""),f=D(null),b=D(1);function M(n=i=>i){let i=f.value!==null?a.value[f.value]:null,l=tt(n(a.value.slice()),c=>x(c.dataRef.domRef)),v=i?l.indexOf(i):null;return v===-1&&(v=null),{items:l,activeItemIndex:v}}let g={menuState:d,buttonRef:p,itemsRef:t,items:a,searchQuery:u,activeItemIndex:f,activationTrigger:b,closeMenu:()=>{d.value=1,f.value=null},openMenu:()=>d.value=0,goToItem(n,i,l){let v=M(),c=mt(n===T.Specific?{focus:T.Specific,id:i}:{focus:n},{resolveItems:()=>v.items,resolveActiveIndex:()=>v.activeItemIndex,resolveId:r=>r.id,resolveDisabled:r=>r.dataRef.disabled});u.value="",f.value=c,b.value=l??1,a.value=v.items},search(n){let i=u.value!==""?0:1;u.value+=n.toLowerCase();let l=(f.value!==null?a.value.slice(f.value+i).concat(a.value.slice(0,f.value+i)):a.value).find(c=>c.dataRef.textValue.startsWith(u.value)&&!c.dataRef.disabled),v=l?a.value.indexOf(l):-1;v===-1||v===f.value||(f.value=v,b.value=1)},clearSearch(){u.value=""},registerItem(n,i){let l=M(v=>[...v,{id:n,dataRef:i}]);a.value=l.items,f.value=l.activeItemIndex,b.value=1},unregisterItem(n){let i=M(l=>{let v=l.findIndex(c=>c.id===n);return v!==-1&&l.splice(v,1),l});a.value=i.items,f.value=i.activeItemIndex,b.value=1}};return nt([p,t],(n,i)=>{var l;g.closeMenu(),Je(i,We.Loose)||(n.preventDefault(),(l=x(p))==null||l.focus())},C(()=>d.value===0)),Ce(Se,g),Ge(C(()=>Qe(d.value,{0:X.Open,1:X.Closed}))),()=>{let n={open:d.value===0,close:g.closeMenu};return Y({ourProps:{},theirProps:e,slot:n,slots:s,attrs:o,name:"Menu"})}}}),_t=B({name:"MenuButton",props:{disabled:{type:Boolean,default:!1},as:{type:[Object,String],default:"button"},id:{type:String,default:null}},setup(e,{attrs:s,slots:o,expose:d}){var p;let t=(p=e.id)!=null?p:`headlessui-menu-button-${le()}`,a=ee("MenuButton");d({el:a.buttonRef,$el:a.buttonRef});function u(g){switch(g.key){case S.Space:case S.Enter:case S.ArrowDown:g.preventDefault(),g.stopPropagation(),a.openMenu(),L(()=>{var n;(n=x(a.itemsRef))==null||n.focus({preventScroll:!0}),a.goToItem(T.First)});break;case S.ArrowUp:g.preventDefault(),g.stopPropagation(),a.openMenu(),L(()=>{var n;(n=x(a.itemsRef))==null||n.focus({preventScroll:!0}),a.goToItem(T.Last)});break}}function f(g){switch(g.key){case S.Space:g.preventDefault();break}}function b(g){e.disabled||(a.menuState.value===0?(a.closeMenu(),L(()=>{var n;return(n=x(a.buttonRef))==null?void 0:n.focus({preventScroll:!0})})):(g.preventDefault(),a.openMenu(),ht(()=>{var n;return(n=x(a.itemsRef))==null?void 0:n.focus({preventScroll:!0})})))}let M=Xe(C(()=>({as:e.as,type:s.type})),a.buttonRef);return()=>{var g;let n={open:a.menuState.value===0},{...i}=e,l={ref:a.buttonRef,id:t,type:M.value,"aria-haspopup":"menu","aria-controls":(g=x(a.itemsRef))==null?void 0:g.id,"aria-expanded":a.menuState.value===0,onKeydown:u,onKeyup:f,onClick:b};return Y({ourProps:l,theirProps:i,slot:n,attrs:s,slots:o,name:"MenuButton"})}}}),kt=B({name:"MenuItems",props:{as:{type:[Object,String],default:"div"},static:{type:Boolean,default:!1},unmount:{type:Boolean,default:!0},id:{type:String,default:null}},setup(e,{attrs:s,slots:o,expose:d}){var p;let t=(p=e.id)!=null?p:`headlessui-menu-items-${le()}`,a=ee("MenuItems"),u=D(null);d({el:a.itemsRef,$el:a.itemsRef}),ct({container:C(()=>x(a.itemsRef)),enabled:C(()=>a.menuState.value===0),accept(n){return n.getAttribute("role")==="menuitem"?NodeFilter.FILTER_REJECT:n.hasAttribute("role")?NodeFilter.FILTER_SKIP:NodeFilter.FILTER_ACCEPT},walk(n){n.setAttribute("role","none")}});function f(n){var i;switch(u.value&&clearTimeout(u.value),n.key){case S.Space:if(a.searchQuery.value!=="")return n.preventDefault(),n.stopPropagation(),a.search(n.key);case S.Enter:if(n.preventDefault(),n.stopPropagation(),a.activeItemIndex.value!==null){let l=a.items.value[a.activeItemIndex.value];(i=x(l.dataRef.domRef))==null||i.click()}a.closeMenu(),Me(x(a.buttonRef));break;case S.ArrowDown:return n.preventDefault(),n.stopPropagation(),a.goToItem(T.Next);case S.ArrowUp:return n.preventDefault(),n.stopPropagation(),a.goToItem(T.Previous);case S.Home:case S.PageUp:return n.preventDefault(),n.stopPropagation(),a.goToItem(T.First);case S.End:case S.PageDown:return n.preventDefault(),n.stopPropagation(),a.goToItem(T.Last);case S.Escape:n.preventDefault(),n.stopPropagation(),a.closeMenu(),L(()=>{var l;return(l=x(a.buttonRef))==null?void 0:l.focus({preventScroll:!0})});break;case S.Tab:n.preventDefault(),n.stopPropagation(),a.closeMenu(),L(()=>et(x(a.buttonRef),n.shiftKey?ie.Previous:ie.Next));break;default:n.key.length===1&&(a.search(n.key),u.value=setTimeout(()=>a.clearSearch(),350));break}}function b(n){switch(n.key){case S.Space:n.preventDefault();break}}let M=Ye(),g=C(()=>M!==null?(M.value&X.Open)===X.Open:a.menuState.value===0);return()=>{var n,i;let l={open:a.menuState.value===0},{...v}=e,c={"aria-activedescendant":a.activeItemIndex.value===null||(n=a.items.value[a.activeItemIndex.value])==null?void 0:n.id,"aria-labelledby":(i=x(a.buttonRef))==null?void 0:i.id,id:t,onKeydown:f,onKeyup:b,role:"menu",tabIndex:0,ref:a.itemsRef};return Y({ourProps:c,theirProps:v,slot:l,attrs:s,slots:o,features:ue.RenderStrategy|ue.Static,visible:g.value,name:"MenuItems"})}}}),wt=B({name:"MenuItem",inheritAttrs:!1,props:{as:{type:[Object,String],default:"template"},disabled:{type:Boolean,default:!1},id:{type:String,default:null}},setup(e,{slots:s,attrs:o,expose:d}){var p;let t=(p=e.id)!=null?p:`headlessui-menu-item-${le()}`,a=ee("MenuItem"),u=D(null);d({el:u,$el:u});let f=C(()=>a.activeItemIndex.value!==null?a.items.value[a.activeItemIndex.value].id===t:!1),b=vt(u),M=C(()=>({disabled:e.disabled,get textValue(){return b()},domRef:u}));fe(()=>a.registerItem(t,M)),Pe(()=>a.unregisterItem(t)),me(()=>{a.menuState.value===0&&f.value&&a.activationTrigger.value!==0&&L(()=>{var r,y;return(y=(r=x(u))==null?void 0:r.scrollIntoView)==null?void 0:y.call(r,{block:"nearest"})})});function g(r){if(e.disabled)return r.preventDefault();a.closeMenu(),Me(x(a.buttonRef))}function n(){if(e.disabled)return a.goToItem(T.Nothing);a.goToItem(T.Specific,t)}let i=dt();function l(r){i.update(r)}function v(r){i.wasMoved(r)&&(e.disabled||f.value||a.goToItem(T.Specific,t,0))}function c(r){i.wasMoved(r)&&(e.disabled||f.value&&a.goToItem(T.Nothing))}return()=>{let{disabled:r,...y}=e,w={active:f.value,disabled:r,close:a.closeMenu};return Y({ourProps:{id:t,ref:u,role:"menuitem",tabIndex:r===!0?void 0:-1,"aria-disabled":r===!0?!0:void 0,onClick:g,onFocus:n,onPointerenter:l,onMouseenter:l,onPointermove:v,onMousemove:v,onPointerleave:c,onMouseleave:c},theirProps:{...o,...y},slot:w,attrs:o,slots:s,name:"MenuItem"})}}});const ne=ve(H.ui.strategy,H.ui.dropdown,Re),It=B({components:{HMenu:yt,HMenuButton:_t,HMenuItems:kt,HMenuItem:wt,UIcon:be,UAvatar:he,UKbd:Ie},inheritAttrs:!1,props:{items:{type:Array,default:()=>[]},mode:{type:String,default:"click",validator:e=>["click","hover"].includes(e)},open:{type:Boolean,default:void 0},disabled:{type:Boolean,default:!1},popper:{type:Object,default:()=>({})},openDelay:{type:Number,default:()=>ne.default.openDelay},closeDelay:{type:Number,default:()=>ne.default.closeDelay},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})}},emits:["update:open"],setup(e,{emit:s}){const{ui:o,attrs:d}=ye("dropdown",G(e,"ui"),ne,G(e,"class")),p=C(()=>Fe(e.mode==="hover"?{offsetDistance:0}:{},e.popper,o.value.popper)),[t,a]=lt(p.value),u=D(null);let f=null,b=null;fe(()=>{var y,w;const c=(y=t.value)==null?void 0:y.$.provides;if(!c)return;const r=Object.getOwnPropertySymbols(c);u.value=r.length&&c[r[0]],e.open&&((w=u.value)==null||w.openMenu())});const M=C(()=>{var w,F,O;if(e.mode!=="hover")return{};const c=((w=e.popper)==null?void 0:w.offsetDistance)||((F=o.value.popper)==null?void 0:F.offsetDistance)||8,r=(O=p.value.placement)==null?void 0:O.split("-")[0],y=`${c}px`;return r==="top"||r==="bottom"?{paddingTop:y,paddingBottom:y}:r==="left"||r==="right"?{paddingLeft:y,paddingRight:y}:{paddingTop:y,paddingBottom:y,paddingLeft:y,paddingRight:y}});function g(c){!c.cancelable||!u.value||(u.value.menuState===0?u.value.closeMenu():u.value.openMenu())}function n(){e.mode!=="hover"||!u.value||(b&&(clearTimeout(b),b=null),u.value.menuState!==0&&(f=f||setTimeout(()=>{u.value.openMenu&&u.value.openMenu(),f=null},e.openDelay)))}function i(){e.mode!=="hover"||!u.value||(f&&(clearTimeout(f),f=null),u.value.menuState!==1&&(b=b||setTimeout(()=>{u.value.closeMenu&&u.value.closeMenu(),b=null},e.closeDelay)))}function l(c,r,{href:y,navigate:w,close:F,isExternal:O}){r.click&&r.click(c),y&&!O&&(w(c),F())}re(()=>e.open,(c,r)=>{u.value&&(r===void 0||c===r||(c?u.value.openMenu():u.value.closeMenu()))}),re(()=>{var c;return(c=u.value)==null?void 0:c.menuState},(c,r)=>{r===void 0||c===r||s("update:open",c===0)});const v=we;return at(()=>Oe()),{ui:o,attrs:d,popper:p,trigger:t,container:a,containerStyle:M,onTouchStart:g,onMouseEnter:n,onMouseLeave:i,onClick:l,getNuxtLinkProps:Ee,twMerge:Ne,twJoin:_e,NuxtLink:v}}}),Mt=["disabled"];function St(e,s,o,d,p,t){const a=W("HMenuButton"),u=be,f=he,b=Ie,M=W("HMenuItem"),g=we,n=W("HMenuItems"),i=W("HMenu");return I(),U(i,z({as:"div",class:e.ui.wrapper},e.attrs,{onMouseleave:e.onMouseLeave}),{default:_(({open:l})=>[k(a,{ref:"trigger",as:"div",disabled:e.disabled,class:P(e.ui.trigger),role:"button",onMouseenter:e.onMouseEnter,onTouchstartPassive:e.onTouchStart},{default:_(()=>[Q(e.$slots,"default",{open:l,disabled:e.disabled},()=>[$("button",{disabled:e.disabled}," Open ",8,Mt)])]),_:2},1032,["disabled","class","onMouseenter","onTouchstartPassive"]),l&&e.items.length?(I(),A("div",{key:0,ref:"container",class:P([e.ui.container,e.ui.width]),style:Ue(e.containerStyle),onMouseenter:s[0]||(s[0]=(...v)=>e.onMouseEnter&&e.onMouseEnter(...v))},[k(ke,z({appear:""},e.ui.transition),{default:_(()=>[$("div",null,[e.popper.arrow?(I(),A("div",{key:0,"data-popper-arrow":"",class:P(Object.values(e.ui.arrow))},null,2)):j("",!0),k(n,{class:P([e.ui.base,e.ui.divide,e.ui.ring,e.ui.rounded,e.ui.shadow,e.ui.background,e.ui.height]),static:""},{default:_(()=>[(I(!0),A(te,null,ae(e.items,(v,c)=>(I(),A("div",{key:c,class:P(e.ui.padding)},[(I(!0),A(te,null,ae(v,(r,y)=>(I(),U(g,z({key:y,ref_for:!0},e.getNuxtLinkProps(r),{custom:""}),{default:_(({href:w,target:F,rel:O,navigate:K,isExternal:q,isActive:Z})=>[k(M,{disabled:r.disabled},{default:_(({active:m,disabled:R,close:xe})=>[(I(),U(Be(w?"a":"button"),{href:R?void 0:w,rel:O,target:F,class:P(e.twMerge(e.twJoin(e.ui.item.base,e.ui.item.padding,e.ui.item.size,e.ui.item.rounded,m||Z?e.ui.item.active:e.ui.item.inactive,R&&e.ui.item.disabled),r.class)),onClick:J=>e.onClick(J,r,{href:w,navigate:K,close:xe,isExternal:q})},{default:_(()=>[Q(e.$slots,r.slot||"item",{item:r},()=>{var J;return[r.icon?(I(),U(u,{key:0,name:r.icon,class:P(e.twMerge(e.twJoin(e.ui.item.icon.base,m||Z?e.ui.item.icon.active:e.ui.item.icon.inactive),r.iconClass))},null,8,["name","class"])):r.avatar?(I(),U(f,z({key:1,ref_for:!0},{size:e.ui.item.avatar.size,...r.avatar},{class:e.ui.item.avatar.base}),null,16,["class"])):j("",!0),$("span",{class:P(e.twMerge(e.ui.item.label,r.labelClass))},E(r.label),3),(J=r.shortcuts)!=null&&J.length?(I(),A("span",{key:2,class:P(e.ui.item.shortcuts)},[(I(!0),A(te,null,ae(r.shortcuts,oe=>(I(),U(b,{key:oe},{default:_(()=>[V(E(oe),1)]),_:2},1024))),128))],2)):j("",!0)]})]),_:2},1032,["href","rel","target","class","onClick"]))]),_:2},1032,["disabled"])]),_:2},1040))),128))],2))),128))]),_:3},8,["class"])])]),_:3},16)],38)):j("",!0)]),_:3},16,["class","onMouseleave"])}const xt=ge(It,[["render",St]]),N=ve(H.ui.strategy,H.ui.chip,it),Dt=B({inheritAttrs:!1,props:{size:{type:String,default:()=>N.default.size,validator(e){return Object.keys(N.size).includes(e)}},color:{type:String,default:()=>N.default.color,validator(e){return["gray",...H.ui.colors].includes(e)}},position:{type:String,default:()=>N.default.position,validator(e){return Object.keys(N.position).includes(e)}},text:{type:[String,Number],default:null},inset:{type:Boolean,default:()=>N.default.inset},show:{type:Boolean,default:!0},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})}},setup(e){const{ui:s,attrs:o}=ye("chip",G(e,"ui"),N,G(e,"class")),d=C(()=>_e(s.value.base,s.value.size[e.size],s.value.position[e.position],e.inset?null:s.value.translate[e.position],s.value.background.replaceAll("{color}",e.color)));return{ui:s,attrs:o,chipClass:d}}});function $t(e,s,o,d,p,t){return I(),A("div",z({class:e.ui.wrapper},e.attrs),[Q(e.$slots,"default"),e.show?(I(),A("span",{key:0,class:P(e.chipClass)},[Q(e.$slots,"content",{},()=>[V(E(e.text),1)])],2)):j("",!0)],16)}const Tt=ge(Dt,[["render",$t]]),Ct={class:"my-6"},Pt={class:"flex items-center justify-between mb-4"},At={class:"flex grid grid-cols-7 gap-3 border rounded p-3"},Rt={class:"col-span-2"},Ft={class:"col-span-2"},Ot={class:"col-span-2"},Et={class:"col-span-1"},Nt={class:"text-center"},Ut={class:"text-center"},Bt={class:"text-center"},ta=B({__name:"users",async setup(e){let s,o;const d=je(),p=st(),t=D({search:"",userId:"",region:"",role:"",users:[],form:{},collapsed:!1,viewDeleted:!1}),a=C(()=>t.value.users.filter(i=>i.deleted==t.value.viewDeleted)),{refresh:u,status:f}=([s,o]=Ve(async()=>ut("users",async()=>{t.value.users=await p("/api/users",{params:{search:t.value.search}})})),s=await s,o(),s);async function b(i,l=t.value.userId){confirm("Подтвердите действие!")&&(await p("/api/users/"+l,{params:{item:i}}),Object.assign(t.value,{userId:"",region:"",role:""}),await u(),d.add({icon:"i-heroicons-check-circle",title:"Информация",description:"Действие успешно выполнено",color:"green"}))}async function M(){await p("/api/users",{method:"POST",body:t.value.form}),t.value.collapsed=!1,Object.assign(t.value.form,{fullname:"",username:""}),await u(),d.add({icon:"i-heroicons-check-circle",title:"Информация",description:"Пользователь успешно добавлен",color:"green"})}const g=i=>{const l=[];return i.fullname&&!i.fullname.match(/^[а-яёЁА-Я-\s]+$/)&&l.push({path:"fullname",message:"Поле должно содержать только русские буквы"}),i.username&&!i.username.match(/^[a-zA-Z_\s]+$/)&&l.push({path:"username",message:"Поле должно содержать только латинские буквы и знаки подчеркивания"}),i.email&&!i.email.match(/^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/)&&l.push({path:"email",message:"Поле должно содержать корректную почту"}),l};Le(()=>t.value.search,()=>{u()},{debounce:500,maxWait:1e3});const n=[[{label:"Сбросить пароль",click:()=>b("drop")}],[{label:"Заблокировать/разблокировать",click:()=>b("block")}],[{label:"Удалить/восстановить",click:()=>b("delete")}]];return(i,l)=>{const v=$e,c=De,r=Te,y=ze,w=Ke,F=qe,O=xt,K=ot,q=Tt,Z=rt;return I(),A("div",null,[k(v,{div:"py-1",cls:"text-2xl text-gray-500",header:"ПОЛЬЗОВАТЕЛИ"}),$("div",Ct,[k(c,{modelValue:h(t).search,"onUpdate:modelValue":l[0]||(l[0]=m=>h(t).search=m),size:"lg",placeholder:"Поиск по имени пользователя"},null,8,["modelValue"])]),$("div",Pt,[k(r,{modelValue:h(t).viewDeleted,"onUpdate:modelValue":l[1]||(l[1]=m=>h(t).viewDeleted=m),label:"Показать удаленные"},null,8,["modelValue"]),k(y,{variant:"link",label:"Добавить пользователя",onClick:l[2]||(l[2]=m=>h(t).collapsed=!h(t).collapsed)})]),k(ke,{name:"slide-fade"},{default:_(()=>[h(t).collapsed?(I(),U(F,{key:0,state:h(t).form,validate:g,onSubmit:He(M,["prevent"])},{default:_(()=>[$("div",At,[$("div",Rt,[k(w,{required:"",class:"mb-3",name:"fullname"},{default:_(()=>[k(c,{modelValue:h(t).form.fullname,"onUpdate:modelValue":l[3]||(l[3]=m=>h(t).form.fullname=m),placeholder:"Имя пользователя"},null,8,["modelValue"])]),_:1})]),$("div",Ft,[k(w,{required:"",class:"mb-3",name:"username"},{default:_(()=>[k(c,{modelValue:h(t).form.username,"onUpdate:modelValue":l[4]||(l[4]=m=>h(t).form.username=m),placeholder:"Логин"},null,8,["modelValue"])]),_:1})]),$("div",Ot,[k(w,{required:"",class:"mb-3",name:"email"},{default:_(()=>[k(c,{modelValue:h(t).form.email,"onUpdate:modelValue":l[5]||(l[5]=m=>h(t).form.email=m),placeholder:"Email"},null,8,["modelValue"])]),_:1})]),$("div",Et,[k(y,{block:"",variant:"outline",color:"gray",label:"Создать",type:"submit"})])])]),_:1},8,["state"])):j("",!0)]),_:1}),k(Z,{loading:h(f)==="pending",progress:{color:"red",animation:"swing"},"empty-state":{icon:"i-heroicons-circle-stack-20-solid",label:"Пользователи не найдены."},columns:[{key:"id",label:"#"},{key:"fullname",label:"Пользователь"},{key:"username",label:"Логин"},{key:"email",label:"Email"},{key:"region",label:"Регион"},{key:"role",label:"Роль"},{key:"created",label:"Создан"},{key:"attempt",label:"Попытка"},{key:"blocked",label:"Блок"},{key:"pswd_create",label:"Обновлен"},{key:"change_pswd",label:"Изм.пароля"}],rows:h(a)},{"id-data":_(({row:m})=>[V(E(m.id),1)]),"fullname-data":_(({row:m})=>[V(E(m.fullname),1)]),"username-data":_(({row:m})=>[k(O,{items:n},{default:_(()=>[k(y,{variant:"link",label:m.username,onClick:R=>h(t).userId=m.id},null,8,["label","onClick"])]),_:2},1024)]),"region-data":_(({row:m})=>[k(K,{modelValue:h(t).region,"onUpdate:modelValue":l[6]||(l[6]=R=>h(t).region=R),placeholder:m.region,options:["Главный офис","РЦ Юг","РЦ Запад","РЦ Урал","РЦ Восток"],onChange:R=>b(h(t).region,m.id)},null,8,["modelValue","placeholder","onChange"])]),"role-data":_(({row:m})=>[k(K,{modelValue:h(t).role,"onUpdate:modelValue":l[7]||(l[7]=R=>h(t).role=R),placeholder:m.role,options:["admin","user","guest"],onChange:R=>b(h(t).role,m.id)},null,8,["modelValue","placeholder","onChange"])]),"created-data":_(({row:m})=>[V(E(h(se)(m.created).value),1)]),"attempt-data":_(({row:m})=>[$("div",Nt,E(m.attempt),1)]),"blocked-data":_(({row:m})=>[$("div",Ut,[k(q,{size:"2xl",color:m.blocked?"red":"green"},null,8,["color"])])]),"pswd_create-data":_(({row:m})=>[V(E(h(se)(m.pswd_create).value),1)]),"change_pswd-data":_(({row:m})=>[$("div",Bt,[k(q,{size:"2xl",color:m.change_pswd?"red":"green"},null,8,["color"])])]),_:1},8,["loading","rows"])])}}});export{ta as default};
