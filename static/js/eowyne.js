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


function ajax_popup(container, url) {
	$.get(url, function(data) {
		$(container).html(data);
		$(container).popup("show");
		initialize_ajax_popup(container);
	});
}


function initialize_ajax_popup(container) {
	$(container + " #form").submit(function(event) {
		event.preventDefault();
		var $form = $(this);
		var url = $form.attr("action");
		var fieldData = {};
		$form.find("input").each(function() {
			var name = $(this).attr("name");
			var value = $(this).val();
			if (name == "cancel") value = false;
			fieldData[name] = value;
		});
		$form.find("select").each(function() {
			var name = $(this).attr("name");
			var value = $(this).val();
			fieldData[name] = value;
		});
		$form.find("textarea").each(function() {
			var name = $(this).attr("name");
			var value = $(this).val();
			fieldData[name] = value;
		});
		$.post( url, fieldData ).done(ajax_popup_result);
	});
	$(container + " #form #cancel").click(function(event) {
		event.preventDefault();
		$(container).popup("hide");
	});
}

function ajax_popup_result(data) {
	if (data.indexOf("</html>") > -1) {
		document.open("text/html");
		document.write(data);
		document.close();
	} else {
		$("#popup").html(data);
		initialize_ajax_popup("#popup");
	}
}