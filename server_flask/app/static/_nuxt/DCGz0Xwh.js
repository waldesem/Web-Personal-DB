import{r as ee,L as Re,N as dt,ar as at,x as T,K as vt,P as Ve,as as zt,J as Te,F as mt,g as Me,M as Ut,_ as Ft,m as qt,k as Ie,l as ht,s as Yt,v as Xt,y as Kt,z as se,S as Gt,o as be,i as Jt,w as Qt,a as Zt,B as G,c as Pe,b as Se,C as Be,D as _t}from"./BPBLQG6i.js";import{b as er,u as tr}from"./B7F370T9.js";const rr={base:"relative inline-flex flex-shrink-0 border-2 border-transparent disabled:cursor-not-allowed disabled:opacity-50 focus:outline-none",rounded:"rounded-full",ring:"focus-visible:ring-2 focus-visible:ring-{color}-500 dark:focus-visible:ring-{color}-400 focus-visible:ring-offset-2 focus-visible:ring-offset-white dark:focus-visible:ring-offset-gray-900",active:"bg-{color}-500 dark:bg-{color}-400",inactive:"bg-gray-200 dark:bg-gray-700",size:{"2xs":"h-3 w-5",xs:"h-3.5 w-6",sm:"h-4 w-7",md:"h-5 w-9",lg:"h-6 w-11",xl:"h-7 w-[3.25rem]","2xl":"h-8 w-[3.75rem]"},container:{base:"pointer-events-none relative inline-block rounded-full bg-white dark:bg-gray-900 shadow transform ring-0 transition ease-in-out duration-200",active:{"2xs":"translate-x-2 rtl:-translate-x-2",xs:"translate-x-2.5 rtl:-translate-x-2.5",sm:"translate-x-3 rtl:-translate-x-3",md:"translate-x-4 rtl:-translate-x-4",lg:"translate-x-5 rtl:-translate-x-5",xl:"translate-x-6 rtl:-translate-x-6","2xl":"translate-x-7 rtl:-translate-x-7"},inactive:"translate-x-0 rtl:-translate-x-0",size:{"2xs":"h-2 w-2",xs:"h-2.5 w-2.5",sm:"h-3 w-3",md:"h-4 w-4",lg:"h-5 w-5",xl:"h-6 w-6","2xl":"h-7 w-7"}},icon:{base:"absolute inset-0 h-full w-full flex items-center justify-center transition-opacity",active:"opacity-100 ease-in duration-200",inactive:"opacity-0 ease-out duration-100",size:{"2xs":"h-2 w-2",xs:"h-2 w-2",sm:"h-2 w-2",md:"h-3 w-3",lg:"h-4 w-4",xl:"h-5 w-5","2xl":"h-6 w-6"},on:"text-{color}-500 dark:text-{color}-400",off:"text-gray-400 dark:text-gray-500",loading:"animate-spin text-{color}-500 dark:text-{color}-400"},default:{onIcon:null,offIcon:null,loadingIcon:"i-heroicons-arrow-path-20-solid",color:"primary",size:"md"}};function D(e){if(e==null)return window;if(e.toString()!=="[object Window]"){var t=e.ownerDocument;return t&&t.defaultView||window}return e}function Z(e){var t=D(e).Element;return e instanceof t||e instanceof Element}function I(e){var t=D(e).HTMLElement;return e instanceof t||e instanceof HTMLElement}function We(e){if(typeof ShadowRoot>"u")return!1;var t=D(e).ShadowRoot;return e instanceof t||e instanceof ShadowRoot}var Q=Math.max,Ae=Math.min,te=Math.round;function Le(){var e=navigator.userAgentData;return e!=null&&e.brands&&Array.isArray(e.brands)?e.brands.map(function(t){return t.brand+"/"+t.version}).join(" "):navigator.userAgent}function gt(){return!/^((?!chrome|android).)*safari/i.test(Le())}function re(e,t,r){t===void 0&&(t=!1),r===void 0&&(r=!1);var a=e.getBoundingClientRect(),n=1,o=1;t&&I(e)&&(n=e.offsetWidth>0&&te(a.width)/e.offsetWidth||1,o=e.offsetHeight>0&&te(a.height)/e.offsetHeight||1);var l=Z(e)?D(e):window,i=l.visualViewport,s=!gt()&&r,f=(a.left+(s&&i?i.offsetLeft:0))/n,u=(a.top+(s&&i?i.offsetTop:0))/o,v=a.width/n,m=a.height/o;return{width:v,height:m,top:u,right:f+v,bottom:u+m,left:f,x:f,y:u}}function ze(e){var t=D(e),r=t.pageXOffset,a=t.pageYOffset;return{scrollLeft:r,scrollTop:a}}function nr(e){return{scrollLeft:e.scrollLeft,scrollTop:e.scrollTop}}function ar(e){return e===D(e)||!I(e)?ze(e):nr(e)}function M(e){return e?(e.nodeName||"").toLowerCase():null}function U(e){return((Z(e)?e.ownerDocument:e.document)||window.document).documentElement}function Ue(e){return re(U(e)).left+ze(e).scrollLeft}function W(e){return D(e).getComputedStyle(e)}function Fe(e){var t=W(e),r=t.overflow,a=t.overflowX,n=t.overflowY;return/auto|scroll|overlay|hidden/.test(r+n+a)}function or(e){var t=e.getBoundingClientRect(),r=te(t.width)/e.offsetWidth||1,a=te(t.height)/e.offsetHeight||1;return r!==1||a!==1}function ir(e,t,r){r===void 0&&(r=!1);var a=I(t),n=I(t)&&or(t),o=U(t),l=re(e,n,r),i={scrollLeft:0,scrollTop:0},s={x:0,y:0};return(a||!a&&!r)&&((M(t)!=="body"||Fe(o))&&(i=ar(t)),I(t)?(s=re(t,!0),s.x+=t.clientLeft,s.y+=t.clientTop):o&&(s.x=Ue(o))),{x:l.left+i.scrollLeft-s.x,y:l.top+i.scrollTop-s.y,width:l.width,height:l.height}}function qe(e){var t=re(e),r=e.offsetWidth,a=e.offsetHeight;return Math.abs(t.width-r)<=1&&(r=t.width),Math.abs(t.height-a)<=1&&(a=t.height),{x:e.offsetLeft,y:e.offsetTop,width:r,height:a}}function Ee(e){return M(e)==="html"?e:e.assignedSlot||e.parentNode||(We(e)?e.host:null)||U(e)}function yt(e){return["html","body","#document"].indexOf(M(e))>=0?e.ownerDocument.body:I(e)&&Fe(e)?e:yt(Ee(e))}function ue(e,t){var r;t===void 0&&(t=[]);var a=yt(e),n=a===((r=e.ownerDocument)==null?void 0:r.body),o=D(a),l=n?[o].concat(o.visualViewport||[],Fe(a)?a:[]):a,i=t.concat(l);return n?i:i.concat(ue(Ee(l)))}function sr(e){return["table","td","th"].indexOf(M(e))>=0}function ot(e){return!I(e)||W(e).position==="fixed"?null:e.offsetParent}function lr(e){var t=/firefox/i.test(Le()),r=/Trident/i.test(Le());if(r&&I(e)){var a=W(e);if(a.position==="fixed")return null}var n=Ee(e);for(We(n)&&(n=n.host);I(n)&&["html","body"].indexOf(M(n))<0;){var o=W(n);if(o.transform!=="none"||o.perspective!=="none"||o.contain==="paint"||["transform","perspective"].indexOf(o.willChange)!==-1||t&&o.willChange==="filter"||t&&o.filter&&o.filter!=="none")return n;n=n.parentNode}return null}function pe(e){for(var t=D(e),r=ot(e);r&&sr(r)&&W(r).position==="static";)r=ot(r);return r&&(M(r)==="html"||M(r)==="body"&&W(r).position==="static")?t:r||lr(e)||t}var S="top",N="bottom",R="right",B="left",Ye="auto",de=[S,N,R,B],ne="start",ce="end",ur="clippingParents",bt="viewport",le="popper",fr="reference",it=de.reduce(function(e,t){return e.concat([t+"-"+ne,t+"-"+ce])},[]),wt=[].concat(de,[Ye]).reduce(function(e,t){return e.concat([t,t+"-"+ne,t+"-"+ce])},[]),cr="beforeRead",pr="read",dr="afterRead",vr="beforeMain",mr="main",hr="afterMain",gr="beforeWrite",yr="write",br="afterWrite",wr=[cr,pr,dr,vr,mr,hr,gr,yr,br];function xr(e){var t=new Map,r=new Set,a=[];e.forEach(function(o){t.set(o.name,o)});function n(o){r.add(o.name);var l=[].concat(o.requires||[],o.requiresIfExists||[]);l.forEach(function(i){if(!r.has(i)){var s=t.get(i);s&&n(s)}}),a.push(o)}return e.forEach(function(o){r.has(o.name)||n(o)}),a}function Or(e){var t=xr(e);return wr.reduce(function(r,a){return r.concat(t.filter(function(n){return n.phase===a}))},[])}function Ar(e){var t;return function(){return t||(t=new Promise(function(r){Promise.resolve().then(function(){t=void 0,r(e())})})),t}}function Er(e){var t=e.reduce(function(r,a){var n=r[a.name];return r[a.name]=n?Object.assign({},n,a,{options:Object.assign({},n.options,a.options),data:Object.assign({},n.data,a.data)}):a,r},{});return Object.keys(t).map(function(r){return t[r]})}function kr(e,t){var r=D(e),a=U(e),n=r.visualViewport,o=a.clientWidth,l=a.clientHeight,i=0,s=0;if(n){o=n.width,l=n.height;var f=gt();(f||!f&&t==="fixed")&&(i=n.offsetLeft,s=n.offsetTop)}return{width:o,height:l,x:i+Ue(e),y:s}}function jr(e){var t,r=U(e),a=ze(e),n=(t=e.ownerDocument)==null?void 0:t.body,o=Q(r.scrollWidth,r.clientWidth,n?n.scrollWidth:0,n?n.clientWidth:0),l=Q(r.scrollHeight,r.clientHeight,n?n.scrollHeight:0,n?n.clientHeight:0),i=-a.scrollLeft+Ue(e),s=-a.scrollTop;return W(n||r).direction==="rtl"&&(i+=Q(r.clientWidth,n?n.clientWidth:0)-o),{width:o,height:l,x:i,y:s}}function xt(e,t){var r=t.getRootNode&&t.getRootNode();if(e.contains(t))return!0;if(r&&We(r)){var a=t;do{if(a&&e.isSameNode(a))return!0;a=a.parentNode||a.host}while(a)}return!1}function He(e){return Object.assign({},e,{left:e.x,top:e.y,right:e.x+e.width,bottom:e.y+e.height})}function Cr(e,t){var r=re(e,!1,t==="fixed");return r.top=r.top+e.clientTop,r.left=r.left+e.clientLeft,r.bottom=r.top+e.clientHeight,r.right=r.left+e.clientWidth,r.width=e.clientWidth,r.height=e.clientHeight,r.x=r.left,r.y=r.top,r}function st(e,t,r){return t===bt?He(kr(e,r)):Z(t)?Cr(t,r):He(jr(U(e)))}function $r(e){var t=ue(Ee(e)),r=["absolute","fixed"].indexOf(W(e).position)>=0,a=r&&I(e)?pe(e):e;return Z(a)?t.filter(function(n){return Z(n)&&xt(n,a)&&M(n)!=="body"}):[]}function Pr(e,t,r,a){var n=t==="clippingParents"?$r(e):[].concat(t),o=[].concat(n,[r]),l=o[0],i=o.reduce(function(s,f){var u=st(e,f,a);return s.top=Q(u.top,s.top),s.right=Ae(u.right,s.right),s.bottom=Ae(u.bottom,s.bottom),s.left=Q(u.left,s.left),s},st(e,l,a));return i.width=i.right-i.left,i.height=i.bottom-i.top,i.x=i.left,i.y=i.top,i}function V(e){return e.split("-")[0]}function ae(e){return e.split("-")[1]}function Xe(e){return["top","bottom"].indexOf(e)>=0?"x":"y"}function Ot(e){var t=e.reference,r=e.element,a=e.placement,n=a?V(a):null,o=a?ae(a):null,l=t.x+t.width/2-r.width/2,i=t.y+t.height/2-r.height/2,s;switch(n){case S:s={x:l,y:t.y-r.height};break;case N:s={x:l,y:t.y+t.height};break;case R:s={x:t.x+t.width,y:i};break;case B:s={x:t.x-r.width,y:i};break;default:s={x:t.x,y:t.y}}var f=n?Xe(n):null;if(f!=null){var u=f==="y"?"height":"width";switch(o){case ne:s[f]=s[f]-(t[u]/2-r[u]/2);break;case ce:s[f]=s[f]+(t[u]/2-r[u]/2);break}}return s}function At(){return{top:0,right:0,bottom:0,left:0}}function Et(e){return Object.assign({},At(),e)}function kt(e,t){return t.reduce(function(r,a){return r[a]=e,r},{})}function Ke(e,t){t===void 0&&(t={});var r=t,a=r.placement,n=a===void 0?e.placement:a,o=r.strategy,l=o===void 0?e.strategy:o,i=r.boundary,s=i===void 0?ur:i,f=r.rootBoundary,u=f===void 0?bt:f,v=r.elementContext,m=v===void 0?le:v,c=r.altBoundary,h=c===void 0?!1:c,p=r.padding,g=p===void 0?0:p,b=Et(typeof g!="number"?g:kt(g,de)),d=m===le?fr:le,O=e.rects.popper,y=e.elements[h?d:m],w=Pr(Z(y)?y:y.contextElement||U(e.elements.popper),s,u,l),x=re(e.elements.reference),A=Ot({reference:x,element:O,strategy:"absolute",placement:n}),E=He(Object.assign({},O,A)),j=m===le?E:x,k={top:w.top-j.top+b.top,bottom:j.bottom-w.bottom+b.bottom,left:w.left-j.left+b.left,right:j.right-w.right+b.right},C=e.modifiersData.offset;if(m===le&&C){var L=C[n];Object.keys(k).forEach(function($){var F=[R,N].indexOf($)>=0?1:-1,q=[S,N].indexOf($)>=0?"y":"x";k[$]+=L[q]*F})}return k}var lt={placement:"bottom",modifiers:[],strategy:"absolute"};function ut(){for(var e=arguments.length,t=new Array(e),r=0;r<e;r++)t[r]=arguments[r];return!t.some(function(a){return!(a&&typeof a.getBoundingClientRect=="function")})}function Sr(e){e===void 0&&(e={});var t=e,r=t.defaultModifiers,a=r===void 0?[]:r,n=t.defaultOptions,o=n===void 0?lt:n;return function(i,s,f){f===void 0&&(f=o);var u={placement:"bottom",orderedModifiers:[],options:Object.assign({},lt,o),modifiersData:{},elements:{reference:i,popper:s},attributes:{},styles:{}},v=[],m=!1,c={state:u,setOptions:function(b){var d=typeof b=="function"?b(u.options):b;p(),u.options=Object.assign({},o,u.options,d),u.scrollParents={reference:Z(i)?ue(i):i.contextElement?ue(i.contextElement):[],popper:ue(s)};var O=Or(Er([].concat(a,u.options.modifiers)));return u.orderedModifiers=O.filter(function(y){return y.enabled}),h(),c.update()},forceUpdate:function(){if(!m){var b=u.elements,d=b.reference,O=b.popper;if(ut(d,O)){u.rects={reference:ir(d,pe(O),u.options.strategy==="fixed"),popper:qe(O)},u.reset=!1,u.placement=u.options.placement,u.orderedModifiers.forEach(function(k){return u.modifiersData[k.name]=Object.assign({},k.data)});for(var y=0;y<u.orderedModifiers.length;y++){if(u.reset===!0){u.reset=!1,y=-1;continue}var w=u.orderedModifiers[y],x=w.fn,A=w.options,E=A===void 0?{}:A,j=w.name;typeof x=="function"&&(u=x({state:u,options:E,name:j,instance:c})||u)}}}},update:Ar(function(){return new Promise(function(g){c.forceUpdate(),g(u)})}),destroy:function(){p(),m=!0}};if(!ut(i,s))return c;c.setOptions(f).then(function(g){!m&&f.onFirstUpdate&&f.onFirstUpdate(g)});function h(){u.orderedModifiers.forEach(function(g){var b=g.name,d=g.options,O=d===void 0?{}:d,y=g.effect;if(typeof y=="function"){var w=y({state:u,name:b,instance:c,options:O}),x=function(){};v.push(w||x)}})}function p(){v.forEach(function(g){return g()}),v=[]}return c}}var we={passive:!0};function Br(e){var t=e.state,r=e.instance,a=e.options,n=a.scroll,o=n===void 0?!0:n,l=a.resize,i=l===void 0?!0:l,s=D(t.elements.popper),f=[].concat(t.scrollParents.reference,t.scrollParents.popper);return o&&f.forEach(function(u){u.addEventListener("scroll",r.update,we)}),i&&s.addEventListener("resize",r.update,we),function(){o&&f.forEach(function(u){u.removeEventListener("scroll",r.update,we)}),i&&s.removeEventListener("resize",r.update,we)}}const jt={name:"eventListeners",enabled:!0,phase:"write",fn:function(){},effect:Br,data:{}};function Dr(e){var t=e.state,r=e.name;t.modifiersData[r]=Ot({reference:t.rects.reference,element:t.rects.popper,strategy:"absolute",placement:t.placement})}const Tr={name:"popperOffsets",enabled:!0,phase:"read",fn:Dr,data:{}};var Ir={top:"auto",right:"auto",bottom:"auto",left:"auto"};function Lr(e,t){var r=e.x,a=e.y,n=t.devicePixelRatio||1;return{x:te(r*n)/n||0,y:te(a*n)/n||0}}function ft(e){var t,r=e.popper,a=e.popperRect,n=e.placement,o=e.variation,l=e.offsets,i=e.position,s=e.gpuAcceleration,f=e.adaptive,u=e.roundOffsets,v=e.isFixed,m=l.x,c=m===void 0?0:m,h=l.y,p=h===void 0?0:h,g=typeof u=="function"?u({x:c,y:p}):{x:c,y:p};c=g.x,p=g.y;var b=l.hasOwnProperty("x"),d=l.hasOwnProperty("y"),O=B,y=S,w=window;if(f){var x=pe(r),A="clientHeight",E="clientWidth";if(x===D(r)&&(x=U(r),W(x).position!=="static"&&i==="absolute"&&(A="scrollHeight",E="scrollWidth")),x=x,n===S||(n===B||n===R)&&o===ce){y=N;var j=v&&x===w&&w.visualViewport?w.visualViewport.height:x[A];p-=j-a.height,p*=s?1:-1}if(n===B||(n===S||n===N)&&o===ce){O=R;var k=v&&x===w&&w.visualViewport?w.visualViewport.width:x[E];c-=k-a.width,c*=s?1:-1}}var C=Object.assign({position:i},f&&Ir),L=u===!0?Lr({x:c,y:p},D(r)):{x:c,y:p};if(c=L.x,p=L.y,s){var $;return Object.assign({},C,($={},$[y]=d?"0":"",$[O]=b?"0":"",$.transform=(w.devicePixelRatio||1)<=1?"translate("+c+"px, "+p+"px)":"translate3d("+c+"px, "+p+"px, 0)",$))}return Object.assign({},C,(t={},t[y]=d?p+"px":"",t[O]=b?c+"px":"",t.transform="",t))}function Hr(e){var t=e.state,r=e.options,a=r.gpuAcceleration,n=a===void 0?!0:a,o=r.adaptive,l=o===void 0?!0:o,i=r.roundOffsets,s=i===void 0?!0:i,f={placement:V(t.placement),variation:ae(t.placement),popper:t.elements.popper,popperRect:t.rects.popper,gpuAcceleration:n,isFixed:t.options.strategy==="fixed"};t.modifiersData.popperOffsets!=null&&(t.styles.popper=Object.assign({},t.styles.popper,ft(Object.assign({},f,{offsets:t.modifiersData.popperOffsets,position:t.options.strategy,adaptive:l,roundOffsets:s})))),t.modifiersData.arrow!=null&&(t.styles.arrow=Object.assign({},t.styles.arrow,ft(Object.assign({},f,{offsets:t.modifiersData.arrow,position:"absolute",adaptive:!1,roundOffsets:s})))),t.attributes.popper=Object.assign({},t.attributes.popper,{"data-popper-placement":t.placement})}const Ct={name:"computeStyles",enabled:!0,phase:"beforeWrite",fn:Hr,data:{}};function Nr(e){var t=e.state;Object.keys(t.elements).forEach(function(r){var a=t.styles[r]||{},n=t.attributes[r]||{},o=t.elements[r];!I(o)||!M(o)||(Object.assign(o.style,a),Object.keys(n).forEach(function(l){var i=n[l];i===!1?o.removeAttribute(l):o.setAttribute(l,i===!0?"":i)}))})}function Rr(e){var t=e.state,r={popper:{position:t.options.strategy,left:"0",top:"0",margin:"0"},arrow:{position:"absolute"},reference:{}};return Object.assign(t.elements.popper.style,r.popper),t.styles=r,t.elements.arrow&&Object.assign(t.elements.arrow.style,r.arrow),function(){Object.keys(t.elements).forEach(function(a){var n=t.elements[a],o=t.attributes[a]||{},l=Object.keys(t.styles.hasOwnProperty(a)?t.styles[a]:r[a]),i=l.reduce(function(s,f){return s[f]="",s},{});!I(n)||!M(n)||(Object.assign(n.style,i),Object.keys(o).forEach(function(s){n.removeAttribute(s)}))})}}const Vr={name:"applyStyles",enabled:!0,phase:"write",fn:Nr,effect:Rr,requires:["computeStyles"]};var Mr=[jt,Tr,Ct,Vr],Wr={left:"right",right:"left",bottom:"top",top:"bottom"};function xe(e){return e.replace(/left|right|bottom|top/g,function(t){return Wr[t]})}var zr={start:"end",end:"start"};function ct(e){return e.replace(/start|end/g,function(t){return zr[t]})}function Ur(e,t){t===void 0&&(t={});var r=t,a=r.placement,n=r.boundary,o=r.rootBoundary,l=r.padding,i=r.flipVariations,s=r.allowedAutoPlacements,f=s===void 0?wt:s,u=ae(a),v=u?i?it:it.filter(function(h){return ae(h)===u}):de,m=v.filter(function(h){return f.indexOf(h)>=0});m.length===0&&(m=v);var c=m.reduce(function(h,p){return h[p]=Ke(e,{placement:p,boundary:n,rootBoundary:o,padding:l})[V(p)],h},{});return Object.keys(c).sort(function(h,p){return c[h]-c[p]})}function Fr(e){if(V(e)===Ye)return[];var t=xe(e);return[ct(e),t,ct(t)]}function qr(e){var t=e.state,r=e.options,a=e.name;if(!t.modifiersData[a]._skip){for(var n=r.mainAxis,o=n===void 0?!0:n,l=r.altAxis,i=l===void 0?!0:l,s=r.fallbackPlacements,f=r.padding,u=r.boundary,v=r.rootBoundary,m=r.altBoundary,c=r.flipVariations,h=c===void 0?!0:c,p=r.allowedAutoPlacements,g=t.options.placement,b=V(g),d=b===g,O=s||(d||!h?[xe(g)]:Fr(g)),y=[g].concat(O).reduce(function(_,z){return _.concat(V(z)===Ye?Ur(t,{placement:z,boundary:u,rootBoundary:v,padding:f,flipVariations:h,allowedAutoPlacements:p}):z)},[]),w=t.rects.reference,x=t.rects.popper,A=new Map,E=!0,j=y[0],k=0;k<y.length;k++){var C=y[k],L=V(C),$=ae(C)===ne,F=[S,N].indexOf(L)>=0,q=F?"width":"height",P=Ke(t,{placement:C,boundary:u,rootBoundary:v,altBoundary:m,padding:f}),H=F?$?R:B:$?N:S;w[q]>x[q]&&(H=xe(H));var ve=xe(H),Y=[];if(o&&Y.push(P[L]<=0),i&&Y.push(P[H]<=0,P[ve]<=0),Y.every(function(_){return _})){j=C,E=!1;break}A.set(C,Y)}if(E)for(var me=h?3:1,ke=function(z){var ie=y.find(function(ge){var X=A.get(ge);if(X)return X.slice(0,z).every(function(je){return je})});if(ie)return j=ie,"break"},oe=me;oe>0;oe--){var he=ke(oe);if(he==="break")break}t.placement!==j&&(t.modifiersData[a]._skip=!0,t.placement=j,t.reset=!0)}}const Yr={name:"flip",enabled:!0,phase:"main",fn:qr,requiresIfExists:["offset"],data:{_skip:!1}};function Xr(e,t,r){var a=V(e),n=[B,S].indexOf(a)>=0?-1:1,o=typeof r=="function"?r(Object.assign({},t,{placement:e})):r,l=o[0],i=o[1];return l=l||0,i=(i||0)*n,[B,R].indexOf(a)>=0?{x:i,y:l}:{x:l,y:i}}function Kr(e){var t=e.state,r=e.options,a=e.name,n=r.offset,o=n===void 0?[0,0]:n,l=wt.reduce(function(u,v){return u[v]=Xr(v,t.rects,o),u},{}),i=l[t.placement],s=i.x,f=i.y;t.modifiersData.popperOffsets!=null&&(t.modifiersData.popperOffsets.x+=s,t.modifiersData.popperOffsets.y+=f),t.modifiersData[a]=l}const Gr={name:"offset",enabled:!0,phase:"main",requires:["popperOffsets"],fn:Kr};function Jr(e){return e==="x"?"y":"x"}function fe(e,t,r){return Q(e,Ae(t,r))}function Qr(e,t,r){var a=fe(e,t,r);return a>r?r:a}function Zr(e){var t=e.state,r=e.options,a=e.name,n=r.mainAxis,o=n===void 0?!0:n,l=r.altAxis,i=l===void 0?!1:l,s=r.boundary,f=r.rootBoundary,u=r.altBoundary,v=r.padding,m=r.tether,c=m===void 0?!0:m,h=r.tetherOffset,p=h===void 0?0:h,g=Ke(t,{boundary:s,rootBoundary:f,padding:v,altBoundary:u}),b=V(t.placement),d=ae(t.placement),O=!d,y=Xe(b),w=Jr(y),x=t.modifiersData.popperOffsets,A=t.rects.reference,E=t.rects.popper,j=typeof p=="function"?p(Object.assign({},t.rects,{placement:t.placement})):p,k=typeof j=="number"?{mainAxis:j,altAxis:j}:Object.assign({mainAxis:0,altAxis:0},j),C=t.modifiersData.offset?t.modifiersData.offset[t.placement]:null,L={x:0,y:0};if(x){if(o){var $,F=y==="y"?S:B,q=y==="y"?N:R,P=y==="y"?"height":"width",H=x[y],ve=H+g[F],Y=H-g[q],me=c?-E[P]/2:0,ke=d===ne?A[P]:E[P],oe=d===ne?-E[P]:-A[P],he=t.elements.arrow,_=c&&he?qe(he):{width:0,height:0},z=t.modifiersData["arrow#persistent"]?t.modifiersData["arrow#persistent"].padding:At(),ie=z[F],ge=z[q],X=fe(0,A[P],_[P]),je=O?A[P]/2-me-X-ie-k.mainAxis:ke-X-ie-k.mainAxis,Ht=O?-A[P]/2+me+X+ge+k.mainAxis:oe+X+ge+k.mainAxis,Ce=t.elements.arrow&&pe(t.elements.arrow),Nt=Ce?y==="y"?Ce.clientTop||0:Ce.clientLeft||0:0,Ge=($=C==null?void 0:C[y])!=null?$:0,Rt=H+je-Ge-Nt,Vt=H+Ht-Ge,Je=fe(c?Ae(ve,Rt):ve,H,c?Q(Y,Vt):Y);x[y]=Je,L[y]=Je-H}if(i){var Qe,Mt=y==="x"?S:B,Wt=y==="x"?N:R,K=x[w],ye=w==="y"?"height":"width",Ze=K+g[Mt],_e=K-g[Wt],$e=[S,B].indexOf(b)!==-1,et=(Qe=C==null?void 0:C[w])!=null?Qe:0,tt=$e?Ze:K-A[ye]-E[ye]-et+k.altAxis,rt=$e?K+A[ye]+E[ye]-et-k.altAxis:_e,nt=c&&$e?Qr(tt,K,rt):fe(c?tt:Ze,K,c?rt:_e);x[w]=nt,L[w]=nt-K}t.modifiersData[a]=L}}const _r={name:"preventOverflow",enabled:!0,phase:"main",fn:Zr,requiresIfExists:["offset"]};var en=function(t,r){return t=typeof t=="function"?t(Object.assign({},r.rects,{placement:r.placement})):t,Et(typeof t!="number"?t:kt(t,de))};function tn(e){var t,r=e.state,a=e.name,n=e.options,o=r.elements.arrow,l=r.modifiersData.popperOffsets,i=V(r.placement),s=Xe(i),f=[B,R].indexOf(i)>=0,u=f?"height":"width";if(!(!o||!l)){var v=en(n.padding,r),m=qe(o),c=s==="y"?S:B,h=s==="y"?N:R,p=r.rects.reference[u]+r.rects.reference[s]-l[s]-r.rects.popper[u],g=l[s]-r.rects.reference[s],b=pe(o),d=b?s==="y"?b.clientHeight||0:b.clientWidth||0:0,O=p/2-g/2,y=v[c],w=d-m[u]-v[h],x=d/2-m[u]/2+O,A=fe(y,x,w),E=s;r.modifiersData[a]=(t={},t[E]=A,t.centerOffset=A-x,t)}}function rn(e){var t=e.state,r=e.options,a=r.element,n=a===void 0?"[data-popper-arrow]":a;n!=null&&(typeof n=="string"&&(n=t.elements.popper.querySelector(n),!n)||xt(t.elements.popper,n)&&(t.elements.arrow=n))}const nn={name:"arrow",enabled:!0,phase:"main",fn:tn,effect:rn,requires:["popperOffsets"],requiresIfExists:["preventOverflow"]},an=Sr({defaultModifiers:[...Mr,Gr,Yr,_r,Ct,jt,nn]});function En({locked:e=!1,overflowPadding:t=8,offsetDistance:r=8,offsetSkid:a=0,gpuAcceleration:n=!0,adaptive:o=!0,scroll:l=!0,resize:i=!0,arrow:s=!1,placement:f,strategy:u},v){const m=ee(null),c=ee(null),h=ee(null);return Re(()=>{dt(p=>{if(!c.value||!m.value&&!(v!=null&&v.value))return;const g=at(c),b=(v==null?void 0:v.value)||at(m);if(!(g instanceof HTMLElement)||!b)return;const d={modifiers:[{name:"flip",enabled:!e},{name:"preventOverflow",options:{padding:t}},{name:"offset",options:{offset:[a,r]}},{name:"computeStyles",options:{adaptive:o,gpuAcceleration:n}},{name:"eventListeners",options:{scroll:l,resize:i}},{name:"arrow",enabled:s}]};f&&(d.placement=f),u&&(d.strategy=u),h.value=an(b,g,d),p(h.value.destroy)})}),[m,c,h]}function on(e,t,r){let a=ee(r==null?void 0:r.value),n=T(()=>e.value!==void 0);return[T(()=>n.value?e.value:a.value),function(o){return n.value||(a.value=o),t==null?void 0:t(o)}]}let $t=Symbol("headlessui.useid"),sn=0;function ln(){return Ve($t,()=>`${++sn}`)()}function un(e){vt($t,e)}function Oe(e){var t;if(e==null||e.value==null)return null;let r=(t=e.value.$el)!=null?t:e.value;return r instanceof Node?r:null}function Pt(e,t,...r){if(e in t){let n=t[e];return typeof n=="function"?n(...r):n}let a=new Error(`Tried to handle "${e}" but there is no handler defined. Only defined handlers are: ${Object.keys(t).map(n=>`"${n}"`).join(", ")}.`);throw Error.captureStackTrace&&Error.captureStackTrace(a,Pt),a}function pt(e,t){if(e)return e;let r=t??"button";if(typeof r=="string"&&r.toLowerCase()==="button")return"button"}function fn(e,t){let r=ee(pt(e.value.type,e.value.as));return Re(()=>{r.value=pt(e.value.type,e.value.as)}),dt(()=>{var a;r.value||Oe(t)&&Oe(t)instanceof HTMLButtonElement&&!((a=Oe(t))!=null&&a.hasAttribute("type"))&&(r.value="button")}),r}var cn=(e=>(e[e.None=0]="None",e[e.RenderStrategy=1]="RenderStrategy",e[e.Static=2]="Static",e))(cn||{}),pn=(e=>(e[e.Unmount=0]="Unmount",e[e.Hidden=1]="Hidden",e))(pn||{});function St({visible:e=!0,features:t=0,ourProps:r,theirProps:a,...n}){var o;let l=Dt(a,r),i=Object.assign(n,{props:l});if(e||t&2&&l.static)return De(i);if(t&1){let s=(o=l.unmount)==null||o?0:1;return Pt(s,{0(){return null},1(){return De({...n,props:{...l,hidden:!0,style:{display:"none"}}})}})}return De(i)}function De({props:e,attrs:t,slots:r,slot:a,name:n}){var o,l;let{as:i,...s}=Tt(e,["unmount","static"]),f=(o=r.default)==null?void 0:o.call(r,a),u={};if(a){let v=!1,m=[];for(let[c,h]of Object.entries(a))typeof h=="boolean"&&(v=!0),h===!0&&m.push(c);v&&(u["data-headlessui-state"]=m.join(" "))}if(i==="template"){if(f=Bt(f??[]),Object.keys(s).length>0||Object.keys(t).length>0){let[v,...m]=f??[];if(!vn(v)||m.length>0)throw new Error(['Passing props on "template"!',"",`The current component <${n} /> is rendering a "template".`,"However we need to passthrough the following props:",Object.keys(s).concat(Object.keys(t)).map(p=>p.trim()).filter((p,g,b)=>b.indexOf(p)===g).sort((p,g)=>p.localeCompare(g)).map(p=>`  - ${p}`).join(`
`),"","You can apply a few solutions:",['Add an `as="..."` prop, to ensure that we render an actual element instead of a "template".',"Render a single element as the child so that we can forward the props onto that element."].map(p=>`  - ${p}`).join(`
`)].join(`
`));let c=Dt((l=v.props)!=null?l:{},s,u),h=zt(v,c,!0);for(let p in c)p.startsWith("on")&&(h.props||(h.props={}),h.props[p]=c[p]);return h}return Array.isArray(f)&&f.length===1?f[0]:f}return Te(i,Object.assign({},s,u),{default:()=>f})}function Bt(e){return e.flatMap(t=>t.type===mt?Bt(t.children):[t])}function Dt(...e){if(e.length===0)return{};if(e.length===1)return e[0];let t={},r={};for(let a of e)for(let n in a)n.startsWith("on")&&typeof a[n]=="function"?(r[n]!=null||(r[n]=[]),r[n].push(a[n])):t[n]=a[n];if(t.disabled||t["aria-disabled"])return Object.assign(t,Object.fromEntries(Object.keys(r).map(a=>[a,void 0])));for(let a in r)Object.assign(t,{[a](n,...o){let l=r[a];for(let i of l){if(n instanceof Event&&n.defaultPrevented)return;i(n,...o)}}});return t}function dn(e){let t=Object.assign({},e);for(let r in t)t[r]===void 0&&delete t[r];return t}function Tt(e,t=[]){let r=Object.assign({},e);for(let a of t)a in r&&delete r[a];return r}function vn(e){return e==null?!1:typeof e.type=="string"||typeof e.type=="object"||typeof e.type=="function"}var It=(e=>(e[e.None=1]="None",e[e.Focusable=2]="Focusable",e[e.Hidden=4]="Hidden",e))(It||{});let mn=Me({name:"Hidden",props:{as:{type:[Object,String],default:"div"},features:{type:Number,default:1}},setup(e,{slots:t,attrs:r}){return()=>{var a;let{features:n,...o}=e,l={"aria-hidden":(n&2)===2?!0:(a=o["aria-hidden"])!=null?a:void 0,hidden:(n&4)===4?!0:void 0,style:{position:"fixed",top:1,left:1,width:1,height:0,padding:0,margin:-1,overflow:"hidden",clip:"rect(0, 0, 0, 0)",whiteSpace:"nowrap",borderWidth:"0",...(n&4)===4&&(n&2)!==2&&{display:"none"}}};return St({ourProps:l,theirProps:o,slot:{},attrs:r,slots:t,name:"Hidden"})}}}),Lt=Symbol("Context");var hn=(e=>(e[e.Open=1]="Open",e[e.Closed=2]="Closed",e[e.Closing=4]="Closing",e[e.Opening=8]="Opening",e))(hn||{});function kn(){return Ve(Lt,null)}function jn(e){vt(Lt,e)}var Ne=(e=>(e.Space=" ",e.Enter="Enter",e.Escape="Escape",e.Backspace="Backspace",e.Delete="Delete",e.ArrowLeft="ArrowLeft",e.ArrowUp="ArrowUp",e.ArrowRight="ArrowRight",e.ArrowDown="ArrowDown",e.Home="Home",e.End="End",e.PageUp="PageUp",e.PageDown="PageDown",e.Tab="Tab",e))(Ne||{});function gn(e){var t,r;let a=(t=e==null?void 0:e.form)!=null?t:e.closest("form");if(a){for(let n of a.elements)if(n!==e&&(n.tagName==="INPUT"&&n.type==="submit"||n.tagName==="BUTTON"&&n.type==="submit"||n.nodeName==="INPUT"&&n.type==="image")){n.click();return}(r=a.requestSubmit)==null||r.call(a)}}let yn=Symbol("GroupContext"),bn=Me({name:"Switch",emits:{"update:modelValue":e=>!0},props:{as:{type:[Object,String],default:"button"},modelValue:{type:Boolean,default:void 0},defaultChecked:{type:Boolean,optional:!0},form:{type:String,optional:!0},name:{type:String,optional:!0},value:{type:String,optional:!0},id:{type:String,default:null},disabled:{type:Boolean,default:!1},tabIndex:{type:Number,default:0}},inheritAttrs:!1,setup(e,{emit:t,attrs:r,slots:a,expose:n}){var o;let l=(o=e.id)!=null?o:`headlessui-switch-${ln()}`,i=Ve(yn,null),[s,f]=on(T(()=>e.modelValue),d=>t("update:modelValue",d),T(()=>e.defaultChecked));function u(){f(!s.value)}let v=ee(null),m=i===null?v:i.switchRef,c=fn(T(()=>({as:e.as,type:r.type})),m);n({el:m,$el:m});function h(d){d.preventDefault(),u()}function p(d){d.key===Ne.Space?(d.preventDefault(),u()):d.key===Ne.Enter&&gn(d.currentTarget)}function g(d){d.preventDefault()}let b=T(()=>{var d,O;return(O=(d=Oe(m))==null?void 0:d.closest)==null?void 0:O.call(d,"form")});return Re(()=>{Ut([b],()=>{if(!b.value||e.defaultChecked===void 0)return;function d(){f(e.defaultChecked)}return b.value.addEventListener("reset",d),()=>{var O;(O=b.value)==null||O.removeEventListener("reset",d)}},{immediate:!0})}),()=>{let{name:d,value:O,form:y,tabIndex:w,...x}=e,A={checked:s.value},E={id:l,ref:m,role:"switch",type:c.value,tabIndex:w===-1?0:w,"aria-checked":s.value,"aria-labelledby":i==null?void 0:i.labelledby.value,"aria-describedby":i==null?void 0:i.describedby.value,onClick:h,onKeyup:p,onKeypress:g};return Te(mt,[d!=null&&s.value!=null?Te(mn,dn({features:It.Hidden,as:"input",type:"checkbox",hidden:!0,readOnly:!0,checked:s.value,form:y,disabled:x.disabled,name:d,value:O})):null,St({ourProps:E,theirProps:{...r,...Tt(x,["modelValue","defaultChecked"])},slot:A,attrs:r,slots:a,name:"Switch"})])}}});const J=qt(Ie.ui.strategy,Ie.ui.toggle,rr),wn=Me({components:{HSwitch:bn,UIcon:ht},inheritAttrs:!1,props:{id:{type:String,default:null},name:{type:String,default:null},modelValue:{type:Boolean,default:!1},disabled:{type:Boolean,default:!1},loading:{type:Boolean,default:!1},onIcon:{type:String,default:()=>J.default.onIcon},offIcon:{type:String,default:()=>J.default.offIcon},loadingIcon:{type:String,default:()=>J.default.loadingIcon},color:{type:String,default:()=>J.default.color,validator(e){return Ie.ui.colors.includes(e)}},size:{type:String,default:()=>J.default.size,validator(e){return Object.keys(J.size).includes(e)}},class:{type:[String,Object,Array],default:()=>""},ui:{type:Object,default:()=>({})}},emits:["update:modelValue","change"],setup(e,{emit:t}){const{ui:r,attrs:a}=Yt("toggle",Xt(e,"ui"),J),{emitFormChange:n,color:o,inputId:l,name:i}=er(e),s=T({get(){return e.modelValue},set(h){t("update:modelValue",h),t("change",h),n()}}),f=T(()=>Kt(se(r.value.base,r.value.size[e.size],r.value.rounded,o.value&&r.value.ring.replaceAll("{color}",o.value),o.value&&(s.value?r.value.active:r.value.inactive).replaceAll("{color}",o.value)),e.class)),u=T(()=>se(r.value.container.base,r.value.container.size[e.size],s.value?r.value.container.active[e.size]:r.value.container.inactive)),v=T(()=>se(r.value.icon.size[e.size],o.value&&r.value.icon.on.replaceAll("{color}",o.value))),m=T(()=>se(r.value.icon.size[e.size],o.value&&r.value.icon.off.replaceAll("{color}",o.value))),c=T(()=>se(r.value.icon.size[e.size],o.value&&r.value.icon.loading.replaceAll("{color}",o.value)));return un(()=>tr("$mRW6KdlcYH")),{ui:r,attrs:a,name:i,inputId:l,active:s,switchClass:f,containerClass:u,onIconClass:v,offIconClass:m,loadingIconClass:c}}});function xn(e,t,r,a,n,o){const l=ht,i=Gt("HSwitch");return be(),Jt(i,_t({id:e.inputId,modelValue:e.active,"onUpdate:modelValue":t[0]||(t[0]=s=>e.active=s),name:e.name,disabled:e.disabled||e.loading,class:e.switchClass},e.attrs),{default:Qt(()=>[Zt("span",{class:G(e.containerClass)},[e.loading?(be(),Pe("span",{key:0,class:G([e.ui.icon.active,e.ui.icon.base]),"aria-hidden":"true"},[Se(l,{name:e.loadingIcon,class:G(e.loadingIconClass)},null,8,["name","class"])],2)):Be("",!0),!e.loading&&e.onIcon?(be(),Pe("span",{key:1,class:G([e.active?e.ui.icon.active:e.ui.icon.inactive,e.ui.icon.base]),"aria-hidden":"true"},[Se(l,{name:e.onIcon,class:G(e.onIconClass)},null,8,["name","class"])],2)):Be("",!0),!e.loading&&e.offIcon?(be(),Pe("span",{key:2,class:G([e.active?e.ui.icon.inactive:e.ui.icon.active,e.ui.icon.base]),"aria-hidden":"true"},[Se(l,{name:e.offIcon,class:G(e.offIconClass)},null,8,["name","class"])],2)):Be("",!0)],2)]),_:1},16,["id","modelValue","name","disabled","class"])}const Cn=Ft(wn,[["render",xn]]);export{St as A,ln as I,cn as N,Tt as T,Cn as _,Pt as a,Ne as b,En as c,kn as d,mn as f,hn as i,un as l,Oe as o,fn as s,jn as t,It as u};
