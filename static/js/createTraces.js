function createTraces(plotData, plotConfig, ohlc) {
    let plotTraces = []

    // create plot traces
    for (let i = 0; i < plotData.length; i++) {
        const plot = plotData[i];
        let vis = true;
        // plotConfig[i]['visible']
        if (plotConfig[i]['name'] === 'atr_target' || plotConfig[i]['name'] === 'rma') {
            vis = false
        }
        console.log(plotConfig[i]['name'])
        console.log('VISIBLE is', vis)
        if (vis) {
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