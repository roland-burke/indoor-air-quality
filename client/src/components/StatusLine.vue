<template>
	<div class="flex justify-evenly items-center">
		<span class="text-left text-lg font-bold w-20">{{ label }}</span>
		<span v-bind:class="value ? 'bg-green-600' : 'bg-red-600'" class="w-5 h-5 m-1 rounded-full border-2 border-black"></span>
	</div>
</template>

<script lang='ts'>
import { defineComponent } from 'vue'

export default defineComponent({
	name: 'StatusLine',
	props: {
		label: String,
		value: Boolean
	}
})
</script>
