<template>
	<div id="nav" class="py-4">
		<router-link to="/">Home</router-link> |
		<router-link to="/controls">Controls</router-link> |
		<router-link to="/about">About</router-link>
	</div>
	<router-view />
</template>

<style>
@import url("https://fonts.googleapis.com/css?family=Arial:100,300,400,500,700,900");

#app {
	font-family: Avenir, Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	text-align: center;
	color: #2c3e50;
}

#nav a {
	font-weight: bold;
	color: #2c3e50;
}

#nav a.router-link-exact-active {
	color: rgba(96, 165, 250);
}
</style>
