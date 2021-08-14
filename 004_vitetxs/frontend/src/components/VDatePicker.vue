<template>
  <div class="input-group datepicker-group">
        <div class="input datepicker">
            <datepicker :name="name" placeholder="Click to select a date" @selected="onSelect" ></datepicker>    
            <span class="input-label">{{label}}</span>
            <span v-if="required" class="input-helper">required</span>
            <span v-else class="input-helper">optional</span>
        </div>
    </div>
</template>
<script>
import Datepicker from "vuejs-datepicker";
export default {
  props: ["label", "name", "onSelect", "required"],
  components: {
    Datepicker,
  }
};
</script>

<style>
.input-group.datepicker-group {
    margin-bottom: 40px;
    position: relative;
    width: 50%;
}

.input-group.datepicker-group * {
    cursor: pointer;
    background: transparent;
}

.input.datepicker {
    border-radius: 0;
}

.input.datepicker input {
	border: none !important;
	border-bottom: 2px solid var(--grey) !important;
	border-radius: 0;
	width: 100%;
	height: 60px !important;
	font-size: 13pt;
	padding-left: 15px;
	padding-top: 17px;
	transition: all .2s;
}

.input.datepicker input:focus {
	outline: none;
}

.input.datepicker .input-label {
	position: absolute;
	line-height: 150%;
	transition: top .2s;
	top: 0;
  left: 5px;
	font-size: 11pt;
	margin-bottom: 35px;
	color: var(--blue);
}

.input.datepicker .input-helper {
	font-size: 9pt;
  position: absolute;
	top: 5px;
  right: 0;
	color: var(--orange);
	letter-spacing: 0.03rem;
	margin: 2px 14px;
}

.input:hover input {
	background: var(--blue-lightest);
	border-color: var(--blue) !important;
}

.input.datepicker input:focus + .input-label {
	color: var(--blue);
}

.vdp-datepicker__calendar, .vdp-datepicker__calendar * {
  background: white !important;
}

@media (max-width: 600px) {
	.input.datepicker input {
		font-size: 10pt;
	}
}
</style>