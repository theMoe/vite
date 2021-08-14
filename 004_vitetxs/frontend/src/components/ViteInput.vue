<template>
    <div class="input-group">
        <label class="input">
            <input v-if="required" type="text" :name="name"  placeholder=" " @input="onChange" v-on:keyup.enter="onSubmit" required>
            <input v-else type="text" :name="name" placeholder=" " @input="onChange" v-on:keyup.enter="onSubmit">
            <span class="input-label">{{label}}</span>
            <span v-if="required" class="input-helper">required</span>
            <span v-else class="input-helper">optional</span>
        </label>
    </div>
</template>
<script>
export default {
    props: ["label", "name", "onChange", "onSubmit", "required"]
}
</script>

<style scoped>
/* build in: https://codepen.io/tstrmn/pen/QWdazwO?editors=1100 */
.input-group {
    margin-bottom: 40px;
    position: relative;
    width: 50%;
}

.input {
    cursor: text;
    border-radius: 0;
}

.input > input {
	border: none;
	border-bottom: 2px solid var(--grey);
    border-radius: 0;
	width: 100%;
	height: 60px;
	font-size: 13pt;
	padding-left: 15px;
	padding-top: 17px;
    background-color: rgba(0,0,0,0);
	transition: all .2s;
}

.input > input:focus {
	outline: none;
}

.input > .input-label {
	position: absolute;
	top: 18px;
	left: 15px;
	line-height: 150%;
	color: var(--grey);
	transition: top .2s;
}

.input > .input-helper {
	font-size: 9pt;
    position: absolute;
	top: 5px;
    right: 0;
	color: var(--orange);
	letter-spacing: 0.03rem;
	margin: 2px 14px;
}

.input:hover > input {
	background-color: var(--blue-lightest);
	border-color: var(--blue);
}

.input > input:focus + .input-label,
.input > input:not(:placeholder-shown) + .input-label {
	top: 0;
	left: 5px;
	font-size: 11pt;
	margin-bottom: 35px;
	color: var(--blue);
}

.input > input:focus + .input-label {
	color: var(--blue);
}

@media (max-width: 600px) {
	.input > input {
		font-size: 10pt;
	}
}
</style>