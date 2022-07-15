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
							<div class="flex w-20 h-10 items-center bg-gray-300 rounded-full p-1 duration-300 ease-in-out" :class="{ 'bg-green-400': this.responseData.alarmEnabled }">
								<div class="bg-white w-8 h-8 rounded-full shadow-md transform duration-300 ease-in-out" :class="{ 'translate-x-10': this.responseData.alarmEnabled }"></div>
							</div>
						</div>
					</div>
					<transition name="fade" mode="out-in">
						<div key="1" v-if="this.responseData.alarmEnabled" class="flex justify-between items-center mb-3">
							<div class="flex flex-col">
								<h2 class="ml-2 text-xl text-left font-bold">Smart Alarm</h2>
								<h3 class="ml-2 text-left">Alarm will automatically turn off during nighttime</h3>
							</div>
							<div class="flex min-w-max justify-between items-center" @click="toggleSmartAlarm()">
								<div class="flex w-20 h-10 items-center bg-gray-300 rounded-full p-1 duration-300 ease-in-out" :class="{ 'bg-green-400': this.responseData.smartAlarmEnabled }">
									<div
										class="bg-white w-8 h-8 rounded-full shadow-md transform duration-300 ease-in-out"
										:class="{
											'translate-x-10': this.responseData.smartAlarmEnabled,
										}"
									></div>
								</div>
							</div>
						</div>
					</transition>
				</div>
				<div>
					<div>
						<div class="flex justify-between items-center mt-3 mb-3">
							<div class="flex flex-col">
								<h2 class="ml-2 text-xl text-left font-bold">Display</h2>
								<h3 class="ml-2 text-left">Turn on the builtin display and show information</h3>
							</div>
							<div class="flex justify-between items-center" @click="toggleDisplay()">
								<div class="w-20 h-10 flex items-center bg-gray-300 rounded-full p-1 duration-300 ease-in-out" :class="{ 'bg-green-400': this.responseData.displayEnabled }">
									<div
										class="bg-white w-8 h-8 rounded-full shadow-md transform duration-300 ease-in-out"
										:class="{
											'translate-x-10': this.responseData.displayEnabled,
										}"
									></div>
								</div>
							</div>
						</div>
					</div>
					<transition name="fade" mode="out-in">
						<div key="2" v-if="this.responseData.displayEnabled">
							<div class="flex justify-between items-center mt-3 mb-3">
								<div class="flex flex-col">
									<h2 class="ml-2 text-xl text-left font-bold">Smart Display</h2>
									<h3 class="ml-2 text-left">The Display will automatically turn off during nighttime</h3>
								</div>
								<div class="flex justify-between items-center" @click="toggleSmartDisplay()">
									<div
										class="w-20 h-10 flex items-center bg-gray-300 rounded-full p-1 duration-300 ease-in-out"
										:class="{
											'bg-green-400': this.responseData.smartDisplayEnabled,
										}"
									>
										<div
											class="bg-white w-8 h-8 rounded-full shadow-md transform duration-300 ease-in-out"
											:class="{
												'translate-x-10': this.responseData.smartDisplayEnabled,
											}"
										></div>
									</div>
								</div>
							</div>
						</div>
					</transition>
				</div>
				<div>
					<div class="flex justify-between items-center pt-3 pb-3 mt-3 mb-3">
						<ul class="items-center w-full text-sm font-medium text-gray-900 bg-white rounded-lg border border-gray-200 sm:flex dark:border-gray-600 dark:text-white">
							<li class="w-full border-b border-gray-200 sm:border-b-0 sm:border-r dark:border-gray-600">
								<div class="flex items-center pl-3">
									<input
										id="horizontal-list-radio-license"
										@click="togglePair(0)"
										:disabled="!this.responseData.displayEnabled"
										type="radio"
										value=""
										:checked="this.responseData.displayMode == 0"
										name="list-radio"
										class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 dark:ring-offset-gray-700 dark:bg-gray-600 dark:border-gray-500"
									/>
									<label for="horizontal-list-radio-license" class="py-3 ml-2 w-full text-sm font-medium text-gray-900 dark:text-gray-300">Show everything</label>
								</div>
							</li>
							<li class="w-full border-gray-200 dark:border-gray-600">
								<div class="flex items-center pl-3">
									<input
										id="horizontal-list-radio-id"
										@click="togglePair(1)"
										:disabled="!this.responseData.displayEnabled"
										type="radio"
										value=""
										:checked="this.responseData.displayMode == 1"
										name="list-radio"
										class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 dark:ring-offset-gray-700 dark:bg-gray-600 dark:border-gray-500"
									/>
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
	<div class="absolute bottom-5 left-1/2 transform -translate-x-1/2 ">

	<div v-if="toastVisible" id="toast-default" class="flex items-center p-4 w-full max-w-xs text-gray-500 bg-white rounded-lg shadow dark:text-gray-400 dark:bg-gray-800" role="alert">
		<div class="ml-3 text-sm font-normal">{{ toastMessage }}</div>
		<button
			type="button"
			class="ml-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex h-8 w-8 dark:text-gray-500 dark:hover:text-white dark:bg-gray-800 dark:hover:bg-gray-700"
			data-dismiss-target="#toast-default"
			aria-label="Close"
			@click="toastVisible = false"
		>
			<span class="sr-only">Close</span>
			<svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
				<path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
			</svg>
		</button>
	</div>
	</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { ResponseData, getUrl } from '@/Global'
