 $('#scBut').on('click', (evt) => {
        evt.preventDefault();
        $.get('http://127.0.0.1:9090/screens/' + $('#screen_in').val() + '/unreserved', (data) => {
            console.log(data);

        })
    });