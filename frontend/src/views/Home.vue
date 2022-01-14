<template>
	<div class="home">
		<Dashboard msg="Welcome to Your Vue.js + TypeScript App" />
	</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Dashboard from '@/components/Dashboard.vue' // @ is an alias to /src

export default defineComponent({
	name: 'Home',
	components: {
		Dashboard
	}
})
</script>
