/**
 *	stack chart js
 */

function draw_stackChart(data) {
	Highcharts.chart('stackChart', {
		chart: {
			type: 'column',
			width: 1200,
			spacingRight: 50,
			spacingLeft: 50,
			style: { fontFamily: '"Noto Sans KR", serif' }
		},
		title: {
			text: null
		},
		xAxis: {
			categories: data.categories,
			labels: {
				style: {
					fontSize: '14px',
					fontFamily: '"Noto Sans KR", serif'
				}
			}
		},
		yAxis: {
			min: 0,
			title: { text: 'Num of Comments' },
			stackLabels: { enabled: false }
		},
		legend: {
			align: 'right',
			verticalAlign: 'top',
			floating: true,
			backgroundColor:
				Highcharts.defaultOptions.legend.backgroundColor || 'white',
			borderColor: '#CCC',
			borderWidth: 1,
			shadow: false
		},
		tooltip: {
			pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
		},
		plotOptions: {
			column: {
				stacking: 'normal',
				dataLabels: { enabled: false },
				pointWidth: 4,
				pointPadding: 0.1,
				groupPadding: 0.2
			}
		},
		series: [{
			name: 'positive',
			data: data.positive,
			color: '#f05650',
			fontFamily: '"Noto Sans KR", serif'
		}, {
			name: 'neutral',
			data: data.neutral,
			color: '#D0D0D0',
			fontFamily: '"Noto Sans KR", serif'
		}, {
			name: 'negative',
			data: data.negative,
			color: '#4AA8D8',
			fontFamily: '"Noto Sans KR", serif'
		}]
	})
}

function load_stackData(stackData) {
	
	if(!stackData || stackData.length === 0) {
		console.log("No data received for stack chart");
		return { categories: [], positive: [0], neutral: [0], negative: [0] };
	}
	
	let categories = [];
	let positive   = [];
	let neutral    = [];
	let negative   = [];
	
	stackData.forEach(item => {
		
		if (!categories.includes(item.date)) categories.push(item.date);
		
		if      (item.sent_type === 'positive') positive.push(Number(item.count));
		else if (item.sent_type === 'negative') negative.push(Number(item.count));
		else if (item.sent_type === 'neutral')  neutral.push(Number(item.count));
	});
	draw_stackChart({ categories, positive, neutral, negative });
}
