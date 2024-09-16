import{u as xe,_ as Fe,b as Oe,a as Le}from"./B8ZzhQbn.js";import{o as M,u as Ne,A as Z,I as se,s as Ue,N as de,a as $,c as Ve,l as je,_ as Be}from"./aOhuXCbN.js";import{P as Y,z as D,q as C,g as N,M as He,N as ye,O as ze,Z as V,Q as Ke,m as he,j as G,_ as _e,k as we,l as re,r as ke,s as Ie,o as S,c as F,E as ue,d as U,t as L,v as j,at as qe,B as Me,C as Se,a6 as Je,S as ce,au as Qe,V as Q,i as O,w as _,b as k,G as E,a as T,$ as We,X as $e,H as B,F as te,y as ne,x as Ge,e as De,L as Xe,h as Ze,A as h,I as pe,D as Ye}from"./B_4c7bjE.js";import{_ as et}from"./2VsBTAQu.js";import{c as Te,w as Pe,h as Ce,a as tt,t as nt,i as X,l as at,v as lt,N as me,_ as Ee,O as ot}from"./BD6kfv-O.js";import{_ as rt}from"./UIKXIBFg.js";import{d as ut,_ as st}from"./CyAbWRfo.js";import{_ as it}from"./C6Jsogy6.js";import{_ as dt}from"./B_ysnhc0.js";import{s as ct,b as ae,c as fe}from"./DupJrylg.js";import"./CyEoj2gn.js";import"./B-pH45DD.js";import"./HQhQkk_r.js";const pt={base:"inline-flex items-center justify-center text-gray-900 dark:text-white",padding:"px-1",size:{xs:"h-4 min-w-[16px] text-[10px]",sm:"h-5 min-w-[20px] text-[11px]",md:"h-6 min-w-[24px] text-[12px]"},rounded:"rounded",font:"font-medium font-sans",background:"bg-gray-100 dark:bg-gray-800",ring:"ring-1 ring-gray-300 dark:ring-gray-700 ring-inset",default:{size:"sm"}};function mt(){return/iPhone/gi.test(window.navigator.platform)||/Mac/gi.test(window.navigator.platform)&&window.navigator.maxTouchPoints>0}function ft(){return/Android/gi.test(window.navigator.userAgent)}function vt(){return mt()||ft()}function W(e,o,l){Te.isServer||Y(i=>{document.addEventListener(e,o,l),i(()=>document.removeEventListener(e,o,l))})}function gt(e,o,l){Te.isServer||Y(i=>{window.addEventListener(e,o,l),i(()=>window.removeEventListener(e,o,l))})}function bt(e,o,l=C(()=>!0)){function i(n,t){if(!l.value||n.defaultPrevented)return;let r=t(n);if(r===null||!r.getRootNode().contains(r))return;let p=function v(b){return typeof b=="function"?v(b()):Array.isArray(b)||b instanceof Set?b:[b]}(e);for(let v of p){if(v===null)continue;let b=v instanceof HTMLElement?v:M(v);if(b!=null&&b.contains(r)||n.composed&&n.composedPath().includes(b))return}return!Pe(r,Ce.Loose)&&r.tabIndex!==-1&&n.preventDefault(),o(n,r)}let d=D(null);W("pointerdown",n=>{var t,r;l.value&&(d.value=((r=(t=n.composedPath)==null?void 0:t.call(n))==null?void 0:r[0])||n.target)},!0),W("mousedown",n=>{var t,r;l.value&&(d.value=((r=(t=n.composedPath)==null?void 0:t.call(n))==null?void 0:r[0])||n.target)},!0),W("click",n=>{vt()||d.value&&(i(n,()=>d.value),d.value=null)},!0),W("touchend",n=>i(n,()=>n.target instanceof HTMLElement?n.target:null),!0),gt("blur",n=>i(n,()=>window.document.activeElement instanceof HTMLIFrameElement?window.document.activeElement:null),!0)}function ve(e){return[e.screenX,e.screenY]}function yt(){let e=D([-1,-1]);return{wasMoved(o){let l=ve(o);return e.value[0]===l[0]&&e.value[1]===l[1]?!1:(e.value=l,!0)},update(o){e.value=ve(o)}}}function ht({container:e,accept:o,walk:l,enabled:i}){Y(()=>{let d=e.value;if(!d||i!==void 0&&!i.value)return;let n=tt(e);if(!n)return;let t=Object.assign(p=>o(p),{acceptNode:o}),r=n.createTreeWalker(d,NodeFilter.SHOW_ELEMENT,t,!1);for(;r.nextNode();)l(r.currentNode)})}function _t(e){throw new Error("Unexpected object: "+e)}var P=(e=>(e[e.First=0]="First",e[e.Previous=1]="Previous",e[e.Next=2]="Next",e[e.Last=3]="Last",e[e.Specific=4]="Specific",e[e.Nothing=5]="Nothing",e))(P||{});function wt(e,o){let l=o.resolveItems();if(l.length<=0)return null;let i=o.resolveActiveIndex(),d=i??-1;switch(e.focus){case 0:{for(let n=0;n<l.length;++n)if(!o.resolveDisabled(l[n],n,l))return n;return i}case 1:{d===-1&&(d=l.length);for(let n=d-1;n>=0;--n)if(!o.resolveDisabled(l[n],n,l))return n;return i}case 2:{for(let n=d+1;n<l.length;++n)if(!o.resolveDisabled(l[n],n,l))return n;return i}case 3:{for(let n=l.length-1;n>=0;--n)if(!o.resolveDisabled(l[n],n,l))return n;return i}case 4:{for(let n=0;n<l.length;++n)if(o.resolveId(l[n],n,l)===e.id)return n;return i}case 5:return null;default:_t(e)}}let ge=/([\u2700-\u27BF]|[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDD10-\uDDFF])/g;function be(e){var o,l;let i=(o=e.innerText)!=null?o:"",d=e.cloneNode(!0);if(!(d instanceof HTMLElement))return i;let n=!1;for(let r of d.querySelectorAll('[hidden],[aria-hidden],[role="img"]'))r.remove(),n=!0;let t=n?(l=d.innerText)!=null?l:"":i;return ge.test(t)&&(t=t.replace(ge,"")),t}function kt(e){let o=e.getAttribute("aria-label");if(typeof o=="string")return o.trim();let l=e.getAttribute("aria-labelledby");if(l){let i=l.split(" ").map(d=>{let n=document.getElementById(d);if(n){let t=n.getAttribute("aria-label");return typeof t=="string"?t.trim():be(n).trim()}return null}).filter(Boolean);if(i.length>0)return i.join(", ")}return be(e).trim()}function It(e){let o=D(""),l=D("");return()=>{let i=M(e);if(!i)return"";let d=i.innerText;if(o.value===d)return l.value;let n=kt(i).trim().toLowerCase();return o.value=d,l.value=n,n}}var Mt=(e=>(e[e.Open=0]="Open",e[e.Closed=1]="Closed",e))(Mt||{}),St=(e=>(e[e.Pointer=0]="Pointer",e[e.Other=1]="Other",e))(St||{});function $t(e){requestAnimationFrame(()=>requestAnimationFrame(e))}let Re=Symbol("MenuContext");function ee(e){let o=Ke(Re,null);if(o===null){let l=new Error(`<${e} /> is missing a parent <Menu /> component.`);throw Error.captureStackTrace&&Error.captureStackTrace(l,ee),l}return o}let Dt=N({name:"Menu",props:{as:{type:[Object,String],default:"template"}},setup(e,{slots:o,attrs:l}){let i=D(1),d=D(null),n=D(null),t=D([]),r=D(""),p=D(null),v=D(1);function b(a=m=>m){let m=p.value!==null?t.value[p.value]:null,u=ot(a(t.value.slice()),c=>M(c.dataRef.domRef)),g=m?u.indexOf(m):null;return g===-1&&(g=null),{items:u,activeItemIndex:g}}let y={menuState:i,buttonRef:d,itemsRef:n,items:t,searchQuery:r,activeItemIndex:p,activationTrigger:v,closeMenu:()=>{i.value=1,p.value=null},openMenu:()=>i.value=0,goToItem(a,m,u){let g=b(),c=wt(a===P.Specific?{focus:P.Specific,id:m}:{focus:a},{resolveItems:()=>g.items,resolveActiveIndex:()=>g.activeItemIndex,resolveId:s=>s.id,resolveDisabled:s=>s.dataRef.disabled});r.value="",p.value=c,v.value=u??1,t.value=g.items},search(a){let m=r.value!==""?0:1;r.value+=a.toLowerCase();let u=(p.value!==null?t.value.slice(p.value+m).concat(t.value.slice(0,p.value+m)):t.value).find(c=>c.dataRef.textValue.startsWith(r.value)&&!c.dataRef.disabled),g=u?t.value.indexOf(u):-1;g===-1||g===p.value||(p.value=g,v.value=1)},clearSearch(){r.value=""},registerItem(a,m){let u=b(g=>[...g,{id:a,dataRef:m}]);t.value=u.items,p.value=u.activeItemIndex,v.value=1},unregisterItem(a){let m=b(u=>{let g=u.findIndex(c=>c.id===a);return g!==-1&&u.splice(g,1),u});t.value=m.items,p.value=m.activeItemIndex,v.value=1}};return bt([d,n],(a,m)=>{var u;y.closeMenu(),Pe(m,Ce.Loose)||(a.preventDefault(),(u=M(d))==null||u.focus())},C(()=>i.value===0)),He(Re,y),nt(C(()=>Ne(i.value,{0:X.Open,1:X.Closed}))),()=>{let a={open:i.value===0,close:y.closeMenu};return Z({ourProps:{},theirProps:e,slot:a,slots:o,attrs:l,name:"Menu"})}}}),Tt=N({name:"MenuButton",props:{disabled:{type:Boolean,default:!1},as:{type:[Object,String],default:"button"},id:{type:String,default:null}},setup(e,{attrs:o,slots:l,expose:i}){var d;let n=(d=e.id)!=null?d:`headlessui-menu-button-${se()}`,t=ee("MenuButton");i({el:t.buttonRef,$el:t.buttonRef});function r(y){switch(y.key){case $.Space:case $.Enter:case $.ArrowDown:y.preventDefault(),y.stopPropagation(),t.openMenu(),V(()=>{var a;(a=M(t.itemsRef))==null||a.focus({preventScroll:!0}),t.goToItem(P.First)});break;case $.ArrowUp:y.preventDefault(),y.stopPropagation(),t.openMenu(),V(()=>{var a;(a=M(t.itemsRef))==null||a.focus({preventScroll:!0}),t.goToItem(P.Last)});break}}function p(y){switch(y.key){case $.Space:y.preventDefault();break}}function v(y){e.disabled||(t.menuState.value===0?(t.closeMenu(),V(()=>{var a;return(a=M(t.buttonRef))==null?void 0:a.focus({preventScroll:!0})})):(y.preventDefault(),t.openMenu(),$t(()=>{var a;return(a=M(t.itemsRef))==null?void 0:a.focus({preventScroll:!0})})))}let b=Ue(C(()=>({as:e.as,type:o.type})),t.buttonRef);return()=>{var y;let a={open:t.menuState.value===0},{...m}=e,u={ref:t.buttonRef,id:n,type:b.value,"aria-haspopup":"menu","aria-controls":(y=M(t.itemsRef))==null?void 0:y.id,"aria-expanded":t.menuState.value===0,onKeydown:r,onKeyup:p,onClick:v};return Z({ourProps:u,theirProps:m,slot:a,attrs:o,slots:l,name:"MenuButton"})}}}),Pt=N({name:"MenuItems",props:{as:{type:[Object,String],default:"div"},static:{type:Boolean,default:!1},unmount:{type:Boolean,default:!0},id:{type:String,default:null}},setup(e,{attrs:o,slots:l,expose:i}){var d;let n=(d=e.id)!=null?d:`headlessui-menu-items-${se()}`,t=ee("MenuItems"),r=D(null);i({el:t.itemsRef,$el:t.itemsRef}),ht({container:C(()=>M(t.itemsRef)),enabled:C(()=>t.menuState.value===0),accept(a){return a.getAttribute("role")==="menuitem"?NodeFilter.FILTER_REJECT:a.hasAttribute("role")?NodeFilter.FILTER_SKIP:NodeFilter.FILTER_ACCEPT},walk(a){a.setAttribute("role","none")}});function p(a){var m;switch(r.value&&clearTimeout(r.value),a.key){case $.Space:if(t.searchQuery.value!=="")return a.preventDefault(),a.stopPropagation(),t.search(a.key);case $.Enter:if(a.preventDefault(),a.stopPropagation(),t.activeItemIndex.value!==null){let u=t.items.value[t.activeItemIndex.value];(m=M(u.dataRef.domRef))==null||m.click()}t.closeMenu(),Ee(M(t.buttonRef));break;case $.ArrowDown:return a.preventDefault(),a.stopPropagation(),t.goToItem(P.Next);case $.ArrowUp:return a.preventDefault(),a.stopPropagation(),t.goToItem(P.Previous);case $.Home:case $.PageUp:return a.preventDefault(),a.stopPropagation(),t.goToItem(P.First);case $.End:case $.PageDown:return a.preventDefault(),a.stopPropagation(),t.goToItem(P.Last);case $.Escape:a.preventDefault(),a.stopPropagation(),t.closeMenu(),V(()=>{var u;return(u=M(t.buttonRef))==null?void 0:u.focus({preventScroll:!0})});break;case $.Tab:a.preventDefault(),a.stopPropagation(),t.closeMenu(),V(()=>lt(M(t.buttonRef),a.shiftKey?me.Previous:me.Next));break;default:a.key.length===1&&(t.search(a.key),r.value=setTimeout(()=>t.clearSearch(),350));break}}function v(a){switch(a.key){case $.Space:a.preventDefault();break}}let b=at(),y=C(()=>b!==null?(b.value&X.Open)===X.Open:t.menuState.value===0);return()=>{var a,m;let u={open:t.menuState.value===0},{...g}=e,c={"aria-activedescendant":t.activeItemIndex.value===null||(a=t.items.value[t.activeItemIndex.value])==null?void 0:a.id,"aria-labelledby":(m=M(t.buttonRef))==null?void 0:m.id,id:n,onKeydown:p,onKeyup:v,role:"menu",tabIndex:0,ref:t.itemsRef};return Z({ourProps:c,theirProps:g,slot:u,attrs:o,slots:l,features:de.RenderStrategy|de.Static,visible:y.value,name:"MenuItems"})}}}),Ct=N({name:"MenuItem",inheritAttrs:!1,props:{as:{type:[Object,String],default:"template"},disabled:{type:Boolean,default:!1},id:{type:String,default:null}},setup(e,{slots:o,attrs:l,expose:i}){var d;let n=(d=e.id)!=null?d:`headlessui-menu-item-${se()}`,t=ee("MenuItem"),r=D(null);i({el:r,$el:r});let p=C(()=>t.activeItemIndex.value!==null?t.items.value[t.activeItemIndex.value].id===n:!1),v=It(r),b=C(()=>({disabled:e.disabled,get textValue(){return v()},domRef:r}));ye(()=>t.registerItem(n,b)),ze(()=>t.unregisterItem(n)),Y(()=>{t.menuState.value===0&&p.value&&t.activationTrigger.value!==0&&V(()=>{var s,w;return(w=(s=M(r))==null?void 0:s.scrollIntoView)==null?void 0:w.call(s,{block:"nearest"})})});function y(s){if(e.disabled)return s.preventDefault();t.closeMenu(),Ee(M(t.buttonRef))}function a(){if(e.disabled)return t.goToItem(P.Nothing);t.goToItem(P.Specific,n)}let m=yt();function u(s){m.update(s)}function g(s){m.wasMoved(s)&&(e.disabled||p.value||t.goToItem(P.Specific,n,0))}function c(s){m.wasMoved(s)&&(e.disabled||p.value&&t.goToItem(P.Nothing))}return()=>{let{disabled:s,...w}=e,I={active:p.value,disabled:s,close:t.closeMenu};return Z({ourProps:{id:n,ref:r,role:"menuitem",tabIndex:s===!0?void 0:-1,"aria-disabled":s===!0?!0:void 0,onClick:y,onFocus:a,onPointerenter:u,onMouseenter:u,onPointermove:g,onMousemove:g,onPointerleave:c,onMouseleave:c},theirProps:{...l,...w},slot:I,attrs:l,slots:o,name:"MenuItem"})}}});const le=he(G.ui.strategy,G.ui.kbd,pt),Et=N({inheritAttrs:!1,props:{value:{type:String,default:null},size:{type:String,default:()=>le.default.size,validator(e){return Object.keys(le.size).includes(e)}},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})}},setup(e){const{ui:o,attrs:l}=we("kbd",re(e,"ui"),le),i=C(()=>ke(Ie(o.value.base,o.value.size[e.size],o.value.padding,o.value.rounded,o.value.font,o.value.background,o.value.ring),e.class));return{ui:o,attrs:l,kbdClass:i}}});function Rt(e,o,l,i,d,n){return S(),F("kbd",j({class:e.kbdClass},e.attrs),[ue(e.$slots,"default",{},()=>[U(L(e.value),1)])],16)}const Ae=_e(Et,[["render",Rt]]),oe=he(G.ui.strategy,G.ui.dropdown,qe),At=N({components:{HMenu:Dt,HMenuButton:Tt,HMenuItems:Pt,HMenuItem:Ct,UIcon:Me,UAvatar:Se,UKbd:Ae},inheritAttrs:!1,props:{items:{type:Array,default:()=>[]},mode:{type:String,default:"click",validator:e=>["click","hover"].includes(e)},open:{type:Boolean,default:void 0},disabled:{type:Boolean,default:!1},popper:{type:Object,default:()=>({})},openDelay:{type:Number,default:()=>oe.default.openDelay},closeDelay:{type:Number,default:()=>oe.default.closeDelay},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})}},emits:["update:open"],setup(e,{emit:o}){const{ui:l,attrs:i}=we("dropdown",re(e,"ui"),oe,re(e,"class")),d=C(()=>Je(e.mode==="hover"?{offsetDistance:0}:{},e.popper,l.value.popper)),[n,t]=Ve(d.value),r=D(null);let p=null,v=null;ye(()=>{var w,I;const c=(w=n.value)==null?void 0:w.$.provides;if(!c)return;const s=Object.getOwnPropertySymbols(c);r.value=s.length&&c[s[0]],e.open&&((I=r.value)==null||I.openMenu())});const b=C(()=>{var I,R,A;if(e.mode!=="hover")return{};const c=((I=e.popper)==null?void 0:I.offsetDistance)||((R=l.value.popper)==null?void 0:R.offsetDistance)||8,s=(A=d.value.placement)==null?void 0:A.split("-")[0],w=`${c}px`;return s==="top"||s==="bottom"?{paddingTop:w,paddingBottom:w}:s==="left"||s==="right"?{paddingLeft:w,paddingRight:w}:{paddingTop:w,paddingBottom:w,paddingLeft:w,paddingRight:w}});function y(c){!c.cancelable||!r.value||(r.value.menuState===0?r.value.closeMenu():r.value.openMenu())}function a(){e.mode!=="hover"||!r.value||(v&&(clearTimeout(v),v=null),r.value.menuState!==0&&(p=p||setTimeout(()=>{r.value.openMenu&&r.value.openMenu(),p=null},e.openDelay)))}function m(){e.mode!=="hover"||!r.value||(p&&(clearTimeout(p),p=null),r.value.menuState!==1&&(v=v||setTimeout(()=>{r.value.closeMenu&&r.value.closeMenu(),v=null},e.closeDelay)))}function u(c,s,{href:w,navigate:I,close:R,isExternal:A}){s.click&&s.click(c),w&&!A&&(I(c),R())}ce(()=>e.open,(c,s)=>{r.value&&(s===void 0||c===s||(c?r.value.openMenu():r.value.closeMenu()))}),ce(()=>{var c;return(c=r.value)==null?void 0:c.menuState},(c,s)=>{s===void 0||c===s||o("update:open",c===0)});const g=De;return je(()=>xe("$ctlRmIk4j0")),{ui:l,attrs:i,popper:d,trigger:n,container:t,containerStyle:b,onTouchStart:y,onMouseEnter:a,onMouseLeave:m,onClick:u,getNuxtLinkProps:Qe,twMerge:ke,twJoin:Ie,NuxtLink:g}}}),xt=["disabled"];function Ft(e,o,l,i,d,n){const t=Q("HMenuButton"),r=Me,p=Se,v=Ae,b=Q("HMenuItem"),y=De,a=Q("HMenuItems"),m=Q("HMenu");return S(),O(m,j({as:"div",class:e.ui.wrapper},e.attrs,{onMouseleave:e.onMouseLeave}),{default:_(({open:u})=>[k(t,{ref:"trigger",as:"div",disabled:e.disabled,class:E(e.ui.trigger),role:"button",onMouseenter:e.onMouseEnter,onTouchstartPassive:e.onTouchStart},{default:_(()=>[ue(e.$slots,"default",{open:u,disabled:e.disabled},()=>[T("button",{disabled:e.disabled}," Open ",8,xt)])]),_:2},1032,["disabled","class","onMouseenter","onTouchstartPassive"]),u&&e.items.length?(S(),F("div",{key:0,ref:"container",class:E([e.ui.container,e.ui.width]),style:We(e.containerStyle),onMouseenter:o[0]||(o[0]=(...g)=>e.onMouseEnter&&e.onMouseEnter(...g))},[k($e,j({appear:""},e.ui.transition),{default:_(()=>[T("div",null,[e.popper.arrow?(S(),F("div",{key:0,"data-popper-arrow":"",class:E(Object.values(e.ui.arrow))},null,2)):B("",!0),k(a,{class:E([e.ui.base,e.ui.divide,e.ui.ring,e.ui.rounded,e.ui.shadow,e.ui.background,e.ui.height]),static:""},{default:_(()=>[(S(!0),F(te,null,ne(e.items,(g,c)=>(S(),F("div",{key:c,class:E(e.ui.padding)},[(S(!0),F(te,null,ne(g,(s,w)=>(S(),O(y,j({key:w,ref_for:!0},e.getNuxtLinkProps(s),{custom:""}),{default:_(({href:I,target:R,rel:A,navigate:H,isExternal:z,isActive:K})=>[k(b,{disabled:s.disabled},{default:_(({active:q,disabled:f,close:x})=>[(S(),O(Ge(I?"a":"button"),{href:f?void 0:I,rel:A,target:R,class:E(e.twMerge(e.twJoin(e.ui.item.base,e.ui.item.padding,e.ui.item.size,e.ui.item.rounded,q||K?e.ui.item.active:e.ui.item.inactive,f&&e.ui.item.disabled),s.class)),onClick:J=>e.onClick(J,s,{href:I,navigate:H,close:x,isExternal:z})},{default:_(()=>[ue(e.$slots,s.slot||"item",{item:s},()=>{var J;return[s.icon?(S(),O(r,{key:0,name:s.icon,class:E(e.twMerge(e.twJoin(e.ui.item.icon.base,q||K?e.ui.item.icon.active:e.ui.item.icon.inactive),s.iconClass))},null,8,["name","class"])):s.avatar?(S(),O(p,j({key:1,ref_for:!0},{size:e.ui.item.avatar.size,...s.avatar},{class:e.ui.item.avatar.base}),null,16,["class"])):B("",!0),T("span",{class:E(e.twMerge(e.ui.item.label,s.labelClass))},L(s.label),3),(J=s.shortcuts)!=null&&J.length?(S(),F("span",{key:2,class:E(e.ui.item.shortcuts)},[(S(!0),F(te,null,ne(s.shortcuts,ie=>(S(),O(v,{key:ie},{default:_(()=>[U(L(ie),1)]),_:2},1024))),128))],2)):B("",!0)]})]),_:2},1032,["href","rel","target","class","onClick"]))]),_:2},1032,["disabled"])]),_:2},1040))),128))],2))),128))]),_:3},8,["class"])])]),_:3},16)],38)):B("",!0)]),_:3},16,["class","onMouseleave"])}const Ot=_e(At,[["render",Ft]]),Lt={class:"my-6"},Nt={class:"flex items-center justify-between mb-4"},Ut={class:"flex grid grid-cols-7 gap-3 border rounded p-3"},Vt={class:"col-span-2"},jt={class:"col-span-2"},Bt={class:"col-span-2"},Ht={class:"col-span-1"},zt={class:"text-center"},Kt={class:"text-center"},qt={class:"text-center"},rn=N({__name:"users",async setup(e){let o,l;const i=Xe(),d=ct(),n=fe(),t=D({search:"",userId:"",region:"",role:"",users:[],form:{},collapsed:!1,viewDeleted:!1}),r=C(()=>t.value.users.filter(m=>m.deleted==t.value.viewDeleted));async function p(){const m=fe();t.value.users=await m(`${ae}/users`,{params:{search:t.value.search}})}async function v(m,u=t.value.userId){confirm("Подтвердите действие!")&&(await n(`${ae}/users/${u}`,{params:{item:m}}),Object.assign(t.value,{userId:"",region:"",role:""}),await p(),i.add({icon:"i-heroicons-check-circle",title:"Информация",description:"Действие успешно выполнено",color:"green"}))}async function b(){await n(`${ae}/users`,{method:"POST",body:t.value.form}),t.value.collapsed=!1,Object.assign(t.value.form,{fullname:"",username:""}),await p(),i.add({icon:"i-heroicons-check-circle",title:"Информация",description:"Пользователь успешно добавлен",color:"green"})}const y=ut(async()=>{await p()},500),a=[[{label:"Сбросить пароль",click:()=>v("drop")}],[{label:"Заблокировать/разблокировать",click:()=>v("block")}],[{label:"Удалить/восстановить",click:()=>v("delete")}]];return[o,l]=Ze(()=>p()),await o,l(),(m,u)=>{const g=Fe,c=Oe,s=Be,w=Ye,I=Le,R=et,A=Ot,H=rt,z=st,K=it,q=dt;return S(),O(q,null,{default:_(()=>[k(g,{div:"py-1",cls:"text-2xl text-gray-500",header:"ПОЛЬЗОВАТЕЛИ"}),T("div",Lt,[k(c,{modelValue:h(t).search,"onUpdate:modelValue":u[0]||(u[0]=f=>h(t).search=f),size:"lg",placeholder:"Поиск по имени пользователя",onInput:pe(h(y),["prevent"])},null,8,["modelValue","onInput"])]),T("div",Nt,[k(s,{modelValue:h(t).viewDeleted,"onUpdate:modelValue":u[1]||(u[1]=f=>h(t).viewDeleted=f),label:"Показать удаленные"},null,8,["modelValue"]),k(w,{variant:"link",label:"Добавить пользователя",onClick:u[2]||(u[2]=f=>h(t).collapsed=!h(t).collapsed)})]),k($e,{name:"slide-fade"},{default:_(()=>[h(t).collapsed?(S(),O(R,{key:0,state:h(t).form,onSubmit:pe(b,["prevent"])},{default:_(()=>[T("div",Ut,[T("div",Vt,[k(I,{required:"",class:"mb-3"},{default:_(()=>[k(c,{modelValue:h(t).form.fullname,"onUpdate:modelValue":u[3]||(u[3]=f=>h(t).form.fullname=f),placeholder:"Имя пользователя"},null,8,["modelValue"])]),_:1})]),T("div",jt,[k(I,{required:"",class:"mb-3"},{default:_(()=>[k(c,{modelValue:h(t).form.username,"onUpdate:modelValue":u[4]||(u[4]=f=>h(t).form.username=f),placeholder:"Логин"},null,8,["modelValue"])]),_:1})]),T("div",Bt,[k(I,{required:"",class:"mb-3"},{default:_(()=>[k(c,{modelValue:h(t).form.email,"onUpdate:modelValue":u[5]||(u[5]=f=>h(t).form.email=f),placeholder:"Email"},null,8,["modelValue"])]),_:1})]),T("div",Ht,[k(w,{block:"",variant:"outline",color:"gray",label:"Создать",type:"submit"})])])]),_:1},8,["state"])):B("",!0)]),_:1}),k(K,{columns:[{key:"id",label:"#"},{key:"fullname",label:"Пользователь"},{key:"username",label:"Логин"},{key:"email",label:"Email"},{key:"region",label:"Регион"},{key:"role",label:"Роль"},{key:"created",label:"Создан"},{key:"attempt",label:"Попытка"},{key:"blocked",label:"Блок"},{key:"pswd_create",label:"Обновлен"},{key:"change_pswd",label:"Изм.пароля"}],rows:h(r)},{"id-data":_(({row:f})=>[U(L(f.id),1)]),"fullname-data":_(({row:f})=>[U(L(f.fullname),1)]),"username-data":_(({row:f})=>[k(A,{items:a},{default:_(()=>[k(w,{variant:"link",label:f.username,onClick:x=>h(t).userId=f.id},null,8,["label","onClick"])]),_:2},1024)]),"region-data":_(({row:f})=>[k(H,{modelValue:h(t).region,"onUpdate:modelValue":u[6]||(u[6]=x=>h(t).region=x),placeholder:f.region,options:Object.values(h(d).classes.value.regions),onChange:x=>v(h(t).region,f.id)},null,8,["modelValue","placeholder","options","onChange"])]),"role-data":_(({row:f})=>[k(H,{modelValue:h(t).role,"onUpdate:modelValue":u[7]||(u[7]=x=>h(t).role=x),placeholder:f.role,options:Object.values(h(d).classes.value.roles),onChange:x=>v(h(t).role,f.id)},null,8,["modelValue","placeholder","options","onChange"])]),"created-data":_(({row:f})=>[U(L(new Date(f.created).toLocaleDateString()),1)]),"attempt-data":_(({row:f})=>[T("div",zt,L(f.attempt),1)]),"blocked-data":_(({row:f})=>[T("div",Kt,[k(z,{size:"2xl",color:f.blocked?"red":"green"},null,8,["color"])])]),"pswd_create-data":_(({row:f})=>[U(L(new Date(f.pswd_create).toLocaleDateString()),1)]),"change_pswd-data":_(({row:f})=>[T("div",qt,[k(z,{size:"2xl",color:f.change_pswd?"red":"green"},null,8,["color"])])]),_:1},8,["rows"])]),_:1})}}});export{rn as default};