/**
 *  trading volume chart
 */

function draw_tradingChart(categories, data) {
	Highcharts.chart('tradingChart', {
		chart: {
			type: 'column',
			width: 1300,
			spacingRight: 50,
			spacingLeft: 50,
			style: { fontFamily: '"Noto Sans KR", serif' },
			zooming: {
				type: 'xy'
			}
		},
		title: {
			text: null
		},
		xAxis: [{
			categories: categories,
			crosshair: true,
			labels: {
				style: {
					fontSize: '14px',
					fontFamily: '"Noto Sans KR", serif'
				}
			}
		}],
		yAxis: [{
			title: { text: 'Trading Volume' },
			labels: {
				format: '{value:,0f}',
				style: {
					color: Highcharts.getOptions().colors[1],
					fontFamily: '"Noto Sans KR", serif'
				}
			}
		}],
		tooltip: {
			pointFormat: 'Trading Volume: {point.y:,0f}'
		},
		series: [{
			name: 'Trading Volume',
			type: 'column',
			yAxis: 0,
			data: data,
			showInLegend: false,
			fontFamily: '"Noto Sans KR", serif'
		}]
	});
}

function load_tradingVol(tradingVol) {

	if (!tradingVol || tradingVol.length === 0) {
		console.log("No data received for pie chart.");
		return;
	}

	let categories = [];
	let data       = [];

	tradingVol.forEach(item => {
		categories.push(item.date);
		
		let color;
		
		if      (item.trend === 'up') color = '#f05650';
		else if (item.trend === 'fd') color = '#D0D0D0';
		else if (item.trend === 'dn') color = '#4AA8D8';
		
		data.push({
			y : parseInt(item.volume),
			color: color
		});
	});
	draw_tradingChart(categories, data);
}