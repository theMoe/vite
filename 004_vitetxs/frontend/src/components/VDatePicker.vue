<template>
  <div class="form-element">
    <p>{{ label }}</p>
    <datepicker @selected="onSelect" :name="name" :formatter="customFormatter"></datepicker>
  </div>
</template>
<script>
import Datepicker from "vuejs-datepicker";
import dayjs from "dayjs";
export default {
  props: ["label", "name", "onSelect"],
  components: {
    Datepicker,
  },
  methods: {
    customFormatter(date) {
      return dayjs(date).format();
    },
  },
};
</script>