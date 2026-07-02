// ===== eraybalat.com · case study page behaviour =====
(function(){
  // reveal on scroll
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)e.target.classList.add('show');});},{threshold:.12});
  document.querySelectorAll('.reveal').forEach(function(el){io.observe(el);});

  // mobile nav
  var toggle=document.querySelector('.nav-toggle'), links=document.getElementById('navlinks');
  if(toggle&&links){
    toggle.addEventListener('click',function(){var open=links.classList.toggle('open');toggle.setAttribute('aria-expanded',open?'true':'false');});
    links.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){links.classList.remove('open');toggle.setAttribute('aria-expanded','false');});});
  }

  // year
  var y=document.getElementById('year'); if(y)y.textContent=new Date().getFullYear();

  // click-to-play YouTube (swaps the poster for a youtube-nocookie embed, no third-party JS until asked)
  document.querySelectorAll('[data-yt]').forEach(function(el){
    el.addEventListener('click',function(e){
      e.preventDefault();
      if(el.querySelector('iframe'))return;
      var id=el.getAttribute('data-yt');
      var f=document.createElement('iframe');
      f.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0&modestbranding=1&playsinline=1';
      f.setAttribute('allow','autoplay; encrypted-media; picture-in-picture; fullscreen');
      f.setAttribute('allowfullscreen','');
      f.setAttribute('title','Video player');
      f.loading='lazy';
      el.appendChild(f);
      el.classList.add('playing');
    });
  });
})();