import axios from 'axios'

export default defineComponent({
	name: 'Controls',
	data: function() {
		return {
			responseData: ResponseData.default(),
			fetcher: 0,
			toastVisible: false,
			toastMessage: ''
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
			})
		},
		saveControls: function() {
			var data = {
				displayEnabled: this.responseData.displayEnabled,
				alarmEnabled: this.responseData.alarmEnabled,
				smartDisplayEnabled: this.responseData.smartDisplayEnabled,
				smartAlarmEnabled: this.responseData.smartAlarmEnabled,
				displayMode: this.responseData.displayMode

			}
			var completeUrl = getUrl() + '/api/controls'
			return axios.post(completeUrl, data)
		},

		testAlarm: function() {
			var completeUrl = getUrl() + '/api/alarm/test'
			return axios.post(completeUrl, {}).then(() => {
				this.toastMessage = 'Successfully sent request'
				this.toastVisible = true
			}).catch((error: any) => {
				this.toastMessage = 'Testing alarm failed: ' + error.message
				this.toastVisible = true
			})
		},

		toggleAlarm: function() {
			this.responseData.alarmEnabled = !this.responseData.alarmEnabled
			if (!this.responseData.alarmEnabled) {
				this.responseData.smartAlarmEnabled = false
			}

			this.saveControls().then((response: any) => {
				console.log(response)
			})
		},
		toggleDisplay: function() {
			this.responseData.displayEnabled = !this.responseData.displayEnabled
			if (!this.responseData.displayEnabled) {
				this.responseData.smartDisplayEnabled = false
			}
			this.saveControls().then((response: any) => {
				console.log(response)
			})
		},
		toggleSmartAlarm: function() {
			this.responseData.smartAlarmEnabled = !this.responseData.smartAlarmEnabled

			this.saveControls().then((response: any) => {
				console.log(response)
			})
		},
		toggleSmartDisplay: function() {
			this.responseData.smartDisplayEnabled = !this.responseData.smartDisplayEnabled
			this.saveControls().then((response: any) => {
				console.log(response)
			})
		},
		togglePair: function(newValue: number) {
			this.responseData.displayMode = newValue
			this.saveControls().then((response: any) => {
				console.log(response)
			})
		}
	}
})
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.fade-enter-active {
	transition: opacity 0.3s;
}

.fade-leave-active {
	transition: opacity 0.3s;
}

.fade-enter-to {
	opacity: 1;
}

.fade-leave-to {
	opacity: 0;
}
</style>
