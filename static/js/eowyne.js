$(document).ready(function() {
	$("#message-area").delay( 3000 ).slideUp("slow");
});

$(document).ready(function() { initialize_filters(); });

function initialize_filters() {
	$("input.eowyne-table-filter").each(function() {
		$(this).on("input", function() { filter_table() });
	});
	$("select.eowyne-table-filter").each(function() {
		$(this).change(function() { filter_table() });
		var n = $(this).parent()[0].cellIndex + 1;
		var identifier = "table td:nth-child(" + n + ")";
		var arr = [];
		$(identifier).each(function(index) {
			var text = $(this).text().trim();
			if (text == "") return;
			if (arr.indexOf(text) > -1) return;
			arr.push(text);
		});
		$(this).append("<option>*</option>");
		for (var i = 0; i < arr.length; i++) {
			$(this).append("<option>" + arr[i] + "</option>");
		}
	});
}

function filter_table() {
	$("tr").show();
	$(".eowyne-table-filter").each(function() {
		var value = $(this).val();
		var n = $(this).parent()[0].cellIndex + 1;
		var identifier = "table td:nth-child(" + n + ")";
		if (value != "" && value != "*") {
			$(identifier + ":not(:contains('" + value + "'))").parent().hide();
			$(this).parent().parent().show();
		}
	});
}

$(document).ready(function() {
	$(".eo-component").each(function(event) {
		var url = $(this).attr("href");
		ajax_component($(this), url);
	});
	$(".eo-popup-window").click(function(event) {
		event.preventDefault();
		var url = $(this).attr("href");
		ajax_popup("#eo-popup-window", url);
	});
});

function ajax_post(url, container, fieldData, o) {
	$.post(url, fieldData).done(function(data) {
		if (data.indexOf("</html>") > -1) {
			document.open("text/html");
			document.write(data);
			document.close();
		} else {
			$(container).html(data);
			o(container);
		}
	});
}

function ajax_get_fields(form) {
	var fieldData = {};
	form.find("input").each(function() {
		var name = $(this).attr("name");
		var value = $(this).val();
		if (name == "cancel") value = false;
		fieldData[name] = value;
	});
	form.find("select").each(function() {
		var name = $(this).attr("name");
		var value = $(this).val();
		fieldData[name] = value;
	});
	form.find("textarea").each(function() {
		var name = $(this).attr("name");
		var value = $(this).val();
		fieldData[name] = value;
	});
	return fieldData;
}

function ajax_component(container, url) {
	$.get(url, function(data) {
		$(container).replaceWith("<div class='eo-component'>" + data + "</div>");
		ajax_component_actions("div.eo-component");
	});
}

function ajax_component_actions(container) {
	$(container + " #form").submit(function(event) {
		event.preventDefault();
		var form = $(this);
		var url = form.attr("action");
		var fieldData = ajax_get_fields(form);
		ajax_post(url, container, fieldData, ajax_component_actions);
	});
}

function ajax_popup(container, url) {
	$.get(url, function(data) {
		$(container).html(data);
		$(container).popup("show");
		ajax_popup_actions(container);
	});
}

function ajax_popup_actions(container) {
	$(container + " #form").submit(function(event) {
		event.preventDefault();
		var form = $(this);
		var url = form.attr("action");
		var fieldData = ajax_get_fields(form);
		ajax_post(url, container, fieldData, ajax_popup_actions);
	});
	$(container + " #form #cancel").click(function(event) {
		event.preventDefault();
		$(container).popup("hide");
	});
}