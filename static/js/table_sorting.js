
const order = (new URL(document.location)).searchParams.get("order");

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
    let orderParams = getOrderParams(column);
    let url = new URL(window.location.href);
    if (orderParams != null) {
        url.searchParams.set('order', orderParams);
        return url;
    }
    url.searchParams.delete('order');
    return url;
}



function orderInitialize(){
    let sortable_columns = document.getElementsByClassName('sortable-columns');
    Array.from(sortable_columns).forEach(column => {
        column.href = getFullUrl(column.id);
    });
    let orderParams = order.split(',');
    for (var i = 0; i < orderParams.length; i++) {
    
        let column = orderParams[i];
        let column_id = column.replace('-', '');
        let col_header = document.getElementById(column_id);
        let header_dict = {
            'rest': 'Rest',
            'rating': 'Rating',
            'my_rating': 'My Rating',
            'category': 'Category',
            'distance': 'Distance'
        };
        let order_direction = '↓';
        if (column.startsWith('-')) {
            order_direction = '↑';
        }
        col_header.innerHTML = header_dict[column_id] + `<sup>${i + 1}</sup> ` + `${order_direction}`;
    
    }
    
}

orderInitialize();