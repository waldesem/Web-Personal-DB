import{Y as h,aK as f,r as D,aL as N,t as B,aM as K,ab as M,N as R,aN as P,aO as z,e as H,aP as S,aQ as E,aR as V,aS as j}from"./lDZheyb0.js";const x=e=>e==="defer"||e===!1;function L(...e){var v;const r=typeof e[e.length-1]=="string"?e.pop():void 0;typeof e[0]!="string"&&e.unshift(r);let[t,l,a={}]=e;if(typeof t!="string")throw new TypeError("[nuxt] [asyncData] key must be a string.");if(typeof l!="function")throw new TypeError("[nuxt] [asyncData] handler must be a function.");const s=h(),w=l,C=()=>f.value,b=()=>s.isHydrating?s.payload.data[t]:s.static.data[t];a.server=a.server??!0,a.default=a.default??C,a.getCachedData=a.getCachedData??b,a.lazy=a.lazy??!1,a.immediate=a.immediate??!0,a.deep=a.deep??f.deep,a.dedupe=a.dedupe??"cancel";const d=a.getCachedData(t,s),_=d!=null;if(!s._asyncData[t]||!a.immediate){(v=s.payload._errors)[t]??(v[t]=f.errorValue);const i=a.deep?D:N;s._asyncData[t]={data:i(_?d:a.default()),pending:D(!_),error:B(s.payload._errors,t),status:D("idle"),_default:a.default}}const n={...s._asyncData[t]};delete n._default,n.refresh=n.execute=(i={})=>{if(s._asyncDataPromises[t]){if(x(i.dedupe??a.dedupe))return s._asyncDataPromises[t];s._asyncDataPromises[t].cancelled=!0}if(i._initial||s.isHydrating&&i._initial!==!1){const c=i._initial?d:a.getCachedData(t,s);if(c!=null)return Promise.resolve(c)}n.pending.value=!0,n.status.value="pending";const u=new Promise((c,o)=>{try{c(w(s))}catch(y){o(y)}}).then(async c=>{if(u.cancelled)return s._asyncDataPromises[t];let o=c;a.transform&&(o=await a.transform(c)),a.pick&&(o=T(o,a.pick)),s.payload.data[t]=o,n.data.value=o,n.error.value=f.errorValue,n.status.value="success"}).catch(c=>{if(u.cancelled)return s._asyncDataPromises[t];n.error.value=z(c),n.data.value=H(a.default()),n.status.value="error"}).finally(()=>{u.cancelled||(n.pending.value=!1,delete s._asyncDataPromises[t])});return s._asyncDataPromises[t]=u,s._asyncDataPromises[t]},n.clear=()=>g(s,t);const m=()=>n.refresh({_initial:!0}),O=a.server!==!1&&s.payload.serverRendered;{const i=S();if(i&&!i._nuxtOnBeforeMountCbs){i._nuxtOnBeforeMountCbs=[];const o=i._nuxtOnBeforeMountCbs;K(()=>{o.forEach(y=>{y()}),o.splice(0,o.length)}),M(()=>o.splice(0,o.length))}O&&s.isHydrating&&(n.error.value||d!=null)?(n.pending.value=!1,n.status.value=n.error.value?"error":"success"):i&&(s.payload.serverRendered&&s.isHydrating||a.lazy)&&a.immediate?i._nuxtOnBeforeMountCbs.push(m):a.immediate&&m();const u=E();if(a.watch){const o=R(a.watch,()=>n.refresh());u&&P(o)}const c=s.hook("app:data:refresh",async o=>{(!o||o.includes(t))&&await n.refresh()});u&&P(c)}const p=Promise.resolve(s._asyncDataPromises[t]).then(()=>n);return Object.assign(p,n),p}function I(...e){const r=typeof e[e.length-1]=="string"?e.pop():void 0;typeof e[0]!="string"&&e.unshift(r);const[t,l,a={}]=e;return L(t,l,{...a,lazy:!0},null)}async function Q(e){await new Promise(t=>V(t));const r=j(e);await h().hooks.callHookParallel("app:data:refresh",r)}function U(e){const r=h(),l=Object.keys(r.payload.data);for(const a of l)g(r,a)}function g(e,r){r in e.payload.data&&(e.payload.data[r]=void 0),r in e.payload._errors&&(e.payload._errors[r]=f.errorValue),e._asyncData[r]&&(e._asyncData[r].data.value=void 0,e._asyncData[r].error.value=f.errorValue,e._asyncData[r].pending.value=!1,e._asyncData[r].status.value="idle"),r in e._asyncDataPromises&&(e._asyncDataPromises[r]&&(e._asyncDataPromises[r].cancelled=!0),e._asyncDataPromises[r]=void 0)}function T(e,r){const t={};for(const l of r)t[l]=e[l];return t}export{I as a,U as c,Q as r,L as u};