/**
 *	pie chart js
 */

function draw_pieChart(data) {
	Highcharts.chart('pieChart', {
		chart: {
			type: 'pie',
			width: 800,
			spacingRight: 50,
			spacingLeft: 50,
			style: { fontFamily: '"Noto Sans KR", serif' }
		},
		title: {
			text: null
		},
		tooltip: {
			valueSuffix: '%',
			style: { fontFamily: '"Noto Sans KR", serif' }
		},
		plotOptions: {
			series: {
				allowPointSelect: true,
				cursor: 'pointer',
				dataLabels: [{
					enabled: true,
					distance: 20,
					style: {
						fontSize: '16px',
						fontWeight: '300',
						fontFamily: '"Noto Sans KR", serif' }
				}, {
					enabled: true,
					distance: -50,
					format: '{point.percentage:.2f}%',
					style: {
						fontSize: '1.2em',
						textOutline: 'none',
						opacity: 0.7,
						fontFamily: '"Noto Sans KR", serif'
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
				{ name: 'Positive', y: data.positive, color: '#f05650' },
				{ name: 'Neutral',  y: data.neutral,  color: '#D0D0D0' },
				{ name: 'Negative', y: data.negative, color: '#4AA8D8' }
			]
		}]
	});
}

function load_pieData(pieData) {

	if (!pieData || pieData.length === 0) {
		console.log("No data received for pie chart.");
		draw_pieChart({ positive: 0, neutral: 0, negative: 0 });
		return;
	}

	let positive = 0;
	let neutral  = 0;
	let negative = 0;

	pieData.forEach(item => {
		if      (item.sent_type === 'positive') positive += Number(item.count);
		else if (item.sent_type === 'negative') negative += Number(item.count);
		else if (item.sent_type === 'neutral')  neutral  += Number(item.count);
	});
	draw_pieChart({ positive, neutral, negative });
}