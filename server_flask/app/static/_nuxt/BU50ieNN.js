import{ay as g,az as f,r as D,aA as B,t as z,aB as E,Z as K,a2 as M,aC as v,aD as H,e as R,aE as S,aF as V}from"./DWkXyvYO.js";const j=e=>e==="defer"||e===!1;function N(...e){var p;const n=typeof e[e.length-1]=="string"?e.pop():void 0;typeof e[0]!="string"&&e.unshift(n);let[t,l,a={}]=e;if(typeof t!="string")throw new TypeError("[nuxt] [asyncData] key must be a string.");if(typeof l!="function")throw new TypeError("[nuxt] [asyncData] handler must be a function.");const s=g(),C=l,w=()=>f.value,b=()=>s.isHydrating?s.payload.data[t]:s.static.data[t];a.server=a.server??!0,a.default=a.default??w,a.getCachedData=a.getCachedData??b,a.lazy=a.lazy??!1,a.immediate=a.immediate??!0,a.deep=a.deep??f.deep,a.dedupe=a.dedupe??"cancel";const d=a.getCachedData(t,s),h=d!=null;if(!s._asyncData[t]||!a.immediate){(p=s.payload._errors)[t]??(p[t]=f.errorValue);const i=a.deep?D:B;s._asyncData[t]={data:i(h?d:a.default()),pending:D(!h),error:z(s.payload._errors,t),status:D("idle"),_default:a.default}}const r={...s._asyncData[t]};delete r._default,r.refresh=r.execute=(i={})=>{if(s._asyncDataPromises[t]){if(j(i.dedupe??a.dedupe))return s._asyncDataPromises[t];s._asyncDataPromises[t].cancelled=!0}if(i._initial||s.isHydrating&&i._initial!==!1){const c=i._initial?d:a.getCachedData(t,s);if(c!=null)return Promise.resolve(c)}r.pending.value=!0,r.status.value="pending";const u=new Promise((c,o)=>{try{c(C(s))}catch(y){o(y)}}).then(async c=>{if(u.cancelled)return s._asyncDataPromises[t];let o=c;a.transform&&(o=await a.transform(c)),a.pick&&(o=F(o,a.pick)),s.payload.data[t]=o,r.data.value=o,r.error.value=f.errorValue,r.status.value="success"}).catch(c=>{if(u.cancelled)return s._asyncDataPromises[t];r.error.value=H(c),r.data.value=R(a.default()),r.status.value="error"}).finally(()=>{u.cancelled||(r.pending.value=!1,delete s._asyncDataPromises[t])});return s._asyncDataPromises[t]=u,s._asyncDataPromises[t]},r.clear=()=>P(s,t);const _=()=>r.refresh({_initial:!0}),O=a.server!==!1&&s.payload.serverRendered;{const i=S();if(i&&!i._nuxtOnBeforeMountCbs){i._nuxtOnBeforeMountCbs=[];const o=i._nuxtOnBeforeMountCbs;E(()=>{o.forEach(y=>{y()}),o.splice(0,o.length)}),K(()=>o.splice(0,o.length))}O&&s.isHydrating&&(r.error.value||d!=null)?(r.pending.value=!1,r.status.value=r.error.value?"error":"success"):i&&(s.payload.serverRendered&&s.isHydrating||a.lazy)&&a.immediate?i._nuxtOnBeforeMountCbs.push(_):a.immediate&&_();const u=V();if(a.watch){const o=M(a.watch,()=>r.refresh());u&&v(o)}const c=s.hook("app:data:refresh",async o=>{(!o||o.includes(t))&&await r.refresh()});u&&v(c)}const m=Promise.resolve(s._asyncDataPromises[t]).then(()=>r);return Object.assign(m,r),m}function x(...e){const n=typeof e[e.length-1]=="string"?e.pop():void 0;typeof e[0]!="string"&&e.unshift(n);const[t,l,a={}]=e;return N(t,l,{...a,lazy:!0},null)}function I(e){const n=g(),l=Object.keys(n.payload.data);for(const a of l)P(n,a)}function P(e,n){n in e.payload.data&&(e.payload.data[n]=void 0),n in e.payload._errors&&(e.payload._errors[n]=f.errorValue),e._asyncData[n]&&(e._asyncData[n].data.value=void 0,e._asyncData[n].error.value=f.errorValue,e._asyncData[n].pending.value=!1,e._asyncData[n].status.value="idle"),n in e._asyncDataPromises&&(e._asyncDataPromises[n]&&(e._asyncDataPromises[n].cancelled=!0),e._asyncDataPromises[n]=void 0)}function F(e,n){const t={};for(const l of n)t[l]=e[l];return t}export{x as a,I as c,N as u};