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
			<legend class="text-2xl px-2 text-left">Overview</legend>
			<div class="divide-y divide-solid">
				<div class="mb-2">
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

				<div>
					<div class="flex justify-evenly items-center mt-2">
                        <div>
                            <StatusLine :label="'BME280:'" :value="false"></StatusLine>
                            <StatusLine :label="'CCS811:'" :value="true"></StatusLine>
                            <StatusLine :label="'Display:'" :value="false"></StatusLine>
                        </div>
						<div>
							<InfoLine
								:label="'Temperature:'"
								:value="
									this.responseData.temperature.toFixed(1) +
									' °C'
								"
							></InfoLine>
                            <InfoLine
								:label="'Humidity:'"
								:value="
									this.responseData.humidity.toFixed(0) +
									' %'
								"
							></InfoLine>
                            <InfoLine
								:label="'Pressure:'"
								:value="
									this.responseData.pressure.toFixed(0) +
									' hPa'
								"
							></InfoLine>
                            <InfoLine
								:label="'TVOC:'"
								:value="
									this.responseData.tvoc.toFixed(0)
								"
							></InfoLine>
                                <InfoLine
								:label="'CO2:'"
								:value="
									this.responseData.co2.toFixed(0) +
									' ppm'
								"
							></InfoLine>
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
import InfoLine from './InfoLine.vue'
import StatusLine from './StatusLine.vue'

export default defineComponent({
	components: { InfoLine, StatusLine },
	name: 'Dashboard',
	props: {
		responseData: ResponseData
	}
})
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped>
</style>
