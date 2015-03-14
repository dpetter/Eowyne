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
