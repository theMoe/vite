<!-- Vue component -->
<template>
  <div class="form-element multi-select">
    <!-- <multiselect v-model="value" :options="options"></multiselect> -->
    <p>{{label}}</p>
    <multiselect 
        v-model="value" 
        :tag-placeholder="tagplaceholder" 
        :placeholder="placeholder" 
        label="name" 
        track-by="name" 
        :options="allOptions" 
        :multiple="multiple" 
        :taggable="taggable"
        :searchable="searchable"
        @input="onChange"
        @tag="addTag">
    </multiselect>
    <!-- <pre class="language-json"><code>{{ value }}</code></pre> -->
  </div>
</template>

<script>
  import Multiselect from 'vue-multiselect'

  export default {
    components: { Multiselect },
    props: {
            label: { type: String },
            name: { type: String, },
            placeholder: { type: String, default: 'Search or add a address', },
            tagplaceholder: {type: String, default: 'Add this as new filter'},
            selected: { type: [Array, Object, String, Number], default: () => [], },
            multiple: { type: Boolean, default: true, },
            //hideSelected: { type: Boolean, default: true, },
            //closeOnSelect: { type: Boolean, default: false, },
            //clearOnSelect: { type: Boolean, default: () => false, },
            options: { type: [Array, Object], default: () => [], },
            taggable: { required: false, type: Boolean, default: false, },
            searchable: { type: Boolean, default: true, },
            onChange: null,
        },
    data () {
        return {
            value: [],
            allOptions: [],
        }
    },
    // computed: {
    //     getValue() {
    //         if (!this.multiple && !Array.isArray(this.value)) {
    //             this.value = [this.value];
    //         }
    //         return this.value;
    //     },
    // },

    // watch: {
    //     value(newValue, oldValue) {
    //         // This will force the v-model of the parent to update
    //         this.$emit('input', this.value);
    //     },
    // },

    mounted() {
        this.value = this.selected;
        this.allOptions = this.options;
    },

    methods: {
        //     addSelection(option) {
        //         if (this.multiple && !~this.value.indexOf(option)) {
        //             this.value.push(option);
        //         } else if (!this.multiple) {
        //             this.value = option;
        //         }
        //     },

        //     removeSelection(option) {
        //         if (this.multiple) {
        //             let index = this.value.indexOf(option)

        //             if (~index) {
        //                 this.value.splice(index, 1);
        //             }
        //         }
        //     },
        addTag(newTag) {
            const tag = {
                name: newTag,
                viteAddress: newTag,
            };
            this.allOptions.push(tag);

            if (this.multiple) {
                this.value.push(tag);
            } else {
                this.value = tag;
            }
            this.onChange(this.value)
        },
        // }

        // addTag (newTag) {
        //     const tag = {
        //         name: newTag,
        //         viteAddress: newTag // newTag.substring(0, 2) + Math.floor((Math.random() * 10000000))
        //     }
        //     this.options.push(tag)
        //     this.value.push(tag)
        // }
    }
}
</script>

<!-- New step!
     Add Multiselect CSS. Can be added as a static asset or inside a component. -->
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>