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
			<legend class="text-2xl px-2 text-left">Controls</legend>
			<div class="divide-y divide-solid">
				<div>
					<div class="flex justify-between items-center mb-3">
						<div class="flex flex-col">
							<h2 class="ml-2 text-xl text-left font-bold">
								Alarm
							</h2>
							<h3 class="ml-2 text-left">
								Give an alarm when the air quality is too bad
							</h3>
						</div>
						<div
							class="flex min-w-max justify-between items-center"
							@click="toggleAlarm()"
						>
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
								:class="{ 'bg-green-400': alarmChecked }"
							>
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
					<div
						v-if="smartAlarmEnabled"
						class="flex justify-between items-center mb-3"
					>
						<div class="flex flex-col">
							<h2 class="ml-2 text-xl text-left font-bold">
								Smart Alarm
							</h2>
							<h3 class="ml-2 text-left">
								Alarm will automatically turn off during
								nighttime
							</h3>
						</div>
						<div
							class="flex min-w-max justify-between items-center"
							@click="toggleSmartAlarm()"
						>
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
								:class="{ 'bg-green-400': smartAlarmChecked }"
							>
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
									:class="{
										'translate-x-10': smartAlarmChecked,
									}"
								></div>
							</div>
						</div>
					</div>
				</div>
				<div>
					<div>
						<div class="flex justify-between items-center mt-3">
							<div class="flex flex-col">
								<h2 class="ml-2 text-xl text-left font-bold">
									Display
								</h2>
								<h3 class="ml-2 text-left">
									Turn on the builtin display and show
									information
								</h3>
							</div>
							<div
								class="flex justify-between items-center"
								@click="toggleDisplay()"
							>
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
										ease-in-out
									"
									:class="{ 'bg-green-400': displayChecked }"
								>
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
										:class="{
											'translate-x-10': displayChecked,
										}"
									></div>
								</div>
							</div>
						</div>
					</div>
					<div
						v-if="smartDisplayEnabled"
						class="ease-in-out duration-1000"
					>
						<div class="flex justify-between items-center mt-3">
							<div class="flex flex-col">
								<h2 class="ml-2 text-xl text-left font-bold">
									Smart Display
								</h2>
								<h3 class="ml-2 text-left">
									The Display will automatically turn off
									during nighttime
								</h3>
							</div>
							<div
								class="flex justify-between items-center"
								@click="toggleSmartDisplay()"
							>
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
										ease-in-out
									"
									:class="{
										'bg-green-400': smartDisplayChecked,
									}"
								>
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
										:class="{
											'translate-x-10':
												smartDisplayChecked,
										}"
									></div>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div>
					<button type="button">Test Alarm</button>
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
		responseData: ResponseData,
		hostUrl: String
	},
	data: function() {
		return {
			alarmChecked: this.responseData.alarmEnabled,
			displayChecked: this.responseData.displayEnabled,
			smartAlarmChecked: false,
			smartDisplayChecked: false,
			smartAlarmEnabled: false,
			smartDisplayEnabled: false
		}
	},
	watch: {
		responseData: function(val) {
			this.alarmChecked = val.alarmEnabled
			this.displayChecked = val.displayEnabled
			if (this.alarmChecked) {
				this.smartAlarmEnabled = true
			}
			if (this.displayChecked) {
				this.smartDisplayEnabled = true
			}
		}
	},
	methods: {
		saveControls: function() {
			var data = {
				displayEnabled: this.displayChecked,
				alarmEnabled: this.alarmChecked,
				smartDisplayEnabled: this.smartDisplayChecked,
				smartAlarmEnabled: this.smartAlarmChecked

			}
			var completeUrl = this.hostUrl + '/api/controls'
			return axios.post(completeUrl, data)
		},

		toggleAlarm: function() {
			this.alarmChecked = !this.alarmChecked
			this.smartAlarmEnabled = this.alarmChecked && true

			this.saveControls().then((response: any) => {
				console.log(response)
			})
		},
		toggleDisplay: function() {
			this.displayChecked = !this.displayChecked
			this.smartDisplayEnabled = this.displayChecked && true

			this.saveControls().then((response: any) => {
				console.log(response)
			})
		},
		toggleSmartAlarm: function() {
			this.smartAlarmChecked = !this.smartAlarmChecked

			this.saveControls().then((response: any) => {
				console.log(response)
			})
		},
		toggleSmartDisplay: function() {
			this.smartDisplayChecked = !this.smartDisplayChecked
			this.saveControls().then((response: any) => {
				console.log(response)
			})
		}
	}
})
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
