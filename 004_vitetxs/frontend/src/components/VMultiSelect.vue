<!-- Vue component -->
<template>
  <div class="multi-select">
    <label>{{label}}</label>
    <span v-if="required">required</span>
    <span v-else>optional</span>
    <div class="filler"/>
    <multiselect v-if="objectOptions"
        v-model="value"
        track-by="name"
        label="name"
        :tag-placeholder="tagplaceholder || 'Add this as new tag'" 
        :placeholder="placeholder || `Search${taggable ? ' or add' : ''} an option`"
        :options="options" 
        :multiple="multiple != null ? multiple : true" 
        :taggable="taggable"
        :searchable="searchable != null ? searchable : true"
        @input="onChange"
        @tag="addTag">
    </multiselect>
    <multiselect v-else
        v-model="value"
        :tag-placeholder="tagplaceholder || 'Add this as new tag'" 
        :placeholder="placeholder || `Search${taggable ? ' or add' : ''} an option`"
        :options="options" 
        :multiple="multiple != null ? multiple : true" 
        :taggable="taggable"
        :searchable="searchable != null ? searchable : true"
        @input="onChange"
        @tag="addTag">
    </multiselect>
  </div>
</template>

<script>
import Multiselect from 'vue-multiselect';
export default {
    components: { Multiselect },
    props: ["label", "placeholder", "tagplaceholder", "selected", "multiple", "options", "taggable", "searchable", "onChange", "required", "objectOptions"],
    data () {
        return {
            value: []
        }
    },
    methods: {
        addTag(newTag) {
            this.value.push(newTag);

            if (this.multiple) {
                this.options.push(newTag);
            } 
            
            this.onChange(this.value);
        },
    }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style>
.multi-select {
    margin-bottom: 40px;
    position: relative;
    width: 50%;
    cursor: pointer;
}

.multi-select .filler {
    width: 100%;
    height: 30px;
}

.multi-select > label {
    position: absolute;
	line-height: 150%;
	transition: top .2s;
	top: 0;
    left: 5px;
	font-size: 11pt;
	margin-bottom: 35px;
	color: var(--blue);
}

.multi-select > span {
    font-size: 9pt;
    position: absolute;
	top: 0;
    right: 0;
	color: var(--orange);
	letter-spacing: 0.03rem;
	margin: 2px 14px;
}

.multi-select input {
    transition: none;
}

.multi-select input:focus {
    font-size: 10.5pt;
}

.multi-select input:focus {
    outline: none;
}

.multiselect__option--highlight, .multiselect__option--highlight::after, .multiselect__tag, .multiselect__tag i {
    background: var(--blue-dark) !important;
}

@media (max-width: 600px) {
	.multiselect * {
		font-size: 10pt !important;
	}
}
</style>