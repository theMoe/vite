<template>
    <div class="button-container">
        <v-progress-circular
                indeterminate
                color="#06254b"
                v-if="requestInProgress"
                class="loading-spinner"
                :size="40"
        />
        <div v-if="!requestInProgress" class="btn" @click="onSubmit">
            <i class="fas fa-file-download"/>
            Download
        </div>
        <div v-else class="btn in-progress">
            <i class="fas fa-file-download"/>
            Download
        </div>
    </div>
</template>
<script>
export default {
    props: ["onSubmit", "requestInProgress"],
}
</script>

<style scoped>
.button-container {
    display: flex;
    width: 100%;
    justify-content: flex-end;
    align-items: center;
    margin: 20px 0 0;
}

.btn {
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    font-size: 18pt;
    font-weight: 300;
    border-radius: 10px;
    height: 55px;
    width: 180px;
    margin: 10px 0 0 0;
    color: var(--blue-lightest);
    background: var(--orange);
    background: radial-gradient( at top right, var(--orange-light) 0%, var(--orange) 100%);
    transition: background-position 0.5s;
}

.btn.in-progress {
    background: var(--orange-light);
    cursor: progress;
}

.btn:hover {
    background-position: 180px;
}

.loading-spinner {
    margin: 10px 25px 0 0;
}
</style>