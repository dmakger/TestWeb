$(function(){
	// $('#new-name-task').val('Название дела');
	// $('#new-description-task').val('Описание дела');

	function disableScroll() {
		// $('html, body').on('mousewheel', function(){
		// 	return false;
		// });
		$('html, body').css('overflow', 'hidden');
	}

	function unDisableScroll() {
		$('html, body').css('overflow', 'auto');
	}

	// При нажатии появляется блок с затемнением
	$('#showShadow').click(function(){
		$('#popup-container').fadeIn(300, disableScroll);
		$('#popup').animate({
			width: '400px',
			height: '700px'
		});
	});

	// При нажатии на затемнение блок пропадает
	$('#popup-container').click(function(event){
		if (event.target == this) {
			$(this).fadeOut(200, unDisableScroll);
			$('#popup').animate({
				width: 0,
				height: 0
			});
		}
	});

	// Cвернуть все записи
	$('#task-list').on('click', '.expand-task', function(){
		$(this).hide();
		$(this).next().show();

		$(this).parents('.main-row').next('.description-task').show(100);
		$(this).parents('.task').animate({
			'min-height': '137px'
		}, 110);
	});

	// Развернуть все записи
	$('#task-list').on('click', '.roll-up-task', function(){
		$(this).hide();
		$(this).prev().show();

		$(this).parents('.main-row').next('.description-task').hide(100);
		$(this).parents('.task').animate({
			'min-height': 0
		}, 100);
	});

	// При необходимости выводит строку "Список пуст..."
	function toggleEmpty() {
		// Если задачи созданны, то если есть запись "Список пуст...", удаляем её
		// Если задач нет, то добавляем запись "Список пуст..."
		if ($('#task-list div').is(':visible')) {
			if ($('#task-list p').is('.empty')) {
				// $('#task-list p.empty').remove();
				$('#task-list p.empty').hide();
			}
		} else {
			// var empty = $('<p className="empty">Список пуст...</p>');
			// $('#task-list').append(empty);
			$('#task-list p.empty').show();
		}
	}

	/**
	 * Целочисленное деление
	 * @param  {int} val делимое. Число которое делим
	 * @param  {int} by  делитель. Число которым делим
	 * @return {int}     Целочисленная разница после деления этих чисел
	 */
	function div(val, by) {
		return (val - val % by) / by;
	}

	/**
	 * Функция для подведения описания под размер блока.
	 * Если текст слишком широкий (больше maxWidth) то переносим текст на следующею строку
	 * @param  {String} description Не отформатированная строка
	 * @return {String}             Строка подходящяя под ширину блока
	 */
	function getFormatedDescription(description) {
		var maxWidth = 50;

		var formattedDescription = "";
		if (description.length > maxWidth-1) {
			var count = div(description.length, maxWidth);
			var border = 0;
			for (var i = 0; i != count; ++i) {
				formattedDescription += description.slice(border, border + maxWidth) + "\n";
				console.log(formattedDescription);
				border += maxWidth;
			}
			formattedDescription += description.slice(border, description.length);

		} else {
			formattedDescription = description;
		}

		return formattedDescription;
	}

	// Добавление задачи
	$('#button-add-task').click(function(){
		// Получаем введенные данные
		var newName = $('#new-name-task').val();
		var newDescription = $('#new-description-task').val();
		// Проверка на заполненность поля
		if (!(newName && newDescription)) {
			return false;
		}

		newDescription = getFormatedDescription(newDescription);

		// Очищаем поля с введенными данными
		$('#new-name-task').val('');
		$('#new-description-task').val('');

		// Добавляем в #task-list элемент с классом task
		var newTask = $('<div class="task"></div>');
		$('#task-list').append(newTask);

		// Добавляем в .task класс main-row и p.description-task
		var mainRow = $('<div class="main-row"></div>')
		var description = $('<p class="description-task"></p>');
		description.text(newDescription);
		$('.task:last').append(mainRow, description);
		// $('.task:last').append(mainRow);

		// Добавлем в .main-row h3.name-task и img.del-task, img.expand-task, img.roll-up-task
		var name = $('<h3 class="name-task"></h3>');
		name.text(newName);
		var img_del = $('<img src="img/cross.svg" alt="Удаление" class="del-task">')
		var img_expand = $('<img src="img/arrow-left.svg" alt="Развернуть" class="expand-task">')
		var img_roll_up = $('<img src="img/arrow-down.svg" alt="Свернуть" class="roll-up-task">')
		$('.task:last .main-row').append(name, img_del, img_expand, img_roll_up);

		toggleEmpty()
	});


	// Удаление задачи
	$('#task-list').on('click', '.del-task', function(){
		$(this).parents('.task').remove();
		toggleEmpty();
	});

	// d364687f1e399c4512045728fa0aa45a
	$.get('http://data.fixer.io/api/latest', {'access_key': 'd364687f1e399c4512045728fa0aa45a'}, function(response){
		$('#plan').text('RUB: ' + response.rates['RUB']);
	});
});