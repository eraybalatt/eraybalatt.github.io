/* Quote form for sub-pages (/hire/, /yapay-zeka-reklam-filmi/, ...): Web3Forms AJAX, same key as the homepage.
   Every lead carries where it came from (page, language, referring site, ?ref=) so Eray can see which channel works. */
(function(){
  var forms=document.querySelectorAll('form.qform');
  if(!forms.length)return;
  var lang=(document.documentElement.lang||'en').slice(0,2);
  var T={
    sending:{en:'Sending…',tr:'Gönderiliyor…'},
    ok:{en:'✓ Thanks! I\'ll get back to you shortly.',tr:'✓ Teşekkürler! Kısa süre içinde size döneceğim.'},
    fail:{en:'Couldn\'t send. Please email eray@eraybalat.com directly.',tr:'Gönderilemedi. Lütfen doğrudan eray@eraybalat.com adresine yazın.'},
    neterr:{en:'Network error. Please email eray@eraybalat.com directly.',tr:'Ağ hatası. Lütfen doğrudan eray@eraybalat.com adresine yazın.'}
  };
  var L=lang==='tr'?'tr':'en';
  function source(){
    var ref='direct';
    try{if(document.referrer){var h=new URL(document.referrer).host;ref=h===location.host?'internal':h;}}catch(_){}
    var camp='';try{camp=new URLSearchParams(location.search).get('ref')||'';}catch(_){}
    return {page:location.pathname,lang:lang,ref:ref,campaign:camp};
  }
  forms.forEach(function(f){
    f.addEventListener('submit',async function(e){
      e.preventDefault();
      var st=f.querySelector('.form-status'),btn=f.querySelector('.form-send');
      st.className='form-status';st.textContent='';
      var data=Object.fromEntries(new FormData(f)),src=source();
      data.page=src.page;data.lang=src.lang;data.ref=src.ref;if(src.campaign)data.campaign=src.campaign;
      data.subject='New project inquiry — eraybalat.com ['+src.lang+' · '+src.page+']';
      var orig=btn.textContent;btn.disabled=true;btn.textContent=T.sending[L];
      try{
        var res=await fetch('https://api.web3forms.com/submit',{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify(data)});
        var out=await res.json();
        if(out.success){st.className='form-status ok';st.textContent=T.ok[L];f.reset();}
        else{st.className='form-status err';st.textContent=T.fail[L];}
      }catch(_){st.className='form-status err';st.textContent=T.neterr[L];}
      btn.disabled=false;btn.textContent=orig;
    });
  });
})();
