// create chart
async function createChart(targetDiv, dataset, plots, plotConfig) {

    const ohlc = await getOhlcv(dataset)
    // create OHLC trace

    const ohlcTrace = {
        x: unpack(ohlc, 'datetime'),
        close: unpack(ohlc, 'close'),
        high: unpack(ohlc, 'high'),
        low: unpack(ohlc, 'low'),
        open: unpack(ohlc, 'open'),

        // cutomise colors
        increasing: {line: {color: 'green'}},
        decreasing: {line: {color: 'red'}},

        type: 'ohlc',
    };
    // create plot traces
    const plotTraces = createTraces(plots, plotConfig, ohlc)

    let data = [ohlcTrace];
    data = data.concat(plotTraces);

    const layout = {
        grid: {rows: 2, columns: 1},
        subplots: [['xy'], ['xy2']],
        dragmode: 'zoom',
        margin: {
            r: 10,
            t: 25,
            b: 40,
            l: 60
        },
        showlegend: false,
        xaxis: {
            autorange: true,
            title: 'Date',
            type: 'date',
            rangeslider: {
                visible: false
            }
        },
        yaxis: {
            autorange: true,
            type: 'linear'
        }
    };

    Plotly.newPlot(targetDiv, data, layout);
}