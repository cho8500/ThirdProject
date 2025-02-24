/**
 *	pie chart js
 */

function draw_pieChart(data) {
	Highcharts.chart('pieChart', {
		chart: {
			type: 'pie'
		},
		title: {
			text: ''
		},
		tooltip: {
			valueSuffix: '%'
		},
		subtitle: {
			text:
				'Source:<a href="https://www.mdpi.com/2072-6643/11/3/684/htm" target="_default">MDPI</a>'
		},
		plotOptions: {
			series: {
				allowPointSelect: true,
				cursor: 'pointer',
				dataLabels: [{
					enabled: true,
					distance: 20
				}, {
					enabled: true,
					distance: -40,
					format: '{point.percentage:.1f}%',
					style: {
						fontSize: '1.2em',
						textOutline: 'none',
						opacity: 0.7
					},
					filter: {
						operator: '>',
						property: 'percentage',
						value: 10
					}
				}]
			}
		},
		series: [{
			name: 'Sentiment',
			data: [
				{ name: 'Positive', y: data.positive.reduce((a, b) => a + b, 0), color: '#ff0000' },
				{ name: 'Neutral',  y: data.neutral.reduce((a, b) => a + b, 0), color: '#808080' },
				{ name: 'Negative', y: data.negative.reduce((a, b) => a + b, 0), color: '#0000ff' }
			]
		}]
	});
}

function load_pieData(pieData) {

	if (!pieData || pieData.length === 0) {
		console.log("No data received for pie chart.");
		return { categories: [], positive: [0], neutral: [0], negative: [0] };
	}

	let positive = 0;
	let neutral  = 0;
	let negative = 0;

	rawData.forEach(item => {

		if      (item.sent_type === 'positive') positive += Number(item.count);
		else if (item.sent_type === 'negative') negative += Number(item.count);
		else if (item.sent_type === 'neutral')  neutral  += Number(item.count);
	});
	
	draw_pieChart({ categories, positive, neutral, negative });
}