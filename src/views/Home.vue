<template>
	<div class="home">
		<Dashboard msg="Welcome to Your Vue.js + TypeScript App" />
		<Controls msg="Welcome to Your Vue.js + TypeScript App" />
	</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Dashboard from '@/components/Dashboard.vue'
import Controls from '@/components/Controls.vue'

export default defineComponent({
	name: 'Home',
	components: {
		Dashboard,
		Controls
	}
})
</script>
