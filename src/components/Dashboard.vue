<template>
	<div class="flex justify-center">
		<fieldset
			class="mx-5 mb-5 p-4 w-5/6 max-w-2xl border-4 rounded-xl border-blue-400"
		>
			<legend class="text-2xl px-2 text-left">Sensor Overview</legend>
			<div class="divide-y divide-solid">
				<div>
					<h1>{{ msg }}</h1>
					<p>Device Name: {{ this.responseData.hostname }}</p>
				</div>
				<div>
					<div class="flex items-center">
						<div class="text-xl font-bold">Temperature:</div>
						<div>{{ this.responseData.temperature }}°C</div>
					</div>
					<div>Humidity: {{ this.responseData.huimdity }}%</div>
					<div>Pressure: {{ this.responseData.pressure }}hPa</div>
					<div>TVOC: {{ this.responseData.tvoc }}°C</div>
					<div>CO2: {{ this.responseData.co2 }}ppm</div>
					<div>Uptime: {{ this.responseData.uptime }}</div>
				</div>
			</div>
		</fieldset>
	</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import axios from 'axios'

class ResponseData {
	hostname: string
	uptime: string
	temperature: number
	humidity: number
	pressure: number
	co2: number
	tvoc: number

	constructor(hostname: string, uptime: string, temperature: number, humidity: number, pressure: number, co2: number, tvoc: number) {
		this.hostname = hostname
		this.uptime = uptime
		this.temperature = temperature
		this.humidity = humidity
		this.pressure = pressure
		this.co2 = co2
		this.tvoc = tvoc
	}

	static of(data: any): ResponseData {
		return new ResponseData(data.hostname, data.uptime, data.temperature, data.humidity, data.pressure, data.co2, data.tvoc)
	}

	static default() {
		return new ResponseData('n.A.', 'n.A.', 0, 0, 0, 0, 0)
	}
}

export default defineComponent({
	name: 'Dashboard',
	props: {
		msg: String
	},
	data: function() {
		return {
			responseData: ResponseData.default()
		}
	},
	mounted: function() {
		this.fetchData()
		this.start()
	},
	methods: {
		start: function() {
			setInterval(() => {
				this.fetchData()
			}, 5000)
		},

		fetchData: function() {
			axios.get('http://localhost:5000/api/data').then((response: any) => {
				console.log(response)
				this.responseData = ResponseData.of(response.data)
			})
		}
	}
})
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
