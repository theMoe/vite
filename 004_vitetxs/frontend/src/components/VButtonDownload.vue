<template>
    <div class="form-element button-container">
        <div class="btn" @click="onSubmit" v-bind:class="[requestInProgress ? 'in-progress' : '']">Download</div>
    </div>
</template>
<script>
export default {
    props: ["onSubmit", "requestInProgress"]
}
</script>