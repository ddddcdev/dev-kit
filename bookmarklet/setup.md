# Bookmarklet

Personal tools, not a general standard (see the README).


### 📋️Title+URL
```js
javascript:(function(){e = document.createElement('textarea');e.textContent = document.title + '\r\n' + document.URL;document.body.appendChild(e);e.select();document.execCommand('copy');e.remove();})();
```

## 📋️\[md\]
```js

```

## 📋️LINK
```js
javascript:(function(){const t=window.getSelection().toString()||document.title,u=window.location.href,l=`<a href="${u}" id="bookmarklet-link" style="color:white;text-decoration:none;">${t}</a>`,e=document.createElement('div');e.innerHTML=l;e.style.cssText="position:fixed;top:0;left:50%;transform:translateX(-50%);z-index:9999;background-color:black;padding:5px;border-radius:5px";document.body.appendChild(e);const r=document.createRange(),n=document.getElementById('bookmarklet-link');r.selectNode(n);const s=window.getSelection();s.removeAllRanges();s.addRange(r);try{const o=document.execCommand('copy');if(!o){alert('Unable to copy the link. Please try another method.');}}catch(err){alert('Unable to copy the link. Please try another method.');}})();
```

### ↔ ChatGPT
```js
javascript:(()=>{try{const id="cgpt-fw-final-v6";document.getElementById(id)?.remove();const s=document.createElement("style");s.id=id;s.textContent=%27html,body{overflow-x:hidden!important;margin:0!important;padding:0!important}main,[role="main"],.container,.mx-auto{max-width:none!important;width:100%!important;margin:0!important;padding:0!important}[class*="px-(--thread-content-margin)"]{padding-left:.25rem!important;padding-right:.25rem!important}[class*="md:px-[60px]"]{padding-left:.25rem!important;padding-right:.25rem!important}.agent-turn,[class*="agent-turn"]{margin-right:0!important}.max-w-3xl,.max-w-4xl,.max-w-5xl,.max-w-6xl,.max-w-7xl,.max-w-screen-lg,.max-w-screen-xl{max-width:none!important;width:100%!important;margin:0!important}pre,code,kbd,samp{max-width:100%!important}pre{white-space:pre-wrap!important;overflow-wrap:anywhere!important;word-break:break-word!important;overflow-x:auto!important}code{overflow-wrap:anywhere!important;word-break:break-word!important}a{overflow-wrap:anywhere!important;word-break:break-word!important}*{box-sizing:border-box!important}*{scrollbar-gutter:auto!important}%27;document.head.appendChild(s);document.querySelectorAll(%27[class*="px-(--thread-content-margin)"]%27).forEach(e=>{e.style.setProperty("--thread-content-margin","0px","important");e.style.paddingLeft=".25rem";e.style.paddingRight=".25rem"});document.querySelectorAll(".agent-turn,[class*=%27agent-turn%27]").forEach(e=>{e.style.marginRight="0"})}catch(e){console.error(e)}})();javascript:(()=>{try{const id="cgpt-fw-pad-05em";document.getElementById(id)?.remove();const s=document.createElement("style");s.id=id;s.textContent=%27[class*="px-(--thread-content-margin)"],.agent-turn,[class*="agent-turn"]{padding-left:.5em!important;padding-right:.5em!important}pre{padding-left:.5em!important;padding-right:.5em!important}%27;document.head.appendChild(s)}catch(e){console.error(e)}})();
```

### ↔ Gemini
```js
javascript:(()=>{const f=()=>document.querySelectorAll("*").forEach(e=>{const s=getComputedStyle(e);if(s.maxWidth!=="none"&&e.style.maxWidth!=="100%")e.style.maxWidth="100%"});f();new MutationObserver(f).observe(document.body,{childList:true,subtree:true});console.log("Monitoring and stretching all new elements...")})();
```

### ↔ Perplexity
```js
javascript:(()=>{const s=document.createElement('style');s.innerHTML=`main,.flex-1,.w-full,.m-auto,.mx-auto,.xl\\:max-w-3xl,.md\\:max-w-3xl{max-width:100%!important;width:100%!important;margin:0!important}.lg\\:max-w-screen-lg,.xl\\:max-w-screen-xl{max-width:100%!important}.px-4,.sm\\:px-6{padding-left:1rem!important;padding-right:1rem!important}`;document.head.appendChild(s);})();
```