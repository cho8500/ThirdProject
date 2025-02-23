/**
 *	stack chart js
 */
// Data retrieved from:
// - https://en.as.com/soccer/which-teams-have-won-the-premier-league-the-most-times-n/
// - https://www.statista.com/statistics/383679/fa-cup-wins-by-team/
// - https://www.uefa.com/uefachampionsleague/history/winners/

function load_stackData(query, day) {
	
	fetch(`data.jsp?query=${query}&day=${day}`)
		.then(response => response.json())
		.then(data => {
			const formatted_stackData = formatStackData(data.stackData);
			draw_stackChart(formatted_stackData);
		});
}

function formatStackData(rawData) {
	
	if (!rawData || rawData.length === 0) {
		console.log("No data received for stack chart.");
		return { categories: [], positive: [0], neutral: [0], negative: [0] };
	}
	
	let categories = [];
	let positive   = [];
	let neutral    = [];
	let negative   = [];
	
	rawData.forEach(item => {
		
		if (!categories.includes(item.date)) categories.push(item.date);
		
		if      (item.sent_type === 'positive') positive.push(Number(item.count));
		else if (item.sent_type === 'negative') negative.push(Number(item.count));
		else if (item.sent_type === 'neutral')  neutral.push(Number(item.count));
	});
	return { categories, positive, neutral, negative };
}

function draw_stackChart(data) {
	
	Highcharts.chart('stackChart', {
		chart: {
			type: 'column',
			width: 1200,
			spacingRight: 50,
			spacingLeft: 50
		},
		title: {
			text: '',
			align: 'left'
		},
		xAxis: {
			categories: data.categories,
			labels: {
				style: {
					fontSize: '14px'
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
				pointWidth: 3,
				pointPadding: 0.1,
				groupPadding: 0.2
			}
		},
		series: [{
			name: 'positive',
			data: data.positive,
			color: '#ff0000'
		}, {
			name: 'neutral',
			data: data.neutral,
			color: '#808080'
		}, {
			name: 'negative',
			data: data.negative,
			color: '#0000ff'
		}]
	})
}