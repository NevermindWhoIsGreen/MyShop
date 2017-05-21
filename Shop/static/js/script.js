(function(){

    function init() {

        // парсим url на предмет переданных параметров фильтров
        var url = window.location.pathname;
        // функция разбора get-параметров, http://stackoverflow.com/questions/979975/how-to-get-the-value-from-the-url-parameter
        function getQueryParams(qs) {
            qs = qs.split("+").join(" ");
            var params = {}, tokens,
                re = /[?&]?([^=]+)=([^&]*)/g;
            while (tokens = re.exec(qs)) {
                params[decodeURIComponent(tokens[1]).slice(7)]
                    = decodeURIComponent(tokens[2]);
            }
            return params;
        }
        // объект с get-параметрами в виде свойств
        var getParams = getQueryParams(document.location.search);
        // в каждый инпут с name, равным имени свойства, кладём значения, которые дальше обрабатываются скриптом
        for (var i in getParams) {
            var input = $('input[name="' + i + '"]'),
                params = getParams[i].replace(/\|/g,',');
            $(input).val(params);
        }


        var filter = $('.geke-filter');

        $(filter).append('<div class="geke-filter-reset"><a href="" title="Сбросить" class="geke-filter-reset">Сбросить все настройки</a></div>').find('.geke-filter-item').each(function(){
            initFilterItem.call(this);
        });
        $(filter).each(function(){
            initFilter.call(this);
        });


        // вызываем каждый фильтр
        function initFilter() {
            var self = this;
            filterBlock(self);
        }

        // вызываем каждый из экземпляров фильтров
        function initFilterItem() {
            var self = this, // тут запоминаем jQuery-DOM-объект
                data = $(this).attr('data');  // и его параметры
            data = $.parseJSON(data);
            view(self, data);
            handler(self, data);
        }

    }


    // блок фильтра
    function filterBlock(block) {
        // сбрасываем все настройки
        $(block).find('.geke-filter-reset').click(function(event){
            event.preventDefault();
            //window.location.href = window.location.pathname;
            $(block).find('.cancel-button').click();
        })
        // делаем get-запрос с параметрами
        $(block).find('.geke-filter-item_submit_button').click(function(event){
            event.preventDefault();
            var url = '?';
            $(block).find('.geke-values').each(function(){
                if ($(this).val() !== '') {
                    values = $(this).val().split(',');
                    url = url + 'filter_' + $(this).attr('name') + '=';
                    for (var i=0; i < values.length; i++) {
                        var theVal = values[i].replace(/\s/g,'_');
                        i === 0 ? (url = url + theVal) : url = url + '|' + theVal;
                    }
                    url = url + '&'
                }
            })
            if (url.slice(-1) === '&') url = url.slice(0,-1);
            window.location.href = window.location.pathname + url;
        })
    }


    // отрисовка элементов экземпляра фильтра
    function view(element, data) {
        // смотрим, что было записано в форме в прошлые сессии или пришло с get-параметрами
        var restoreData = $(element).find('.geke-values').val().split(',');

        if (data.type !== 'slider') restoreList();

        function restoreList() {
            // словарь id элементов списка
            var listGlossary = [];
            $(element).find('li').each(function(){
                listGlossary.push($(this).attr('data-id'));
            })
            // находим совпадение, отмечаем элемент, если оно есть
            for (var i=0; i< restoreData.length; i++) {
                var n = listGlossary.indexOf(restoreData[i]) + 1;
                if (n > -1) $(element).find('li:nth-child(' + n + ')').addClass('active');
            }
        }


        // присваиваем элементу фильтра класс, соответствующий типу
        $(element).addClass('' + data.type + '');

        // для элементов типа list делаем имитацию чекбоксов
        if (data.type === 'list') {
            $(element).find('li').each(function(){
                $(this).html('<div class="geke-filter-checkbox"><span></span></div><div class="geke-fliter-list-text">' + $(this).text() + '</div>')
            })
        }

        // слайдер
        if (data.type === 'slider') {
            // случайный id для слайдера, чтобы не мешать с другими экземплярами слайдеров, требуется для корректной работы jQuery UI Slider
            var slider_id = Math.round(Math.random()*(9999999)) + 1;
            $(element).find('span').remove();
            $(element).append('<div id="slider_' + slider_id + '" class="slider_id"></div><div class="slider_values"><span id="slider_values_left_' + slider_id + '" class="geke-filter-slider-value-left"></span><span id="slider_values_right_' + slider_id + '" class="geke-filter-slider-value-right"></span></div>');
        }

        // рисуем кнопку "Применить"
        $(element).append('<div class="geke-filter-item_submit"><a href="" title="Отфильтровать" class="geke-filter-item_submit_button">Применить</a></div>');
        // рисуем крестик с отменой
        $(element).prepend('<a href="" title="Сбросить фильтр" class="cancel-button"></a>');
        // если есть предыдущие значения, показываем
        if ($(element).find('.geke-values').val().length > 0) $(element).find('.cancel-button').css('display', 'block');

    }


    // взаимодействие с фильтрами
    function handler(element, data) {

        var input = $(element).find('.geke-values'),
            inputVal = [];    // сюда записываем выбранные значения, ключая из прошлых сессий

        if (data.type == 'slider') {
            handlerSlider();
        } else {
            handlerList();
        }


        // для списка и календаря
        function handlerList() {
            if ($(input).val().length > 0) {
                inputVal = $(input).val().split(',')
            }
            $(element).find('li').click(function(){
                var x = $(this).attr('data-id');
                if (!$(this).hasClass('active')) {
                    inputVal.push(x);
                } else {
                    inputVal.splice(inputVal.indexOf(x), 1)
                }
                $(this).toggleClass('active');
                $(input).val(inputVal.join(','));
                if (inputVal.length > 0) {
                    $(element).find('.cancel-button').show();
                } else {
                    $(element).find('.cancel-button').hide();
                }
            });

            // нажимаем на крестик
            $(element).find('.cancel-button').click(function(event){
                event.preventDefault();
                $(element).find('li').each(function(){
                    $(this).removeClass('active');
                })
                $(input).val('');
                inputVal = [];
                $(this).hide();
            })
        }

        // для слайдера
        function handlerSlider() {
            var slider_id = $(element).find('.slider_id').attr('id').slice(7),
                thisSlider = $('#slider_' + slider_id);

            if ($(input).val().length > 0) {
                inputVal = $(input).val().split(',')
            }

            var val1 = $('#slider_values_left_' + slider_id),
                val2 = $('#slider_values_right_' + slider_id),
                slMin = parseInt(data.min),
                slMax = parseInt(data.max);

            $(thisSlider).slider({
                range : true,
                values : [slMin, slMax],
                min : slMin,
                max : slMax,
                animate : true,
                range : true,
                slide : function(event, ui) {
                    $(val1).text(ui.values[0] + ' руб.');
                    $(val2).text(ui.values[1] + ' руб.');
                    // если установили изначальные значения, тогда оставляем инпут пустым
                    if (ui.values[0] === slMin && ui.values[1] === slMax) {
                        $(input).val('');
                        $(element).find('.cancel-button').hide();
                    } else {
                        $(input).val(ui.values[0] + ',' + ui.values[1]);
                        $(element).find('.cancel-button').show();
                    }
                }
            });

            // восстанавливаем данные слайдера (если есть) после инициализации
            (function restoreSlider() {
                if (inputVal.length > 1) {
                    $(thisSlider).slider({
                        values : [inputVal[0], inputVal[1]]
                    });
                    $(val1).text(inputVal[0] + ' руб.');
                    $(val2).text(inputVal[1] + ' руб.');
                } else {
                    $(val1).text(slMin + ' руб.');
                    $(val2).text(slMax + ' руб.');
                }
            })();

            // нажимаем на крестик
            $(element).find('.cancel-button').click(function(event){
                event.preventDefault();
                $(thisSlider).slider({
                    values : [slMin, slMax]
                });
                $(val1).text(slMin + ' руб.');
                $(val2).text(slMax + ' руб.');
                $(input).val('');
                inputVal = [];
                $(this).hide();
            })
        }
    }

    window.onload = function() {init();}

})();

//ajax поиск на сайте
$(function(){
    $('#search').on('keyup', function(){
       var _this = $(this),
               found = $('#main-search-found');
        if (_this.val().length >= 3) {
            $.ajax({
                type: "POST",
                url: "/search/",
                data: {
                    'search_query': $('#search').val(),
                    'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                },
                dataType: 'html',
                success: function(data){
                    found.html(data).slideDown();
                    console.log(data);
                }
            });
        } else {
            found.slideUp();
        }
    }).on('focusout', function(){
        $('#main-search-found').slideUp();
    }).on('focus', function(){
        if ($(this).val().length >= 3) {
            $('#main-search-found').slideDown();
        }
    });
});