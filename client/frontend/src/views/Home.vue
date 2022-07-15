<template>
	<div class="home">
		<Dashboard :responseData="this.responseData" :sensorData="this.sensorData" />
	</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Dashboard from '@/components/Dashboard.vue'
import axios from 'axios'
import { SensorData, ResponseData, getUrl } from '@/Global'

export default defineComponent({
	name: 'Home',
	components: {
		Dashboard
	},
	data: function() {
		return {
			data: [],
			responseData: ResponseData.default(),
			sensorData: SensorData.default(),
			fetcher: 0
		}
	},
	mounted: function() {
		this.fetchData()
		this.start()
	},
	beforeUnmount() {
		clearInterval(this.fetcher)
	},
	methods: {
		start: function() {
			this.fetcher = setInterval(() => {
				this.fetchData()
			}, 2000)
		},

		fetchData: function() {
			axios.get(getUrl() + '/api/data').then((response: any) => {
				console.log(response)
				this.responseData = ResponseData.of(response.data)
				this.sensorData = SensorData.of(response.data.sensors)
			})
		}
	}
})
</script>
