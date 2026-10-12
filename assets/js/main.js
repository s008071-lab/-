/* ==========================================================================
   Ideal properties — main.js
   ========================================================================== */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- ページ遷移時のスクロール位置リセット ---------- */
  // ブラウザは再読み込みや「戻る/進む」で直前のスクロール位置を復元する。
  // 別ページを開いたのに途中までスクロールされて見えるのを防ぐため、自動復元を
  // 止め、ページを開いた時点で必ず先頭へ戻す。
  // ただし #付きのリンク（例: about.html#merit）は、その見出しへの移動が目的
  // なので対象外とする。
  if ('scrollRestoration' in history) {
    try { history.scrollRestoration = 'manual'; } catch (e) { /* 非対応環境は無視 */ }
  }

  function jumpToTop() {
    if (location.hash && location.hash.length > 1) return; // アンカー遷移は尊重する
    var root = document.documentElement;
    var prev = root.style.scrollBehavior;
    root.style.scrollBehavior = 'auto'; // CSS の smooth スクロールを一時的に無効化
    window.scrollTo(0, 0);
    if (document.body) document.body.scrollTop = 0;
    root.scrollTop = 0;
    root.style.scrollBehavior = prev;

    // iframe に埋め込まれている場合、内側を先頭に戻しても外側のスクロール位置が
    // 残る。同一オリジンであればこれも先頭へ戻す（別オリジンでは例外を握りつぶす）。
    if (window.parent && window.parent !== window) {
      try { window.parent.scrollTo(0, 0); } catch (e) { /* クロスオリジンでは操作不可 */ }
    }
  }

  jumpToTop();
  // 読み込み完了後に復元が走る場合と、bfcache からの復帰（戻る/進む）に備える。
  window.addEventListener('load', jumpToTop);
  window.addEventListener('pageshow', jumpToTop);

  /* ---------- Header: stuck state ---------- */
  var hdr = document.querySelector('.hdr');
  var fab = document.querySelector('.fab');
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (hdr) hdr.classList.toggle('is-stuck', y > 24);
    if (fab) fab.classList.toggle('is-on', y > 520);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Drawer ---------- */
  var burger = document.querySelector('.burger');
  var drawer = document.querySelector('.drawer');
  function setDrawer(open) {
    if (!burger || !drawer) return;
    burger.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    drawer.classList.toggle('is-open', open);
    document.body.classList.toggle('is-locked', open);
    var items = drawer.querySelectorAll('.drawer__item');
    for (var i = 0; i < items.length; i++) {
      items[i].style.transitionDelay = open ? (0.12 + i * 0.045) + 's' : '0s';
    }
  }
  if (burger) {
    burger.addEventListener('click', function () {
      setDrawer(!drawer.classList.contains('is-open'));
    });
  }
  if (drawer) {
    drawer.addEventListener('click', function (e) {
      if (e.target.closest('a')) setDrawer(false);
    });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && drawer && drawer.classList.contains('is-open')) setDrawer(false);
  });

  /* ---------- Scroll reveal ---------- */
  var revealables = document.querySelectorAll('[data-reveal]');
  if (reduced || !('IntersectionObserver' in window)) {
    for (var r = 0; r < revealables.length; r++) revealables[r].classList.add('is-in');
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('is-in');
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    for (var k = 0; k < revealables.length; k++) io.observe(revealables[k]);
  }

  /* ---------- Count-up numbers ---------- */
  var counters = document.querySelectorAll('[data-count]');
  function runCount(el) {
    var target = parseFloat(el.getAttribute('data-count'));
    var decimals = parseInt(el.getAttribute('data-decimals') || '0', 10);
    var dur = 1500;
    if (reduced) { el.textContent = target.toLocaleString('ja-JP', { minimumFractionDigits: decimals, maximumFractionDigits: decimals }); return; }
    var start = null;
    function frame(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 4);
      var v = target * eased;
      el.textContent = v.toLocaleString('ja-JP', { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
      if (p < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }
  if (counters.length) {
    if (!('IntersectionObserver' in window)) {
      for (var c = 0; c < counters.length; c++) runCount(counters[c]);
    } else {
      var cio = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { runCount(en.target); cio.unobserve(en.target); }
        });
      }, { threshold: 0.35 });
      for (var n = 0; n < counters.length; n++) {
        // ヒーロー内の数値は画面の高さが低い端末でも「0」のまま残らないよう、
        // スクロールを待たずに登場アニメーションの直後から動かす。
        if (counters[n].closest('.hero')) {
          (function (el) { setTimeout(function () { runCount(el); }, 1100); })(counters[n]);
        } else {
          cio.observe(counters[n]);
        }
      }
    }
  }

  /* ---------- Accordion ---------- */
  var accBtns = document.querySelectorAll('.acc__q');
  for (var a = 0; a < accBtns.length; a++) {
    accBtns[a].addEventListener('click', function () {
      var expanded = this.getAttribute('aria-expanded') === 'true';
      var panel = document.getElementById(this.getAttribute('aria-controls'));
      this.setAttribute('aria-expanded', expanded ? 'false' : 'true');
      if (panel) panel.setAttribute('data-open', expanded ? 'false' : 'true');
    });
  }

  /* ---------- News filter (news page) ---------- */
  var filterBtns = document.querySelectorAll('[data-filter]');
  if (filterBtns.length) {
    for (var f = 0; f < filterBtns.length; f++) {
      filterBtns[f].addEventListener('click', function () {
        var key = this.getAttribute('data-filter');
        for (var b = 0; b < filterBtns.length; b++) {
          filterBtns[b].classList.toggle('btn--ghost', filterBtns[b] !== this);
          filterBtns[b].setAttribute('aria-pressed', filterBtns[b] === this ? 'true' : 'false');
        }
        var items = document.querySelectorAll('[data-cat]');
        for (var i = 0; i < items.length; i++) {
          var show = key === 'all' || items[i].getAttribute('data-cat') === key;
          items[i].hidden = !show;
        }
      });
    }
  }

  /* ---------- Contact form (front-end validation + mailto fallback) ---------- */
  var form = document.querySelector('[data-contact-form]');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var fd = new FormData(form);
      var lines = [];
      fd.forEach(function (v, k) {
        if (k === 'agree') return;
        lines.push(k + ': ' + v);
      });
      var status = form.querySelector('[data-form-status]');
      if (status) {
        status.hidden = false;
        status.textContent = '送信内容を確認しました。現在このサイトはデモ環境のため、実際の送信は行われません。お急ぎの方はLINEまたはお電話をご利用ください。';
        status.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'center' });
      }
      // console output kept for integration hand-off
      if (window.console) console.log('[contact form payload]\n' + lines.join('\n'));
    });
  }

  /* ---------- Current year ---------- */
  var yrs = document.querySelectorAll('[data-year]');
  for (var y = 0; y < yrs.length; y++) yrs[y].textContent = new Date().getFullYear();
})();
