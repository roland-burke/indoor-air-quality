<template>
	<div class="flex justify-center">
		<fieldset
			class="mx-5 p-4 w-5/6 max-w-2xl border-4 rounded-xl border-blue-400">
			<legend class="text-2xl px-2 text-left">Controls</legend>
			<div class="divide-y divide-solid">
				<div class="flex justify-between items-center mb-3">
					<div class="flex flex-col">
						<h2 class="ml-2 text-xl text-left font-bold">Enable Alarm</h2>
						<h3 class="ml-2 text-left">Give an alarm when the air quality is too bad</h3>
					</div>
					<div
						class="flex min-w-max justify-between items-center"
						@click="toggleAlarm()">
						<div
							class="
								flex
								w-20
								h-10
								items-center
								bg-gray-300
								rounded-full
								p-1
								duration-300
								ease-in-out
							"
							:class="{ 'bg-green-400': alarmChecked }">
							<div
								class="
									bg-white
									w-8
									h-8
									rounded-full
									shadow-md
									transform
									duration-300
									ease-in-out
								"
								:class="{ 'translate-x-10': alarmChecked }"
							></div>
						</div>
					</div>
				</div>
				<div>
					<div class="flex justify-between items-center mt-3">
						<div class="flex flex-col">
							<h2 class="ml-2 text-xl text-left font-bold">Enable Display</h2>
							<h3 class="ml-2 text-left">Turn on the builtin display and show information</h3>
						</div>
						<div
							class="flex justify-between items-center"
							@click="toggleDisplay()">
							<div
								class="
									w-20
									h-10
									flex
									items-center
									bg-gray-300
									rounded-full
									p-1
									duration-300
									ease-in-out"
								:class="{ 'bg-green-400': displayChecked }">
								<div
									class="
										bg-white
										w-8
										h-8
										rounded-full
										shadow-md
										transform
										duration-300
										ease-in-out"
									:class="{ 'translate-x-10': displayChecked }"
								></div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</fieldset>
	</div>
</template>

<script lang="ts">
import { ResponseData } from '@/views/Home.vue'
import { defineComponent } from 'vue'
import axios from 'axios'

export default defineComponent({
	name: 'Controls',
	props: {
		responseData: ResponseData
	},
	data: function() {
		return {
			alarmChecked: this.responseData.alarmEnabled,
			displayChecked: this.responseData.displayEnabled
		}
	},
	watch: {
		responseData: function(val) {
			this.alarmChecked = val.alarmEnabled
			this.displayChecked = val.displayEnabled
		}
	},
	methods: {
		toggleAlarm: function() {
			this.alarmChecked = !this.alarmChecked
			axios.post('http://localhost:5000/api/controls/alarm/' + this.alarmChecked).then((response: any) => {
				console.log(response)
			})
		},
		toggleDisplay: function() {
			this.displayChecked = !this.displayChecked
			axios.post('http://localhost:5000/api/controls/display/' + this.displayChecked).then((response: any) => {
				console.log(response)
			})
		}
	}
})
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
