$('#scBut').on('click', (evt) => {
    evt.preventDefault();
    $.getJSON('http://127.0.0.1:9090/screens/' + $('#screen_in').val() + '/unreserved', (data) => {
        let seats = data["seats"];
        for (let sc in data["seats"]) {
            let row = seats[sc];
            for (let key in row) {
                console.log(row[key]);
                $('#seats').append(
                    ' <form>\n' +
                    '                <h3>{}</h3>\n'.format(key) +
                    '                <select multiple class="form-control" id="sel_{}">\n'.format(key) +
                                        options(row,key)+
                    '                </select>\n' +
                    '            </form>'
                )

            }
        }
    })
});

function options(data, key) {
    let str = '';
    for(let x in data[key]){
        str+="<option>{}</option>".format(x)
    }
    return str;
}

String.prototype.format = function () {
    var i = 0, args = arguments;
    return this.replace(/{}/g, function () {
        return typeof args[i] !== 'undefined' ? args[i++] : '';
    });
};