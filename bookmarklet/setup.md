# Bookmarklet


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
javascript:(()=>{const s=document.createElement('style');s.textContent=`.max-w-3xl,.max-w-4xl,.max-w-5xl,.max-w-6xl,.max-w-7xl,.max-w-screen-lg,.max-w-screen-xl,.mx-auto,.container{max-width:100%!important;width:100%!important;margin-left:0!important;margin-right:0!important}.px-4,.px-6,.px-md,.sm\\:px-6{padding-left:1rem!important;padding-right:1rem!important}@media(min-width:768px){.col-span-8,.col-span-9,.col-span-10,.col-span-12{width:100%!important}.col-span-4,.col-span-3,.col-span-2{display:none!important}}`;document.head.appendChild(s);})();
```

### ↔ Perplexity
```js
javascript:(()=>{const s=document.createElement('style');s.innerHTML=`main,.flex-1,.w-full,.m-auto,.mx-auto,.xl\\:max-w-3xl,.md\\:max-w-3xl{max-width:100%!important;width:100%!important;margin:0!important}.lg\\:max-w-screen-lg,.xl\\:max-w-screen-xl{max-width:100%!important}.px-4,.sm\\:px-6{padding-left:1rem!important;padding-right:1rem!important}`;document.head.appendChild(s);})();
```