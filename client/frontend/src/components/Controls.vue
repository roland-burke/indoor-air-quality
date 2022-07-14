<template>
	<div class="flex justify-center">
		<fieldset class="mx-5 mb-8 p-4 w-5/6 max-w-2xl border-4 rounded-xl shadow-md border-blue-400">
			<legend class="text-2xl px-2 text-left">Controls</legend>
			<div class="divide-y divide-solid">
				<div>
					<div class="flex justify-between items-center mb-3">
						<div class="flex flex-col">
							<h2 class="ml-2 text-xl text-left font-bold">Alarm</h2>
							<h3 class="ml-2 text-left">Give an alarm when the air quality is too bad</h3>
						</div>
						<div class="flex min-w-max justify-between items-center" @click="toggleAlarm()">
							<div class="flex w-20 h-10 items-center bg-gray-300 rounded-full p-1 duration-300 ease-in-out" :class="{ 'bg-green-400': alarmChecked }">
								<div class="bg-white w-8 h-8 rounded-full shadow-md transform duration-300 ease-in-out" :class="{ 'translate-x-10': alarmChecked }"></div>
							</div>
						</div>
					</div>
					<div v-if="alarmChecked" class="flex justify-between items-center mb-3">
						<div class="flex flex-col">
							<h2 class="ml-2 text-xl text-left font-bold">Smart Alarm</h2>
							<h3 class="ml-2 text-left">Alarm will automatically turn off during nighttime</h3>
						</div>
						<div class="flex min-w-max justify-between items-center" @click="toggleSmartAlarm()">
							<div class="flex w-20 h-10 items-center bg-gray-300 rounded-full p-1 duration-300 ease-in-out" :class="{ 'bg-green-400': smartAlarmChecked }">
								<div
									class="bg-white w-8 h-8 rounded-full shadow-md transform duration-300 ease-in-out"
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
						<div class="flex justify-between items-center mt-3 mb-3">
							<div class="flex flex-col">
								<h2 class="ml-2 text-xl text-left font-bold">Display</h2>
								<h3 class="ml-2 text-left">Turn on the builtin display and show information</h3>
							</div>
							<div class="flex justify-between items-center" @click="toggleDisplay()">
								<div class="w-20 h-10 flex items-center bg-gray-300 rounded-full p-1 duration-300 ease-in-out" :class="{ 'bg-green-400': displayChecked }">
									<div
										class="bg-white w-8 h-8 rounded-full shadow-md transform duration-300 ease-in-out"
										:class="{
											'translate-x-10': displayChecked,
										}"
									></div>
								</div>
							</div>
						</div>
					</div>
					<div v-if="displayChecked" class="ease-in-out duration-1000">
						<div class="flex justify-between items-center mt-3 mb-3">
							<div class="flex flex-col">
								<h2 class="ml-2 text-xl text-left font-bold">Smart Display</h2>
								<h3 class="ml-2 text-left">The Display will automatically turn off during nighttime</h3>
							</div>
							<div class="flex justify-between items-center" @click="toggleSmartDisplay()">
								<div
									class="w-20 h-10 flex items-center bg-gray-300 rounded-full p-1 duration-300 ease-in-out"
									:class="{
										'bg-green-400': smartDisplayChecked,
									}"
								>
									<div
										class="bg-white w-8 h-8 rounded-full shadow-md transform duration-300 ease-in-out"
										:class="{
											'translate-x-10': smartDisplayChecked,
										}"
									></div>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div>
					<div class="flex justify-between items-center pt-3 pb-3 mt-3 mb-3">

					<ul class="items-center w-full text-sm font-medium text-gray-900 bg-white rounded-lg border border-gray-200 sm:flex dark:border-gray-600 dark:text-white">
						<li class="w-full border-b border-gray-200 sm:border-b-0 sm:border-r dark:border-gray-600">
							<div class="flex items-center pl-3">
								<input id="horizontal-list-radio-license" @click="togglePair(0)" type="radio" value="" :checked="displayMode == 0" name="list-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 dark:ring-offset-gray-700 dark:bg-gray-600 dark:border-gray-500" />
								<label for="horizontal-list-radio-license" class="py-3 ml-2 w-full text-sm font-medium text-gray-900 dark:text-gray-300">Show everything</label>
							</div>
						</li>
						<li class="w-full border-gray-200 dark:border-gray-600">
							<div class="flex items-center pl-3">
								<input id="horizontal-list-radio-id" @click="togglePair(1)" type="radio" value="" :checked="displayMode == 1" name="list-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 dark:ring-offset-gray-700 dark:bg-gray-600 dark:border-gray-500" />
								<label for="horizontal-list-radio-id" class="py-3 ml-2 w-full text-sm font-medium text-gray-900 dark:text-gray-300">Show data in pairs</label>
							</div>
						</li>
					</ul>
					</div>
				</div>
				<div>
					<div class="mt-4">
						<button v-on:click="testAlarm()" class="hover:bg-blue-400 rounded-lg bg-transparent p-2 border-2">Test Alarm</button>
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
		responseData: ResponseData,
		hostUrl: String
	},
	data: function() {
		return {
			alarmChecked: this.responseData.alarmEnabled,
			displayChecked: this.responseData.displayEnabled,
			smartAlarmChecked: this.responseData.smartAlarmEnabled,
			smartDisplayChecked: this.responseData.smartDisplayEnabled,
			displayMode: this.responseData.displayMode
		}
	},
	watch: {
		responseData: function(data) {
			this.alarmChecked = data.alarmEnabled
			this.displayChecked = data.displayEnabled
			this.smartAlarmChecked = data.smartAlarmEnabled
			this.smartDisplayChecked = data.smartDisplayEnabled
			this.displayMode = data.displayMode
		}
	},
	methods: {
		saveControls: function() {
			var data = {
				displayEnabled: this.displayChecked,
				alarmEnabled: this.alarmChecked,
				smartDisplayEnabled: this.smartDisplayChecked,
				smartAlarmEnabled: this.smartAlarmChecked,
				displayMode: this.displayMode

			}
			var completeUrl = this.hostUrl + '/api/controls'
			return axios.post(completeUrl, data)
		},

		testAlarm: function() {
			var completeUrl = this.hostUrl + '/api/alarm/test'
			return axios.post(completeUrl, {})
		},

		toggleAlarm: function() {
			this.alarmChecked = !this.alarmChecked
			if (!this.alarmChecked) {
				this.smartAlarmChecked = false
			}

			this.saveControls().then((response: any) => {
				console.log(response)
			})
		},
		toggleDisplay: function() {
			this.displayChecked = !this.displayChecked
			if (!this.displayChecked) {
				this.smartDisplayChecked = false
			}
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
		},
		togglePair: function(newValue: number) {
			this.displayMode = newValue
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
