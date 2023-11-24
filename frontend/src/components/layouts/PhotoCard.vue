<script setup lang="ts">

const props = defineProps({
  url: String,
  param: {
    type: Array<String>,
    required: true
  },
  func: {
    type: Function,
    required: true
  }
});

</script>

<template>
  <div class="card" style="width: 16rem;">
    <img :src="props.url ? props.url : '/no-photo.png'" 
          style="width: 100%; height: auto;" class="card-img-top" alt="...">
    <div class="card-body">
      <form @change="props.func($event, ...props.param)" class="form">
        <input class="form-control form-control-sm" id="formImage" type="file">                  
      </form>
    </div>
  </div>
</template>