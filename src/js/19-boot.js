
  var ready = function () { build(); features(); selAllInit(); jpMapInit(); navInit(); };
  if ('requestIdleCallback' in window) requestIdleCallback(ready); else setTimeout(ready, 50);
  if ('serviceWorker' in navigator && location.protocol.indexOf('http') === 0) { navigator.serviceWorker.register('sw.js').catch(function () {}); navigator.serviceWorker.addEventListener('message', function (e) { if (e.data && e.data.type === 'update') toast('Nouvelle version disponible.', 'Recharger', function () { location.reload(); }); }); }
})();
