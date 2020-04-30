function get_u1_data() {
	$.ajax({
		url:"/u1",
		success: function(data) {
			u1_option.series[0].data[0].value = data.pos
			u1_option.series[0].data[1].value = data.neg
			u1_option.series[0].data[2].value = data.neu
			u1Chart.setOption(u1_option)
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}
get_u1_data()
setInterval(get_u1_data, 1000*10)

function get_u2_data() {
	$.ajax({
		url:"/u2",
		success: function(data) {
			u2_option.series[0].data[0].value = data.pos
			u2_option.series[0].data[1].value = data.neg
			u2_option.series[0].data[2].value = data.neu
			u2Chart.setOption(u2_option)
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}
get_u2_data()
setInterval(get_u2_data, 1000*10)

function get_u3_data() {
	$.ajax({
		url:"/u3",
		success: function(data) {
			u3_option.series[0].data[0].value = data.pos
			u3_option.series[0].data[1].value = data.neg
			u3_option.series[0].data[2].value = data.neu
			u3Chart.setOption(u3_option)
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}
get_u3_data()
setInterval(get_u3_data, 1000*10)

function get_d1_data() {
	$.ajax({
		url:"/d1",
		success: function(data) {
			d1_option.yAxis.data = data.xm
			d1_option.series[0].data = data.sl
			d1Chart.setOption(d1_option)
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}
get_d1_data()
setInterval(get_d1_data, 1000*10)

function get_d2_data() {
	$.ajax({
		url:"/d2",
		success: function(data) {
			d2_option.yAxis.data = data.xm
			d2_option.series[0].data = data.sl
			d2Chart.setOption(d2_option)
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}
get_d2_data()
setInterval(get_d2_data, 1000*10)