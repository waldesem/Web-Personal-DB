import{n as pr,z as br,aI as W,L as X}from"./B_4c7bjE.js";const Dr=()=>async(h,p={})=>{if(j.value)p.headers={...p.headers,Authorization:`${j.value}`};else return pr("/login");try{return await $fetch(h,p)}catch(y){return console.error(y),pr("/login")}};var ar={},q={};q.byteLength=Or;q.toByteArray=Yr;q.fromByteArray=qr;var _=[],R=[],Mr=typeof Uint8Array<"u"?Uint8Array:Array,K="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";for(var b=0,Pr=K.length;b<Pr;++b)_[b]=K[b],R[K.charCodeAt(b)]=b;R[45]=62;R[95]=63;function lr(s){var h=s.length;if(h%4>0)throw new Error("Invalid string. Length must be a multiple of 4");var p=s.indexOf("=");p===-1&&(p=h);var y=p===h?0:4-p%4;return[p,y]}function Or(s){var h=lr(s),p=h[0],y=h[1];return(p+y)*3/4-y}function Gr(s,h,p){return(h+p)*3/4-p}function Yr(s){var h,p=lr(s),y=p[0],w=p[1],l=new Mr(Gr(s,y,w)),f=0,o=w>0?y-4:y,x;for(x=0;x<o;x+=4)h=R[s.charCodeAt(x)]<<18|R[s.charCodeAt(x+1)]<<12|R[s.charCodeAt(x+2)]<<6|R[s.charCodeAt(x+3)],l[f++]=h>>16&255,l[f++]=h>>8&255,l[f++]=h&255;return w===2&&(h=R[s.charCodeAt(x)]<<2|R[s.charCodeAt(x+1)]>>4,l[f++]=h&255),w===1&&(h=R[s.charCodeAt(x)]<<10|R[s.charCodeAt(x+1)]<<4|R[s.charCodeAt(x+2)]>>2,l[f++]=h>>8&255,l[f++]=h&255),l}function Wr(s){return _[s>>18&63]+_[s>>12&63]+_[s>>6&63]+_[s&63]}function jr(s,h,p){for(var y,w=[],l=h;l<p;l+=3)y=(s[l]<<16&16711680)+(s[l+1]<<8&65280)+(s[l+2]&255),w.push(Wr(y));return w.join("")}function qr(s){for(var h,p=s.length,y=p%3,w=[],l=16383,f=0,o=p-y;f<o;f+=l)w.push(jr(s,f,f+l>o?o:f+l));return y===1?(h=s[p-1],w.push(_[h>>2]+_[h<<4&63]+"==")):y===2&&(h=(s[p-2]<<8)+s[p-1],w.push(_[h>>10]+_[h>>4&63]+_[h<<2&63]+"=")),w.join("")}var Z={};/*! ieee754. BSD-3-Clause License. Feross Aboukhadijeh <https://feross.org/opensource> */Z.read=function(s,h,p,y,w){var l,f,o=w*8-y-1,x=(1<<o)-1,A=x>>1,m=-7,I=p?w-1:0,C=p?-1:1,U=s[h+I];for(I+=C,l=U&(1<<-m)-1,U>>=-m,m+=o;m>0;l=l*256+s[h+I],I+=C,m-=8);for(f=l&(1<<-m)-1,l>>=-m,m+=y;m>0;f=f*256+s[h+I],I+=C,m-=8);if(l===0)l=1-A;else{if(l===x)return f?NaN:(U?-1:1)*(1/0);f=f+Math.pow(2,y),l=l-A}return(U?-1:1)*f*Math.pow(2,l-y)};Z.write=function(s,h,p,y,w,l){var f,o,x,A=l*8-w-1,m=(1<<A)-1,I=m>>1,C=w===23?Math.pow(2,-24)-Math.pow(2,-77):0,U=y?0:l-1,M=y?1:-1,P=h<0||h===0&&1/h<0?1:0;for(h=Math.abs(h),isNaN(h)||h===1/0?(o=isNaN(h)?1:0,f=m):(f=Math.floor(Math.log(h)/Math.LN2),h*(x=Math.pow(2,-f))<1&&(f--,x*=2),f+I>=1?h+=C/x:h+=C*Math.pow(2,1-I),h*x>=2&&(f++,x/=2),f+I>=m?(o=0,f=m):f+I>=1?(o=(h*x-1)*Math.pow(2,w),f=f+I):(o=h*Math.pow(2,I-1)*Math.pow(2,w),f=0));w>=8;s[p+U]=o&255,U+=M,o/=256,w-=8);for(f=f<<w|o,A+=w;A>0;s[p+U]=f&255,U+=M,f/=256,A-=8);s[p+U-M]|=P*128};/*!
 * The buffer module from node.js, for the browser.
 *
 * @author   Feross Aboukhadijeh <https://feross.org>
 * @license  MIT
 */(function(s){const h=q,p=Z,y=typeof Symbol=="function"&&typeof Symbol.for=="function"?Symbol.for("nodejs.util.inspect.custom"):null;s.Buffer=o,s.SlowBuffer=wr,s.INSPECT_MAX_BYTES=50;const w=2147483647;s.kMaxLength=w,o.TYPED_ARRAY_SUPPORT=l(),!o.TYPED_ARRAY_SUPPORT&&typeof console<"u"&&typeof console.error=="function"&&console.error("This browser lacks typed array (Uint8Array) support which is required by `buffer` v5.x. Use `buffer` v4.x if you require old browser support.");function l(){try{const e=new Uint8Array(1),r={foo:function(){return 42}};return Object.setPrototypeOf(r,Uint8Array.prototype),Object.setPrototypeOf(e,r),e.foo()===42}catch{return!1}}Object.defineProperty(o.prototype,"parent",{enumerable:!0,get:function(){if(o.isBuffer(this))return this.buffer}}),Object.defineProperty(o.prototype,"offset",{enumerable:!0,get:function(){if(o.isBuffer(this))return this.byteOffset}});function f(e){if(e>w)throw new RangeError('The value "'+e+'" is invalid for option "size"');const r=new Uint8Array(e);return Object.setPrototypeOf(r,o.prototype),r}function o(e,r,t){if(typeof e=="number"){if(typeof r=="string")throw new TypeError('The "string" argument must be of type string. Received type number');return I(e)}return x(e,r,t)}o.poolSize=8192;function x(e,r,t){if(typeof e=="string")return C(e,r);if(ArrayBuffer.isView(e))return M(e);if(e==null)throw new TypeError("The first argument must be one of type string, Buffer, ArrayBuffer, Array, or Array-like Object. Received type "+typeof e);if(S(e,ArrayBuffer)||e&&S(e.buffer,ArrayBuffer)||typeof SharedArrayBuffer<"u"&&(S(e,SharedArrayBuffer)||e&&S(e.buffer,SharedArrayBuffer)))return P(e,r,t);if(typeof e=="number")throw new TypeError('The "value" argument must not be of type number. Received type number');const i=e.valueOf&&e.valueOf();if(i!=null&&i!==e)return o.from(i,r,t);const n=yr(e);if(n)return n;if(typeof Symbol<"u"&&Symbol.toPrimitive!=null&&typeof e[Symbol.toPrimitive]=="function")return o.from(e[Symbol.toPrimitive]("string"),r,t);throw new TypeError("The first argument must be one of type string, Buffer, ArrayBuffer, Array, or Array-like Object. Received type "+typeof e)}o.from=function(e,r,t){return x(e,r,t)},Object.setPrototypeOf(o.prototype,Uint8Array.prototype),Object.setPrototypeOf(o,Uint8Array);function A(e){if(typeof e!="number")throw new TypeError('"size" argument must be of type number');if(e<0)throw new RangeError('The value "'+e+'" is invalid for option "size"')}function m(e,r,t){return A(e),e<=0?f(e):r!==void 0?typeof t=="string"?f(e).fill(r,t):f(e).fill(r):f(e)}o.alloc=function(e,r,t){return m(e,r,t)};function I(e){return A(e),f(e<0?0:z(e)|0)}o.allocUnsafe=function(e){return I(e)},o.allocUnsafeSlow=function(e){return I(e)};function C(e,r){if((typeof r!="string"||r==="")&&(r="utf8"),!o.isEncoding(r))throw new TypeError("Unknown encoding: "+r);const t=Q(e,r)|0;let i=f(t);const n=i.write(e,r);return n!==t&&(i=i.slice(0,n)),i}function U(e){const r=e.length<0?0:z(e.length)|0,t=f(r);for(let i=0;i<r;i+=1)t[i]=e[i]&255;return t}function M(e){if(S(e,Uint8Array)){const r=new Uint8Array(e);return P(r.buffer,r.byteOffset,r.byteLength)}return U(e)}function P(e,r,t){if(r<0||e.byteLength<r)throw new RangeError('"offset" is outside of buffer bounds');if(e.byteLength<r+(t||0))throw new RangeError('"length" is outside of buffer bounds');let i;return r===void 0&&t===void 0?i=new Uint8Array(e):t===void 0?i=new Uint8Array(e,r):i=new Uint8Array(e,r,t),Object.setPrototypeOf(i,o.prototype),i}function yr(e){if(o.isBuffer(e)){const r=z(e.length)|0,t=f(r);return t.length===0||e.copy(t,0,0,r),t}if(e.length!==void 0)return typeof e.length!="number"||V(e.length)?f(0):U(e);if(e.type==="Buffer"&&Array.isArray(e.data))return U(e.data)}function z(e){if(e>=w)throw new RangeError("Attempt to allocate Buffer larger than maximum size: 0x"+w.toString(16)+" bytes");return e|0}function wr(e){return+e!=e&&(e=0),o.alloc(+e)}o.isBuffer=function(r){return r!=null&&r._isBuffer===!0&&r!==o.prototype},o.compare=function(r,t){if(S(r,Uint8Array)&&(r=o.from(r,r.offset,r.byteLength)),S(t,Uint8Array)&&(t=o.from(t,t.offset,t.byteLength)),!o.isBuffer(r)||!o.isBuffer(t))throw new TypeError('The "buf1", "buf2" arguments must be one of type Buffer or Uint8Array');if(r===t)return 0;let i=r.length,n=t.length;for(let u=0,c=Math.min(i,n);u<c;++u)if(r[u]!==t[u]){i=r[u],n=t[u];break}return i<n?-1:n<i?1:0},o.isEncoding=function(r){switch(String(r).toLowerCase()){case"hex":case"utf8":case"utf-8":case"ascii":case"latin1":case"binary":case"base64":case"ucs2":case"ucs-2":case"utf16le":case"utf-16le":return!0;default:return!1}},o.concat=function(r,t){if(!Array.isArray(r))throw new TypeError('"list" argument must be an Array of Buffers');if(r.length===0)return o.alloc(0);let i;if(t===void 0)for(t=0,i=0;i<r.length;++i)t+=r[i].length;const n=o.allocUnsafe(t);let u=0;for(i=0;i<r.length;++i){let c=r[i];if(S(c,Uint8Array))u+c.length>n.length?(o.isBuffer(c)||(c=o.from(c)),c.copy(n,u)):Uint8Array.prototype.set.call(n,c,u);else if(o.isBuffer(c))c.copy(n,u);else throw new TypeError('"list" argument must be an Array of Buffers');u+=c.length}return n};function Q(e,r){if(o.isBuffer(e))return e.length;if(ArrayBuffer.isView(e)||S(e,ArrayBuffer))return e.byteLength;if(typeof e!="string")throw new TypeError('The "string" argument must be one of type string, Buffer, or ArrayBuffer. Received type '+typeof e);const t=e.length,i=arguments.length>2&&arguments[2]===!0;if(!i&&t===0)return 0;let n=!1;for(;;)switch(r){case"ascii":case"latin1":case"binary":return t;case"utf8":case"utf-8":return J(e).length;case"ucs2":case"ucs-2":case"utf16le":case"utf-16le":return t*2;case"hex":return t>>>1;case"base64":return sr(e).length;default:if(n)return i?-1:J(e).length;r=(""+r).toLowerCase(),n=!0}}o.byteLength=Q;function xr(e,r,t){let i=!1;if((r===void 0||r<0)&&(r=0),r>this.length||((t===void 0||t>this.length)&&(t=this.length),t<=0)||(t>>>=0,r>>>=0,t<=r))return"";for(e||(e="utf8");;)switch(e){case"hex":return Tr(this,r,t);case"utf8":case"utf-8":return tr(this,r,t);case"ascii":return Ar(this,r,t);case"latin1":case"binary":return Ur(this,r,t);case"base64":return Ir(this,r,t);case"ucs2":case"ucs-2":case"utf16le":case"utf-16le":return Rr(this,r,t);default:if(i)throw new TypeError("Unknown encoding: "+e);e=(e+"").toLowerCase(),i=!0}}o.prototype._isBuffer=!0;function L(e,r,t){const i=e[r];e[r]=e[t],e[t]=i}o.prototype.swap16=function(){const r=this.length;if(r%2!==0)throw new RangeError("Buffer size must be a multiple of 16-bits");for(let t=0;t<r;t+=2)L(this,t,t+1);return this},o.prototype.swap32=function(){const r=this.length;if(r%4!==0)throw new RangeError("Buffer size must be a multiple of 32-bits");for(let t=0;t<r;t+=4)L(this,t,t+3),L(this,t+1,t+2);return this},o.prototype.swap64=function(){const r=this.length;if(r%8!==0)throw new RangeError("Buffer size must be a multiple of 64-bits");for(let t=0;t<r;t+=8)L(this,t,t+7),L(this,t+1,t+6),L(this,t+2,t+5),L(this,t+3,t+4);return this},o.prototype.toString=function(){const r=this.length;return r===0?"":arguments.length===0?tr(this,0,r):xr.apply(this,arguments)},o.prototype.toLocaleString=o.prototype.toString,o.prototype.equals=function(r){if(!o.isBuffer(r))throw new TypeError("Argument must be a Buffer");return this===r?!0:o.compare(this,r)===0},o.prototype.inspect=function(){let r="";const t=s.INSPECT_MAX_BYTES;return r=this.toString("hex",0,t).replace(/(.{2})/g,"$1 ").trim(),this.length>t&&(r+=" ... "),"<Buffer "+r+">"},y&&(o.prototype[y]=o.prototype.inspect),o.prototype.compare=function(r,t,i,n,u){if(S(r,Uint8Array)&&(r=o.from(r,r.offset,r.byteLength)),!o.isBuffer(r))throw new TypeError('The "target" argument must be one of type Buffer or Uint8Array. Received type '+typeof r);if(t===void 0&&(t=0),i===void 0&&(i=r?r.length:0),n===void 0&&(n=0),u===void 0&&(u=this.length),t<0||i>r.length||n<0||u>this.length)throw new RangeError("out of range index");if(n>=u&&t>=i)return 0;if(n>=u)return-1;if(t>=i)return 1;if(t>>>=0,i>>>=0,n>>>=0,u>>>=0,this===r)return 0;let c=u-n,a=i-t;const E=Math.min(c,a),d=this.slice(n,u),g=r.slice(t,i);for(let B=0;B<E;++B)if(d[B]!==g[B]){c=d[B],a=g[B];break}return c<a?-1:a<c?1:0};function v(e,r,t,i,n){if(e.length===0)return-1;if(typeof t=="string"?(i=t,t=0):t>2147483647?t=2147483647:t<-2147483648&&(t=-2147483648),t=+t,V(t)&&(t=n?0:e.length-1),t<0&&(t=e.length+t),t>=e.length){if(n)return-1;t=e.length-1}else if(t<0)if(n)t=0;else return-1;if(typeof r=="string"&&(r=o.from(r,i)),o.isBuffer(r))return r.length===0?-1:rr(e,r,t,i,n);if(typeof r=="number")return r=r&255,typeof Uint8Array.prototype.indexOf=="function"?n?Uint8Array.prototype.indexOf.call(e,r,t):Uint8Array.prototype.lastIndexOf.call(e,r,t):rr(e,[r],t,i,n);throw new TypeError("val must be string, number or Buffer")}function rr(e,r,t,i,n){let u=1,c=e.length,a=r.length;if(i!==void 0&&(i=String(i).toLowerCase(),i==="ucs2"||i==="ucs-2"||i==="utf16le"||i==="utf-16le")){if(e.length<2||r.length<2)return-1;u=2,c/=2,a/=2,t/=2}function E(g,B){return u===1?g[B]:g.readUInt16BE(B*u)}let d;if(n){let g=-1;for(d=t;d<c;d++)if(E(e,d)===E(r,g===-1?0:d-g)){if(g===-1&&(g=d),d-g+1===a)return g*u}else g!==-1&&(d-=d-g),g=-1}else for(t+a>c&&(t=c-a),d=t;d>=0;d--){let g=!0;for(let B=0;B<a;B++)if(E(e,d+B)!==E(r,B)){g=!1;break}if(g)return d}return-1}o.prototype.includes=function(r,t,i){return this.indexOf(r,t,i)!==-1},o.prototype.indexOf=function(r,t,i){return v(this,r,t,i,!0)},o.prototype.lastIndexOf=function(r,t,i){return v(this,r,t,i,!1)};function Br(e,r,t,i){t=Number(t)||0;const n=e.length-t;i?(i=Number(i),i>n&&(i=n)):i=n;const u=r.length;i>u/2&&(i=u/2);let c;for(c=0;c<i;++c){const a=parseInt(r.substr(c*2,2),16);if(V(a))return c;e[t+c]=a}return c}function dr(e,r,t,i){return G(J(r,e.length-t),e,t,i)}function Er(e,r,t,i){return G($r(r),e,t,i)}function gr(e,r,t,i){return G(sr(r),e,t,i)}function mr(e,r,t,i){return G(Lr(r,e.length-t),e,t,i)}o.prototype.write=function(r,t,i,n){if(t===void 0)n="utf8",i=this.length,t=0;else if(i===void 0&&typeof t=="string")n=t,i=this.length,t=0;else if(isFinite(t))t=t>>>0,isFinite(i)?(i=i>>>0,n===void 0&&(n="utf8")):(n=i,i=void 0);else throw new Error("Buffer.write(string, encoding, offset[, length]) is no longer supported");const u=this.length-t;if((i===void 0||i>u)&&(i=u),r.length>0&&(i<0||t<0)||t>this.length)throw new RangeError("Attempt to write outside buffer bounds");n||(n="utf8");let c=!1;for(;;)switch(n){case"hex":return Br(this,r,t,i);case"utf8":case"utf-8":return dr(this,r,t,i);case"ascii":case"latin1":case"binary":return Er(this,r,t,i);case"base64":return gr(this,r,t,i);case"ucs2":case"ucs-2":case"utf16le":case"utf-16le":return mr(this,r,t,i);default:if(c)throw new TypeError("Unknown encoding: "+n);n=(""+n).toLowerCase(),c=!0}},o.prototype.toJSON=function(){return{type:"Buffer",data:Array.prototype.slice.call(this._arr||this,0)}};function Ir(e,r,t){return r===0&&t===e.length?h.fromByteArray(e):h.fromByteArray(e.slice(r,t))}function tr(e,r,t){t=Math.min(e.length,t);const i=[];let n=r;for(;n<t;){const u=e[n];let c=null,a=u>239?4:u>223?3:u>191?2:1;if(n+a<=t){let E,d,g,B;switch(a){case 1:u<128&&(c=u);break;case 2:E=e[n+1],(E&192)===128&&(B=(u&31)<<6|E&63,B>127&&(c=B));break;case 3:E=e[n+1],d=e[n+2],(E&192)===128&&(d&192)===128&&(B=(u&15)<<12|(E&63)<<6|d&63,B>2047&&(B<55296||B>57343)&&(c=B));break;case 4:E=e[n+1],d=e[n+2],g=e[n+3],(E&192)===128&&(d&192)===128&&(g&192)===128&&(B=(u&15)<<18|(E&63)<<12|(d&63)<<6|g&63,B>65535&&B<1114112&&(c=B))}}c===null?(c=65533,a=1):c>65535&&(c-=65536,i.push(c>>>10&1023|55296),c=56320|c&1023),i.push(c),n+=a}return Fr(i)}const er=4096;function Fr(e){const r=e.length;if(r<=er)return String.fromCharCode.apply(String,e);let t="",i=0;for(;i<r;)t+=String.fromCharCode.apply(String,e.slice(i,i+=er));return t}function Ar(e,r,t){let i="";t=Math.min(e.length,t);for(let n=r;n<t;++n)i+=String.fromCharCode(e[n]&127);return i}function Ur(e,r,t){let i="";t=Math.min(e.length,t);for(let n=r;n<t;++n)i+=String.fromCharCode(e[n]);return i}function Tr(e,r,t){const i=e.length;(!r||r<0)&&(r=0),(!t||t<0||t>i)&&(t=i);let n="";for(let u=r;u<t;++u)n+=kr[e[u]];return n}function Rr(e,r,t){const i=e.slice(r,t);let n="";for(let u=0;u<i.length-1;u+=2)n+=String.fromCharCode(i[u]+i[u+1]*256);return n}o.prototype.slice=function(r,t){const i=this.length;r=~~r,t=t===void 0?i:~~t,r<0?(r+=i,r<0&&(r=0)):r>i&&(r=i),t<0?(t+=i,t<0&&(t=0)):t>i&&(t=i),t<r&&(t=r);const n=this.subarray(r,t);return Object.setPrototypeOf(n,o.prototype),n};function F(e,r,t){if(e%1!==0||e<0)throw new RangeError("offset is not uint");if(e+r>t)throw new RangeError("Trying to access beyond buffer length")}o.prototype.readUintLE=o.prototype.readUIntLE=function(r,t,i){r=r>>>0,t=t>>>0,i||F(r,t,this.length);let n=this[r],u=1,c=0;for(;++c<t&&(u*=256);)n+=this[r+c]*u;return n},o.prototype.readUintBE=o.prototype.readUIntBE=function(r,t,i){r=r>>>0,t=t>>>0,i||F(r,t,this.length);let n=this[r+--t],u=1;for(;t>0&&(u*=256);)n+=this[r+--t]*u;return n},o.prototype.readUint8=o.prototype.readUInt8=function(r,t){return r=r>>>0,t||F(r,1,this.length),this[r]},o.prototype.readUint16LE=o.prototype.readUInt16LE=function(r,t){return r=r>>>0,t||F(r,2,this.length),this[r]|this[r+1]<<8},o.prototype.readUint16BE=o.prototype.readUInt16BE=function(r,t){return r=r>>>0,t||F(r,2,this.length),this[r]<<8|this[r+1]},o.prototype.readUint32LE=o.prototype.readUInt32LE=function(r,t){return r=r>>>0,t||F(r,4,this.length),(this[r]|this[r+1]<<8|this[r+2]<<16)+this[r+3]*16777216},o.prototype.readUint32BE=o.prototype.readUInt32BE=function(r,t){return r=r>>>0,t||F(r,4,this.length),this[r]*16777216+(this[r+1]<<16|this[r+2]<<8|this[r+3])},o.prototype.readBigUInt64LE=$(function(r){r=r>>>0,N(r,"offset");const t=this[r],i=this[r+7];(t===void 0||i===void 0)&&O(r,this.length-8);const n=t+this[++r]*2**8+this[++r]*2**16+this[++r]*2**24,u=this[++r]+this[++r]*2**8+this[++r]*2**16+i*2**24;return BigInt(n)+(BigInt(u)<<BigInt(32))}),o.prototype.readBigUInt64BE=$(function(r){r=r>>>0,N(r,"offset");const t=this[r],i=this[r+7];(t===void 0||i===void 0)&&O(r,this.length-8);const n=t*2**24+this[++r]*2**16+this[++r]*2**8+this[++r],u=this[++r]*2**24+this[++r]*2**16+this[++r]*2**8+i;return(BigInt(n)<<BigInt(32))+BigInt(u)}),o.prototype.readIntLE=function(r,t,i){r=r>>>0,t=t>>>0,i||F(r,t,this.length);let n=this[r],u=1,c=0;for(;++c<t&&(u*=256);)n+=this[r+c]*u;return u*=128,n>=u&&(n-=Math.pow(2,8*t)),n},o.prototype.readIntBE=function(r,t,i){r=r>>>0,t=t>>>0,i||F(r,t,this.length);let n=t,u=1,c=this[r+--n];for(;n>0&&(u*=256);)c+=this[r+--n]*u;return u*=128,c>=u&&(c-=Math.pow(2,8*t)),c},o.prototype.readInt8=function(r,t){return r=r>>>0,t||F(r,1,this.length),this[r]&128?(255-this[r]+1)*-1:this[r]},o.prototype.readInt16LE=function(r,t){r=r>>>0,t||F(r,2,this.length);const i=this[r]|this[r+1]<<8;return i&32768?i|4294901760:i},o.prototype.readInt16BE=function(r,t){r=r>>>0,t||F(r,2,this.length);const i=this[r+1]|this[r]<<8;return i&32768?i|4294901760:i},o.prototype.readInt32LE=function(r,t){return r=r>>>0,t||F(r,4,this.length),this[r]|this[r+1]<<8|this[r+2]<<16|this[r+3]<<24},o.prototype.readInt32BE=function(r,t){return r=r>>>0,t||F(r,4,this.length),this[r]<<24|this[r+1]<<16|this[r+2]<<8|this[r+3]},o.prototype.readBigInt64LE=$(function(r){r=r>>>0,N(r,"offset");const t=this[r],i=this[r+7];(t===void 0||i===void 0)&&O(r,this.length-8);const n=this[r+4]+this[r+5]*2**8+this[r+6]*2**16+(i<<24);return(BigInt(n)<<BigInt(32))+BigInt(t+this[++r]*2**8+this[++r]*2**16+this[++r]*2**24)}),o.prototype.readBigInt64BE=$(function(r){r=r>>>0,N(r,"offset");const t=this[r],i=this[r+7];(t===void 0||i===void 0)&&O(r,this.length-8);const n=(t<<24)+this[++r]*2**16+this[++r]*2**8+this[++r];return(BigInt(n)<<BigInt(32))+BigInt(this[++r]*2**24+this[++r]*2**16+this[++r]*2**8+i)}),o.prototype.readFloatLE=function(r,t){return r=r>>>0,t||F(r,4,this.length),p.read(this,r,!0,23,4)},o.prototype.readFloatBE=function(r,t){return r=r>>>0,t||F(r,4,this.length),p.read(this,r,!1,23,4)},o.prototype.readDoubleLE=function(r,t){return r=r>>>0,t||F(r,8,this.length),p.read(this,r,!0,52,8)},o.prototype.readDoubleBE=function(r,t){return r=r>>>0,t||F(r,8,this.length),p.read(this,r,!1,52,8)};function T(e,r,t,i,n,u){if(!o.isBuffer(e))throw new TypeError('"buffer" argument must be a Buffer instance');if(r>n||r<u)throw new RangeError('"value" argument is out of bounds');if(t+i>e.length)throw new RangeError("Index out of range")}o.prototype.writeUintLE=o.prototype.writeUIntLE=function(r,t,i,n){if(r=+r,t=t>>>0,i=i>>>0,!n){const a=Math.pow(2,8*i)-1;T(this,r,t,i,a,0)}let u=1,c=0;for(this[t]=r&255;++c<i&&(u*=256);)this[t+c]=r/u&255;return t+i},o.prototype.writeUintBE=o.prototype.writeUIntBE=function(r,t,i,n){if(r=+r,t=t>>>0,i=i>>>0,!n){const a=Math.pow(2,8*i)-1;T(this,r,t,i,a,0)}let u=i-1,c=1;for(this[t+u]=r&255;--u>=0&&(c*=256);)this[t+u]=r/c&255;return t+i},o.prototype.writeUint8=o.prototype.writeUInt8=function(r,t,i){return r=+r,t=t>>>0,i||T(this,r,t,1,255,0),this[t]=r&255,t+1},o.prototype.writeUint16LE=o.prototype.writeUInt16LE=function(r,t,i){return r=+r,t=t>>>0,i||T(this,r,t,2,65535,0),this[t]=r&255,this[t+1]=r>>>8,t+2},o.prototype.writeUint16BE=o.prototype.writeUInt16BE=function(r,t,i){return r=+r,t=t>>>0,i||T(this,r,t,2,65535,0),this[t]=r>>>8,this[t+1]=r&255,t+2},o.prototype.writeUint32LE=o.prototype.writeUInt32LE=function(r,t,i){return r=+r,t=t>>>0,i||T(this,r,t,4,4294967295,0),this[t+3]=r>>>24,this[t+2]=r>>>16,this[t+1]=r>>>8,this[t]=r&255,t+4},o.prototype.writeUint32BE=o.prototype.writeUInt32BE=function(r,t,i){return r=+r,t=t>>>0,i||T(this,r,t,4,4294967295,0),this[t]=r>>>24,this[t+1]=r>>>16,this[t+2]=r>>>8,this[t+3]=r&255,t+4};function ir(e,r,t,i,n){fr(r,i,n,e,t,7);let u=Number(r&BigInt(4294967295));e[t++]=u,u=u>>8,e[t++]=u,u=u>>8,e[t++]=u,u=u>>8,e[t++]=u;let c=Number(r>>BigInt(32)&BigInt(4294967295));return e[t++]=c,c=c>>8,e[t++]=c,c=c>>8,e[t++]=c,c=c>>8,e[t++]=c,t}function nr(e,r,t,i,n){fr(r,i,n,e,t,7);let u=Number(r&BigInt(4294967295));e[t+7]=u,u=u>>8,e[t+6]=u,u=u>>8,e[t+5]=u,u=u>>8,e[t+4]=u;let c=Number(r>>BigInt(32)&BigInt(4294967295));return e[t+3]=c,c=c>>8,e[t+2]=c,c=c>>8,e[t+1]=c,c=c>>8,e[t]=c,t+8}o.prototype.writeBigUInt64LE=$(function(r,t=0){return ir(this,r,t,BigInt(0),BigInt("0xffffffffffffffff"))}),o.prototype.writeBigUInt64BE=$(function(r,t=0){return nr(this,r,t,BigInt(0),BigInt("0xffffffffffffffff"))}),o.prototype.writeIntLE=function(r,t,i,n){if(r=+r,t=t>>>0,!n){const E=Math.pow(2,8*i-1);T(this,r,t,i,E-1,-E)}let u=0,c=1,a=0;for(this[t]=r&255;++u<i&&(c*=256);)r<0&&a===0&&this[t+u-1]!==0&&(a=1),this[t+u]=(r/c>>0)-a&255;return t+i},o.prototype.writeIntBE=function(r,t,i,n){if(r=+r,t=t>>>0,!n){const E=Math.pow(2,8*i-1);T(this,r,t,i,E-1,-E)}let u=i-1,c=1,a=0;for(this[t+u]=r&255;--u>=0&&(c*=256);)r<0&&a===0&&this[t+u+1]!==0&&(a=1),this[t+u]=(r/c>>0)-a&255;return t+i},o.prototype.writeInt8=function(r,t,i){return r=+r,t=t>>>0,i||T(this,r,t,1,127,-128),r<0&&(r=255+r+1),this[t]=r&255,t+1},o.prototype.writeInt16LE=function(r,t,i){return r=+r,t=t>>>0,i||T(this,r,t,2,32767,-32768),this[t]=r&255,this[t+1]=r>>>8,t+2},o.prototype.writeInt16BE=function(r,t,i){return r=+r,t=t>>>0,i||T(this,r,t,2,32767,-32768),this[t]=r>>>8,this[t+1]=r&255,t+2},o.prototype.writeInt32LE=function(r,t,i){return r=+r,t=t>>>0,i||T(this,r,t,4,2147483647,-2147483648),this[t]=r&255,this[t+1]=r>>>8,this[t+2]=r>>>16,this[t+3]=r>>>24,t+4},o.prototype.writeInt32BE=function(r,t,i){return r=+r,t=t>>>0,i||T(this,r,t,4,2147483647,-2147483648),r<0&&(r=4294967295+r+1),this[t]=r>>>24,this[t+1]=r>>>16,this[t+2]=r>>>8,this[t+3]=r&255,t+4},o.prototype.writeBigInt64LE=$(function(r,t=0){return ir(this,r,t,-BigInt("0x8000000000000000"),BigInt("0x7fffffffffffffff"))}),o.prototype.writeBigInt64BE=$(function(r,t=0){return nr(this,r,t,-BigInt("0x8000000000000000"),BigInt("0x7fffffffffffffff"))});function or(e,r,t,i,n,u){if(t+i>e.length)throw new RangeError("Index out of range");if(t<0)throw new RangeError("Index out of range")}function ur(e,r,t,i,n){return r=+r,t=t>>>0,n||or(e,r,t,4),p.write(e,r,t,i,23,4),t+4}o.prototype.writeFloatLE=function(r,t,i){return ur(this,r,t,!0,i)},o.prototype.writeFloatBE=function(r,t,i){return ur(this,r,t,!1,i)};function cr(e,r,t,i,n){return r=+r,t=t>>>0,n||or(e,r,t,8),p.write(e,r,t,i,52,8),t+8}o.prototype.writeDoubleLE=function(r,t,i){return cr(this,r,t,!0,i)},o.prototype.writeDoubleBE=function(r,t,i){return cr(this,r,t,!1,i)},o.prototype.copy=function(r,t,i,n){if(!o.isBuffer(r))throw new TypeError("argument should be a Buffer");if(i||(i=0),!n&&n!==0&&(n=this.length),t>=r.length&&(t=r.length),t||(t=0),n>0&&n<i&&(n=i),n===i||r.length===0||this.length===0)return 0;if(t<0)throw new RangeError("targetStart out of bounds");if(i<0||i>=this.length)throw new RangeError("Index out of range");if(n<0)throw new RangeError("sourceEnd out of bounds");n>this.length&&(n=this.length),r.length-t<n-i&&(n=r.length-t+i);const u=n-i;return this===r&&typeof Uint8Array.prototype.copyWithin=="function"?this.copyWithin(t,i,n):Uint8Array.prototype.set.call(r,this.subarray(i,n),t),u},o.prototype.fill=function(r,t,i,n){if(typeof r=="string"){if(typeof t=="string"?(n=t,t=0,i=this.length):typeof i=="string"&&(n=i,i=this.length),n!==void 0&&typeof n!="string")throw new TypeError("encoding must be a string");if(typeof n=="string"&&!o.isEncoding(n))throw new TypeError("Unknown encoding: "+n);if(r.length===1){const c=r.charCodeAt(0);(n==="utf8"&&c<128||n==="latin1")&&(r=c)}}else typeof r=="number"?r=r&255:typeof r=="boolean"&&(r=Number(r));if(t<0||this.length<t||this.length<i)throw new RangeError("Out of range index");if(i<=t)return this;t=t>>>0,i=i===void 0?this.length:i>>>0,r||(r=0);let u;if(typeof r=="number")for(u=t;u<i;++u)this[u]=r;else{const c=o.isBuffer(r)?r:o.from(r,n),a=c.length;if(a===0)throw new TypeError('The value "'+r+'" is invalid for argument "value"');for(u=0;u<i-t;++u)this[u+t]=c[u%a]}return this};const k={};function H(e,r,t){k[e]=class extends t{constructor(){super(),Object.defineProperty(this,"message",{value:r.apply(this,arguments),writable:!0,configurable:!0}),this.name=`${this.name} [${e}]`,this.stack,delete this.name}get code(){return e}set code(n){Object.defineProperty(this,"code",{configurable:!0,enumerable:!0,value:n,writable:!0})}toString(){return`${this.name} [${e}]: ${this.message}`}}}H("ERR_BUFFER_OUT_OF_BOUNDS",function(e){return e?`${e} is outside of buffer bounds`:"Attempt to access memory outside buffer bounds"},RangeError),H("ERR_INVALID_ARG_TYPE",function(e,r){return`The "${e}" argument must be of type number. Received type ${typeof r}`},TypeError),H("ERR_OUT_OF_RANGE",function(e,r,t){let i=`The value of "${e}" is out of range.`,n=t;return Number.isInteger(t)&&Math.abs(t)>2**32?n=hr(String(t)):typeof t=="bigint"&&(n=String(t),(t>BigInt(2)**BigInt(32)||t<-(BigInt(2)**BigInt(32)))&&(n=hr(n)),n+="n"),i+=` It must be ${r}. Received ${n}`,i},RangeError);function hr(e){let r="",t=e.length;const i=e[0]==="-"?1:0;for(;t>=i+4;t-=3)r=`_${e.slice(t-3,t)}${r}`;return`${e.slice(0,t)}${r}`}function Cr(e,r,t){N(r,"offset"),(e[r]===void 0||e[r+t]===void 0)&&O(r,e.length-(t+1))}function fr(e,r,t,i,n,u){if(e>t||e<r){const c=typeof r=="bigint"?"n":"";let a;throw r===0||r===BigInt(0)?a=`>= 0${c} and < 2${c} ** ${(u+1)*8}${c}`:a=`>= -(2${c} ** ${(u+1)*8-1}${c}) and < 2 ** ${(u+1)*8-1}${c}`,new k.ERR_OUT_OF_RANGE("value",a,e)}Cr(i,n,u)}function N(e,r){if(typeof e!="number")throw new k.ERR_INVALID_ARG_TYPE(r,"number",e)}function O(e,r,t){throw Math.floor(e)!==e?(N(e,t),new k.ERR_OUT_OF_RANGE("offset","an integer",e)):r<0?new k.ERR_BUFFER_OUT_OF_BOUNDS:new k.ERR_OUT_OF_RANGE("offset",`>= 0 and <= ${r}`,e)}const Sr=/[^+/0-9A-Za-z-_]/g;function _r(e){if(e=e.split("=")[0],e=e.trim().replace(Sr,""),e.length<2)return"";for(;e.length%4!==0;)e=e+"=";return e}function J(e,r){r=r||1/0;let t;const i=e.length;let n=null;const u=[];for(let c=0;c<i;++c){if(t=e.charCodeAt(c),t>55295&&t<57344){if(!n){if(t>56319){(r-=3)>-1&&u.push(239,191,189);continue}else if(c+1===i){(r-=3)>-1&&u.push(239,191,189);continue}n=t;continue}if(t<56320){(r-=3)>-1&&u.push(239,191,189),n=t;continue}t=(n-55296<<10|t-56320)+65536}else n&&(r-=3)>-1&&u.push(239,191,189);if(n=null,t<128){if((r-=1)<0)break;u.push(t)}else if(t<2048){if((r-=2)<0)break;u.push(t>>6|192,t&63|128)}else if(t<65536){if((r-=3)<0)break;u.push(t>>12|224,t>>6&63|128,t&63|128)}else if(t<1114112){if((r-=4)<0)break;u.push(t>>18|240,t>>12&63|128,t>>6&63|128,t&63|128)}else throw new Error("Invalid code point")}return u}function $r(e){const r=[];for(let t=0;t<e.length;++t)r.push(e.charCodeAt(t)&255);return r}function Lr(e,r){let t,i,n;const u=[];for(let c=0;c<e.length&&!((r-=2)<0);++c)t=e.charCodeAt(c),i=t>>8,n=t%256,u.push(n),u.push(i);return u}function sr(e){return h.toByteArray(_r(e))}function G(e,r,t,i){let n;for(n=0;n<i&&!(n+t>=r.length||n>=e.length);++n)r[n+t]=e[n];return n}function S(e,r){return e instanceof r||e!=null&&e.constructor!=null&&e.constructor.name!=null&&e.constructor.name===r.name}function V(e){return e!==e}const kr=function(){const e="0123456789abcdef",r=new Array(256);for(let t=0;t<16;++t){const i=t*16;for(let n=0;n<16;++n)r[i+n]=e[t]+e[n]}return r}();function $(e){return typeof BigInt>"u"?Nr:e}function Nr(){throw new Error("BigInt not supported")}})(ar);const Y=Dr(),D="/api",j=br(""),Jr=()=>j.value?W("user",()=>JSON.parse(ar.Buffer.from(j.value.split(".")[1],"base64").toString())):{},Vr=()=>{const s=W(`${D}/classes`,()=>({}));async function h(){s.value=await $fetch(`${D}/classes`)}return{classes:s,getClassify:h}},Xr=()=>{const s=W("anketa",()=>({})),h=W("share",()=>({candId:""}));async function p(f,o=h.value.candId){s.value[f]=await Y(`${D}/${f}/${o}`)}async function y(f,o){const x=await Y(`${D}/${f}/${h.value.candId}`,{method:"POST",body:o});console.log(x),X().add({icon:"i-heroicons-check-circle",title:"Успешно",description:"Информация обновлена",color:"green"})}async function w(f,o){if(!confirm("Вы действительно хотите удалить запись?"))return;const x=await Y(`${D}/${o}/${f}`,{method:"DELETE"});console.log(x),X().add({icon:"i-heroicons-information-circle",title:"Информация",description:`Запись с ID ${f} удалена`,color:"primary"})}async function l(f,o,x){const A=X(),m=new FormData;if(f){for(const C of f)m.append("file",C);const I=await Y(`${D}/file/${o}/${x}`,{method:"POST",body:m});console.log(I),A.add({icon:"i-heroicons-check-circle",title:"Информация",description:"Файлы успешно загружены",color:"green"})}else A.add({icon:"i-heroicons-exclamation-triangle",title:"Внимание",description:"Ошибка при загрузке файла",color:"red"});m.delete("file")}return{anketa:s,share:h,getItem:p,updateItem:y,deleteItem:w,submitFile:l}};export{Jr as a,D as b,Dr as c,Xr as d,Vr as s,j as u};