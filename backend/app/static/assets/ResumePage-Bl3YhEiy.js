const __vite__fileDeps=["./HeaderDiv-CUQQRNex.js","./index-D2OLA4OR.js","./index-BqKjTnG4.css","./FileForm-CFD10zx8.js","./_plugin-vue_export-helper-DlAUqK2U.js","./FileForm-By8_2B11.css","./ResumeForm-B0kj5Tnj.js","./state-BHhWPIxB.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{d as p,c as l,b as o,u as e,e as a,F as u,o as d,i as c,h as s,j as r}from"./index-D2OLA4OR.js";import{f}from"./state-BHhWPIxB.js";const v={class:"position-relative"},E={class:"position-absolute bottom-100 end-0 px-3"},b=a("label",{for:"file",class:"text-primary fs-5",style:{cursor:"pointer"}},"Загрузить json ☇ ",-1),V=p({__name:"ResumePage",setup(F){const i=s(()=>r(()=>import("./HeaderDiv-CUQQRNex.js"),__vite__mapDeps([0,1,2]),import.meta.url)),m=s(()=>r(()=>import("./FileForm-CFD10zx8.js"),__vite__mapDeps([3,1,2,4,5]),import.meta.url)),_=s(()=>r(()=>import("./ResumeForm-B0kj5Tnj.js"),__vite__mapDeps([6,1,2,7]),import.meta.url));return(A,t)=>(d(),l(u,null,[o(e(i),{"page-header":"Создать анкету"}),a("div",v,[a("div",E,[b,o(e(m),{accept:".json",onSubmit:t[0]||(t[0]=n=>e(f).submitFile(n,"persons","0"))})])]),o(e(_),{onCancel:t[1]||(t[1]=n=>e(c).push({name:"persons"}))})],64))}});export{V as default};