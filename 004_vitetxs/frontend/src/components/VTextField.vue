<template>
    <div class="form-element">
        <p>{{label}}</p>
        <input type="text" class="input" :name="name" @input="onChange" v-on:keyup.enter="onSubmit"/>
      </div>
</template>
<script>
export default {
    props: ["label", "name", "onChange", "onSubmit"]
}
</script>
