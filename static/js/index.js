// ── NAVBAR SCROLL ──
const navbar=document.getElementById('navbar');
window.addEventListener('scroll',()=>{
  navbar.classList.toggle('scrolled',window.scrollY>20);
});

// ── HAMBURGER ──
const hbg=document.getElementById('hamburger');
const mob=document.getElementById('mobile-menu');
hbg.addEventListener('click',()=>{
  hbg.classList.toggle('open');
  mob.classList.toggle('open');
});
mob.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{
  hbg.classList.remove('open');mob.classList.remove('open');
}));

// ── HERO WORDS ──
function buildWords(id, text, color, baseDelay){
  const el=document.getElementById(id);
  const words=text.split(' ');
  words.forEach((w,i)=>{
    const span=document.createElement('span');
    span.className='word';
    span.textContent=w+(i<words.length-1?' ':'');
    span.style.animationDelay=(baseDelay+i*0.06)+'s';
    el.appendChild(span);
  });
}
buildWords('line1','Get paid today.',null,.4);
buildWords('line2','Not next week.',null,.65);

// ── PHONE PROGRESS & TYPEWRITER ──
setTimeout(()=>{
  const fill=document.getElementById('prog-fill');
  const pct=document.getElementById('prog-pct');
  const tv=document.getElementById('trust-val');
  fill.style.width='75%';
  let n=0;
  const iv=setInterval(()=>{
    n=Math.min(n+2,75);
    pct.textContent=n+'%';
    tv.textContent=n;
    if(n>=75)clearInterval(iv);
  },26);
},1000);

function phoneTypewriter(){
  const el=document.getElementById('phone-ai-text');
  const text='Emeka, your ₦15,000 advance is approved. Keep grinding! 🔥';
  el.textContent='';
  let i=0;
  const iv=setInterval(()=>{
    if(i<text.length){el.textContent+=text[i++];}
    else clearInterval(iv);
  },45);
}
setTimeout(phoneTypewriter,2200);

// ── TICKER ──
(function(){
  const items=[
    '⚡ 1,200+ Workers Registered',
    '💸 ₦2.4M+ Advanced',
    '✅ 94% Approval Rate',
    '🔥 Average decision: 8 seconds',
    '🇳🇬 Built for Lagos hustle',
  ];
  const sep='<span class="ticker-sep">·</span>';
  let html='';
  [1,2].forEach(()=>{
    items.forEach((item,i)=>{
      html+=`<span class="ticker-item">${item}</span>`;
      if(i<items.length-1)html+=sep;
      html+=sep;
    });
  });
  document.getElementById('ticker-track').innerHTML=html;
})();

// ── INTERSECTION OBSERVER HELPER ──
function onView(selector,cb,threshold=.2){
  const obs=new IntersectionObserver((entries)=>{
    entries.forEach(e=>cb(e,obs));
  },{threshold});
  document.querySelectorAll(selector).forEach(el=>obs.observe(el));
}

// ── STEPS ANIMATE ──
onView('.step-card',(e)=>{
  if(e.isIntersecting){
    const d=parseInt(e.target.dataset.delay)||0;
    setTimeout(()=>e.target.classList.add('animated'),d);
  } else {
    e.target.classList.remove('animated');
  }
});

// ── TERMINAL DEMO ──
let terminalRunning=false;
function runTerminal(){
  if(terminalRunning)return;
  terminalRunning=true;
  ['tl1','tl2','tl3','tl4','tl5'].forEach(id=>{
    document.getElementById(id).classList.remove('show');
  });
  const loading=document.getElementById('t-loading');
  const bar=document.getElementById('t-bar');
  const approved=document.getElementById('t-approved');
  const reason=document.getElementById('t-reason');
  const results=document.getElementById('t-results');
  loading.classList.remove('show');
  bar.style.width='0';bar.style.transition='none';
  approved.classList.remove('show');
  reason.classList.remove('show');reason.textContent='';
  results.classList.remove('show');

  const lines=['tl1','tl2','tl3','tl4','tl5'];
  lines.forEach((id,i)=>{
    setTimeout(()=>document.getElementById(id).classList.add('show'),i*280);
  });

  setTimeout(()=>{
    loading.classList.add('show');
    setTimeout(()=>{
      bar.style.transition='width 1.5s ease';
      bar.style.width='100%';
    },100);
  },lines.length*280+200);

  setTimeout(()=>{
    approved.classList.add('show');
    const reasonText="Emeka has maintained consistent earnings between ₦7,200 and ₦11,000 over 8 logged shifts. His trust score of 75 reflects reliable hustle. Advancing ₦15,000 — keep grinding.";
    reason.classList.add('show');
    let ri=0;
    const riv=setInterval(()=>{
      if(ri<reasonText.length){reason.textContent+=reasonText[ri++];}
      else clearInterval(riv);
    },22);
  },lines.length*280+2200);

  setTimeout(()=>{
    results.classList.add('show');
    setTimeout(()=>terminalRunning=false,1000);
  },lines.length*280+5200);
}

