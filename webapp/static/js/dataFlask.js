function myFunction(x) {
        $.getJSON($SCRIPT_ROOT + '/check_selected', {
        post: x
        }, function(data) {
            var response = data.result;
            console.log(response);
            }
        });
}