<template>
	<div class="flex justify-center">
		<fieldset
			class="m-10 p-4 w-3/6 max-w-2xl border-4 rounded-xl border-blue-400"
		>
			<legend class="text-2xl px-2 text-left">Controls</legend>
			<div class="divide-y divide-solid">
				<div>
					<div
						class="flex justify-between items-center"
						@click="toggleAlarm = !toggleAlarm"
					>
						<div
							class="
								w-16
								h-10
								flex
								items-center
								bg-gray-300
								rounded-full
								p-1
								duration-300
								ease-in-out
							"
							:class="{ 'bg-green-400': toggleAlarm }"
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
								:class="{ 'translate-x-6': toggleAlarm }"
							></div>
						</div>
						<h2>Alarm when the air quality is too bad</h2>
					</div>
				</div>
				<div>
					<div>
						<div
							class="flex justify-between items-center"
							@click="toggleDisplay = !toggleDisplay">
							<div
								class="
									w-16
									h-10
									flex
									items-center
									bg-gray-300
									rounded-full
									p-1
									duration-300
									ease-in-out
								"
								:class="{ 'bg-green-400': toggleDisplay }">
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
									:class="{ 'translate-x-6': toggleDisplay }"
								></div>
							</div>
							<h2>Show the information on the builtin display</h2>
						</div>
					</div>
				</div>
			</div>
		</fieldset>
	</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
	name: 'Controls',
	props: {
		msg: String
	},
	data: function () {
		return {
			toggleAlarm: false,
			toggleDisplay: false
		}
	}
})
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
