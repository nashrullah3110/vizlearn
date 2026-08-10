/* Make the homepage track rails navigable.
 *
 * Each rail is a horizontal scroller holding 12-41 cards and showing four.
 * Measured on the Machine Learning rail at 1440px: 7,680px of content in a
 * 1,336px window - 83% of every track was off-screen behind an affordance
 * nobody could see, because .no-scrollbar hides the scrollbar and there were
 * no arrows. The fifth card clipping at the frame edge was the only clue that
 * more existed.
 *
 * This adds the missing controls: a button at each end, a fade over the edge
 * that has more content behind it, and scroll-snap so a click lands cleanly on
 * a card rather than halfway through one.
 *
 * Attaches by observing the container the hub re-renders into, so switching
 * tracks (which replaces the whole innerHTML) re-enhances the new rails
 * without the inline renderer needing to know this file exists.
 */
(function () {
  'use strict';

  var ARROW = {
    left: '<path d="M15 18l-6-6 6-6"/>',
    right: '<path d="M9 18l6-6-6-6"/>'
  };

  function icon(dir) {
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" ' +
      'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ARROW[dir] + '</svg>';
  }

  /* Scroll set directly, with no animation.
   *
   * Every smooth option was tried and each one is a *silent no-op* in an
   * engine that does not produce frames - measured here: scrollBy with
   * behavior:'smooth' left scrollLeft at 0, CSS scroll-behavior:smooth turned
   * a plain scrollLeft assignment into a no-op too, and requestAnimationFrame
   * callbacks never fired at all (0 of 2). A direct assignment moved the rail
   * to 612 every time.
   *
   * An arrow that does nothing is a worse failure than one that jumps, and it
   * fails invisibly, so this takes the guaranteed path. scroll-snap-type on
   * the rail still lands the movement tidily on a card edge.
   */
  function glide(rail, to) {
    var max = rail.scrollWidth - rail.clientWidth;
    rail.scrollLeft = Math.max(0, Math.min(max, to));
  }

  function button(dir, label) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'vz-rail-btn vz-rail-' + dir;
    b.setAttribute('aria-label', label);
    b.innerHTML = icon(dir);
    return b;
  }

  function enhance(rail) {
    if (rail.dataset.vzRail) return;
    rail.dataset.vzRail = '1';

    // The rail needs a positioned parent to hang the buttons and fades on. It
    // is created here rather than in the markup so the inline renderer's
    // template stays untouched.
    var frame = document.createElement('div');
    frame.className = 'vz-rail-frame';
    rail.parentNode.insertBefore(frame, rail);
    frame.appendChild(rail);

    // A scroller full of links is a landmark a screen reader should be able to
    // find and describe; it had neither a role nor a name.
    var name = '';
    var section = frame.closest('section');
    var h = section && section.querySelector('h2');
    if (h) name = h.textContent.trim();
    rail.setAttribute('role', 'group');
    rail.setAttribute('aria-label', name ? name + ' modules' : 'Modules');
    // Focusable so the rail can be scrolled with the arrow keys, not only by
    // tabbing through every card inside it.
    rail.tabIndex = 0;

    var prev = button('left', 'Scroll ' + (name || 'modules') + ' left');
    var next = button('right', 'Scroll ' + (name || 'modules') + ' right');
    frame.appendChild(prev);
    frame.appendChild(next);

    function nudge(dir) {
      // Just under one viewport, so the card at the edge stays visible as an
      // anchor rather than jumping past it.
      var step = Math.max(240, rail.clientWidth - 120);
      glide(rail, rail.scrollLeft + (dir === 'left' ? -step : step));
      // Refreshed here rather than left to the scroll event. That event is
      // dispatched at the next rendering opportunity, so in any context that
      // is not painting - a background tab, a headless browser - the arrows
      // would keep pointing at content that had already run out. The listener
      // below still covers wheel and drag scrolling.
      update();
    }
    prev.addEventListener('click', function () { nudge('left'); });
    next.addEventListener('click', function () { nudge('right'); });

    function update() {
      var max = rail.scrollWidth - rail.clientWidth;
      var x = rail.scrollLeft;
      // 2px of slack: sub-pixel layout means scrollLeft rarely hits 0 or max
      // exactly, and without it an arrow stays lit at the end of the rail.
      frame.classList.toggle('at-start', x <= 2);
      frame.classList.toggle('at-end', x >= max - 2);
      frame.classList.toggle('no-overflow', max <= 2);
    }

    rail.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  }

  function scan(root) {
    var rails = (root || document).querySelectorAll('.carousel-wrapper');
    for (var i = 0; i < rails.length; i++) enhance(rails[i]);
  }

  function init() {
    scan(document);

    // The hub replaces its whole card container when the topic changes, which
    // throws away every enhanced rail and inserts fresh ones.
    var host = document.getElementById('course-container') ||
               document.querySelector('[id*="course"]') ||
               document.body;
    if (window.MutationObserver) {
      new MutationObserver(function () { scan(host); })
        .observe(host, { childList: true, subtree: true });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
