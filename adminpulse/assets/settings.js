jQuery(function ($) {
	$('.ap-color').wpColorPicker();
	$('#ap-menu-list').sortable({ handle: '.dashicons-menu', axis: 'y' });
	$('.ap-pick').on('click', function (e) {
		e.preventDefault();
		var $in = $(this).prev('input');
		var frame = wp.media({ multiple: false, library: { type: 'image' } });
		frame.on('select', function () { $in.val(frame.state().get('selection').first().toJSON().url); });
		frame.open();
	});
});
