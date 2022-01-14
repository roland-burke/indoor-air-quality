<template>
<div class="flex justify-center">
	<fieldset class="m-10 p-4 w-3/6 max-w-2xl border-4 rounded-xl border-blue-400">
		<legend class="text-2xl px-2 text-left">Sensor Overview</legend>
		<div class="divide-y divide-solid">
			<div>
				<h1>{{ msg }}</h1>
				<p>Device Name {{ deviceName }}</p>
			</div>
			<div>
				<div class="flex items-center">
					<div class="text-xl font-bold">Temperature:</div>
					<div>{{ temperature }}°C</div>
				</div>
				<div>Humidity: {{ humidity }}%</div>
				<div>Pressure: {{ pressure }}hPa</div>
				<div>TVOC: {{ tvoc }}°C</div>
				<div>CO2: {{ co2 }}ppm</div>
				<div>Uptime: {{ uptime }}</div>
			</div>
		</div>
	</fieldset>
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
</style>
