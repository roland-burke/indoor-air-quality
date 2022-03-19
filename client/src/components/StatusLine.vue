<template>
	<div class="flex justify-evenly items-center">
		<span class="text-left text-lg font-bold w-24">{{ label }}</span>
		<span v-if="value" class="w-6 h-6 m-1 bg-green-600 rounded-full border-2 border-black"></span>
        <span v-if="!value" class="w-6 h-6 m-1 bg-red-600 rounded-full border-2 border-black"></span>
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
