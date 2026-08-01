document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('order-form');
    var clientSelect = document.getElementById('id_client');
    var carSelect = document.getElementById('id_car');
    if (!form || !clientSelect || !carSelect || clientSelect.disabled) {
        return;
    }
    clientSelect.addEventListener('change', function () {
        carSelect.length = 0;
        if (!clientSelect.value) {
            return;
        }
        fetch(form.dataset.carsUrl.replace('0', clientSelect.value))
            .then(function (response) { return response.json(); })
            .then(function (data) {
                data.car_choices.forEach(function (choice) {
                    carSelect.add(new Option(choice[1], choice[0]));
                });
            });
    });
});
