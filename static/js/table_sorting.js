
const params = (new URL(document.location)).searchParams;
const order = params.get("order");
function getOrderParams(column) {
    if (order != null & order != "") {

        var orderList = order.split(',');
        // if column is in list
        if (orderList.includes(column)) {


            // if column exists but is pos, change to neg
            orderList[orderList.indexOf(column)] = "-".concat(column);
            return orderList.join(',');
        }
        else if (orderList.includes("-".concat(column))) {
            // if column is negative already, remove column
            orderList = orderList.filter(e => e !== "-".concat(column));
            if (orderList.length > 0) {
                return orderList.join(',');
            }
            return null;

        }

        else {
            orderList.push(column);

        }

    }

    // if order query param is empty, just order by column
    else {
        return column;
    }

    return orderList.join(',');


}



function getFullUrl(column) {
    const orderParams = getOrderParams(column);
    if (orderParams != null) {
        return "//127.0.0.1:8000/my-rests/1?order=".concat(getOrderParams(column))
    }
    return "//127.0.0.1:8000/my-rests/1"
}

const sortable_columns = document.getElementsByClassName('sortable-columns');
Array.from(sortable_columns).forEach(column => {
    column.href = getFullUrl(column.id);
});

var orderParams = order.split(',');
for (var i = 0; i < orderParams.length; i++) {

    column = orderParams[i];
    let column_id = column.replace('-', '');
    col_header = document.getElementById(column_id);
    var header_dict = {
        'rest': 'Rest',
        'rating': 'Rating',
        'my_rating': 'My Rating',
        'category': 'Category'
    };
    var order_direction = '↓';
    if (column.startsWith('-')) {
        order_direction = '↑';
    }
    col_header.innerHTML = header_dict[column_id] + `<sup>${i + 1}</sup> ` + `${order_direction}`;

}
