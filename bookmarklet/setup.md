# Bookmarklet

Personal tools, not a general standard (see the README).

Install: open [index.html](index.html) in the browser (`open bookmarklet/index.html` on macOS,
`explorer.exe "$(wslpath -w bookmarklet/index.html)"` on WSL) and drag a button to the bookmarks bar. Or create a
bookmark and paste the code as its URL. After editing this file, regenerate the page with
`python3 bookmarklet/build-page.py`.

Copying uses the async Clipboard API and falls
back to `execCommand('copy')` where it is not available.

## Copy

### 📋️Title+URL

Page title and URL on two lines.

```js
javascript:(()=>{const c=(p,h)=>(h?navigator.clipboard.write([new ClipboardItem({'text/plain':new Blob([p],{type:'text/plain'}),'text/html':new Blob([h],{type:'text/html'})})]):navigator.clipboard.writeText(p)).catch(()=>{const e=document.createElement('textarea');e.value=p;document.body.appendChild(e);e.select();document.execCommand('copy');e.remove()});c(document.title+'\n'+location.href)})();
```

### 📋️[md]

Markdown link `[title](url)`. Uses the selected text as the title when there is a selection.

```js
javascript:(()=>{const c=(p,h)=>(h?navigator.clipboard.write([new ClipboardItem({'text/plain':new Blob([p],{type:'text/plain'}),'text/html':new Blob([h],{type:'text/html'})})]):navigator.clipboard.writeText(p)).catch(()=>{const e=document.createElement('textarea');e.value=p;document.body.appendChild(e);e.select();document.execCommand('copy');e.remove()});const t=(getSelection().toString()||document.title).replace(/[\[\]]/g,'\\$&');c('['+t+']('+location.href+')')})();
```

### 📋️LINK

Rich link (HTML) for pasting into documents and chat apps; plain text is the title. Uses the
selected text when there is a selection. Shows "Copied" for 1.5 s.

```js
javascript:(()=>{const c=(p,h)=>(h?navigator.clipboard.write([new ClipboardItem({'text/plain':new Blob([p],{type:'text/plain'}),'text/html':new Blob([h],{type:'text/html'})})]):navigator.clipboard.writeText(p)).catch(()=>{const e=document.createElement('textarea');e.value=p;document.body.appendChild(e);e.select();document.execCommand('copy');e.remove()});const t=getSelection().toString()||document.title,u=location.href,x=s=>s.replace(/[&<>"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'})[m]);c(t,'<a href="'+x(u)+'">'+x(t)+'</a>').then(()=>{const d=document.createElement('div');d.textContent='Copied: '+t;d.style.cssText='position:fixed;top:8px;left:50%25;transform:translateX(-50%25);z-index:2147483647;background:#000;color:#fff;padding:4px 10px;border-radius:5px;font:13px sans-serif';document.body.appendChild(d);setTimeout(()=>d.remove(),1500)})})();
```

## Wide chat view

Click once to widen the conversation to the window, again to restore. Each one targets the site's
current markup and breaks when the site changes it. Last checked 2026-11-03.

### ↔ ChatGPT

Overrides the conversation width variable; also wraps long code lines.

```js
javascript:(()=>{const id='dk-wide',o=document.getElementById(id);if(o){o.remove();return}const s=document.createElement('style');s.id=id;s.textContent='[class*="--thread-content-max-width"]{--thread-content-max-width:100%25!important;--thread-body-max-width:100%25!important}pre{white-space:pre-wrap!important;overflow-wrap:anywhere!important}';document.head.appendChild(s)})();
```

### ↔ Gemini

Lifts the width cap inside the conversation (images keep theirs) with a 24px side margin.

```js
javascript:(()=>{const id='dk-wide',o=document.getElementById(id);if(o){o.remove();return}const s=document.createElement('style');s.id=id;s.textContent='.conversation-container{padding-inline:24px!important;box-sizing:border-box}.conversation-container :not(img,svg,video,canvas,picture){max-width:none!important}.conversation-container .table-content{padding-inline:0!important}';document.head.appendChild(s)})();
```

### ↔ Perplexity

Lifts the thread width cap and collapses the empty side columns.

```js
javascript:(()=>{const id='dk-wide',o=document.getElementById(id);if(o){o.remove();return}const s=document.createElement('style');s.id=id;s.textContent='.max-w-threadContentWidth,.prose{max-width:none!important}[class*="grid-cols-[var(--context-pane-width)"]{--context-pane-width:0px!important}';document.head.appendChild(s)})();
```
