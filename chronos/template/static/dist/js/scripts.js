$(document).ready(function () {
    $(":input").inputmask();
    $(".summernote").summernote({
        toolbar: [
            ['style', ['bold', 'italic', 'underline', 'clear']],
            ['fontsize', ['fontsize']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
        ],
        height: 150
    });
    $('.formset_row').formset({
        addText: 'Novo Checklist',
        deleteText: 'Excluir',
        prefix: 'checklists'
    });
    var eventos = document.getElementById('eventos').value;
    var events_data = JSON.parse(eventos);
    var Calendar = FullCalendar.Calendar;
    var calendarEl = document.getElementById('calendar');
    var calendar = new Calendar(calendarEl, {
        locale: 'pt-br',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay',
        },
        buttonText: {
            today: 'Hoje',
            month: 'Mês',
            week: 'Semana',
            day: 'Dia',
            list: 'Lista'
        },
        themeSystem: 'bootstrap',
        editable: false,
        droppable: false,
        events: events_data
    })
    calendar.render();
});