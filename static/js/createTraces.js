function createTraces(plotData, plotConfig, ohlc) {
    let plotTraces = []

    // create plot traces
    for (let i = 0; i < plotData.length; i++) {
        const plot = plotData[i];
        console.log('VISIBLE', plotConfig[i]['visible'])
        if (plotConfig[i]['visible']) {
            plotTraces.push({
            x: unpack(ohlc, 'datetime'),
            y: plot,
            xaxis: 'x',
            yaxis: !plotConfig[i]['overlay'] ? 'y2' : 'y',
            type: 'scatter',
            name: plot.name,
            line: {
                color: plot.color,
                width: 1
            }
        })
        }
    }
    return plotTraces
}