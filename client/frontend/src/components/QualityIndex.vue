<template>
	<div class="flex border-2 h-6">
		<div v-if="this.indexLevel > 0" class="bg-blue-400 w-1/6 h-5"></div>
		<div v-if="this.indexLevel > 1" class="bg-green-400 w-1/6 h-5"></div>
		<div v-if="this.indexLevel > 2" class="bg-yellow-300 w-1/6 h-5"></div>
		<div v-if="this.indexLevel > 3" class="bg-yellow-500 w-1/6 h-5"></div>
		<div v-if="this.indexLevel > 4" class="bg-red-500 w-1/6 h-5"></div>
		<div v-if="this.indexLevel > 5" class="bg-red-700 w-1/6 h-5"></div>
	</div>
	<div>Level: {{ indexLevel }} ({{ this.getLevelName(this.indexLevel) }})</div>
	<div v-if="this.indexLevel === 4 || this.indexLevel === 5" class="p-4 mt-3 mb-2 text-sm text-yellow-700 bg-yellow-100 rounded-lg dark:bg-yellow-200 dark:text-yellow-800" role="alert"><span class="font-bold">Warning!</span> Air Quality is in a critical condition, please take action!</div>
	<div v-if="this.indexLevel === 6" class="p-4 mt-3 mb-2 text-sm text-red-700 bg-red-100 rounded-lg dark:bg-red-200 dark:text-red-800" role="alert"><span class="font-bold">Danger!</span> Air Quality is in a serious condition! Please take immediate Action!</div>
</template>

<script lang='ts'>
import { defineComponent } from 'vue'

export default defineComponent({
	components: {},
	name: 'Dashboard',
	props: {
		indexLevel: Number
	},
	methods: {
		getLevelName: function(level: number): string {
			switch (level) {
				case 1:
					return 'Excellent'
				case 2:
					return 'Fine'
				case 3:
					return 'Moderate'
				case 4:
					return 'Poor'
				case 5:
					return 'Very Poor'
				case 6:
					return 'Dangerous'
				default:
					return 'Undefined'
			}
		}
	}
})
</script>
