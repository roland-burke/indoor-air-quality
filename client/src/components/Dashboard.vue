<template>
	<div class="flex justify-center">
		<fieldset
			class="
				mx-5
				mb-5
				p-4
				w-5/6
				max-w-2xl
				border-4
				rounded-xl
				shadow-md
				border-blue-400
			"
		>
			<legend class="text-2xl px-2 text-left">Sensor Overview</legend>
			<div class="divide-y divide-solid">
				<div class="mb-2">
					<div class="flex items-center">
						<h1 class="text-xl font-bold mr-2">Device Name:</h1>
						<p>{{ this.responseData.hostname }}</p>
					</div>
					<div class="flex items-center">
						<h1 class="text-base font-bold mr-2">Uptime:</h1>
						<p>{{ this.responseData.uptime }}</p>
					</div>
				</div>

				<div>
					<div class="flex justify-evenly items-center mt-2">
						<div>
							<div class="text-lg text-left font-bold mr-2">
								Temperature:
							</div>
							<div class="text-lg text-left font-bold mr-2">
								Humidity:
							</div>
							<div class="text-lg text-left font-bold mr-2">
								Pressure:
							</div>
							<div class="text-lg text-left font-bold mr-2">
								TVOC:
							</div>
							<div class="text-lg text-left font-bold mr-2">
								CO2:
							</div>
						</div>
						<div>
							<div class="text-left">{{ this.responseData.temperature.toFixed(1) }} °C</div>
							<div class="text-left">
								{{ this.responseData.humidity.toFixed(0) }} %
							</div>
							<div class="text-left">
								{{ this.responseData.pressure.toFixed(0) }} hPa
							</div>
							<div class="text-left">
								{{ this.responseData.tvoc.toFixed(0) }}
							</div>
							<div class="text-left">
								{{ this.responseData.co2.toFixed(0) }} ppm
							</div>
						</div>
					</div>
				</div>
			</div>
		</fieldset>
	</div>
</template>

<script lang='ts'>
import { defineComponent } from 'vue'
import { ResponseData } from '@/views/Home.vue'

export default defineComponent({
	name: 'Dashboard',
	props: {
		responseData: ResponseData
	}
})
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped>
</style>
