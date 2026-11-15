(function () {
	'use strict';
	var cfg = window.AdminPulse || {};
	var root = document.documentElement;

	// ---- Dark mode ----
	function isDark() { return root.classList.contains('ap-dark'); }
	function save(mode) {
		var fd = new FormData();
		fd.append('action', 'adminpulse_dark'); fd.append('nonce', cfg.nonce); fd.append('mode', mode);
		fetch(cfg.ajax, { method: 'POST', body: fd, credentials: 'same-origin' });
	}
	document.addEventListener('click', function (e) {
		var t = e.target.closest('.adminpulse-dark-toggle, #wp-admin-bar-adminpulse-dark a');
		if (t) {
			e.preventDefault();
			var next = isDark() ? 'off' : 'on';
			root.classList.toggle('ap-dark', next === 'on');
			save(next);
		}
		if (e.target.closest('.adminpulse-search-open, #wp-admin-bar-adminpulse-search a')) { e.preventDefault(); openPalette(); }
	});

	// ---- Command palette ----
	var el, input, list, items = [], active = 0, timer, ctrl;
	function build() {
		el = document.createElement('div');
		el.className = 'ap-palette'; el.hidden = true;
		el.innerHTML = '<div class="ap-palette-box" role="dialog" aria-modal="true" aria-label="Search"><input type="search" autocomplete="off"><ul role="listbox"></ul></div>';
		document.body.appendChild(el);
		input = el.querySelector('input'); list = el.querySelector('ul');
		input.placeholder = (cfg.i18n || {}).placeholder || 'Search…';
		el.addEventListener('mousedown', function (e) { if (e.target === el) closePalette(); });
		input.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(query, 180); });
		input.addEventListener('keydown', function (e) {
			if (e.key === 'ArrowDown') { move(1); e.preventDefault(); }
			else if (e.key === 'ArrowUp') { move(-1); e.preventDefault(); }
			else if (e.key === 'Enter' && items[active]) { window.location.href = items[active].url; }
		});
	}
	function openPalette() { if (!el) build(); el.hidden = false; input.value = ''; list.innerHTML = ''; items = []; input.focus(); }
	function closePalette() { if (el) el.hidden = true; }
	function move(d) {
		if (!items.length) return;
		active = (active + d + items.length) % items.length; paint();
	}
	function paint() {
		list.innerHTML = '';
		items.forEach(function (it, i) {
			var li = document.createElement('li');
			li.setAttribute('role', 'option');
			if (i === active) li.className = 'is-active';
			var a = document.createElement('a'); a.href = it.url; a.textContent = it.title;
			var s = document.createElement('span'); s.textContent = it.type;
			li.appendChild(a); li.appendChild(s); list.appendChild(li);
		});
		if (!items.length && input.value.length > 1) {
			var n = document.createElement('li'); n.className = 'ap-none'; n.textContent = (cfg.i18n || {}).none; list.appendChild(n);
		}
	}
	function query() {
		var q = input.value.trim();
		if (q.length < 2) { items = []; paint(); return; }
		if (ctrl) ctrl.abort();
		ctrl = new AbortController();
		fetch(cfg.rest + 'search?q=' + encodeURIComponent(q), { headers: { 'X-WP-Nonce': cfg.restNonce }, credentials: 'same-origin', signal: ctrl.signal })
			.then(function (r) { return r.json(); })
			.then(function (d) { items = Array.isArray(d) ? d : []; active = 0; paint(); })
			.catch(function () {});
	}
	document.addEventListener('keydown', function (e) {
		if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); openPalette(); }
		else if (e.key === 'Escape') closePalette();
	});
})();
