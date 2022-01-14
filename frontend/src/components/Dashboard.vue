<template>
	<div class="board">
		<h1>{{ msg }}</h1>
		<p>Device Name {{ deviceName }}</p>
		<div class="text-xl text-left text-red-700">Temperature: {{ temperature }}°C</div>
		<div>Humidity: {{ humidity }}%</div>
		<div>Pressure: {{ pressure }}hPa</div>
		<div>TVOC: {{ tvoc }}°C</div>
		<div>CO2: {{ co2 }}ppm</div>
		<div>Uptime: {{ uptime }}</div>
	</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
	name: 'Dashboard',
	props: {
		msg: String
	},
	data: function () {
		return {
			deviceName: 'dummyDevice',
			uptime: '00:02:32',
			temperature: 12.3,
			humidtiy: 34,
			pressure: 1200,
			co2: 800,
			tvoc: 100
		}
	}
})
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.board {
	margin: 40px 0 0;
	border: 4px solid #4242b9;
	border-radius: 6px;
}

.temperature {
	font-size: 2rem;
}
</style>
