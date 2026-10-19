(function () {
  var KEY = 'gc-theme';
  function apply(t) {
    document.documentElement.dataset.theme = t;
    document.querySelectorAll('iframe.pv').forEach(function (f) {
      try { f.contentDocument.documentElement.dataset.theme = t; } catch (e) {}
    });
  }
  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  var t = saved || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  apply(t);
  window.toggle = function () {
    t = t === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem(KEY, t); } catch (e) {}
    apply(t);
  };
  document.querySelectorAll('iframe.pv').forEach(function (f) {
    f.addEventListener('load', function () {
      try {
        f.contentDocument.documentElement.dataset.theme = t;
        var h = f.contentDocument.documentElement.scrollHeight;
        if (h > 40) f.height = h;
      } catch (e) {}
    });
  });
  var cv = document.querySelector('.cover>div');
  function fit() { if (!cv) return; var s = Math.min(1, document.documentElement.clientWidth / 960); cv.style.transform = 'scale(' + s + ')'; cv.parentNode.style.height = (288 * s) + 'px'; }
  fit(); addEventListener('resize', fit);
})();
