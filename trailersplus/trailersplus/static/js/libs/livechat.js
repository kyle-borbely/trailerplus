(function() {
	if (window.location.href.indexOf('/es/') > 0) {
		var se = document.createElement('script');
		se.type = 'text/javascript';
		se.async = true;
		se.src =
			'//storage.googleapis.com/code.snapengage.com/js/a9c9b043-9e79-48eb-bb37-9ba2a77d40d1.js';
		var done = false;
		se.onload = se.onreadystatechange = function() {
			if (
				!done &&
				(!this.readyState ||
					this.readyState === 'loaded' ||
					this.readyState === 'complete')
			) {
				done = true;
				window.chatOpen('es');
			}
		};
		var s = document.getElementsByTagName('script')[0];
		s.parentNode.insertBefore(se, s);
	} else {
		var se = document.createElement('script');
		se.type = 'text/javascript';
		se.async = true;
		se.src =
			'//storage.googleapis.com/code.snapengage.com/js/a5f2af92-88ea-455e-bace-e4344df42892.js';
		var done = false;
		se.onload = se.onreadystatechange = function() {
			if (
				!done &&
				(!this.readyState ||
					this.readyState === 'loaded' ||
					this.readyState === 'complete')
			) {
				done = true;
				window.chatOpen();
			}
		};
		var s = document.getElementsByTagName('script')[0];
		s.parentNode.insertBefore(se, s);
	}
})();
