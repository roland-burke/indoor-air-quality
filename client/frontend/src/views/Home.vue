<template>
	<div class="home">
		<Dashboard :responseData="this.responseData" :sensorData="this.sensorData" />
		<Controls :responseData="this.responseData" :hostUrl="this.getUrl()" />
	</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Dashboard from '@/components/Dashboard.vue'
import Controls from '@/components/Controls.vue'
import axios from 'axios'

export class SensorData {
	temperature: number
	humidity: number
	pressure: number
	co2: number
	tvoc: number
	bme280Status: boolean
	ccs811Status: boolean

	constructor(
		temperature: number,
		humidity: number,
		pressure: number,
		co2: number,
		tvoc: number,
		bme280Status: boolean,
		ccs811Status: boolean

	) {
		this.temperature = temperature
		this.humidity = humidity
		this.pressure = pressure
		this.co2 = co2
		this.tvoc = tvoc
		this.bme280Status = bme280Status
		this.ccs811Status = ccs811Status
	}

	static of(data: any): SensorData {
		return new SensorData(
			data.temperature,
			data.humidity,
			data.pressure,
			data.co2,
			data.tvoc,
			data.bme280Status,
			data.ccs811Status
		)
	}

	static default() {
		return new SensorData(0, 0, 0, 0, 0, false, false)
	}
}

export class ResponseData {
	hostname: string
	uptime: string
	room: string
	ipAddr: string
	macAddr: string

	alarmEnabled: boolean
	displayEnabled: boolean
	smartAlarmEnabled: boolean
	smartDisplayEnabled: boolean
	displayMode: number

	constructor(
		hostname: string,
		uptime: string,
		room: string,
		ipAddr: string,
		macAddr: string,
		alarmEnabled: boolean,
		displayEnabled: boolean,
		smartAlarmEnabled: boolean,
		smartDisplayEnabled: boolean,
		displayMode: number
	) {
		this.hostname = hostname
		this.uptime = uptime
		this.room = room
		this.ipAddr = ipAddr
		this.macAddr = macAddr
		this.alarmEnabled = alarmEnabled
		this.displayEnabled = displayEnabled
		this.smartAlarmEnabled = smartAlarmEnabled
		this.smartDisplayEnabled = smartDisplayEnabled
		this.displayMode = displayMode
	}

	static of(data: any): ResponseData {
		return new ResponseData(
			data.meta.hostname,
			data.meta.uptime,
			data.meta.room,
			data.meta.ipAddr,
			data.meta.macAddr,
			data.controls.alarmEnabled,
			data.controls.displayEnabled,
			data.controls.smartAlarmEnabled,
			data.controls.smartDisplayEnabled,
			data.controls.displayMode
		)
	}

	static default() {
		return new ResponseData('n.A.', 'n.A.', 'n.A.', 'n.A.', 'n.A.', false, false, false, false, 0)
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
			data: [],
			responseData: ResponseData.default(),
			sensorData: SensorData.default()
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
				this.sensorData = SensorData.of(response.data.sensors)
			})
		},

		getUrl: function() {
			var url = document.location.protocol + '//' + document.location.host
			// var url = 'http://localhost:5000'
			return url
		}
	}
})
</script>
