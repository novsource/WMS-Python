var tds = document.querySelectorAll('td');

for (var i = 0; i < tds.length; i++) {
	tds[i].addEventListener('click', function func() {
		var input = document.createElement('input');
		input.value = this.innerHTML;
		this.innerHTML = '';
		this.appendChild(input);

		var td = this;
		input.addEventListener('blur', function() {
			td.innerHTML = this.value;
			td.addEventListener('click', func);
		});

		this.removeEventListener('click', func);
	});
}