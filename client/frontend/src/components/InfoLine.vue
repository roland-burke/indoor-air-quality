<template>
	<div class="flex justify-evenly items-center my-2">
		<div class="w-7 mr-3">
			<img :src="icon" />
		</div>
		<span v-if="label != null" class="text-left font-bold mr-3">{{ label }}</span>
		<span class="text-left text-xl w-20">{{ value }}</span>
	</div>
</template>

<script lang='ts'>
import { defineComponent } from 'vue'

export default defineComponent({
	name: 'InfoLine',
	props: {
		label: String,
		value: String,
		icon: null
	}
})
</script>
