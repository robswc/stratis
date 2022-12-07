// create chart
async function createChart(targetDiv, dataset, positions, plots, plotConfig) {

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

    let tradeEntries = []
    let tradeExits = []
    for (let i = 0; i < ohlc.length; i++) {
        tradeEntries.push(null)
        tradeExits.push(null)
    }

    for (let i = 0; i < positions.length; i++) {
        tradeEntries[positions[i]['data_index']] = positions[i]['entry_price']
        tradeExits[positions[i]['filled_data_index']] = positions[i]['exit_price']
    }

    // create trade traces
    const tradeEntriesTrace = {
        x: unpack(ohlc, 'datetime'),
        y: tradeEntries,
        type: 'scatter',
        name: 'trades',
        mode: 'markers',
        marker: {
            color: 'rgb(17, 157, 255)',
            symbol: 'triangle-up',
            size: 10,
            line: {
                color: 'rgb(0,0,0)',
                width: 1
            }
        },
    }

        // create trade traces
    const tradeExitsTrace = {
        x: unpack(ohlc, 'datetime'),
        y: tradeExits,
        type: 'scatter',
        name: 'trades',
        mode: 'markers',
        marker: {
            color: 'rgb(231,17,255)',
            symbol: 'square',
            size: 10,
            line: {
                color: 'rgb(0,0,0)',
                width: 1
            }
        },
    }

    let data = [ohlcTrace, tradeEntriesTrace, tradeExitsTrace];
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
        showlegend: true,
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