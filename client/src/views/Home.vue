<template>
	<div class="home">
		<Dashboard :responseData="this.responseData" />
		<Controls :responseData="this.responseData" :hostUrl="this.getUrl()"/>
	</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Dashboard from '@/components/Dashboard.vue'
import Controls from '@/components/Controls.vue'
import axios from 'axios'

export class ResponseData {
	hostname: string
	uptime: string
	room: string
	temperature: number
	humidity: number
	pressure: number
	co2: number
	tvoc: number
	alarmEnabled: boolean
	displayEnabled: boolean

	constructor(
		hostname: string,
		uptime: string,
		room: string,
		temperature: number,
		humidity: number,
		pressure: number,
		co2: number,
		tvoc: number,
		alarmEnabled: boolean,
		displayEnabled: boolean
	) {
		this.hostname = hostname
		this.uptime = uptime
		this.room = room
		this.temperature = temperature
		this.humidity = humidity
		this.pressure = pressure
		this.co2 = co2
		this.tvoc = tvoc
		this.alarmEnabled = alarmEnabled
		this.displayEnabled = displayEnabled
	}

	static of(data: any): ResponseData {
		return new ResponseData(
			data.meta.hostname,
			data.meta.uptime,
			data.meta.room,
			data.sensors.temperature,
			data.sensors.humidity,
			data.sensors.pressure,
			data.sensors.co2,
			data.sensors.tvoc,
			data.controls.alarmEnabled,
			data.controls.displayEnabled
		)
	}

	static default() {
		return new ResponseData('n.A.', 'n.A.', 'n.A.', 0, 0, 0, 0, 0, false, false)
	}
}

export default defineComponent({
	name: 'Home',
	components: {
		Dashboard,
		Controls
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
			}, 2000)
		},

		fetchData: function() {
			axios.get(this.getUrl() + '/api/data').then((response: any) => {
				console.log(response)
				this.responseData = ResponseData.of(response.data)
			})
		},

		getUrl: function() {
			// var url = document.location.protocol + '//' + document.location.host
			var url = 'http://localhost:5000'
			return url
		}
	}
})
</script>
