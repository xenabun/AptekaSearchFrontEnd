document.addEventListener('DOMContentLoaded', function() {
	const min_priceSlider = document.getElementById("min_price");
	const min_priceValue = document.getElementById("min_priceValue");
	const max_priceSlider = document.getElementById("max_price");
	const max_priceValue = document.getElementById("max_priceValue");
	min_priceSlider.oninput = function(e) {
		min_priceValue.value = e.target.value;
		if (parseInt(e.target.value) > parseInt(max_priceValue.value)) {
			max_priceSlider.value = e.target.value;
			max_priceValue.value = e.target.value;
		}
	};
	max_priceSlider.oninput = function(e) {
		max_priceValue.value = e.target.value;
		if (parseInt(e.target.value) < parseInt(min_priceValue.value)) {
			min_priceSlider.value = e.target.value;
			min_priceValue.value = e.target.value;
		}
	};
	min_priceValue.onchange = function() {
		min_priceSlider.value = Math.min(Math.max(parseInt(min_priceValue.value), min_priceSlider.min), min_priceSlider.max) || min_priceSlider.min;
		min_priceValue.value = Math.min(Math.max(parseInt(min_priceValue.value), min_priceSlider.min), min_priceSlider.max) || min_priceSlider.min;
	};
	max_priceValue.onchange = function() {
		max_priceSlider.value = Math.min(Math.max(parseInt(max_priceValue.value), max_priceSlider.min), max_priceSlider.max) || max_priceSlider.max;
		max_priceValue.value = Math.min(Math.max(parseInt(max_priceValue.value), max_priceSlider.min), max_priceSlider.max) || max_priceSlider.max;
	};
});


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