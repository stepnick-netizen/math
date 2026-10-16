
(function(){
  var cb=document.getElementById('copyReport');
  if(!cb||typeof renderReport!=='function'||!navigator.share)return;
  var uk=document.documentElement.lang==='uk';
  var b=document.createElement('button');
  b.type='button';b.className='btn';b.id='shareReport';b.style.background='var(--sky)';
  b.textContent=uk?'Надіслати звіт':'Send my report';
  cb.parentNode.insertBefore(b,cb);
  b.onclick=function(){
    renderReport();
    var txt=document.getElementById('reportText').value, fb=document.getElementById('copyFb');
    navigator.share({title:document.title,text:txt}).then(function(){
      fb.className='fb good pop';
      fb.textContent=uk?'Готово! Якщо застосунок ще відкритий, натисни там «Надіслати».':'Done! If the app is still open, tap Send there.';
    }).catch(function(e){
      if(e&&e.name==='AbortError')return;
      fb.className='fb bad';
      fb.textContent=uk?'Меню «Поділитися» не відкрилось. Натисни «Скопіювати звіт» і встав текст у повідомлення.':'The share menu didn’t open. Tap "Copy my report" and paste it into a message.';
    });
  };
})();
