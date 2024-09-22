import{m as ft,j as ue,_ as Le,f as Re,q as ct,s as pt,v as dt,x as vt,y as gt,o as _,h as ht,w as be,c as we,A as Se,z as J,B as De,C as mt,ae as zt,ah as Ft,J as Ut,R as qt,N as It,r as xe,K as yt,M as bt,aF as Xt,O as Yt,F as Gt,aG as et,aA as Jt,d as Kt,t as Qt}from"./BL57t9pv.js";const Zt={base:"inline-flex items-center",rounded:"rounded-md",font:"font-medium",size:{xs:"text-xs px-1.5 py-0.5",sm:"text-xs px-2 py-1",md:"text-sm px-2 py-1",lg:"text-sm px-2.5 py-1.5"},color:{white:{solid:"ring-1 ring-inset ring-gray-300 dark:ring-gray-700 text-gray-900 dark:text-white bg-white dark:bg-gray-900"},gray:{solid:"ring-1 ring-inset ring-gray-300 dark:ring-gray-700 text-gray-700 dark:text-gray-200 bg-gray-50 dark:bg-gray-800"},black:{solid:"text-white dark:text-gray-900 bg-gray-900 dark:bg-white"}},variant:{solid:"bg-{color}-500 dark:bg-{color}-400 text-white dark:text-gray-900",outline:"text-{color}-500 dark:text-{color}-400 ring-1 ring-inset ring-{color}-500 dark:ring-{color}-400",soft:"bg-{color}-50 dark:bg-{color}-400 dark:bg-opacity-10 text-{color}-500 dark:text-{color}-400",subtle:"bg-{color}-50 dark:bg-{color}-400 dark:bg-opacity-10 text-{color}-500 dark:text-{color}-400 ring-1 ring-inset ring-{color}-500 dark:ring-{color}-400 ring-opacity-25 dark:ring-opacity-25"},default:{size:"sm",variant:"solid",color:"primary"}},_t={base:"",background:"bg-white dark:bg-gray-900",divide:"divide-y divide-gray-200 dark:divide-gray-800",ring:"ring-1 ring-gray-200 dark:ring-gray-800",rounded:"rounded-lg",shadow:"shadow",body:{base:"",background:"",padding:"px-4 py-5 sm:p-6"},header:{base:"",background:"",padding:"px-4 py-5 sm:px-6"},footer:{base:"",background:"",padding:"px-4 py-4 sm:px-6"}},er=ft(ue.ui.strategy,ue.ui.card,_t),tr=Re({inheritAttrs:!1,props:{as:{type:String,default:"div"},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})}},setup(e){const{ui:t,attrs:r}=ct("card",pt(e,"ui"),er),n=dt(()=>vt(gt(t.value.base,t.value.rounded,t.value.divide,t.value.ring,t.value.shadow,t.value.background),e.class));return{ui:t,attrs:r,cardClass:n}}});function rr(e,t,r,n,a,o){return _(),ht(zt(e.$attrs.onSubmit?"form":e.as),mt({class:e.cardClass},e.attrs),{default:be(()=>[e.$slots.header?(_(),we("div",{key:0,class:Se([e.ui.header.base,e.ui.header.padding,e.ui.header.background])},[J(e.$slots,"header")],2)):De("",!0),e.$slots.default?(_(),we("div",{key:1,class:Se([e.ui.body.base,e.ui.body.padding,e.ui.body.background])},[J(e.$slots,"default")],2)):De("",!0),e.$slots.footer?(_(),we("div",{key:2,class:Se([e.ui.footer.base,e.ui.footer.padding,e.ui.footer.background])},[J(e.$slots,"footer")],2)):De("",!0)]),_:3},16,["class"])}const nr=Le(tr,[["render",rr]]),ar={};function or(e,t){const r=nr;return _(),ht(r,{ui:{body:{padding:"px-4 py-5 sm:p-4"},header:{padding:"px-4 py-5 sm:p-4"},footer:{padding:"px-4 py-4 sm:p-1"}}},Ft({default:be(()=>[J(e.$slots,"default")]),_:2},[e.$slots.header?{name:"header",fn:be(()=>[J(e.$slots,"header")]),key:"0"}:void 0,e.$slots.footer?{name:"footer",fn:be(()=>[J(e.$slots,"footer")]),key:"1"}:void 0]),1024)}const wn=Le(ar,[["render",or]]);var tt;let wt=Symbol("headlessui.useid"),ir=0;const xn=(tt=qt)!=null?tt:function(){return It(wt,()=>`${++ir}`)()};function On(e){Ut(wt,e)}function Ce(e){var t;if(e==null||e.value==null)return null;let r=(t=e.value.$el)!=null?t:e.value;return r instanceof Node?r:null}function xt(e,t,...r){if(e in t){let a=t[e];return typeof a=="function"?a(...r):a}let n=new Error(`Tried to handle "${e}" but there is no handler defined. Only defined handlers are: ${Object.keys(t).map(a=>`"${a}"`).join(", ")}.`);throw Error.captureStackTrace&&Error.captureStackTrace(n,xt),n}function rt(e,t){if(e)return e;let r=t??"button";if(typeof r=="string"&&r.toLowerCase()==="button")return"button"}function kn(e,t){let r=xe(rt(e.value.type,e.value.as));return yt(()=>{r.value=rt(e.value.type,e.value.as)}),bt(()=>{var n;r.value||Ce(t)&&Ce(t)instanceof HTMLButtonElement&&!((n=Ce(t))!=null&&n.hasAttribute("type"))&&(r.value="button")}),r}var sr=(e=>(e[e.None=0]="None",e[e.RenderStrategy=1]="RenderStrategy",e[e.Static=2]="Static",e))(sr||{}),lr=(e=>(e[e.Unmount=0]="Unmount",e[e.Hidden=1]="Hidden",e))(lr||{});function ur({visible:e=!0,features:t=0,ourProps:r,theirProps:n,...a}){var o;let l=kt(n,r),i=Object.assign(a,{props:l});if(e||t&2&&l.static)return Be(i);if(t&1){let s=(o=l.unmount)==null||o?0:1;return xt(s,{0(){return null},1(){return Be({...a,props:{...l,hidden:!0,style:{display:"none"}}})}})}return Be(i)}function Be({props:e,attrs:t,slots:r,slot:n,name:a}){var o,l;let{as:i,...s}=fr(e,["unmount","static"]),f=(o=r.default)==null?void 0:o.call(r,n),u={};if(n){let d=!1,m=[];for(let[c,g]of Object.entries(n))typeof g=="boolean"&&(d=!0),g===!0&&m.push(c);d&&(u["data-headlessui-state"]=m.join(" "))}if(i==="template"){if(f=Ot(f??[]),Object.keys(s).length>0||Object.keys(t).length>0){let[d,...m]=f??[];if(!cr(d)||m.length>0)throw new Error(['Passing props on "template"!',"",`The current component <${a} /> is rendering a "template".`,"However we need to passthrough the following props:",Object.keys(s).concat(Object.keys(t)).map(p=>p.trim()).filter((p,v,y)=>y.indexOf(p)===v).sort((p,v)=>p.localeCompare(v)).map(p=>`  - ${p}`).join(`
`),"","You can apply a few solutions:",['Add an `as="..."` prop, to ensure that we render an actual element instead of a "template".',"Render a single element as the child so that we can forward the props onto that element."].map(p=>`  - ${p}`).join(`
`)].join(`
`));let c=kt((l=d.props)!=null?l:{},s,u),g=Xt(d,c,!0);for(let p in c)p.startsWith("on")&&(g.props||(g.props={}),g.props[p]=c[p]);return g}return Array.isArray(f)&&f.length===1?f[0]:f}return Yt(i,Object.assign({},s,u),{default:()=>f})}function Ot(e){return e.flatMap(t=>t.type===Gt?Ot(t.children):[t])}function kt(...e){if(e.length===0)return{};if(e.length===1)return e[0];let t={},r={};for(let n of e)for(let a in n)a.startsWith("on")&&typeof n[a]=="function"?(r[a]!=null||(r[a]=[]),r[a].push(n[a])):t[a]=n[a];if(t.disabled||t["aria-disabled"])return Object.assign(t,Object.fromEntries(Object.keys(r).map(n=>[n,void 0])));for(let n in r)Object.assign(t,{[n](a,...o){let l=r[n];for(let i of l){if(a instanceof Event&&a.defaultPrevented)return;i(a,...o)}}});return t}function $n(e){let t=Object.assign({},e);for(let r in t)t[r]===void 0&&delete t[r];return t}function fr(e,t=[]){let r=Object.assign({},e);for(let n of t)n in r&&delete r[n];return r}function cr(e){return e==null?!1:typeof e.type=="string"||typeof e.type=="object"||typeof e.type=="function"}var pr=(e=>(e[e.None=1]="None",e[e.Focusable=2]="Focusable",e[e.Hidden=4]="Hidden",e))(pr||{});let An=Re({name:"Hidden",props:{as:{type:[Object,String],default:"div"},features:{type:Number,default:1}},setup(e,{slots:t,attrs:r}){return()=>{var n;let{features:a,...o}=e,l={"aria-hidden":(a&2)===2?!0:(n=o["aria-hidden"])!=null?n:void 0,hidden:(a&4)===4?!0:void 0,style:{position:"fixed",top:1,left:1,width:1,height:0,padding:0,margin:-1,overflow:"hidden",clip:"rect(0, 0, 0, 0)",whiteSpace:"nowrap",borderWidth:"0",...(a&4)===4&&(a&2)!==2&&{display:"none"}}};return ur({ourProps:l,theirProps:o,slot:{},attrs:r,slots:t,name:"Hidden"})}}});var dr=(e=>(e.Space=" ",e.Enter="Enter",e.Escape="Escape",e.Backspace="Backspace",e.Delete="Delete",e.ArrowLeft="ArrowLeft",e.ArrowUp="ArrowUp",e.ArrowRight="ArrowRight",e.ArrowDown="ArrowDown",e.Home="Home",e.End="End",e.PageUp="PageUp",e.PageDown="PageDown",e.Tab="Tab",e))(dr||{});function B(e){if(e==null)return window;if(e.toString()!=="[object Window]"){var t=e.ownerDocument;return t&&t.defaultView||window}return e}function Q(e){var t=B(e).Element;return e instanceof t||e instanceof Element}function T(e){var t=B(e).HTMLElement;return e instanceof t||e instanceof HTMLElement}function He(e){if(typeof ShadowRoot>"u")return!1;var t=B(e).ShadowRoot;return e instanceof t||e instanceof ShadowRoot}var K=Math.max,ke=Math.min,ee=Math.round;function Te(){var e=navigator.userAgentData;return e!=null&&e.brands&&Array.isArray(e.brands)?e.brands.map(function(t){return t.brand+"/"+t.version}).join(" "):navigator.userAgent}function $t(){return!/^((?!chrome|android).)*safari/i.test(Te())}function te(e,t,r){t===void 0&&(t=!1),r===void 0&&(r=!1);var n=e.getBoundingClientRect(),a=1,o=1;t&&T(e)&&(a=e.offsetWidth>0&&ee(n.width)/e.offsetWidth||1,o=e.offsetHeight>0&&ee(n.height)/e.offsetHeight||1);var l=Q(e)?B(e):window,i=l.visualViewport,s=!$t()&&r,f=(n.left+(s&&i?i.offsetLeft:0))/a,u=(n.top+(s&&i?i.offsetTop:0))/o,d=n.width/a,m=n.height/o;return{width:d,height:m,top:u,right:f+d,bottom:u+m,left:f,x:f,y:u}}function We(e){var t=B(e),r=t.pageXOffset,n=t.pageYOffset;return{scrollLeft:r,scrollTop:n}}function vr(e){return{scrollLeft:e.scrollLeft,scrollTop:e.scrollTop}}function gr(e){return e===B(e)||!T(e)?We(e):vr(e)}function N(e){return e?(e.nodeName||"").toLowerCase():null}function U(e){return((Q(e)?e.ownerDocument:e.document)||window.document).documentElement}function Ne(e){return te(U(e)).left+We(e).scrollLeft}function V(e){return B(e).getComputedStyle(e)}function Ve(e){var t=V(e),r=t.overflow,n=t.overflowX,a=t.overflowY;return/auto|scroll|overlay|hidden/.test(r+a+n)}function hr(e){var t=e.getBoundingClientRect(),r=ee(t.width)/e.offsetWidth||1,n=ee(t.height)/e.offsetHeight||1;return r!==1||n!==1}function mr(e,t,r){r===void 0&&(r=!1);var n=T(t),a=T(t)&&hr(t),o=U(t),l=te(e,a,r),i={scrollLeft:0,scrollTop:0},s={x:0,y:0};return(n||!n&&!r)&&((N(t)!=="body"||Ve(o))&&(i=gr(t)),T(t)?(s=te(t,!0),s.x+=t.clientLeft,s.y+=t.clientTop):o&&(s.x=Ne(o))),{x:l.left+i.scrollLeft-s.x,y:l.top+i.scrollTop-s.y,width:l.width,height:l.height}}function ze(e){var t=te(e),r=e.offsetWidth,n=e.offsetHeight;return Math.abs(t.width-r)<=1&&(r=t.width),Math.abs(t.height-n)<=1&&(n=t.height),{x:e.offsetLeft,y:e.offsetTop,width:r,height:n}}function $e(e){return N(e)==="html"?e:e.assignedSlot||e.parentNode||(He(e)?e.host:null)||U(e)}function At(e){return["html","body","#document"].indexOf(N(e))>=0?e.ownerDocument.body:T(e)&&Ve(e)?e:At($e(e))}function se(e,t){var r;t===void 0&&(t=[]);var n=At(e),a=n===((r=e.ownerDocument)==null?void 0:r.body),o=B(n),l=a?[o].concat(o.visualViewport||[],Ve(n)?n:[]):n,i=t.concat(l);return a?i:i.concat(se($e(l)))}function yr(e){return["table","td","th"].indexOf(N(e))>=0}function nt(e){return!T(e)||V(e).position==="fixed"?null:e.offsetParent}function br(e){var t=/firefox/i.test(Te()),r=/Trident/i.test(Te());if(r&&T(e)){var n=V(e);if(n.position==="fixed")return null}var a=$e(e);for(He(a)&&(a=a.host);T(a)&&["html","body"].indexOf(N(a))<0;){var o=V(a);if(o.transform!=="none"||o.perspective!=="none"||o.contain==="paint"||["transform","perspective"].indexOf(o.willChange)!==-1||t&&o.willChange==="filter"||t&&o.filter&&o.filter!=="none")return a;a=a.parentNode}return null}function ce(e){for(var t=B(e),r=nt(e);r&&yr(r)&&V(r).position==="static";)r=nt(r);return r&&(N(r)==="html"||N(r)==="body"&&V(r).position==="static")?t:r||br(e)||t}var D="top",R="bottom",H="right",C="left",Fe="auto",pe=[D,R,H,C],re="start",fe="end",wr="clippingParents",jt="viewport",ie="popper",xr="reference",at=pe.reduce(function(e,t){return e.concat([t+"-"+re,t+"-"+fe])},[]),Et=[].concat(pe,[Fe]).reduce(function(e,t){return e.concat([t,t+"-"+re,t+"-"+fe])},[]),Or="beforeRead",kr="read",$r="afterRead",Ar="beforeMain",jr="main",Er="afterMain",Pr="beforeWrite",Sr="write",Dr="afterWrite",Cr=[Or,kr,$r,Ar,jr,Er,Pr,Sr,Dr];function Br(e){var t=new Map,r=new Set,n=[];e.forEach(function(o){t.set(o.name,o)});function a(o){r.add(o.name);var l=[].concat(o.requires||[],o.requiresIfExists||[]);l.forEach(function(i){if(!r.has(i)){var s=t.get(i);s&&a(s)}}),n.push(o)}return e.forEach(function(o){r.has(o.name)||a(o)}),n}function Tr(e){var t=Br(e);return Cr.reduce(function(r,n){return r.concat(t.filter(function(a){return a.phase===n}))},[])}function Mr(e){var t;return function(){return t||(t=new Promise(function(r){Promise.resolve().then(function(){t=void 0,r(e())})})),t}}function Lr(e){var t=e.reduce(function(r,n){var a=r[n.name];return r[n.name]=a?Object.assign({},a,n,{options:Object.assign({},a.options,n.options),data:Object.assign({},a.data,n.data)}):n,r},{});return Object.keys(t).map(function(r){return t[r]})}function Rr(e,t){var r=B(e),n=U(e),a=r.visualViewport,o=n.clientWidth,l=n.clientHeight,i=0,s=0;if(a){o=a.width,l=a.height;var f=$t();(f||!f&&t==="fixed")&&(i=a.offsetLeft,s=a.offsetTop)}return{width:o,height:l,x:i+Ne(e),y:s}}function Hr(e){var t,r=U(e),n=We(e),a=(t=e.ownerDocument)==null?void 0:t.body,o=K(r.scrollWidth,r.clientWidth,a?a.scrollWidth:0,a?a.clientWidth:0),l=K(r.scrollHeight,r.clientHeight,a?a.scrollHeight:0,a?a.clientHeight:0),i=-n.scrollLeft+Ne(e),s=-n.scrollTop;return V(a||r).direction==="rtl"&&(i+=K(r.clientWidth,a?a.clientWidth:0)-o),{width:o,height:l,x:i,y:s}}function Pt(e,t){var r=t.getRootNode&&t.getRootNode();if(e.contains(t))return!0;if(r&&He(r)){var n=t;do{if(n&&e.isSameNode(n))return!0;n=n.parentNode||n.host}while(n)}return!1}function Me(e){return Object.assign({},e,{left:e.x,top:e.y,right:e.x+e.width,bottom:e.y+e.height})}function Wr(e,t){var r=te(e,!1,t==="fixed");return r.top=r.top+e.clientTop,r.left=r.left+e.clientLeft,r.bottom=r.top+e.clientHeight,r.right=r.left+e.clientWidth,r.width=e.clientWidth,r.height=e.clientHeight,r.x=r.left,r.y=r.top,r}function ot(e,t,r){return t===jt?Me(Rr(e,r)):Q(t)?Wr(t,r):Me(Hr(U(e)))}function Nr(e){var t=se($e(e)),r=["absolute","fixed"].indexOf(V(e).position)>=0,n=r&&T(e)?ce(e):e;return Q(n)?t.filter(function(a){return Q(a)&&Pt(a,n)&&N(a)!=="body"}):[]}function Vr(e,t,r,n){var a=t==="clippingParents"?Nr(e):[].concat(t),o=[].concat(a,[r]),l=o[0],i=o.reduce(function(s,f){var u=ot(e,f,n);return s.top=K(u.top,s.top),s.right=ke(u.right,s.right),s.bottom=ke(u.bottom,s.bottom),s.left=K(u.left,s.left),s},ot(e,l,n));return i.width=i.right-i.left,i.height=i.bottom-i.top,i.x=i.left,i.y=i.top,i}function W(e){return e.split("-")[0]}function ne(e){return e.split("-")[1]}function Ue(e){return["top","bottom"].indexOf(e)>=0?"x":"y"}function St(e){var t=e.reference,r=e.element,n=e.placement,a=n?W(n):null,o=n?ne(n):null,l=t.x+t.width/2-r.width/2,i=t.y+t.height/2-r.height/2,s;switch(a){case D:s={x:l,y:t.y-r.height};break;case R:s={x:l,y:t.y+t.height};break;case H:s={x:t.x+t.width,y:i};break;case C:s={x:t.x-r.width,y:i};break;default:s={x:t.x,y:t.y}}var f=a?Ue(a):null;if(f!=null){var u=f==="y"?"height":"width";switch(o){case re:s[f]=s[f]-(t[u]/2-r[u]/2);break;case fe:s[f]=s[f]+(t[u]/2-r[u]/2);break}}return s}function Dt(){return{top:0,right:0,bottom:0,left:0}}function Ct(e){return Object.assign({},Dt(),e)}function Bt(e,t){return t.reduce(function(r,n){return r[n]=e,r},{})}function qe(e,t){t===void 0&&(t={});var r=t,n=r.placement,a=n===void 0?e.placement:n,o=r.strategy,l=o===void 0?e.strategy:o,i=r.boundary,s=i===void 0?wr:i,f=r.rootBoundary,u=f===void 0?jt:f,d=r.elementContext,m=d===void 0?ie:d,c=r.altBoundary,g=c===void 0?!1:c,p=r.padding,v=p===void 0?0:p,y=Ct(typeof v!="number"?v:Bt(v,pe)),x=m===ie?xr:ie,k=e.rects.popper,h=e.elements[g?x:m],b=Vr(Q(h)?h:h.contextElement||U(e.elements.popper),s,u,l),w=te(e.elements.reference),O=St({reference:w,element:k,strategy:"absolute",placement:a}),j=Me(Object.assign({},k,O)),A=m===ie?j:w,$={top:b.top-A.top+y.top,bottom:A.bottom-b.bottom+y.bottom,left:b.left-A.left+y.left,right:A.right-b.right+y.right},E=e.modifiersData.offset;if(m===ie&&E){var M=E[a];Object.keys($).forEach(function(P){var q=[H,R].indexOf(P)>=0?1:-1,I=[D,R].indexOf(P)>=0?"y":"x";$[P]+=M[I]*q})}return $}var it={placement:"bottom",modifiers:[],strategy:"absolute"};function st(){for(var e=arguments.length,t=new Array(e),r=0;r<e;r++)t[r]=arguments[r];return!t.some(function(n){return!(n&&typeof n.getBoundingClientRect=="function")})}function zr(e){e===void 0&&(e={});var t=e,r=t.defaultModifiers,n=r===void 0?[]:r,a=t.defaultOptions,o=a===void 0?it:a;return function(i,s,f){f===void 0&&(f=o);var u={placement:"bottom",orderedModifiers:[],options:Object.assign({},it,o),modifiersData:{},elements:{reference:i,popper:s},attributes:{},styles:{}},d=[],m=!1,c={state:u,setOptions:function(y){var x=typeof y=="function"?y(u.options):y;p(),u.options=Object.assign({},o,u.options,x),u.scrollParents={reference:Q(i)?se(i):i.contextElement?se(i.contextElement):[],popper:se(s)};var k=Tr(Lr([].concat(n,u.options.modifiers)));return u.orderedModifiers=k.filter(function(h){return h.enabled}),g(),c.update()},forceUpdate:function(){if(!m){var y=u.elements,x=y.reference,k=y.popper;if(st(x,k)){u.rects={reference:mr(x,ce(k),u.options.strategy==="fixed"),popper:ze(k)},u.reset=!1,u.placement=u.options.placement,u.orderedModifiers.forEach(function($){return u.modifiersData[$.name]=Object.assign({},$.data)});for(var h=0;h<u.orderedModifiers.length;h++){if(u.reset===!0){u.reset=!1,h=-1;continue}var b=u.orderedModifiers[h],w=b.fn,O=b.options,j=O===void 0?{}:O,A=b.name;typeof w=="function"&&(u=w({state:u,options:j,name:A,instance:c})||u)}}}},update:Mr(function(){return new Promise(function(v){c.forceUpdate(),v(u)})}),destroy:function(){p(),m=!0}};if(!st(i,s))return c;c.setOptions(f).then(function(v){!m&&f.onFirstUpdate&&f.onFirstUpdate(v)});function g(){u.orderedModifiers.forEach(function(v){var y=v.name,x=v.options,k=x===void 0?{}:x,h=v.effect;if(typeof h=="function"){var b=h({state:u,name:y,instance:c,options:k}),w=function(){};d.push(b||w)}})}function p(){d.forEach(function(v){return v()}),d=[]}return c}}var ye={passive:!0};function Fr(e){var t=e.state,r=e.instance,n=e.options,a=n.scroll,o=a===void 0?!0:a,l=n.resize,i=l===void 0?!0:l,s=B(t.elements.popper),f=[].concat(t.scrollParents.reference,t.scrollParents.popper);return o&&f.forEach(function(u){u.addEventListener("scroll",r.update,ye)}),i&&s.addEventListener("resize",r.update,ye),function(){o&&f.forEach(function(u){u.removeEventListener("scroll",r.update,ye)}),i&&s.removeEventListener("resize",r.update,ye)}}const Tt={name:"eventListeners",enabled:!0,phase:"write",fn:function(){},effect:Fr,data:{}};function Ur(e){var t=e.state,r=e.name;t.modifiersData[r]=St({reference:t.rects.reference,element:t.rects.popper,strategy:"absolute",placement:t.placement})}const qr={name:"popperOffsets",enabled:!0,phase:"read",fn:Ur,data:{}};var Ir={top:"auto",right:"auto",bottom:"auto",left:"auto"};function Xr(e,t){var r=e.x,n=e.y,a=t.devicePixelRatio||1;return{x:ee(r*a)/a||0,y:ee(n*a)/a||0}}function lt(e){var t,r=e.popper,n=e.popperRect,a=e.placement,o=e.variation,l=e.offsets,i=e.position,s=e.gpuAcceleration,f=e.adaptive,u=e.roundOffsets,d=e.isFixed,m=l.x,c=m===void 0?0:m,g=l.y,p=g===void 0?0:g,v=typeof u=="function"?u({x:c,y:p}):{x:c,y:p};c=v.x,p=v.y;var y=l.hasOwnProperty("x"),x=l.hasOwnProperty("y"),k=C,h=D,b=window;if(f){var w=ce(r),O="clientHeight",j="clientWidth";if(w===B(r)&&(w=U(r),V(w).position!=="static"&&i==="absolute"&&(O="scrollHeight",j="scrollWidth")),w=w,a===D||(a===C||a===H)&&o===fe){h=R;var A=d&&w===b&&b.visualViewport?b.visualViewport.height:w[O];p-=A-n.height,p*=s?1:-1}if(a===C||(a===D||a===R)&&o===fe){k=H;var $=d&&w===b&&b.visualViewport?b.visualViewport.width:w[j];c-=$-n.width,c*=s?1:-1}}var E=Object.assign({position:i},f&&Ir),M=u===!0?Xr({x:c,y:p},B(r)):{x:c,y:p};if(c=M.x,p=M.y,s){var P;return Object.assign({},E,(P={},P[h]=x?"0":"",P[k]=y?"0":"",P.transform=(b.devicePixelRatio||1)<=1?"translate("+c+"px, "+p+"px)":"translate3d("+c+"px, "+p+"px, 0)",P))}return Object.assign({},E,(t={},t[h]=x?p+"px":"",t[k]=y?c+"px":"",t.transform="",t))}function Yr(e){var t=e.state,r=e.options,n=r.gpuAcceleration,a=n===void 0?!0:n,o=r.adaptive,l=o===void 0?!0:o,i=r.roundOffsets,s=i===void 0?!0:i,f={placement:W(t.placement),variation:ne(t.placement),popper:t.elements.popper,popperRect:t.rects.popper,gpuAcceleration:a,isFixed:t.options.strategy==="fixed"};t.modifiersData.popperOffsets!=null&&(t.styles.popper=Object.assign({},t.styles.popper,lt(Object.assign({},f,{offsets:t.modifiersData.popperOffsets,position:t.options.strategy,adaptive:l,roundOffsets:s})))),t.modifiersData.arrow!=null&&(t.styles.arrow=Object.assign({},t.styles.arrow,lt(Object.assign({},f,{offsets:t.modifiersData.arrow,position:"absolute",adaptive:!1,roundOffsets:s})))),t.attributes.popper=Object.assign({},t.attributes.popper,{"data-popper-placement":t.placement})}const Mt={name:"computeStyles",enabled:!0,phase:"beforeWrite",fn:Yr,data:{}};function Gr(e){var t=e.state;Object.keys(t.elements).forEach(function(r){var n=t.styles[r]||{},a=t.attributes[r]||{},o=t.elements[r];!T(o)||!N(o)||(Object.assign(o.style,n),Object.keys(a).forEach(function(l){var i=a[l];i===!1?o.removeAttribute(l):o.setAttribute(l,i===!0?"":i)}))})}function Jr(e){var t=e.state,r={popper:{position:t.options.strategy,left:"0",top:"0",margin:"0"},arrow:{position:"absolute"},reference:{}};return Object.assign(t.elements.popper.style,r.popper),t.styles=r,t.elements.arrow&&Object.assign(t.elements.arrow.style,r.arrow),function(){Object.keys(t.elements).forEach(function(n){var a=t.elements[n],o=t.attributes[n]||{},l=Object.keys(t.styles.hasOwnProperty(n)?t.styles[n]:r[n]),i=l.reduce(function(s,f){return s[f]="",s},{});!T(a)||!N(a)||(Object.assign(a.style,i),Object.keys(o).forEach(function(s){a.removeAttribute(s)}))})}}const Kr={name:"applyStyles",enabled:!0,phase:"write",fn:Gr,effect:Jr,requires:["computeStyles"]};var Qr=[Tt,qr,Mt,Kr],Zr={left:"right",right:"left",bottom:"top",top:"bottom"};function Oe(e){return e.replace(/left|right|bottom|top/g,function(t){return Zr[t]})}var _r={start:"end",end:"start"};function ut(e){return e.replace(/start|end/g,function(t){return _r[t]})}function en(e,t){t===void 0&&(t={});var r=t,n=r.placement,a=r.boundary,o=r.rootBoundary,l=r.padding,i=r.flipVariations,s=r.allowedAutoPlacements,f=s===void 0?Et:s,u=ne(n),d=u?i?at:at.filter(function(g){return ne(g)===u}):pe,m=d.filter(function(g){return f.indexOf(g)>=0});m.length===0&&(m=d);var c=m.reduce(function(g,p){return g[p]=qe(e,{placement:p,boundary:a,rootBoundary:o,padding:l})[W(p)],g},{});return Object.keys(c).sort(function(g,p){return c[g]-c[p]})}function tn(e){if(W(e)===Fe)return[];var t=Oe(e);return[ut(e),t,ut(t)]}function rn(e){var t=e.state,r=e.options,n=e.name;if(!t.modifiersData[n]._skip){for(var a=r.mainAxis,o=a===void 0?!0:a,l=r.altAxis,i=l===void 0?!0:l,s=r.fallbackPlacements,f=r.padding,u=r.boundary,d=r.rootBoundary,m=r.altBoundary,c=r.flipVariations,g=c===void 0?!0:c,p=r.allowedAutoPlacements,v=t.options.placement,y=W(v),x=y===v,k=s||(x||!g?[Oe(v)]:tn(v)),h=[v].concat(k).reduce(function(Z,z){return Z.concat(W(z)===Fe?en(t,{placement:z,boundary:u,rootBoundary:d,padding:f,flipVariations:g,allowedAutoPlacements:p}):z)},[]),b=t.rects.reference,w=t.rects.popper,O=new Map,j=!0,A=h[0],$=0;$<h.length;$++){var E=h[$],M=W(E),P=ne(E)===re,q=[D,R].indexOf(M)>=0,I=q?"width":"height",S=qe(t,{placement:E,boundary:u,rootBoundary:d,altBoundary:m,padding:f}),L=q?P?H:C:P?R:D;b[I]>w[I]&&(L=Oe(L));var de=Oe(L),X=[];if(o&&X.push(S[M]<=0),i&&X.push(S[L]<=0,S[de]<=0),X.every(function(Z){return Z})){A=E,j=!1;break}O.set(E,X)}if(j)for(var ve=g?3:1,Ae=function(z){var oe=h.find(function(he){var Y=O.get(he);if(Y)return Y.slice(0,z).every(function(je){return je})});if(oe)return A=oe,"break"},ae=ve;ae>0;ae--){var ge=Ae(ae);if(ge==="break")break}t.placement!==A&&(t.modifiersData[n]._skip=!0,t.placement=A,t.reset=!0)}}const nn={name:"flip",enabled:!0,phase:"main",fn:rn,requiresIfExists:["offset"],data:{_skip:!1}};function an(e,t,r){var n=W(e),a=[C,D].indexOf(n)>=0?-1:1,o=typeof r=="function"?r(Object.assign({},t,{placement:e})):r,l=o[0],i=o[1];return l=l||0,i=(i||0)*a,[C,H].indexOf(n)>=0?{x:i,y:l}:{x:l,y:i}}function on(e){var t=e.state,r=e.options,n=e.name,a=r.offset,o=a===void 0?[0,0]:a,l=Et.reduce(function(u,d){return u[d]=an(d,t.rects,o),u},{}),i=l[t.placement],s=i.x,f=i.y;t.modifiersData.popperOffsets!=null&&(t.modifiersData.popperOffsets.x+=s,t.modifiersData.popperOffsets.y+=f),t.modifiersData[n]=l}const sn={name:"offset",enabled:!0,phase:"main",requires:["popperOffsets"],fn:on};function ln(e){return e==="x"?"y":"x"}function le(e,t,r){return K(e,ke(t,r))}function un(e,t,r){var n=le(e,t,r);return n>r?r:n}function fn(e){var t=e.state,r=e.options,n=e.name,a=r.mainAxis,o=a===void 0?!0:a,l=r.altAxis,i=l===void 0?!1:l,s=r.boundary,f=r.rootBoundary,u=r.altBoundary,d=r.padding,m=r.tether,c=m===void 0?!0:m,g=r.tetherOffset,p=g===void 0?0:g,v=qe(t,{boundary:s,rootBoundary:f,padding:d,altBoundary:u}),y=W(t.placement),x=ne(t.placement),k=!x,h=Ue(y),b=ln(h),w=t.modifiersData.popperOffsets,O=t.rects.reference,j=t.rects.popper,A=typeof p=="function"?p(Object.assign({},t.rects,{placement:t.placement})):p,$=typeof A=="number"?{mainAxis:A,altAxis:A}:Object.assign({mainAxis:0,altAxis:0},A),E=t.modifiersData.offset?t.modifiersData.offset[t.placement]:null,M={x:0,y:0};if(w){if(o){var P,q=h==="y"?D:C,I=h==="y"?R:H,S=h==="y"?"height":"width",L=w[h],de=L+v[q],X=L-v[I],ve=c?-j[S]/2:0,Ae=x===re?O[S]:j[S],ae=x===re?-j[S]:-O[S],ge=t.elements.arrow,Z=c&&ge?ze(ge):{width:0,height:0},z=t.modifiersData["arrow#persistent"]?t.modifiersData["arrow#persistent"].padding:Dt(),oe=z[q],he=z[I],Y=le(0,O[S],Z[S]),je=k?O[S]/2-ve-Y-oe-$.mainAxis:Ae-Y-oe-$.mainAxis,Lt=k?-O[S]/2+ve+Y+he+$.mainAxis:ae+Y+he+$.mainAxis,Ee=t.elements.arrow&&ce(t.elements.arrow),Rt=Ee?h==="y"?Ee.clientTop||0:Ee.clientLeft||0:0,Ie=(P=E==null?void 0:E[h])!=null?P:0,Ht=L+je-Ie-Rt,Wt=L+Lt-Ie,Xe=le(c?ke(de,Ht):de,L,c?K(X,Wt):X);w[h]=Xe,M[h]=Xe-L}if(i){var Ye,Nt=h==="x"?D:C,Vt=h==="x"?R:H,G=w[b],me=b==="y"?"height":"width",Ge=G+v[Nt],Je=G-v[Vt],Pe=[D,C].indexOf(y)!==-1,Ke=(Ye=E==null?void 0:E[b])!=null?Ye:0,Qe=Pe?Ge:G-O[me]-j[me]-Ke+$.altAxis,Ze=Pe?G+O[me]+j[me]-Ke-$.altAxis:Je,_e=c&&Pe?un(Qe,G,Ze):le(c?Qe:Ge,G,c?Ze:Je);w[b]=_e,M[b]=_e-G}t.modifiersData[n]=M}}const cn={name:"preventOverflow",enabled:!0,phase:"main",fn,requiresIfExists:["offset"]};var pn=function(t,r){return t=typeof t=="function"?t(Object.assign({},r.rects,{placement:r.placement})):t,Ct(typeof t!="number"?t:Bt(t,pe))};function dn(e){var t,r=e.state,n=e.name,a=e.options,o=r.elements.arrow,l=r.modifiersData.popperOffsets,i=W(r.placement),s=Ue(i),f=[C,H].indexOf(i)>=0,u=f?"height":"width";if(!(!o||!l)){var d=pn(a.padding,r),m=ze(o),c=s==="y"?D:C,g=s==="y"?R:H,p=r.rects.reference[u]+r.rects.reference[s]-l[s]-r.rects.popper[u],v=l[s]-r.rects.reference[s],y=ce(o),x=y?s==="y"?y.clientHeight||0:y.clientWidth||0:0,k=p/2-v/2,h=d[c],b=x-m[u]-d[g],w=x/2-m[u]/2+k,O=le(h,w,b),j=s;r.modifiersData[n]=(t={},t[j]=O,t.centerOffset=O-w,t)}}function vn(e){var t=e.state,r=e.options,n=r.element,a=n===void 0?"[data-popper-arrow]":n;a!=null&&(typeof a=="string"&&(a=t.elements.popper.querySelector(a),!a)||Pt(t.elements.popper,a)&&(t.elements.arrow=a))}const gn={name:"arrow",enabled:!0,phase:"main",fn:dn,effect:vn,requires:["popperOffsets"],requiresIfExists:["preventOverflow"]},hn=zr({defaultModifiers:[...Qr,sn,nn,cn,Mt,Tt,gn]});function jn({locked:e=!1,overflowPadding:t=8,offsetDistance:r=8,offsetSkid:n=0,gpuAcceleration:a=!0,adaptive:o=!0,scroll:l=!0,resize:i=!0,arrow:s=!1,placement:f,strategy:u},d){const m=xe(null),c=xe(null),g=xe(null);return yt(()=>{bt(p=>{if(!c.value||!m.value&&!(d!=null&&d.value))return;const v=et(c),y=(d==null?void 0:d.value)||et(m);if(!(v instanceof HTMLElement)||!y)return;const x={modifiers:[{name:"flip",enabled:!e},{name:"preventOverflow",options:{padding:t}},{name:"offset",options:{offset:[n,r]}},{name:"computeStyles",options:{adaptive:o,gpuAcceleration:a}},{name:"eventListeners",options:{scroll:l,resize:i}},{name:"arrow",enabled:s}]};f&&(x.placement=f),u&&(x.strategy=u),g.value=hn(y,v,x),p(g.value.destroy)})}),[m,c,g]}const F=ft(ue.ui.strategy,ue.ui.badge,Zt),mn=Re({inheritAttrs:!1,props:{size:{type:String,default:()=>F.default.size,validator(e){return Object.keys(F.size).includes(e)}},color:{type:String,default:()=>F.default.color,validator(e){return[...ue.ui.colors,...Object.keys(F.color)].includes(e)}},variant:{type:String,default:()=>F.default.variant,validator(e){return[...Object.keys(F.variant),...Object.values(F.color).flatMap(t=>Object.keys(t))].includes(e)}},label:{type:[String,Number],default:null},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})}},setup(e){const{ui:t,attrs:r}=ct("badge",pt(e,"ui"),F),{size:n,rounded:a}=Jt({ui:t,props:e}),o=dt(()=>{var i,s;const l=((s=(i=t.value.color)==null?void 0:i[e.color])==null?void 0:s[e.variant])||t.value.variant[e.variant];return vt(gt(t.value.base,t.value.font,a.value,t.value.size[n.value],l==null?void 0:l.replaceAll("{color}",e.color)),e.class)});return{attrs:r,badgeClass:o}}});function yn(e,t,r,n,a,o){return _(),we("span",mt({class:e.badgeClass},e.attrs),[J(e.$slots,"default",{},()=>[Kt(Qt(e.label),1)])],16)}const En=Le(mn,[["render",yn]]);export{ur as A,$n as E,sr as N,fr as T,En as _,dr as a,pr as b,On as c,jn as d,wn as e,An as f,xn as i,Ce as o,kn as s,xt as u};
