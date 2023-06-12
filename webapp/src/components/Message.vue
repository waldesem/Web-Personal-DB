<template>
  <div class="py-3">
    <div class="alert alert-dismissible" :class="attr" role="info">{{text}}
      <button class="btn-close" type="button" data-bs-dismiss="alert"></button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AlertMessage',
  props: {
    attr: String,
    text: String
  }
};
</script>