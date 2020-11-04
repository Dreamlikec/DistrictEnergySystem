function drawChart(result){
	var myChart = echarts.init(document.getElementById('main'));
	var data = generateData(result);
	var option = {
		toolbox: {
			showTitle: true,
			feature: {
				dataView: {                
				show: true,
					title: '数据表',
				}
			},
			right:'50px',
		},
		tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross'
            },
            backgroundColor: 'rgba(245, 245, 245, 0.8)',
            borderWidth: 1,
            borderColor: '#ccc',
            padding: 10,
            textStyle: {
                color: '#000'
            },
			formatter: function(params) {
　　			var result = params[0].axisValue + "</br>"
　　			params.forEach(function (item) {

					result += item.marker + item.seriesName +":  "+ item.value + '</br>'
　　			})
　　			return result
            }
		},
		//
    	legend: {
       		data: ['热负荷', '冷负荷']
    	},
		grid: {
			bottom: 70,
			left:'50px',
			right:'50px'
		},
		dataZoom: [{
			type: 'inside'
		}, {
			type: 'slider'
		}],
		xAxis: [{
			type: 'category',
			data: data.time,
			axisLine: {
				lineStyle: {
					color: "#999"
				}
			}
		}],
		yAxis: [{
			type: 'value',
			splitNumber: 4,
			splitLine: {
				lineStyle: {
					type: 'dashed',
					color: '#DDD'
				}
			},
			axisLine: {
				show: false,
				lineStyle: {
					color: "#333"
				},
			},
			nameTextStyle: {
				color: "#999"
			},
			splitArea: {
				show: false
			}
		}],
		series: [{
            name: '热负荷',
            type: 'line',
            data: data.hot,
            color: "#F58080",
            lineStyle: {
                normal: {
                    width: 2,
                    color: {
                        type: 'linear',

                        colorStops: [{
                            offset: 0,
                            color: '#FFCAD4' // 0% 处的颜色
                        }, {
                            offset: 0.4,
                            color: '#F58080' // 100% 处的颜色
                        }, {
                            offset: 1,
                            color: '#F58080' // 100% 处的颜色
                        }],
                        globalCoord: false // 缺省为 false
                    },
                    shadowColor: 'rgba(245,128,128, 0.5)',
                    shadowBlur: 5,
                    shadowOffsetY: 2
                }
            },
            itemStyle: {
                normal: {
                    color: '#F58080',
                    borderWidth: 2,
                    /*shadowColor: 'rgba(72,216,191, 0.3)',
                     shadowBlur: 100,*/
                    borderColor: "#F58080"
                }
            },
            smooth: true
        },
        {
            name: '冷负荷',
            type: 'line',
            data: data.cool,
            lineStyle: {
                normal: {
                    width: 2,
                    color: {
                        type: 'linear',

                        colorStops: [{
                                offset: 0,
                                color: '#1994d8' // 0% 处的颜色
                            },
                            {
                                offset: 0.4,
                                color: '#1994d8' // 100% 处的颜色
                            }, {
                                offset: 1,
                                color: '#1994d8' // 100% 处的颜色
                            }
                        ],
                        globalCoord: false // 缺省为 false
                    },
                    shadowColor: 'rgb(25,148,216)',
                    shadowBlur: 5,
                    shadowOffsetY: 2
                }
            },
            itemStyle: {
                normal: {
                    color: '#312cf4',
                    borderWidth: 2,
                    /*shadowColor: 'rgba(72,216,191, 0.3)',
                     shadowBlur: 100,*/
                    borderColor: "#312cf4"
                }
            },
            smooth: true
        },
    ]};
	myChart.setOption(option);
}
function generateData(items) {
	var timeData = [];
	var coolData = [];
	var hotData  = [];
	for (var i = 0; i < items.length; i++) {
            timeData.push(echarts.format.formatTime('yyyy/MM/dd hh', items[i][0]));
            coolData.push(parseFloat(items[i][1]).toFixed(2));
            hotData.push(parseFloat(items[i][2]).toFixed(2));
	}
	return {
		time: timeData,
		cool: coolData,
		hot:  hotData
	};
}