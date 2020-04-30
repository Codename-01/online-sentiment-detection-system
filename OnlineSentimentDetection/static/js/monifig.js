var u1Chart = echarts.init(document.getElementById('u1'));

// 指定图表的配置项和数据
var u1_option = {
    tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    series: [

        {
            name: '微信',
            type: 'pie',
            radius: ['30%', '45%'],
            label: {
                formatter: '{b|{b}}\n  {per|{d}%} ',
                backgroundColor: '#eee',
                borderColor: '#aaa',
                borderWidth: 1,
                borderRadius: 4,
                // shadowBlur:3,
                // shadowOffsetX: 2,
                // shadowOffsetY: 2,
                // shadowColor: '#999',
                // padding: [0, 7],
                rich: {
                    a: {
                        color: '#999',
                        lineHeight: 22,
                        align: 'center'
                    },
                    // abg: {
                    //     backgroundColor: '#333',
                    //     width: '100%',
                    //     align: 'right',
                    //     height: 22,
                    //     borderRadius: [4, 4, 0, 0]
                    // },
                    hr: {
                        borderColor: '#aaa',
                        width: '80%',
                        borderWidth: 0.5,
                        height: 0
                    },
                    b: {
                        fontSize: 12,
                        lineHeight: 16,
                        align: 'center'
                    },
                    per: {
                        color: '#eee',
                        backgroundColor: '#334455',
                        padding: [2, 4],
                        borderRadius: 2,
                        align: 'center'
                    }
                }
            },
            data: [
                {value: 335, name: '正面'},
                {value: 310, name: '负面'},
                {value: 534, name: '中性'}
            ]
        }
    ]
};

// 使用刚指定的配置项和数据显示图表。
u1Chart.setOption(u1_option);


var u2Chart = echarts.init(document.getElementById('u2'));

// 指定图表的配置项和数据
var u2_option = {
    tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    series: [

        {
            name: '微博',
            type: 'pie',
            radius: ['30%', '45%'],
            label: {
                formatter: '{b|{b}}\n  {per|{d}%} ',
                backgroundColor: '#eee',
                borderColor: '#aaa',
                borderWidth: 1,
                borderRadius: 4,
                // shadowBlur:3,
                // shadowOffsetX: 2,
                // shadowOffsetY: 2,
                // shadowColor: '#999',
                // padding: [0, 7],
                rich: {
                    a: {
                        color: '#999',
                        lineHeight: 22,
                        align: 'center'
                    },
                    // abg: {
                    //     backgroundColor: '#333',
                    //     width: '100%',
                    //     align: 'right',
                    //     height: 22,
                    //     borderRadius: [4, 4, 0, 0]
                    // },
                    hr: {
                        borderColor: '#aaa',
                        width: '80%',
                        borderWidth: 0.5,
                        height: 0
                    },
                    b: {
                        fontSize: 12,
                        lineHeight: 16,
                        align: 'center'
                    },
                    per: {
                        color: '#eee',
                        backgroundColor: '#334455',
                        padding: [2, 4],
                        borderRadius: 2,
                        align: 'center'
                    }
                }
            },
            data: [
                {value: 335, name: '正面'},
                {value: 310, name: '负面'},
                {value: 234, name: '中性'}
            ]
        }
    ]
};

// 使用刚指定的配置项和数据显示图表。
u2Chart.setOption(u2_option);


var u3Chart = echarts.init(document.getElementById('u3'));

// 指定图表的配置项和数据
var u3_option = {
    tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    series: [

        {
            name: '美团',
            type: 'pie',
            radius: ['30%', '45%'],
            label: {
                formatter: '{b|{b}}\n  {per|{d}%} ',
                backgroundColor: '#eee',
                borderColor: '#aaa',
                borderWidth: 1,
                borderRadius: 4,
                // shadowBlur:3,
                // shadowOffsetX: 2,
                // shadowOffsetY: 2,
                // shadowColor: '#999',
                // padding: [0, 7],
                rich: {
                    a: {
                        color: '#999',
                        lineHeight: 22,
                        align: 'center'
                    },
                    // abg: {
                    //     backgroundColor: '#333',
                    //     width: '100%',
                    //     align: 'right',
                    //     height: 22,
                    //     borderRadius: [4, 4, 0, 0]
                    // },
                    hr: {
                        borderColor: '#aaa',
                        width: '80%',
                        borderWidth: 0.5,
                        height: 0
                    },
                    b: {
                        fontSize: 12,
                        lineHeight: 16,
                        align: 'center'
                    },
                    per: {
                        color: '#eee',
                        backgroundColor: '#334455',
                        padding: [2, 4],
                        borderRadius: 2,
                        align: 'center'
                    }
                }
            },
            data: [
                {value: 635, name: '正面'},
                {value: 310, name: '负面'},
                {value: 234, name: '中性'}
            ]
        }
    ]
};

// 使用刚指定的配置项和数据显示图表。
u3Chart.setOption(u3_option);


var d1Chart = echarts.init(document.getElementById('d1'));

// 指定图表的配置项和数据
var d1_option = {
    title: {
        text: '资讯平台top5',
		left: 'center',
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },

    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: {
        type: 'value',
        boundaryGap: [0, 0.01]
    },
    yAxis: {
        type: 'category',
        data: ['新闻手机端', '新闻网页端', '微信', '微博', '纸媒']
    },
    series: [
        {
            name: '2020年',
            type: 'bar',
            label: {
                show: true,
                position: 'insideRight'
            },
            data: [182030, 128489, 95034, 84970, 61744],
			itemStyle: {
			    normal: {
			　　　　　//这里是重点
			        color: function(params) {
			            //注意，如果颜色太少的话，后面颜色不会自动循环，最好多定义几个颜色
			            var colorList = ['#c23531','#2f4554', '#61a0a8', '#d48265', '#91c7ae', '#749f83', '#ca8622'];
			            return colorList[params.dataIndex]
			        }
			    }
			}
        }
    ]
};

// 使用刚指定的配置项和数据显示图表。
d1Chart.setOption(d1_option);



var d2Chart = echarts.init(document.getElementById('d2'));

// 指定图表的配置项和数据
var d2_option = {
    title: {
        text: '口碑平台top5',
		left: 'center',
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },

    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: {
        type: 'value',
        boundaryGap: [0, 0.01]
    },
    yAxis: {
        type: 'category',
        data: ['微博', '美团', '贴吧', '股吧', '论坛']
    },
    series: [
        {
            name: '2020年',
            type: 'bar',
            label: {
                show: true,
                position: 'insideRight'
            },
            data: [18203, 15848, 9503, 6497, 5174],
			itemStyle: {
			    normal: {
			　　　　　//这里是重点
			        color: function(params) {
			            //注意，如果颜色太少的话，后面颜色不会自动循环，最好多定义几个颜色
			            var colorList = ['#c23531','#2f4554', '#61a0a8', '#d48265', '#91c7ae', '#749f83', '#ca8622'];
			            return colorList[params.dataIndex]
			        }
			    }
			}
        }
    ]
};

// 使用刚指定的配置项和数据显示图表。
d2Chart.setOption(d2_option);	