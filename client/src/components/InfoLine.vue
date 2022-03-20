<template>
	<div class="flex justify-evenly items-center">
		<span class="text-left text-lg font-bold w-32">{{ label }}</span>
		<span class="text-left w-14">{{ value }}</span>
	</div>
</template>

<script lang='ts'>
import { defineComponent } from 'vue'

export default defineComponent({
	name: 'InfoLine',
	props: {
		label: String,
		value: String
	}
})
</script>
