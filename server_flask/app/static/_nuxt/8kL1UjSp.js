import{R as Ie,ad as se,r as x,af as L,ae as ie,d as H,ab as ye,q as E,F as W,a1 as me,ac as xe,m as ue,h as G,_ as de,l as ce,t as Q,K as je,O as $e,ah as Le,aj as fe,o as k,y as M,g as A,b as B,z as O,x as I,f as T,T as Se,B as D,c as z,A as F,am as He,i as pe,j as ee,s as he,v as Y,D as V,a5 as ze,a6 as Re,E as Ce,C as Fe,a7 as Ke,ap as Ge,e as U,k as qe,n as Je}from"./DSZgY0GN.js";import{k as Ve,e as ve,c as ne,f as re,o as l,m as ke,u as X,t as We,a as le,w as Qe,j as Xe,A as we,i as Z,s as Ye,P as J,g as K,l as Ze,N as Te,b as q,d as ge,h as et}from"./i0GrmJZB.js";import{a as tt,w as at}from"./DQ78UH2T.js";import{u as ot}from"./Dvr36W2A.js";import{_ as Oe}from"./CmpAJq3q.js";import{u as nt}from"./Ce3U9u9Y.js";import{u as rt}from"./Ci_tIRZB.js";import{c as lt}from"./DXFhoKA3.js";const st={base:"mx-auto",padding:"px-4 sm:px-6 lg:px-8",constrained:"max-w-7xl"},it={wrapper:{base:"flex items-center align-center text-center",horizontal:"w-full flex-row",vertical:"flex-col"},container:{base:"font-medium text-gray-700 dark:text-gray-200 flex",horizontal:"mx-3 whitespace-nowrap",vertical:"my-2"},border:{base:"flex border-gray-200 dark:border-gray-800",horizontal:"w-full",vertical:"h-full",size:{horizontal:{"2xs":"border-t",xs:"border-t-[2px]",sm:"border-t-[3px]",md:"border-t-[4px]",lg:"border-t-[5px]",xl:"border-t-[6px]"},vertical:{"2xs":"border-s",xs:"border-s-[2px]",sm:"border-s-[3px]",md:"border-s-[4px]",lg:"border-s-[5px]",xl:"border-s-[6px]"}},type:{solid:"border-solid",dotted:"border-dotted",dashed:"border-dashed"}},icon:{base:"flex-shrink-0 w-5 h-5"},avatar:{base:"flex-shrink-0",size:"2xs"},label:"text-sm",default:{size:"2xs"}},ut={wrapper:"relative",base:"group relative flex items-center gap-1.5 focus:outline-none focus-visible:outline-none dark:focus-visible:outline-none focus-visible:before:ring-inset focus-visible:before:ring-1 focus-visible:before:ring-primary-500 dark:focus-visible:before:ring-primary-400 before:absolute before:inset-px before:rounded-md disabled:cursor-not-allowed disabled:opacity-75",ring:"focus-visible:ring-inset focus-visible:ring-2 focus-visible:ring-primary-500 dark:focus-visible:ring-primary-400",padding:"px-2.5 py-1.5",width:"w-full",rounded:"rounded-md",font:"font-medium",size:"text-sm",active:"text-gray-900 dark:text-white before:bg-gray-100 dark:before:bg-gray-800",inactive:"text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:before:bg-gray-50 dark:hover:before:bg-gray-800/50",label:"truncate relative",icon:{base:"flex-shrink-0 w-5 h-5 relative",active:"text-gray-700 dark:text-gray-200",inactive:"text-gray-400 dark:text-gray-500 group-hover:text-gray-700 dark:group-hover:text-gray-200"},avatar:{base:"flex-shrink-0",size:"2xs"},badge:{base:"flex-shrink-0 ml-auto relative rounded",color:"gray",variant:"solid",size:"xs"},divider:{wrapper:{base:"p-2"}}},dt={wrapper:"relative",container:"z-50 group",trigger:"inline-flex w-full",width:"",background:"bg-white dark:bg-gray-900",shadow:"shadow-lg",rounded:"rounded-md",ring:"ring-1 ring-gray-200 dark:ring-gray-800",base:"overflow-hidden focus:outline-none relative",transition:{enterActiveClass:"transition ease-out duration-200",enterFromClass:"opacity-0 translate-y-1",enterToClass:"opacity-100 translate-y-0",leaveActiveClass:"transition ease-in duration-150",leaveFromClass:"opacity-100 translate-y-0",leaveToClass:"opacity-0 translate-y-1"},overlay:{base:"fixed inset-0 transition-opacity z-50",background:"bg-gray-200/75 dark:bg-gray-800/75",transition:{enterActiveClass:"ease-out duration-200",enterFromClass:"opacity-0",enterToClass:"opacity-100",leaveActiveClass:"ease-in duration-150",leaveFromClass:"opacity-100",leaveToClass:"opacity-0"}},popper:{strategy:"fixed"},default:{openDelay:0,closeDelay:0},arrow:Ie};function ct(e,o,d,f){Ve.isServer||se(g=>{e=e??window,e.addEventListener(o,d,f),g(()=>e.removeEventListener(o,d,f))})}var j=(e=>(e[e.Forwards=0]="Forwards",e[e.Backwards=1]="Backwards",e))(j||{});function _e(){let e=x(0);return tt("keydown",o=>{o.key==="Tab"&&(e.value=o.shiftKey?1:0)}),e}function pt({defaultContainers:e=[],portals:o,mainTreeNodeRef:d}={}){let f=x(null),g=ve(f);function b(){var t,a,i;let p=[];for(let r of e)r!==null&&(r instanceof HTMLElement?p.push(r):"value"in r&&r.value instanceof HTMLElement&&p.push(r.value));if(o!=null&&o.value)for(let r of o.value)p.push(r);for(let r of(t=g==null?void 0:g.querySelectorAll("html > *, body > *"))!=null?t:[])r!==document.body&&r!==document.head&&r instanceof HTMLElement&&r.id!=="headlessui-portal-root"&&(r.contains(l(f))||r.contains((i=(a=l(f))==null?void 0:a.getRootNode())==null?void 0:i.host)||p.some(h=>r.contains(h))||p.push(r));return p}return{resolveContainers:b,contains(t){return b().some(a=>a.contains(t))},mainTreeNodeRef:f,MainTreeNode(){return d!=null?null:L(re,{features:ne.Hidden,ref:f})}}}let Ee=Symbol("PortalParentContext");function vt(){let e=ie(Ee,null),o=x([]);function d(b){return o.value.push(b),e&&e.register(b),()=>f(b)}function f(b){let t=o.value.indexOf(b);t!==-1&&o.value.splice(t,1),e&&e.unregister(b)}let g={register:d,unregister:f,portals:o};return[o,H({name:"PortalWrapper",setup(b,{slots:t}){return ye(Ee,g),()=>{var a;return(a=t.default)==null?void 0:a.call(t)}}})]}var ft=(e=>(e[e.Open=0]="Open",e[e.Closed=1]="Closed",e))(ft||{});let Be=Symbol("PopoverContext");function Pe(e){let o=ie(Be,null);if(o===null){let d=new Error(`<${e} /> is missing a parent <${De.name} /> component.`);throw Error.captureStackTrace&&Error.captureStackTrace(d,Pe),d}return o}let bt=Symbol("PopoverGroupContext");function Ae(){return ie(bt,null)}let Me=Symbol("PopoverPanelContext");function gt(){return ie(Me,null)}let De=H({name:"Popover",inheritAttrs:!1,props:{as:{type:[Object,String],default:"div"}},setup(e,{slots:o,attrs:d,expose:f}){var g;let b=x(null);f({el:b,$el:b});let t=x(1),a=x(null),i=x(null),p=x(null),r=x(null),h=E(()=>ve(b)),$=E(()=>{var n,v;if(!l(a)||!l(r))return!1;for(let ae of document.querySelectorAll("body > *"))if(Number(ae==null?void 0:ae.contains(l(a)))^Number(ae==null?void 0:ae.contains(l(r))))return!0;let c=ke(),C=c.indexOf(l(a)),N=(C+c.length-1)%c.length,R=(C+1)%c.length,te=c[N],Ue=c[R];return!((n=l(r))!=null&&n.contains(te))&&!((v=l(r))!=null&&v.contains(Ue))}),s={popoverState:t,buttonId:x(null),panelId:x(null),panel:r,button:a,isPortalled:$,beforePanelSentinel:i,afterPanelSentinel:p,togglePopover(){t.value=X(t.value,{0:1,1:0})},closePopover(){t.value!==1&&(t.value=1)},close(n){s.closePopover();let v=n?n instanceof HTMLElement?n:n.value instanceof HTMLElement?l(n):l(s.button):l(s.button);v==null||v.focus()}};ye(Be,s),We(E(()=>X(t.value,{0:le.Open,1:le.Closed})));let _={buttonId:s.buttonId,panelId:s.panelId,close(){s.closePopover()}},u=Ae(),P=u==null?void 0:u.registerPopover,[S,m]=vt(),w=pt({mainTreeNodeRef:u==null?void 0:u.mainTreeNodeRef,portals:S,defaultContainers:[a,r]});function y(){var n,v,c,C;return(C=u==null?void 0:u.isFocusWithinPopoverGroup())!=null?C:((n=h.value)==null?void 0:n.activeElement)&&(((v=l(a))==null?void 0:v.contains(h.value.activeElement))||((c=l(r))==null?void 0:c.contains(h.value.activeElement)))}return se(()=>P==null?void 0:P(_)),ct((g=h.value)==null?void 0:g.defaultView,"focus",n=>{var v,c;n.target!==window&&n.target instanceof HTMLElement&&t.value===0&&(y()||a&&r&&(w.contains(n.target)||(v=l(s.beforePanelSentinel))!=null&&v.contains(n.target)||(c=l(s.afterPanelSentinel))!=null&&c.contains(n.target)||s.closePopover()))},!0),at(w.resolveContainers,(n,v)=>{var c;s.closePopover(),Qe(v,Xe.Loose)||(n.preventDefault(),(c=l(a))==null||c.focus())},E(()=>t.value===0)),()=>{let n={open:t.value===0,close:s.close};return L(W,[L(m,{},()=>we({theirProps:{...e,...d},ourProps:{ref:b},slot:n,slots:o,attrs:d,name:"Popover"})),L(w.MainTreeNode)])}}}),yt=H({name:"PopoverButton",props:{as:{type:[Object,String],default:"button"},disabled:{type:[Boolean],default:!1},id:{type:String,default:null}},inheritAttrs:!1,setup(e,{attrs:o,slots:d,expose:f}){var g;let b=(g=e.id)!=null?g:`headlessui-popover-button-${Z()}`,t=Pe("PopoverButton"),a=E(()=>ve(t.button));f({el:t.button,$el:t.button}),me(()=>{t.buttonId.value=b}),xe(()=>{t.buttonId.value=null});let i=Ae(),p=i==null?void 0:i.closeOthers,r=gt(),h=E(()=>r===null?!1:r.value===t.panelId.value),$=x(null),s=`headlessui-focus-sentinel-${Z()}`;h.value||se(()=>{t.button.value=l($)});let _=Ye(E(()=>({as:e.as,type:o.type})),$);function u(n){var v,c,C,N,R;if(h.value){if(t.popoverState.value===1)return;switch(n.key){case q.Space:case q.Enter:n.preventDefault(),(c=(v=n.target).click)==null||c.call(v),t.closePopover(),(C=l(t.button))==null||C.focus();break}}else switch(n.key){case q.Space:case q.Enter:n.preventDefault(),n.stopPropagation(),t.popoverState.value===1&&(p==null||p(t.buttonId.value)),t.togglePopover();break;case q.Escape:if(t.popoverState.value!==0)return p==null?void 0:p(t.buttonId.value);if(!l(t.button)||(N=a.value)!=null&&N.activeElement&&!((R=l(t.button))!=null&&R.contains(a.value.activeElement)))return;n.preventDefault(),n.stopPropagation(),t.closePopover();break}}function P(n){h.value||n.key===q.Space&&n.preventDefault()}function S(n){var v,c;e.disabled||(h.value?(t.closePopover(),(v=l(t.button))==null||v.focus()):(n.preventDefault(),n.stopPropagation(),t.popoverState.value===1&&(p==null||p(t.buttonId.value)),t.togglePopover(),(c=l(t.button))==null||c.focus()))}function m(n){n.preventDefault(),n.stopPropagation()}let w=_e();function y(){let n=l(t.panel);if(!n)return;function v(){X(w.value,{[j.Forwards]:()=>J(n,K.First),[j.Backwards]:()=>J(n,K.Last)})===ge.Error&&J(ke().filter(c=>c.dataset.headlessuiFocusGuard!=="true"),X(w.value,{[j.Forwards]:K.Next,[j.Backwards]:K.Previous}),{relativeTo:l(t.button)})}v()}return()=>{let n=t.popoverState.value===0,v={open:n},{...c}=e,C=h.value?{ref:$,type:_.value,onKeydown:u,onClick:S}:{ref:$,id:b,type:_.value,"aria-expanded":t.popoverState.value===0,"aria-controls":l(t.panel)?t.panelId.value:void 0,disabled:e.disabled?!0:void 0,onKeydown:u,onKeyup:P,onClick:S,onMousedown:m};return L(W,[we({ourProps:C,theirProps:{...o,...c},slot:v,attrs:o,slots:d,name:"PopoverButton"}),n&&!h.value&&t.isPortalled.value&&L(re,{id:s,features:ne.Focusable,"data-headlessui-focus-guard":!0,as:"button",type:"button",onFocus:y})])}}}),mt=H({name:"PopoverPanel",props:{as:{type:[Object,String],default:"div"},static:{type:Boolean,default:!1},unmount:{type:Boolean,default:!0},focus:{type:Boolean,default:!1},id:{type:String,default:null}},inheritAttrs:!1,setup(e,{attrs:o,slots:d,expose:f}){var g;let b=(g=e.id)!=null?g:`headlessui-popover-panel-${Z()}`,{focus:t}=e,a=Pe("PopoverPanel"),i=E(()=>ve(a.panel)),p=`headlessui-focus-sentinel-before-${Z()}`,r=`headlessui-focus-sentinel-after-${Z()}`;f({el:a.panel,$el:a.panel}),me(()=>{a.panelId.value=b}),xe(()=>{a.panelId.value=null}),ye(Me,a.panelId),se(()=>{var m,w;if(!t||a.popoverState.value!==0||!a.panel)return;let y=(m=i.value)==null?void 0:m.activeElement;(w=l(a.panel))!=null&&w.contains(y)||J(l(a.panel),K.First)});let h=Ze(),$=E(()=>h!==null?(h.value&le.Open)===le.Open:a.popoverState.value===0);function s(m){var w,y;switch(m.key){case q.Escape:if(a.popoverState.value!==0||!l(a.panel)||i.value&&!((w=l(a.panel))!=null&&w.contains(i.value.activeElement)))return;m.preventDefault(),m.stopPropagation(),a.closePopover(),(y=l(a.button))==null||y.focus();break}}function _(m){var w,y,n,v,c;let C=m.relatedTarget;C&&l(a.panel)&&((w=l(a.panel))!=null&&w.contains(C)||(a.closePopover(),((n=(y=l(a.beforePanelSentinel))==null?void 0:y.contains)!=null&&n.call(y,C)||(c=(v=l(a.afterPanelSentinel))==null?void 0:v.contains)!=null&&c.call(v,C))&&C.focus({preventScroll:!0})))}let u=_e();function P(){let m=l(a.panel);if(!m)return;function w(){X(u.value,{[j.Forwards]:()=>{var y;J(m,K.First)===ge.Error&&((y=l(a.afterPanelSentinel))==null||y.focus())},[j.Backwards]:()=>{var y;(y=l(a.button))==null||y.focus({preventScroll:!0})}})}w()}function S(){let m=l(a.panel);if(!m)return;function w(){X(u.value,{[j.Forwards]:()=>{let y=l(a.button),n=l(a.panel);if(!y)return;let v=ke(),c=v.indexOf(y),C=v.slice(0,c+1),N=[...v.slice(c+1),...C];for(let R of N.slice())if(R.dataset.headlessuiFocusGuard==="true"||n!=null&&n.contains(R)){let te=N.indexOf(R);te!==-1&&N.splice(te,1)}J(N,K.First,{sorted:!1})},[j.Backwards]:()=>{var y;J(m,K.Previous)===ge.Error&&((y=l(a.button))==null||y.focus())}})}w()}return()=>{let m={open:a.popoverState.value===0,close:a.close},{focus:w,...y}=e,n={ref:a.panel,id:b,onKeydown:s,onFocusout:t&&a.popoverState.value===0?_:void 0,tabIndex:-1};return we({ourProps:n,theirProps:{...o,...y},attrs:o,slot:m,slots:{...d,default:(...v)=>{var c;return[L(W,[$.value&&a.isPortalled.value&&L(re,{id:p,ref:a.beforePanelSentinel,features:ne.Focusable,"data-headlessui-focus-guard":!0,as:"button",type:"button",onFocus:P}),(c=d.default)==null?void 0:c.call(d,...v),$.value&&a.isPortalled.value&&L(re,{id:r,ref:a.afterPanelSentinel,features:ne.Focusable,"data-headlessui-focus-guard":!0,as:"button",type:"button",onFocus:S})])]}},features:Te.RenderStrategy|Te.Static,visible:$.value,name:"PopoverPanel"})}}});const be=ue(G.ui.strategy,G.ui.popover,dt),ht=H({components:{HPopover:De,HPopoverButton:yt,HPopoverPanel:mt},inheritAttrs:!1,props:{mode:{type:String,default:"click",validator:e=>["click","hover"].includes(e)},open:{type:Boolean,default:void 0},disabled:{type:Boolean,default:!1},openDelay:{type:Number,default:()=>be.default.openDelay},closeDelay:{type:Number,default:()=>be.default.closeDelay},overlay:{type:Boolean,default:!1},popper:{type:Object,default:()=>({})},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})}},emits:["update:open"],setup(e,{emit:o}){const{ui:d,attrs:f}=ce("popover",Q(e,"ui"),be,Q(e,"class")),g=E(()=>je(e.mode==="hover"?{offsetDistance:0}:{},e.popper,d.value.popper)),[b,t]=ot(g.value),a=x(null),i=x(null);let p=null,r=null;me(()=>{var S,m;const u=(S=a.value)==null?void 0:S.$.provides;if(!u)return;const P=Object.getOwnPropertySymbols(u);i.value=P.length&&u[P[0]],e.open&&((m=i.value)==null||m.togglePopover())});const h=E(()=>{var m,w,y;if(e.mode!=="hover")return{};const u=((m=e.popper)==null?void 0:m.offsetDistance)||((w=d.value.popper)==null?void 0:w.offsetDistance)||8,P=(y=g.value.placement)==null?void 0:y.split("-")[0],S=`${u}px`;return P==="top"||P==="bottom"?{paddingTop:S,paddingBottom:S}:P==="left"||P==="right"?{paddingLeft:S,paddingRight:S}:{paddingTop:S,paddingBottom:S,paddingLeft:S,paddingRight:S}});function $(u){!u.cancelable||!i.value||e.mode==="click"||(i.value.popoverState===0?i.value.closePopover():i.value.togglePopover())}function s(){e.mode!=="hover"||!i.value||(r&&(clearTimeout(r),r=null),i.value.popoverState!==0&&(p=p||setTimeout(()=>{i.value.togglePopover&&i.value.togglePopover(),p=null},e.openDelay)))}function _(){e.mode!=="hover"||!i.value||(p&&(clearTimeout(p),p=null),i.value.popoverState!==1&&(r=r||setTimeout(()=>{i.value.closePopover&&i.value.closePopover(),r=null},e.closeDelay)))}return $e(()=>e.open,(u,P)=>{i.value&&(P===void 0||u===P||(u?i.value.popoverState=0:i.value.closePopover()))}),$e(()=>{var u;return(u=i.value)==null?void 0:u.popoverState},(u,P)=>{P===void 0||u===P||o("update:open",u===0)}),et(()=>Le()),{ui:d,attrs:f,popover:a,popper:g,trigger:b,container:t,containerStyle:h,onTouchStart:$,onMouseEnter:s,onMouseLeave:_}}}),kt=["disabled"];function wt(e,o,d,f,g,b){const t=fe("HPopoverButton"),a=fe("HPopoverPanel"),i=fe("HPopover");return k(),M(i,D({ref:"popover",class:e.ui.wrapper},e.attrs,{onMouseleave:e.onMouseLeave}),{default:A(({open:p,close:r})=>[B(t,{ref:"trigger",as:"div",disabled:e.disabled,class:O(e.ui.trigger),role:"button",onMouseenter:e.onMouseEnter,onTouchstartPassive:e.onTouchStart},{default:A(()=>[I(e.$slots,"default",{open:p,close:r},()=>[T("button",{disabled:e.disabled}," Open ",8,kt)])]),_:2},1032,["disabled","class","onMouseenter","onTouchstartPassive"]),e.overlay?(k(),M(Se,D({key:0,appear:""},e.ui.overlay.transition),{default:A(()=>[p?(k(),z("div",{key:0,class:O([e.ui.overlay.base,e.ui.overlay.background])},null,2)):F("",!0)]),_:2},1040)):F("",!0),p?(k(),z("div",{key:1,ref:"container",class:O([e.ui.container,e.ui.width]),style:He(e.containerStyle),onMouseenter:o[0]||(o[0]=(...h)=>e.onMouseEnter&&e.onMouseEnter(...h))},[B(Se,D({appear:""},e.ui.transition),{default:A(()=>[T("div",null,[e.popper.arrow?(k(),z("div",{key:0,"data-popper-arrow":"",class:O(Object.values(e.ui.arrow))},null,2)):F("",!0),B(a,{class:O([e.ui.base,e.ui.background,e.ui.ring,e.ui.rounded,e.ui.shadow]),static:""},{default:A(()=>[I(e.$slots,"panel",{open:p,close:r})]),_:2},1032,["class"])])]),_:2},1040)],38)):F("",!0)]),_:3},16,["class","onMouseleave"])}const Pt=de(ht,[["render",wt]]),oe=ue(G.ui.strategy,G.ui.divider,it),$t=H({components:{UIcon:pe,UAvatar:ee},inheritAttrs:!1,props:{label:{type:String,default:null},icon:{type:String,default:null},avatar:{type:Object,default:null},size:{type:String,default:()=>oe.default.size,validator(e){return Object.keys(oe.border.size.horizontal).includes(e)||Object.keys(oe.border.size.vertical).includes(e)}},orientation:{type:String,default:"horizontal",validator:e=>["horizontal","vertical"].includes(e)},type:{type:String,default:"solid",validator:e=>["solid","dotted","dashed"].includes(e)},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})}},setup(e){const{ui:o,attrs:d}=ce("divider",Q(e,"ui"),oe),f=E(()=>he(Y(o.value.wrapper.base,o.value.wrapper[e.orientation]),e.class)),g=E(()=>Y(o.value.container.base,o.value.container[e.orientation])),b=E(()=>Y(o.value.border.base,o.value.border[e.orientation],o.value.border.size[e.orientation][e.size],o.value.border.type[e.type]));return{ui:o,attrs:d,wrapperClass:f,containerClass:g,borderClass:b}}});function St(e,o,d,f,g,b){const t=pe,a=ee;return k(),z("div",D({class:e.wrapperClass},e.attrs),[T("div",{class:O(e.borderClass)},null,2),e.label||e.icon||e.avatar||e.$slots.default?(k(),z(W,{key:0},[T("div",{class:O(e.containerClass)},[I(e.$slots,"default",{},()=>[e.label?(k(),z("span",{key:0,class:O(e.ui.label)},V(e.label),3)):e.icon?(k(),M(t,{key:1,name:e.icon,class:O(e.ui.icon.base)},null,8,["name","class"])):e.avatar?(k(),M(a,D({key:2},{size:e.ui.avatar.size,...e.avatar},{class:e.ui.avatar.base}),null,16,["class"])):F("",!0)])],2),T("div",{class:O(e.borderClass)},null,2)],64)):F("",!0)],16)}const Ne=de($t,[["render",St]]),Ct=ue(G.ui.strategy,G.ui.verticalNavigation,ut),Tt=H({components:{UIcon:pe,UAvatar:ee,UBadge:Oe,ULink:ze,UDivider:Ne},inheritAttrs:!1,props:{links:{type:Array,default:()=>[]},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})}},setup(e){const{ui:o,attrs:d}=ce("verticalNavigation",Q(e,"ui"),Ct,Q(e,"class")),f=E(()=>Array.isArray(e.links[0])?e.links:[e.links]);return{ui:o,attrs:d,sections:f,getULinkProps:Re,twMerge:he,twJoin:Y}}}),Et={key:0,class:"sr-only"};function xt(e,o,d,f,g,b){const t=ee,a=pe,i=Oe,p=ze,r=Ne;return k(),z("nav",D({class:e.ui.wrapper},e.attrs),[(k(!0),z(W,null,Ce(e.sections,(h,$)=>(k(),z("ul",{key:`section${$}`},[(k(!0),z(W,null,Ce(h,(s,_)=>(k(),z("li",{key:`section${$}-${_}`},[B(p,D({ref_for:!0},e.getULinkProps(s),{class:[e.ui.base,e.ui.padding,e.ui.width,e.ui.ring,e.ui.rounded,e.ui.font,e.ui.size],"active-class":e.ui.active,"inactive-class":e.ui.inactive,onClick:s.click,onKeyup:o[0]||(o[0]=Ke(u=>u.target.blur(),["enter"]))}),{default:A(({isActive:u})=>[I(e.$slots,"avatar",{link:s,isActive:u},()=>[s.avatar?(k(),M(t,D({key:0,ref_for:!0},{size:e.ui.avatar.size,...s.avatar},{class:[e.ui.avatar.base]}),null,16,["class"])):F("",!0)]),I(e.$slots,"icon",{link:s,isActive:u},()=>[s.icon?(k(),M(a,{key:0,name:s.icon,class:O(e.twMerge(e.twJoin(e.ui.icon.base,u?e.ui.icon.active:e.ui.icon.inactive),s.iconClass))},null,8,["name","class"])):F("",!0)]),I(e.$slots,"default",{link:s,isActive:u},()=>[s.label?(k(),z("span",{key:0,class:O(e.twMerge(e.ui.label,s.labelClass))},[u?(k(),z("span",Et," Current page: ")):F("",!0),Fe(" "+V(s.label),1)],2)):F("",!0)]),I(e.$slots,"badge",{link:s,isActive:u},()=>[s.badge?(k(),M(i,D({key:0,ref_for:!0},{size:e.ui.badge.size,color:e.ui.badge.color,variant:e.ui.badge.variant,...typeof s.badge=="string"||typeof s.badge=="number"?{label:s.badge}:s.badge},{class:e.ui.badge.base}),null,16,["class"])):F("",!0)])]),_:2},1040,["class","active-class","inactive-class","onClick"])]))),128)),$<e.sections.length-1?(k(),M(r,{key:0,ui:e.ui.divider},null,8,["ui"])):F("",!0)]))),128))],16)}const zt=de(Tt,[["render",xt]]),Ft=ue(G.ui.strategy,G.ui.container,st),Ot=H({inheritAttrs:!1,props:{as:{type:String,default:"div"},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})}},setup(e){const{ui:o,attrs:d}=ce("container",Q(e,"ui"),Ft),f=E(()=>he(Y(o.value.base,o.value.padding,o.value.constrained),e.class));return{ui:o,attrs:d,containerClass:f}}});function _t(e,o,d,f,g,b){return k(),M(Ge(e.as),D({class:e.containerClass},e.attrs),{default:A(()=>[I(e.$slots,"default")]),_:3},16,["class"])}const Bt=de(Ot,[["render",_t]]),At={class:"sticky pt-8 pb-16"},Mt={class:"flex justify-between relative"},Dt={class:"absolute top-0 left-0"},Nt={class:"m-3 text-center text-sm text-gray-600"},Ut={class:"grid grid-cols-12 gap-6"},It={key:0,class:"flex flex-col w-full h-screen col-span-2 pt-3 border-r border-gray-200"},Vt=H({__name:"default",setup(e){const o=nt(),d=x(!0);async function f(){if(confirm("Вы действительно хотите выйти?"))return rt.value=null,lt(),Je("/login")}const g=[[{label:"кандидаты",icon:"i-heroicons-user-circle",to:"/persons"}],[{label:"создать",icon:"i-heroicons-newspaper",to:"/resume"}],[{label:"пользователи",icon:"i-heroicons-user-group",to:"/users"}],[{label:"информация",icon:"i-heroicons-information-circle",to:"/info"}],[{label:"выход",icon:"i-heroicons-arrow-left-end-on-rectangle",to:"/login",click:()=>f()}]],b=E(()=>o.value?o.value.role==="admin"?g.filter(t=>t[0].to!=="/resume"):o.value.role==="user"?g.filter(t=>t[0].to!=="/users"):g.filter(t=>t[0].to!=="/users"&&t[0].to!=="/resume"):[]);return(t,a)=>{const i=qe,p=ee,r=Pt,h=zt,$=Bt;return k(),M($,{ui:{constrained:"max-w-none",padding:"px-4 sm:px-6 lg:px-12"}},{default:A(()=>[T("header",At,[T("div",Mt,[T("div",Dt,[B(i,{icon:"i-heroicons-bars-4",variant:"ghost",onClick:a[0]||(a[0]=s=>d.value=!U(d))})]),a[3]||(a[3]=T("div",{class:"absolute top-0 left-12 inline-flex text-xl font-bold"},[T("h3",{class:"text-blue-800"},"STAFFSEC"),Fe("   "),T("h3",{class:"text-red-600"},"ФИНТЕХ")],-1)),B(i,{class:"absolute top-0 right-0",icon:"i-heroicons-moon",variant:t.$colorMode.preference=="dark"?"soft":"ghost",onClick:a[1]||(a[1]=s=>t.$colorMode.preference="dark")},null,8,["variant"]),B(i,{class:"absolute top-0 right-12",icon:"i-heroicons-sun",variant:t.$colorMode.preference=="light"?"soft":"ghost",onClick:a[2]||(a[2]=s=>t.$colorMode.preference="light")},null,8,["variant"]),B(r,{class:"absolute top-0 right-24",mode:"hover",popper:{placement:"top-start"}},{panel:A(()=>[T("div",Nt,[T("div",null,V(U(o).fullname),1),T("div",null,"Логин: "+V(U(o).username),1),T("div",null,"Регион: "+V(U(o).region),1),T("div",null,"Роль: "+V(U(o).role),1)])]),default:A(()=>[B(p,{alt:U(o).fullname},null,8,["alt"])]),_:1})])]),T("div",Ut,[U(d)?(k(),z("div",It,[B(h,{links:U(b),ui:{active:"text-red-800 dark:text-white before:bg-gray-0 dark:before:bg-gray-0",inactive:"text-primary-800 dark:text-gray-400 hover:text-red-600 dark:hover:text-white hover:before:bg-gray-0 dark:hover:before:bg-gray-800/50",size:"text-xl mt-4",icon:{active:"text-red-800 dark:text-white",inactive:"text-primary-800 dark:text-gray-400 hover:text-red-600 dark:hover:text-white"}}},null,8,["links"])])):F("",!0),T("div",{class:O(["flex flex-col py-8",U(d)?"col-span-10":"col-span-12"])},[I(t.$slots,"default")],2)])]),_:3})}}});export{Vt as default};
