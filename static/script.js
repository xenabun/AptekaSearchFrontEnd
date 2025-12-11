
document.addEventListener('DOMContentLoaded', function() {
	const min_price_value = document.getElementById("min_price");
	const min_price_const = document.getElementById("min_price_const");
	const max_price_value = document.getElementById("max_price");
	const max_price_const = document.getElementById("max_price_const");
	const search_submit = document.getElementById('mysubmit');

	document.getElementById('loading-icon').style.display = 'none';
	search_submit.onclick = function() {
		set_page(1);
		show_load();
	};

	min_price_value.onchange = function() {
		min_price_value.value = Math.min(Math.max(parseFloat(min_price_value.value), parseFloat(min_price_const.value)), parseFloat(max_price_const.value)) || parseFloat(min_price_const.value);
		if (parseFloat(min_price_value.value) > parseFloat(max_price_value.value)) {
			max_price_value.value = min_price_value.value
		}
	};
	max_price_value.onchange = function() {
		max_price_value.value = Math.min(Math.max(parseFloat(max_price_value.value), parseFloat(min_price_const.value)), parseFloat(max_price_const.value)) || parseFloat(max_price_const.value);
		if (parseFloat(max_price_value.value) < parseFloat(min_price_value.value)) {
			min_price_value.value = max_price_value.value
		}
	};
});

function get_page() {
	return +document.getElementById('search-form').page.value;
}
function get_min_page() {
	return +document.getElementById('search-form').min_page.value;
}
function get_max_page() {
	return +document.getElementById('search-form').max_page.value;
}
function set_page(new_page) {
	search_form = document.getElementById('search-form');
	search_form.page.value = new_page;
	search_form.submit();
}

function show_load() {
	const loading_icon = document.getElementById('loading-icon');
	loading_icon.style.display = 'flex';
}

function sortTable(n) {
	var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
	table = document.getElementById("search-result");
	theaders = document.querySelectorAll("#search-result > thead > tr > th");
	for (i = 0; i < theaders.length; i++) {
		header = theaders[i];
		hspan = header.getElementsByTagName('span')[0];
		hspan.innerHTML = '';
	}
	switching = true;
	dir = "asc";
	while (switching) {
		switching = false;
		rows = table.querySelectorAll('tbody > tr');
		// console.log(rows);
		for (i = 0; i < rows.length - 1; i++) {
			shouldSwitch = false;
			x = rows[i].getElementsByTagName("td")[n];
			y = rows[i + 1].getElementsByTagName("td")[n];
			if (dir == "asc") {
				xspan = x.getElementsByTagName('span');
				yspan = y.getElementsByTagName('span');
				if (xspan.length > 0 && yspan.length > 0) {
					if (Number(xspan[0].innerHTML) > Number(yspan[0].innerHTML)) {
						shouldSwitch = true;
						break;
					}
				} else {
					if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
						shouldSwitch = true;
						break;
					}
				}
			} else if (dir == "desc") {
				xspan = x.getElementsByTagName('span');
				yspan = y.getElementsByTagName('span');
				if (xspan.length > 0 && yspan.length > 0) {
					if (Number(xspan[0].innerHTML) < Number(yspan[0].innerHTML)) {
						shouldSwitch = true;
						break;
					}
				} else {
					if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
						shouldSwitch = true;
						break;
					}
				}
			}
		}
		if (shouldSwitch) {
			rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
			switching = true;
			switchcount ++;
		} else {
			if (switchcount == 0 && dir == "asc") {
				dir = "desc";
				switching = true;
			}
		}
	}
	header = theaders[n];
	hspan = header.getElementsByTagName('span')[0];
	if (dir === 'asc') {
		hspan.innerHTML = '↓';
	} else if (dir === 'desc') {
		hspan.innerHTML = '↑';
	}
}