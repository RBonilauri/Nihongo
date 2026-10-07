/* Célébration 100 % : écran festif + feux d'artifice minimalistes */
(function(){
  const MSG=['Sans-faute, bravo !','Parfait, tu es en feu !','Impeccable, さすが !','Zéro faute, quel talent !','Magnifique, continue comme ça !'];
  let raf=0, cv=null;
  function stop(){ cancelAnimationFrame(raf); raf=0; if(cv){cv.remove();cv=null;} }
  function fire(host){
    stop();
    if(matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    cv=document.createElement('canvas'); cv.className='q-fw';
    const W=cv.width=innerWidth, H=cv.height=innerHeight; document.body.appendChild(cv);
    const g=cv.getContext('2d'), cols=['#e8b84a','#d9453a','#fff3d0','#f08fa0'];
    const rk=[], sp=[]; let t0=performance.now(), last=t0, nxt=0, n=0;
    function launch(){ const x=W*(.15+Math.random()*.7);
      rk.push({x,y:H,vy:-(H*.0011+Math.random()*H*.0004),ty:H*(.18+Math.random()*.25),c:cols[n++%cols.length]}); }
    function burst(x,y,c){ const k=26;
      for(let i=0;i<k;i++){ const a=i/k*6.283+Math.random()*.2, v=1.6+Math.random()*1.6;
        sp.push({x,y,vx:Math.cos(a)*v,vy:Math.sin(a)*v,l:1,c}); } }
    function loop(now){
      if(!host.isConnected){stop();return;}
      const dt=Math.min(now-last,40)/16.7; last=now; const el=now-t0;
      g.clearRect(0,0,W,H);
      if(el>nxt && el<3200){ launch(); nxt=el+450+Math.random()*350; }
      for(let i=rk.length-1;i>=0;i--){ const r=rk[i]; r.y+=r.vy*dt*16.7;
        g.fillStyle=r.c; g.globalAlpha=.9; g.fillRect(r.x-1,r.y,2,10);
        if(r.y<=r.ty){ burst(r.x,r.y,r.c); rk.splice(i,1); } }
      for(let i=sp.length-1;i>=0;i--){ const s=sp[i];
        s.x+=s.vx*dt; s.y+=s.vy*dt; s.vx*=.985; s.vy=s.vy*.985+.035*dt; s.l-=.014*dt;
        if(s.l<=0){sp.splice(i,1);continue;}
        g.globalAlpha=s.l; g.fillStyle=s.c; g.beginPath(); g.arc(s.x,s.y,1.8*s.l+.6,0,6.283); g.fill(); }
      if(el<3200||rk.length||sp.length) raf=requestAnimationFrame(loop); else stop();
    }
    raf=requestAnimationFrame(loop);
  }
  function check(el){
    if(el.classList.contains('perfect')) return;
    const n=el.querySelector('.n'); if(!n) return;
    const m=n.textContent.match(/(\d+)\s*\/\s*(\d+)/); if(!m) return;
    const ok=+m[1], tot=+m[2]; if(tot<5||ok!==tot) return;
    el.classList.add('perfect');
    const top=document.createElement('div'); top.className='q-crown';
    top.innerHTML='<span class="q-em">🎉</span><b>完璧！</b><i>'+MSG[Math.floor(Math.random()*MSG.length)]+'</i>';
    el.insertBefore(top,el.firstChild);
    el.addEventListener('click',()=>fire(el));
    fire(el);
  }
  new MutationObserver(ms=>{ for(const m of ms) for(const a of m.addedNodes){
    if(a.nodeType!==1) continue;
    if(a.matches('.q-score')) check(a); else a.querySelectorAll&&a.querySelectorAll('.q-score').forEach(check);
  }}).observe(document.body,{childList:true,subtree:true});
  window.__celebrate=check;
})();
