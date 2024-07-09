import{i as J,a as q}from"./index-BazHhciZ.js";function Le(e,t){return function(){return e.apply(t,arguments)}}const{toString:nt}=Object.prototype,{getPrototypeOf:fe}=Object,K=(e=>t=>{const n=nt.call(t);return e[n]||(e[n]=n.slice(8,-1).toLowerCase())})(Object.create(null)),T=e=>(e=e.toLowerCase(),t=>K(t)===e),G=e=>t=>typeof t===e,{isArray:B}=Array,I=G("undefined");function rt(e){return e!==null&&!I(e)&&e.constructor!==null&&!I(e.constructor)&&S(e.constructor.isBuffer)&&e.constructor.isBuffer(e)}const Be=T("ArrayBuffer");function st(e){let t;return typeof ArrayBuffer<"u"&&ArrayBuffer.isView?t=ArrayBuffer.isView(e):t=e&&e.buffer&&Be(e.buffer),t}const ot=G("string"),S=G("function"),Ue=G("number"),X=e=>e!==null&&typeof e=="object",it=e=>e===!0||e===!1,M=e=>{if(K(e)!=="object")return!1;const t=fe(e);return(t===null||t===Object.prototype||Object.getPrototypeOf(t)===null)&&!(Symbol.toStringTag in e)&&!(Symbol.iterator in e)},at=T("Date"),ct=T("File"),lt=T("Blob"),ut=T("FileList"),ft=e=>X(e)&&S(e.pipe),dt=e=>{let t;return e&&(typeof FormData=="function"&&e instanceof FormData||S(e.append)&&((t=K(e))==="formdata"||t==="object"&&S(e.toString)&&e.toString()==="[object FormData]"))},pt=T("URLSearchParams"),[ht,mt,yt,wt]=["ReadableStream","Request","Response","Headers"].map(T),bt=e=>e.trim?e.trim():e.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g,"");function H(e,t,{allOwnKeys:n=!1}={}){if(e===null||typeof e>"u")return;let r,s;if(typeof e!="object"&&(e=[e]),B(e))for(r=0,s=e.length;r<s;r++)t.call(null,e[r],r,e);else{const o=n?Object.getOwnPropertyNames(e):Object.keys(e),i=o.length;let c;for(r=0;r<i;r++)c=o[r],t.call(null,e[c],c,e)}}function De(e,t){t=t.toLowerCase();const n=Object.keys(e);let r=n.length,s;for(;r-- >0;)if(s=n[r],t===s.toLowerCase())return s;return null}const ke=typeof globalThis<"u"?globalThis:typeof self<"u"?self:typeof window<"u"?window:global,je=e=>!I(e)&&e!==ke;function se(){const{caseless:e}=je(this)&&this||{},t={},n=(r,s)=>{const o=e&&De(t,s)||s;M(t[o])&&M(r)?t[o]=se(t[o],r):M(r)?t[o]=se({},r):B(r)?t[o]=r.slice():t[o]=r};for(let r=0,s=arguments.length;r<s;r++)arguments[r]&&H(arguments[r],n);return t}const gt=(e,t,n,{allOwnKeys:r}={})=>(H(t,(s,o)=>{n&&S(s)?e[o]=Le(s,n):e[o]=s},{allOwnKeys:r}),e),Et=e=>(e.charCodeAt(0)===65279&&(e=e.slice(1)),e),Rt=(e,t,n,r)=>{e.prototype=Object.create(t.prototype,r),e.prototype.constructor=e,Object.defineProperty(e,"super",{value:t.prototype}),n&&Object.assign(e.prototype,n)},St=(e,t,n,r)=>{let s,o,i;const c={};if(t=t||{},e==null)return t;do{for(s=Object.getOwnPropertyNames(e),o=s.length;o-- >0;)i=s[o],(!r||r(i,e,t))&&!c[i]&&(t[i]=e[i],c[i]=!0);e=n!==!1&&fe(e)}while(e&&(!n||n(e,t))&&e!==Object.prototype);return t},Ot=(e,t,n)=>{e=String(e),(n===void 0||n>e.length)&&(n=e.length),n-=t.length;const r=e.indexOf(t,n);return r!==-1&&r===n},At=e=>{if(!e)return null;if(B(e))return e;let t=e.length;if(!Ue(t))return null;const n=new Array(t);for(;t-- >0;)n[t]=e[t];return n},Tt=(e=>t=>e&&t instanceof e)(typeof Uint8Array<"u"&&fe(Uint8Array)),xt=(e,t)=>{const r=(e&&e[Symbol.iterator]).call(e);let s;for(;(s=r.next())&&!s.done;){const o=s.value;t.call(e,o[0],o[1])}},Ct=(e,t)=>{let n;const r=[];for(;(n=e.exec(t))!==null;)r.push(n);return r},Pt=T("HTMLFormElement"),Nt=e=>e.toLowerCase().replace(/[-_\s]([a-z\d])(\w*)/g,function(n,r,s){return r.toUpperCase()+s}),ge=(({hasOwnProperty:e})=>(t,n)=>e.call(t,n))(Object.prototype),Ft=T("RegExp"),qe=(e,t)=>{const n=Object.getOwnPropertyDescriptors(e),r={};H(n,(s,o)=>{let i;(i=t(s,o,e))!==!1&&(r[o]=i||s)}),Object.defineProperties(e,r)},_t=e=>{qe(e,(t,n)=>{if(S(e)&&["arguments","caller","callee"].indexOf(n)!==-1)return!1;const r=e[n];if(S(r)){if(t.enumerable=!1,"writable"in t){t.writable=!1;return}t.set||(t.set=()=>{throw Error("Can not rewrite read-only method '"+n+"'")})}})},Lt=(e,t)=>{const n={},r=s=>{s.forEach(o=>{n[o]=!0})};return B(e)?r(e):r(String(e).split(t)),n},Bt=()=>{},Ut=(e,t)=>e!=null&&Number.isFinite(e=+e)?e:t,ee="abcdefghijklmnopqrstuvwxyz",Ee="0123456789",Ie={DIGIT:Ee,ALPHA:ee,ALPHA_DIGIT:ee+ee.toUpperCase()+Ee},Dt=(e=16,t=Ie.ALPHA_DIGIT)=>{let n="";const{length:r}=t;for(;e--;)n+=t[Math.random()*r|0];return n};function kt(e){return!!(e&&S(e.append)&&e[Symbol.toStringTag]==="FormData"&&e[Symbol.iterator])}const jt=e=>{const t=new Array(10),n=(r,s)=>{if(X(r)){if(t.indexOf(r)>=0)return;if(!("toJSON"in r)){t[s]=r;const o=B(r)?[]:{};return H(r,(i,c)=>{const f=n(i,s+1);!I(f)&&(o[c]=f)}),t[s]=void 0,o}}return r};return n(e,0)},qt=T("AsyncFunction"),It=e=>e&&(X(e)||S(e))&&S(e.then)&&S(e.catch),a={isArray:B,isArrayBuffer:Be,isBuffer:rt,isFormData:dt,isArrayBufferView:st,isString:ot,isNumber:Ue,isBoolean:it,isObject:X,isPlainObject:M,isReadableStream:ht,isRequest:mt,isResponse:yt,isHeaders:wt,isUndefined:I,isDate:at,isFile:ct,isBlob:lt,isRegExp:Ft,isFunction:S,isStream:ft,isURLSearchParams:pt,isTypedArray:Tt,isFileList:ut,forEach:H,merge:se,extend:gt,trim:bt,stripBOM:Et,inherits:Rt,toFlatObject:St,kindOf:K,kindOfTest:T,endsWith:Ot,toArray:At,forEachEntry:xt,matchAll:Ct,isHTMLForm:Pt,hasOwnProperty:ge,hasOwnProp:ge,reduceDescriptors:qe,freezeMethods:_t,toObjectSet:Lt,toCamelCase:Nt,noop:Bt,toFiniteNumber:Ut,findKey:De,global:ke,isContextDefined:je,ALPHABET:Ie,generateString:Dt,isSpecCompliantForm:kt,toJSONObject:jt,isAsyncFn:qt,isThenable:It};function h(e,t,n,r,s){Error.call(this),Error.captureStackTrace?Error.captureStackTrace(this,this.constructor):this.stack=new Error().stack,this.message=e,this.name="AxiosError",t&&(this.code=t),n&&(this.config=n),r&&(this.request=r),s&&(this.response=s)}a.inherits(h,Error,{toJSON:function(){return{message:this.message,name:this.name,description:this.description,number:this.number,fileName:this.fileName,lineNumber:this.lineNumber,columnNumber:this.columnNumber,stack:this.stack,config:a.toJSONObject(this.config),code:this.code,status:this.response&&this.response.status?this.response.status:null}}});const He=h.prototype,Me={};["ERR_BAD_OPTION_VALUE","ERR_BAD_OPTION","ECONNABORTED","ETIMEDOUT","ERR_NETWORK","ERR_FR_TOO_MANY_REDIRECTS","ERR_DEPRECATED","ERR_BAD_RESPONSE","ERR_BAD_REQUEST","ERR_CANCELED","ERR_NOT_SUPPORT","ERR_INVALID_URL"].forEach(e=>{Me[e]={value:e}});Object.defineProperties(h,Me);Object.defineProperty(He,"isAxiosError",{value:!0});h.from=(e,t,n,r,s,o)=>{const i=Object.create(He);return a.toFlatObject(e,i,function(f){return f!==Error.prototype},c=>c!=="isAxiosError"),h.call(i,e.message,t,n,r,s),i.cause=e,i.name=e.name,o&&Object.assign(i,o),i};const Ht=null;function oe(e){return a.isPlainObject(e)||a.isArray(e)}function $e(e){return a.endsWith(e,"[]")?e.slice(0,-2):e}function Re(e,t,n){return e?e.concat(t).map(function(s,o){return s=$e(s),!n&&o?"["+s+"]":s}).join(n?".":""):t}function Mt(e){return a.isArray(e)&&!e.some(oe)}const $t=a.toFlatObject(a,{},null,function(t){return/^is[A-Z]/.test(t)});function Q(e,t,n){if(!a.isObject(e))throw new TypeError("target must be an object");t=t||new FormData,n=a.toFlatObject(n,{metaTokens:!0,dots:!1,indexes:!1},!1,function(m,E){return!a.isUndefined(E[m])});const r=n.metaTokens,s=n.visitor||l,o=n.dots,i=n.indexes,f=(n.Blob||typeof Blob<"u"&&Blob)&&a.isSpecCompliantForm(t);if(!a.isFunction(s))throw new TypeError("visitor must be a function");function u(d){if(d===null)return"";if(a.isDate(d))return d.toISOString();if(!f&&a.isBlob(d))throw new h("Blob is not supported. Use a Buffer instead.");return a.isArrayBuffer(d)||a.isTypedArray(d)?f&&typeof Blob=="function"?new Blob([d]):Buffer.from(d):d}function l(d,m,E){let R=d;if(d&&!E&&typeof d=="object"){if(a.endsWith(m,"{}"))m=r?m:m.slice(0,-2),d=JSON.stringify(d);else if(a.isArray(d)&&Mt(d)||(a.isFileList(d)||a.endsWith(m,"[]"))&&(R=a.toArray(d)))return m=$e(m),R.forEach(function(w,D){!(a.isUndefined(w)||w===null)&&t.append(i===!0?Re([m],D,o):i===null?m:m+"[]",u(w))}),!1}return oe(d)?!0:(t.append(Re(E,m,o),u(d)),!1)}const p=[],b=Object.assign($t,{defaultVisitor:l,convertValue:u,isVisitable:oe});function y(d,m){if(!a.isUndefined(d)){if(p.indexOf(d)!==-1)throw Error("Circular reference detected in "+m.join("."));p.push(d),a.forEach(d,function(R,x){(!(a.isUndefined(R)||R===null)&&s.call(t,R,a.isString(x)?x.trim():x,m,b))===!0&&y(R,m?m.concat(x):[x])}),p.pop()}}if(!a.isObject(e))throw new TypeError("data must be an object");return y(e),t}function Se(e){const t={"!":"%21","'":"%27","(":"%28",")":"%29","~":"%7E","%20":"+","%00":"\0"};return encodeURIComponent(e).replace(/[!'()~]|%20|%00/g,function(r){return t[r]})}function de(e,t){this._pairs=[],e&&Q(e,this,t)}const ze=de.prototype;ze.append=function(t,n){this._pairs.push([t,n])};ze.toString=function(t){const n=t?function(r){return t.call(this,r,Se)}:Se;return this._pairs.map(function(s){return n(s[0])+"="+n(s[1])},"").join("&")};function zt(e){return encodeURIComponent(e).replace(/%3A/gi,":").replace(/%24/g,"$").replace(/%2C/gi,",").replace(/%20/g,"+").replace(/%5B/gi,"[").replace(/%5D/gi,"]")}function Je(e,t,n){if(!t)return e;const r=n&&n.encode||zt,s=n&&n.serialize;let o;if(s?o=s(t,n):o=a.isURLSearchParams(t)?t.toString():new de(t,n).toString(r),o){const i=e.indexOf("#");i!==-1&&(e=e.slice(0,i)),e+=(e.indexOf("?")===-1?"?":"&")+o}return e}class Oe{constructor(){this.handlers=[]}use(t,n,r){return this.handlers.push({fulfilled:t,rejected:n,synchronous:r?r.synchronous:!1,runWhen:r?r.runWhen:null}),this.handlers.length-1}eject(t){this.handlers[t]&&(this.handlers[t]=null)}clear(){this.handlers&&(this.handlers=[])}forEach(t){a.forEach(this.handlers,function(r){r!==null&&t(r)})}}const Ve={silentJSONParsing:!0,forcedJSONParsing:!0,clarifyTimeoutError:!1},Jt=typeof URLSearchParams<"u"?URLSearchParams:de,Vt=typeof FormData<"u"?FormData:null,vt=typeof Blob<"u"?Blob:null,Wt={isBrowser:!0,classes:{URLSearchParams:Jt,FormData:Vt,Blob:vt},protocols:["http","https","file","blob","url","data"]},pe=typeof window<"u"&&typeof document<"u",Kt=(e=>pe&&["ReactNative","NativeScript","NS"].indexOf(e)<0)(typeof navigator<"u"&&navigator.product),Gt=typeof WorkerGlobalScope<"u"&&self instanceof WorkerGlobalScope&&typeof self.importScripts=="function",Xt=pe&&window.location.href||"http://localhost",Qt=Object.freeze(Object.defineProperty({__proto__:null,hasBrowserEnv:pe,hasStandardBrowserEnv:Kt,hasStandardBrowserWebWorkerEnv:Gt,origin:Xt},Symbol.toStringTag,{value:"Module"})),O={...Qt,...Wt};function Zt(e,t){return Q(e,new O.classes.URLSearchParams,Object.assign({visitor:function(n,r,s,o){return O.isNode&&a.isBuffer(n)?(this.append(r,n.toString("base64")),!1):o.defaultVisitor.apply(this,arguments)}},t))}function Yt(e){return a.matchAll(/\w+|\[(\w*)]/g,e).map(t=>t[0]==="[]"?"":t[1]||t[0])}function en(e){const t={},n=Object.keys(e);let r;const s=n.length;let o;for(r=0;r<s;r++)o=n[r],t[o]=e[o];return t}function ve(e){function t(n,r,s,o){let i=n[o++];if(i==="__proto__")return!0;const c=Number.isFinite(+i),f=o>=n.length;return i=!i&&a.isArray(s)?s.length:i,f?(a.hasOwnProp(s,i)?s[i]=[s[i],r]:s[i]=r,!c):((!s[i]||!a.isObject(s[i]))&&(s[i]=[]),t(n,r,s[i],o)&&a.isArray(s[i])&&(s[i]=en(s[i])),!c)}if(a.isFormData(e)&&a.isFunction(e.entries)){const n={};return a.forEachEntry(e,(r,s)=>{t(Yt(r),s,n,0)}),n}return null}function tn(e,t,n){if(a.isString(e))try{return(t||JSON.parse)(e),a.trim(e)}catch(r){if(r.name!=="SyntaxError")throw r}return(n||JSON.stringify)(e)}const he={transitional:Ve,adapter:["xhr","http","fetch"],transformRequest:[function(t,n){const r=n.getContentType()||"",s=r.indexOf("application/json")>-1,o=a.isObject(t);if(o&&a.isHTMLForm(t)&&(t=new FormData(t)),a.isFormData(t))return s?JSON.stringify(ve(t)):t;if(a.isArrayBuffer(t)||a.isBuffer(t)||a.isStream(t)||a.isFile(t)||a.isBlob(t)||a.isReadableStream(t))return t;if(a.isArrayBufferView(t))return t.buffer;if(a.isURLSearchParams(t))return n.setContentType("application/x-www-form-urlencoded;charset=utf-8",!1),t.toString();let c;if(o){if(r.indexOf("application/x-www-form-urlencoded")>-1)return Zt(t,this.formSerializer).toString();if((c=a.isFileList(t))||r.indexOf("multipart/form-data")>-1){const f=this.env&&this.env.FormData;return Q(c?{"files[]":t}:t,f&&new f,this.formSerializer)}}return o||s?(n.setContentType("application/json",!1),tn(t)):t}],transformResponse:[function(t){const n=this.transitional||he.transitional,r=n&&n.forcedJSONParsing,s=this.responseType==="json";if(a.isResponse(t)||a.isReadableStream(t))return t;if(t&&a.isString(t)&&(r&&!this.responseType||s)){const i=!(n&&n.silentJSONParsing)&&s;try{return JSON.parse(t)}catch(c){if(i)throw c.name==="SyntaxError"?h.from(c,h.ERR_BAD_RESPONSE,this,null,this.response):c}}return t}],timeout:0,xsrfCookieName:"XSRF-TOKEN",xsrfHeaderName:"X-XSRF-TOKEN",maxContentLength:-1,maxBodyLength:-1,env:{FormData:O.classes.FormData,Blob:O.classes.Blob},validateStatus:function(t){return t>=200&&t<300},headers:{common:{Accept:"application/json, text/plain, */*","Content-Type":void 0}}};a.forEach(["delete","get","head","post","put","patch"],e=>{he.headers[e]={}});const me=he,nn=a.toObjectSet(["age","authorization","content-length","content-type","etag","expires","from","host","if-modified-since","if-unmodified-since","last-modified","location","max-forwards","proxy-authorization","referer","retry-after","user-agent"]),rn=e=>{const t={};let n,r,s;return e&&e.split(`
`).forEach(function(i){s=i.indexOf(":"),n=i.substring(0,s).trim().toLowerCase(),r=i.substring(s+1).trim(),!(!n||t[n]&&nn[n])&&(n==="set-cookie"?t[n]?t[n].push(r):t[n]=[r]:t[n]=t[n]?t[n]+", "+r:r)}),t},Ae=Symbol("internals");function k(e){return e&&String(e).trim().toLowerCase()}function $(e){return e===!1||e==null?e:a.isArray(e)?e.map($):String(e)}function sn(e){const t=Object.create(null),n=/([^\s,;=]+)\s*(?:=\s*([^,;]+))?/g;let r;for(;r=n.exec(e);)t[r[1]]=r[2];return t}const on=e=>/^[-_a-zA-Z0-9^`|~,!#$%&'*+.]+$/.test(e.trim());function te(e,t,n,r,s){if(a.isFunction(r))return r.call(this,t,n);if(s&&(t=n),!!a.isString(t)){if(a.isString(r))return t.indexOf(r)!==-1;if(a.isRegExp(r))return r.test(t)}}function an(e){return e.trim().toLowerCase().replace(/([a-z\d])(\w*)/g,(t,n,r)=>n.toUpperCase()+r)}function cn(e,t){const n=a.toCamelCase(" "+t);["get","set","has"].forEach(r=>{Object.defineProperty(e,r+n,{value:function(s,o,i){return this[r].call(this,t,s,o,i)},configurable:!0})})}class Z{constructor(t){t&&this.set(t)}set(t,n,r){const s=this;function o(c,f,u){const l=k(f);if(!l)throw new Error("header name must be a non-empty string");const p=a.findKey(s,l);(!p||s[p]===void 0||u===!0||u===void 0&&s[p]!==!1)&&(s[p||f]=$(c))}const i=(c,f)=>a.forEach(c,(u,l)=>o(u,l,f));if(a.isPlainObject(t)||t instanceof this.constructor)i(t,n);else if(a.isString(t)&&(t=t.trim())&&!on(t))i(rn(t),n);else if(a.isHeaders(t))for(const[c,f]of t.entries())o(f,c,r);else t!=null&&o(n,t,r);return this}get(t,n){if(t=k(t),t){const r=a.findKey(this,t);if(r){const s=this[r];if(!n)return s;if(n===!0)return sn(s);if(a.isFunction(n))return n.call(this,s,r);if(a.isRegExp(n))return n.exec(s);throw new TypeError("parser must be boolean|regexp|function")}}}has(t,n){if(t=k(t),t){const r=a.findKey(this,t);return!!(r&&this[r]!==void 0&&(!n||te(this,this[r],r,n)))}return!1}delete(t,n){const r=this;let s=!1;function o(i){if(i=k(i),i){const c=a.findKey(r,i);c&&(!n||te(r,r[c],c,n))&&(delete r[c],s=!0)}}return a.isArray(t)?t.forEach(o):o(t),s}clear(t){const n=Object.keys(this);let r=n.length,s=!1;for(;r--;){const o=n[r];(!t||te(this,this[o],o,t,!0))&&(delete this[o],s=!0)}return s}normalize(t){const n=this,r={};return a.forEach(this,(s,o)=>{const i=a.findKey(r,o);if(i){n[i]=$(s),delete n[o];return}const c=t?an(o):String(o).trim();c!==o&&delete n[o],n[c]=$(s),r[c]=!0}),this}concat(...t){return this.constructor.concat(this,...t)}toJSON(t){const n=Object.create(null);return a.forEach(this,(r,s)=>{r!=null&&r!==!1&&(n[s]=t&&a.isArray(r)?r.join(", "):r)}),n}[Symbol.iterator](){return Object.entries(this.toJSON())[Symbol.iterator]()}toString(){return Object.entries(this.toJSON()).map(([t,n])=>t+": "+n).join(`
`)}get[Symbol.toStringTag](){return"AxiosHeaders"}static from(t){return t instanceof this?t:new this(t)}static concat(t,...n){const r=new this(t);return n.forEach(s=>r.set(s)),r}static accessor(t){const r=(this[Ae]=this[Ae]={accessors:{}}).accessors,s=this.prototype;function o(i){const c=k(i);r[c]||(cn(s,i),r[c]=!0)}return a.isArray(t)?t.forEach(o):o(t),this}}Z.accessor(["Content-Type","Content-Length","Accept","Accept-Encoding","User-Agent","Authorization"]);a.reduceDescriptors(Z.prototype,({value:e},t)=>{let n=t[0].toUpperCase()+t.slice(1);return{get:()=>e,set(r){this[n]=r}}});a.freezeMethods(Z);const A=Z;function ne(e,t){const n=this||me,r=t||n,s=A.from(r.headers);let o=r.data;return a.forEach(e,function(c){o=c.call(n,o,s.normalize(),t?t.status:void 0)}),s.normalize(),o}function We(e){return!!(e&&e.__CANCEL__)}function U(e,t,n){h.call(this,e??"canceled",h.ERR_CANCELED,t,n),this.name="CanceledError"}a.inherits(U,h,{__CANCEL__:!0});function Ke(e,t,n){const r=n.config.validateStatus;!n.status||!r||r(n.status)?e(n):t(new h("Request failed with status code "+n.status,[h.ERR_BAD_REQUEST,h.ERR_BAD_RESPONSE][Math.floor(n.status/100)-4],n.config,n.request,n))}function ln(e){const t=/^([-+\w]{1,25})(:?\/\/|:)/.exec(e);return t&&t[1]||""}function un(e,t){e=e||10;const n=new Array(e),r=new Array(e);let s=0,o=0,i;return t=t!==void 0?t:1e3,function(f){const u=Date.now(),l=r[o];i||(i=u),n[s]=f,r[s]=u;let p=o,b=0;for(;p!==s;)b+=n[p++],p=p%e;if(s=(s+1)%e,s===o&&(o=(o+1)%e),u-i<t)return;const y=l&&u-l;return y?Math.round(b*1e3/y):void 0}}function fn(e,t){let n=0;const r=1e3/t;let s=null;return function(){const i=this===!0,c=Date.now();if(i||c-n>r)return s&&(clearTimeout(s),s=null),n=c,e.apply(null,arguments);s||(s=setTimeout(()=>(s=null,n=Date.now(),e.apply(null,arguments)),r-(c-n)))}}const V=(e,t,n=3)=>{let r=0;const s=un(50,250);return fn(o=>{const i=o.loaded,c=o.lengthComputable?o.total:void 0,f=i-r,u=s(f),l=i<=c;r=i;const p={loaded:i,total:c,progress:c?i/c:void 0,bytes:f,rate:u||void 0,estimated:u&&c&&l?(c-i)/u:void 0,event:o,lengthComputable:c!=null};p[t?"download":"upload"]=!0,e(p)},n)},dn=O.hasStandardBrowserEnv?function(){const t=/(msie|trident)/i.test(navigator.userAgent),n=document.createElement("a");let r;function s(o){let i=o;return t&&(n.setAttribute("href",i),i=n.href),n.setAttribute("href",i),{href:n.href,protocol:n.protocol?n.protocol.replace(/:$/,""):"",host:n.host,search:n.search?n.search.replace(/^\?/,""):"",hash:n.hash?n.hash.replace(/^#/,""):"",hostname:n.hostname,port:n.port,pathname:n.pathname.charAt(0)==="/"?n.pathname:"/"+n.pathname}}return r=s(window.location.href),function(i){const c=a.isString(i)?s(i):i;return c.protocol===r.protocol&&c.host===r.host}}():function(){return function(){return!0}}(),pn=O.hasStandardBrowserEnv?{write(e,t,n,r,s,o){const i=[e+"="+encodeURIComponent(t)];a.isNumber(n)&&i.push("expires="+new Date(n).toGMTString()),a.isString(r)&&i.push("path="+r),a.isString(s)&&i.push("domain="+s),o===!0&&i.push("secure"),document.cookie=i.join("; ")},read(e){const t=document.cookie.match(new RegExp("(^|;\\s*)("+e+")=([^;]*)"));return t?decodeURIComponent(t[3]):null},remove(e){this.write(e,"",Date.now()-864e5)}}:{write(){},read(){return null},remove(){}};function hn(e){return/^([a-z][a-z\d+\-.]*:)?\/\//i.test(e)}function mn(e,t){return t?e.replace(/\/?\/$/,"")+"/"+t.replace(/^\/+/,""):e}function Ge(e,t){return e&&!hn(t)?mn(e,t):t}const Te=e=>e instanceof A?{...e}:e;function _(e,t){t=t||{};const n={};function r(u,l,p){return a.isPlainObject(u)&&a.isPlainObject(l)?a.merge.call({caseless:p},u,l):a.isPlainObject(l)?a.merge({},l):a.isArray(l)?l.slice():l}function s(u,l,p){if(a.isUndefined(l)){if(!a.isUndefined(u))return r(void 0,u,p)}else return r(u,l,p)}function o(u,l){if(!a.isUndefined(l))return r(void 0,l)}function i(u,l){if(a.isUndefined(l)){if(!a.isUndefined(u))return r(void 0,u)}else return r(void 0,l)}function c(u,l,p){if(p in t)return r(u,l);if(p in e)return r(void 0,u)}const f={url:o,method:o,data:o,baseURL:i,transformRequest:i,transformResponse:i,paramsSerializer:i,timeout:i,timeoutMessage:i,withCredentials:i,withXSRFToken:i,adapter:i,responseType:i,xsrfCookieName:i,xsrfHeaderName:i,onUploadProgress:i,onDownloadProgress:i,decompress:i,maxContentLength:i,maxBodyLength:i,beforeRedirect:i,transport:i,httpAgent:i,httpsAgent:i,cancelToken:i,socketPath:i,responseEncoding:i,validateStatus:c,headers:(u,l)=>s(Te(u),Te(l),!0)};return a.forEach(Object.keys(Object.assign({},e,t)),function(l){const p=f[l]||s,b=p(e[l],t[l],l);a.isUndefined(b)&&p!==c||(n[l]=b)}),n}const Xe=e=>{const t=_({},e);let{data:n,withXSRFToken:r,xsrfHeaderName:s,xsrfCookieName:o,headers:i,auth:c}=t;t.headers=i=A.from(i),t.url=Je(Ge(t.baseURL,t.url),e.params,e.paramsSerializer),c&&i.set("Authorization","Basic "+btoa((c.username||"")+":"+(c.password?unescape(encodeURIComponent(c.password)):"")));let f;if(a.isFormData(n)){if(O.hasStandardBrowserEnv||O.hasStandardBrowserWebWorkerEnv)i.setContentType(void 0);else if((f=i.getContentType())!==!1){const[u,...l]=f?f.split(";").map(p=>p.trim()).filter(Boolean):[];i.setContentType([u||"multipart/form-data",...l].join("; "))}}if(O.hasStandardBrowserEnv&&(r&&a.isFunction(r)&&(r=r(t)),r||r!==!1&&dn(t.url))){const u=s&&o&&pn.read(o);u&&i.set(s,u)}return t},yn=typeof XMLHttpRequest<"u",wn=yn&&function(e){return new Promise(function(n,r){const s=Xe(e);let o=s.data;const i=A.from(s.headers).normalize();let{responseType:c}=s,f;function u(){s.cancelToken&&s.cancelToken.unsubscribe(f),s.signal&&s.signal.removeEventListener("abort",f)}let l=new XMLHttpRequest;l.open(s.method.toUpperCase(),s.url,!0),l.timeout=s.timeout;function p(){if(!l)return;const y=A.from("getAllResponseHeaders"in l&&l.getAllResponseHeaders()),m={data:!c||c==="text"||c==="json"?l.responseText:l.response,status:l.status,statusText:l.statusText,headers:y,config:e,request:l};Ke(function(R){n(R),u()},function(R){r(R),u()},m),l=null}"onloadend"in l?l.onloadend=p:l.onreadystatechange=function(){!l||l.readyState!==4||l.status===0&&!(l.responseURL&&l.responseURL.indexOf("file:")===0)||setTimeout(p)},l.onabort=function(){l&&(r(new h("Request aborted",h.ECONNABORTED,s,l)),l=null)},l.onerror=function(){r(new h("Network Error",h.ERR_NETWORK,s,l)),l=null},l.ontimeout=function(){let d=s.timeout?"timeout of "+s.timeout+"ms exceeded":"timeout exceeded";const m=s.transitional||Ve;s.timeoutErrorMessage&&(d=s.timeoutErrorMessage),r(new h(d,m.clarifyTimeoutError?h.ETIMEDOUT:h.ECONNABORTED,s,l)),l=null},o===void 0&&i.setContentType(null),"setRequestHeader"in l&&a.forEach(i.toJSON(),function(d,m){l.setRequestHeader(m,d)}),a.isUndefined(s.withCredentials)||(l.withCredentials=!!s.withCredentials),c&&c!=="json"&&(l.responseType=s.responseType),typeof s.onDownloadProgress=="function"&&l.addEventListener("progress",V(s.onDownloadProgress,!0)),typeof s.onUploadProgress=="function"&&l.upload&&l.upload.addEventListener("progress",V(s.onUploadProgress)),(s.cancelToken||s.signal)&&(f=y=>{l&&(r(!y||y.type?new U(null,e,l):y),l.abort(),l=null)},s.cancelToken&&s.cancelToken.subscribe(f),s.signal&&(s.signal.aborted?f():s.signal.addEventListener("abort",f)));const b=ln(s.url);if(b&&O.protocols.indexOf(b)===-1){r(new h("Unsupported protocol "+b+":",h.ERR_BAD_REQUEST,e));return}l.send(o||null)})},bn=(e,t)=>{let n=new AbortController,r;const s=function(f){if(!r){r=!0,i();const u=f instanceof Error?f:this.reason;n.abort(u instanceof h?u:new U(u instanceof Error?u.message:u))}};let o=t&&setTimeout(()=>{s(new h(`timeout ${t} of ms exceeded`,h.ETIMEDOUT))},t);const i=()=>{e&&(o&&clearTimeout(o),o=null,e.forEach(f=>{f&&(f.removeEventListener?f.removeEventListener("abort",s):f.unsubscribe(s))}),e=null)};e.forEach(f=>f&&f.addEventListener&&f.addEventListener("abort",s));const{signal:c}=n;return c.unsubscribe=i,[c,()=>{o&&clearTimeout(o),o=null}]},gn=function*(e,t){let n=e.byteLength;if(!t||n<t){yield e;return}let r=0,s;for(;r<n;)s=r+t,yield e.slice(r,s),r=s},En=async function*(e,t,n){for await(const r of e)yield*gn(ArrayBuffer.isView(r)?r:await n(String(r)),t)},xe=(e,t,n,r,s)=>{const o=En(e,t,s);let i=0;return new ReadableStream({type:"bytes",async pull(c){const{done:f,value:u}=await o.next();if(f){c.close(),r();return}let l=u.byteLength;n&&n(i+=l),c.enqueue(new Uint8Array(u))},cancel(c){return r(c),o.return()}},{highWaterMark:2})},Ce=(e,t)=>{const n=e!=null;return r=>setTimeout(()=>t({lengthComputable:n,total:e,loaded:r}))},Y=typeof fetch=="function"&&typeof Request=="function"&&typeof Response=="function",Qe=Y&&typeof ReadableStream=="function",ie=Y&&(typeof TextEncoder=="function"?(e=>t=>e.encode(t))(new TextEncoder):async e=>new Uint8Array(await new Response(e).arrayBuffer())),Rn=Qe&&(()=>{let e=!1;const t=new Request(O.origin,{body:new ReadableStream,method:"POST",get duplex(){return e=!0,"half"}}).headers.has("Content-Type");return e&&!t})(),Pe=64*1024,ae=Qe&&!!(()=>{try{return a.isReadableStream(new Response("").body)}catch{}})(),v={stream:ae&&(e=>e.body)};Y&&(e=>{["text","arrayBuffer","blob","formData","stream"].forEach(t=>{!v[t]&&(v[t]=a.isFunction(e[t])?n=>n[t]():(n,r)=>{throw new h(`Response type '${t}' is not supported`,h.ERR_NOT_SUPPORT,r)})})})(new Response);const Sn=async e=>{if(e==null)return 0;if(a.isBlob(e))return e.size;if(a.isSpecCompliantForm(e))return(await new Request(e).arrayBuffer()).byteLength;if(a.isArrayBufferView(e))return e.byteLength;if(a.isURLSearchParams(e)&&(e=e+""),a.isString(e))return(await ie(e)).byteLength},On=async(e,t)=>{const n=a.toFiniteNumber(e.getContentLength());return n??Sn(t)},An=Y&&(async e=>{let{url:t,method:n,data:r,signal:s,cancelToken:o,timeout:i,onDownloadProgress:c,onUploadProgress:f,responseType:u,headers:l,withCredentials:p="same-origin",fetchOptions:b}=Xe(e);u=u?(u+"").toLowerCase():"text";let[y,d]=s||o||i?bn([s,o],i):[],m,E;const R=()=>{!m&&setTimeout(()=>{y&&y.unsubscribe()}),m=!0};let x;try{if(f&&Rn&&n!=="get"&&n!=="head"&&(x=await On(l,r))!==0){let C=new Request(t,{method:"POST",body:r,duplex:"half"}),L;a.isFormData(r)&&(L=C.headers.get("content-type"))&&l.setContentType(L),C.body&&(r=xe(C.body,Pe,Ce(x,V(f)),null,ie))}a.isString(p)||(p=p?"cors":"omit"),E=new Request(t,{...b,signal:y,method:n.toUpperCase(),headers:l.normalize().toJSON(),body:r,duplex:"half",withCredentials:p});let w=await fetch(E);const D=ae&&(u==="stream"||u==="response");if(ae&&(c||D)){const C={};["status","statusText","headers"].forEach(be=>{C[be]=w[be]});const L=a.toFiniteNumber(w.headers.get("content-length"));w=new Response(xe(w.body,Pe,c&&Ce(L,V(c,!0)),D&&R,ie),C)}u=u||"text";let tt=await v[a.findKey(v,u)||"text"](w,e);return!D&&R(),d&&d(),await new Promise((C,L)=>{Ke(C,L,{data:tt,headers:A.from(w.headers),status:w.status,statusText:w.statusText,config:e,request:E})})}catch(w){throw R(),w&&w.name==="TypeError"&&/fetch/i.test(w.message)?Object.assign(new h("Network Error",h.ERR_NETWORK,e,E),{cause:w.cause||w}):h.from(w,w&&w.code,e,E)}}),ce={http:Ht,xhr:wn,fetch:An};a.forEach(ce,(e,t)=>{if(e){try{Object.defineProperty(e,"name",{value:t})}catch{}Object.defineProperty(e,"adapterName",{value:t})}});const Ne=e=>`- ${e}`,Tn=e=>a.isFunction(e)||e===null||e===!1,Ze={getAdapter:e=>{e=a.isArray(e)?e:[e];const{length:t}=e;let n,r;const s={};for(let o=0;o<t;o++){n=e[o];let i;if(r=n,!Tn(n)&&(r=ce[(i=String(n)).toLowerCase()],r===void 0))throw new h(`Unknown adapter '${i}'`);if(r)break;s[i||"#"+o]=r}if(!r){const o=Object.entries(s).map(([c,f])=>`adapter ${c} `+(f===!1?"is not supported by the environment":"is not available in the build"));let i=t?o.length>1?`since :
`+o.map(Ne).join(`
`):" "+Ne(o[0]):"as no adapter specified";throw new h("There is no suitable adapter to dispatch the request "+i,"ERR_NOT_SUPPORT")}return r},adapters:ce};function re(e){if(e.cancelToken&&e.cancelToken.throwIfRequested(),e.signal&&e.signal.aborted)throw new U(null,e)}function Fe(e){return re(e),e.headers=A.from(e.headers),e.data=ne.call(e,e.transformRequest),["post","put","patch"].indexOf(e.method)!==-1&&e.headers.setContentType("application/x-www-form-urlencoded",!1),Ze.getAdapter(e.adapter||me.adapter)(e).then(function(r){return re(e),r.data=ne.call(e,e.transformResponse,r),r.headers=A.from(r.headers),r},function(r){return We(r)||(re(e),r&&r.response&&(r.response.data=ne.call(e,e.transformResponse,r.response),r.response.headers=A.from(r.response.headers))),Promise.reject(r)})}const Ye="1.7.2",ye={};["object","boolean","number","function","string","symbol"].forEach((e,t)=>{ye[e]=function(r){return typeof r===e||"a"+(t<1?"n ":" ")+e}});const _e={};ye.transitional=function(t,n,r){function s(o,i){return"[Axios v"+Ye+"] Transitional option '"+o+"'"+i+(r?". "+r:"")}return(o,i,c)=>{if(t===!1)throw new h(s(i," has been removed"+(n?" in "+n:"")),h.ERR_DEPRECATED);return n&&!_e[i]&&(_e[i]=!0,console.warn(s(i," has been deprecated since v"+n+" and will be removed in the near future"))),t?t(o,i,c):!0}};function xn(e,t,n){if(typeof e!="object")throw new h("options must be an object",h.ERR_BAD_OPTION_VALUE);const r=Object.keys(e);let s=r.length;for(;s-- >0;){const o=r[s],i=t[o];if(i){const c=e[o],f=c===void 0||i(c,o,e);if(f!==!0)throw new h("option "+o+" must be "+f,h.ERR_BAD_OPTION_VALUE);continue}if(n!==!0)throw new h("Unknown option "+o,h.ERR_BAD_OPTION)}}const le={assertOptions:xn,validators:ye},P=le.validators;class W{constructor(t){this.defaults=t,this.interceptors={request:new Oe,response:new Oe}}async request(t,n){try{return await this._request(t,n)}catch(r){if(r instanceof Error){let s;Error.captureStackTrace?Error.captureStackTrace(s={}):s=new Error;const o=s.stack?s.stack.replace(/^.+\n/,""):"";try{r.stack?o&&!String(r.stack).endsWith(o.replace(/^.+\n.+\n/,""))&&(r.stack+=`
`+o):r.stack=o}catch{}}throw r}}_request(t,n){typeof t=="string"?(n=n||{},n.url=t):n=t||{},n=_(this.defaults,n);const{transitional:r,paramsSerializer:s,headers:o}=n;r!==void 0&&le.assertOptions(r,{silentJSONParsing:P.transitional(P.boolean),forcedJSONParsing:P.transitional(P.boolean),clarifyTimeoutError:P.transitional(P.boolean)},!1),s!=null&&(a.isFunction(s)?n.paramsSerializer={serialize:s}:le.assertOptions(s,{encode:P.function,serialize:P.function},!0)),n.method=(n.method||this.defaults.method||"get").toLowerCase();let i=o&&a.merge(o.common,o[n.method]);o&&a.forEach(["delete","get","head","post","put","patch","common"],d=>{delete o[d]}),n.headers=A.concat(i,o);const c=[];let f=!0;this.interceptors.request.forEach(function(m){typeof m.runWhen=="function"&&m.runWhen(n)===!1||(f=f&&m.synchronous,c.unshift(m.fulfilled,m.rejected))});const u=[];this.interceptors.response.forEach(function(m){u.push(m.fulfilled,m.rejected)});let l,p=0,b;if(!f){const d=[Fe.bind(this),void 0];for(d.unshift.apply(d,c),d.push.apply(d,u),b=d.length,l=Promise.resolve(n);p<b;)l=l.then(d[p++],d[p++]);return l}b=c.length;let y=n;for(p=0;p<b;){const d=c[p++],m=c[p++];try{y=d(y)}catch(E){m.call(this,E);break}}try{l=Fe.call(this,y)}catch(d){return Promise.reject(d)}for(p=0,b=u.length;p<b;)l=l.then(u[p++],u[p++]);return l}getUri(t){t=_(this.defaults,t);const n=Ge(t.baseURL,t.url);return Je(n,t.params,t.paramsSerializer)}}a.forEach(["delete","get","head","options"],function(t){W.prototype[t]=function(n,r){return this.request(_(r||{},{method:t,url:n,data:(r||{}).data}))}});a.forEach(["post","put","patch"],function(t){function n(r){return function(o,i,c){return this.request(_(c||{},{method:t,headers:r?{"Content-Type":"multipart/form-data"}:{},url:o,data:i}))}}W.prototype[t]=n(),W.prototype[t+"Form"]=n(!0)});const z=W;class we{constructor(t){if(typeof t!="function")throw new TypeError("executor must be a function.");let n;this.promise=new Promise(function(o){n=o});const r=this;this.promise.then(s=>{if(!r._listeners)return;let o=r._listeners.length;for(;o-- >0;)r._listeners[o](s);r._listeners=null}),this.promise.then=s=>{let o;const i=new Promise(c=>{r.subscribe(c),o=c}).then(s);return i.cancel=function(){r.unsubscribe(o)},i},t(function(o,i,c){r.reason||(r.reason=new U(o,i,c),n(r.reason))})}throwIfRequested(){if(this.reason)throw this.reason}subscribe(t){if(this.reason){t(this.reason);return}this._listeners?this._listeners.push(t):this._listeners=[t]}unsubscribe(t){if(!this._listeners)return;const n=this._listeners.indexOf(t);n!==-1&&this._listeners.splice(n,1)}static source(){let t;return{token:new we(function(s){t=s}),cancel:t}}}const Cn=we;function Pn(e){return function(n){return e.apply(null,n)}}function Nn(e){return a.isObject(e)&&e.isAxiosError===!0}const ue={Continue:100,SwitchingProtocols:101,Processing:102,EarlyHints:103,Ok:200,Created:201,Accepted:202,NonAuthoritativeInformation:203,NoContent:204,ResetContent:205,PartialContent:206,MultiStatus:207,AlreadyReported:208,ImUsed:226,MultipleChoices:300,MovedPermanently:301,Found:302,SeeOther:303,NotModified:304,UseProxy:305,Unused:306,TemporaryRedirect:307,PermanentRedirect:308,BadRequest:400,Unauthorized:401,PaymentRequired:402,Forbidden:403,NotFound:404,MethodNotAllowed:405,NotAcceptable:406,ProxyAuthenticationRequired:407,RequestTimeout:408,Conflict:409,Gone:410,LengthRequired:411,PreconditionFailed:412,PayloadTooLarge:413,UriTooLong:414,UnsupportedMediaType:415,RangeNotSatisfiable:416,ExpectationFailed:417,ImATeapot:418,MisdirectedRequest:421,UnprocessableEntity:422,Locked:423,FailedDependency:424,TooEarly:425,UpgradeRequired:426,PreconditionRequired:428,TooManyRequests:429,RequestHeaderFieldsTooLarge:431,UnavailableForLegalReasons:451,InternalServerError:500,NotImplemented:501,BadGateway:502,ServiceUnavailable:503,GatewayTimeout:504,HttpVersionNotSupported:505,VariantAlsoNegotiates:506,InsufficientStorage:507,LoopDetected:508,NotExtended:510,NetworkAuthenticationRequired:511};Object.entries(ue).forEach(([e,t])=>{ue[t]=e});const Fn=ue;function et(e){const t=new z(e),n=Le(z.prototype.request,t);return a.extend(n,z.prototype,t,{allOwnKeys:!0}),a.extend(n,t,null,{allOwnKeys:!0}),n.create=function(s){return et(_(e,s))},n}const g=et(me);g.Axios=z;g.CanceledError=U;g.CancelToken=Cn;g.isCancel=We;g.VERSION=Ye;g.toFormData=Q;g.AxiosError=h;g.Cancel=g.CanceledError;g.all=function(t){return Promise.all(t)};g.spread=Pn;g.isAxiosError=Nn;g.mergeConfig=_;g.AxiosHeaders=A;g.formToJSON=e=>ve(a.isHTMLForm(e)?new FormData(e):e);g.getAdapter=Ze.getAdapter;g.HttpStatusCode=Fn;g.default=g;const F=g.create();F.interceptors.request.use(async e=>{const t=localStorage.getItem("user_token");return t?(e.headers.Authorization=`Basic ${t}`,e):(J.push({name:"login"}),Promise.reject("Token not available"))},e=>Promise.reject(e));F.interceptors.response.use(e=>e,async e=>{if(e.request.status==401||e.request.status==403)J.push({name:"login"});else if(e.request.status==400)N.setAlert("alert-warning","Операция завершилась неудачно");else return Promise.reject(e)});const j="",Ln=q({userId:"",username:"",hasAdmin:!1}),Bn=q({regions:{},standing:{},conclusions:{},relations:{},affilations:{},educations:{},addresses:{},contacts:{},documents:{},poligrafs:{}}),N={alertMessage:q({attr:"",text:"",show:!1}),setAlert(e,t){this.alertMessage.show=!0,this.alertMessage.attr=e,this.alertMessage.text=t,setTimeout(()=>{this.alertMessage.show=!1},1e4)}},Un={anketa:q({persons:{},previous:[],educations:[],staffs:[],documents:[],addresses:[],contacts:[],relations:[],workplaces:[],affilations:[],checks:[],poligrafs:[],investigations:[],inquiries:[]}),share:q({candId:"",imageUrl:""}),async getItem(e,t="view"){if(!(t==="self"&&!confirm("Вы действительно хотите включить/выключить режим правки")))try{const n=e==="image"?await F.get(`${j}/image/${this.share.candId}`,{responseType:"blob"}):await F.get(`${j}/${e}/${this.share.candId}`,{params:{action:t}});e==="image"?this.share.imageUrl=window.URL.createObjectURL(new Blob([n.data])):this.anketa[e]=n.data,t==="self"&&N.setAlert("alert-info","Анкета назначена пользователю")}catch(n){console.error(n)}},async updateItem(e,t){try{const n=await F.post(`${j}/${e}/${this.share.candId}`,t);console.log(n.status),["checks","poligrafs"].includes(e)&&this.getItem("persons"),this.getItem(e),N.setAlert("alert-success","Запись успешно добавлена")}catch(n){console.error(n)}},async deleteItem(e,t){if(confirm("Вы действительно хотите удалить запись?"))try{const n=await F.delete(`${j}/${t}/${e}`);console.log(n.status),t==="persons"?J.push({name:"persons"}):this.getItem(t),N.setAlert("alert-info",`Запись с ID ${e} удалена`)}catch(n){console.error(n)}},async submitFile(e,t,n){const r=new FormData,s=e.target;if(s&&s.files){for(let o=0;o<s.files.length;o++)if(s.files[o].size>10*1024*1024){N.setAlert("alert-warning","Превышен максимальный размер файла"),s.value="";return}else r.append("file",s.files[o]);try{const o=await F.post(`${j}/file/${t}/${n}`,r);if(console.log(o.status),t==="image"&&this.getItem(t),t==="persons"){const{person_id:i}=o.data;J.push({name:"profile",params:{id:i}})}N.setAlert("alert-success","Файл или файлы успешно загружен/добавлены")}catch(o){console.error(o)}}else N.setAlert("alert-warning","Ошибка при загрузке файла")}};export{g as a,j as b,F as c,Bn as d,Ln as e,Un as f,N as s};
