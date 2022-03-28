<template>
	<div class="flex justify-evenly items-center my-3">
		<div class="w-7">
			<img :src="icon" />
		</div>
		<span v-if="label != null" class="text-left text-lg font-bold w-24">{{ label }}</span>
		<span class="text-left text-lg w-20">{{ value }}</span>
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
