<template>
	<div class="flex justify-center">
		<fieldset class="mx-5 mb-5 p-4 w-5/6 max-w-2xl border-4 rounded-xl shadow-md border-blue-400">
			<legend class="text-2xl px-2 text-left">Overview</legend>
			<div class="divide-y divide-solid">
				<div class="mb-2">
					<div class="flex flex-row justify-between">
						<div>
							<div class="flex items-center">
								<h1 class="text-xl font-bold mr-2">Device Name:</h1>
								<p>{{ this.responseData.hostname }}</p>
							</div>
							<div class="flex items-center">
								<h1 class="text-base font-bold mr-2">Room:</h1>
								<p>{{ this.responseData.room }}</p>
							</div>
							<div class="flex items-center">
								<h1 class="text-base font-bold mr-2">Uptime:</h1>
								<p>{{ this.responseData.uptime }}</p>
							</div>
						</div>
						<div class="flex flex-col items-end justify-end">
							<div class="flex text-base">{{ this.responseData.ipAddr }}</div>
							<div class="flex text-sm">{{ this.responseData.macAddr }}</div>
						</div>
					</div>
				</div>

				<div class="flex justify-evenly items-center pt-2 my-2">
					<StatusLine :label="'BME280:'" :value="this.sensorData.bme280Status"></StatusLine>
					<StatusLine :label="'CCS811:'" :value="this.sensorData.ccs811Status"></StatusLine>
					<StatusLine :label="'Display:'" :value="this.responseData.displayWorking"></StatusLine>
				</div>

				<div class="flex justify-evenly items-center">
					<div class="flex flex-col">
						<InfoLine :icon="require('@/assets/Temperature.svg')" :value="this.sensorData.temperature.toFixed(1) + ' °C'"></InfoLine>
						<InfoLine :icon="require('@/assets/Humidity.svg')" :value="this.sensorData.humidity.toFixed(0) + ' %'"></InfoLine>
						<InfoLine :icon="require('@/assets/Pressure.svg')" :value="this.sensorData.pressure.toFixed(0) + ' hPa'"></InfoLine>
					</div>
					<div class="flex flex-col justify-center items-center">
						<InfoLine :label="'TVOC:'" :value="this.sensorData.tvoc.toFixed(0) + ' ppb'"></InfoLine>
						<InfoLine :label="'CO2:'" :value="this.sensorData.co2.toFixed(0) + ' ppm'"></InfoLine>
					</div>
				</div>
				<div class="pt-5">
					<QualityIndex :indexLevel="this.sensorData.indexLevel"></QualityIndex>
				</div>
			</div>
		</fieldset>
	</div>
</template>

<script lang='ts'>
import { defineComponent } from 'vue'
import { ResponseData, SensorData } from '@/Global'
import InfoLine from './InfoLine.vue'
import StatusLine from './StatusLine.vue'
import QualityIndex from './QualityIndex.vue'

export default defineComponent({
	components: { InfoLine, StatusLine, QualityIndex },
	name: 'Dashboard',
	props: {
		responseData: ResponseData,
		sensorData: SensorData
	}
})
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped>
</style>