const termObs=new IntersectionObserver((entries)=>{
  entries.forEach(e=>{
    if(e.isIntersecting){runTerminal();}
    else{terminalRunning=false;}
  });
},{threshold:.2});
const demoEl=document.getElementById('demo');
if(demoEl)termObs.observe(demoEl);

// ── FEATURE CARDS ──
onView('.feat-card',(e)=>{
  if(e.isIntersecting){
    const d=parseInt(e.target.dataset.delay)||0;
    setTimeout(()=>{
      e.target.style.transition=`opacity .45s ease ${d}ms, transform .45s ease ${d}ms`;
      e.target.classList.add('animated');
    },d);
  } else {
    e.target.classList.remove('animated');
    e.target.style.transition='none';
  }
});

// ── STATS COUNT UP ──
function countUp(el,target,suffix,prefix,duration=2000){
  const start=performance.now();
  function step(now){
    const p=Math.min((now-start)/duration,1);
    const ease=1-Math.pow(1-p,3);
    const val=Math.round(ease*target);
    if(prefix==='₦'&&target>=1000000){
      el.textContent='₦'+(val/1000000).toFixed(1)+'M+';
    } else if(target>=1000){
      el.textContent=prefix+val.toLocaleString()+suffix;
    } else {
      el.textContent=prefix+val+suffix;
    }
    if(p<1)requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

onView('.stat-block',(e)=>{
  if(e.isIntersecting){
    const d=parseInt(e.target.dataset.delay)||0;
    setTimeout(()=>{
      e.target.classList.add('animated');
      const id=e.target.querySelector('.stat-big').id;
      if(id==='stat1')countUp(document.getElementById('stat1'),2400000,'','₦');
      if(id==='stat2')countUp(document.getElementById('stat2'),1200,'+','');
      if(id==='stat3')countUp(document.getElementById('stat3'),8,'s','');
    },d);
  } else {
    e.target.classList.remove('animated');
    const id=e.target.querySelector('.stat-big').id;
    if(id==='stat1')document.getElementById('stat1').textContent='₦0';
    if(id==='stat2')document.getElementById('stat2').textContent='0';
    if(id==='stat3')document.getElementById('stat3').textContent='0s';
  }
});

// ── PARTICLES ──
(function(){
  const canvas=document.getElementById('particles-canvas');
  if(!canvas)return;
  const ctx=canvas.getContext('2d');
  let particles=[];

  function resize(){
    canvas.width=canvas.offsetWidth;
    canvas.height=canvas.offsetHeight;
  }
  resize();
  window.addEventListener('resize',resize);

  for(let i=0;i<22;i++){
    particles.push({
      x:Math.random()*canvas.width,
      y:canvas.height+Math.random()*200,
      r:2+Math.random()*5,
      speed:.4+Math.random()*.9,
      opacity:.15+Math.random()*.35
    });
  }

  function draw(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    particles.forEach(p=>{
      ctx.beginPath();
      ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
      ctx.fillStyle=`rgba(10,102,64,${p.opacity})`;
      ctx.fill();
      p.y-=p.speed;
      if(p.y<-20){
        p.y=canvas.height+10;
        p.x=Math.random()*canvas.width;
      }
    });
    requestAnimationFrame(draw);
  }
  draw();
})();
