// fetch data
async function getOhlcv(dataset) {
    // make ajax request
    console.log('fetching data...', dataset)
    const response = await fetch('/api/v1/data?name=' + dataset);
    // parse json
    const data = await response.json();
    // return data
    return data.map(d => {
        return {
            datetime: new Date(d.datetime),
            open: d.open,
            high: d.high,
            low: d.low,
            close: d.close,
            volume: d.volume
        }
    });

}

function unpack(rows, key) {
    return rows.map(function (row) {
        return row[key];
    });
}