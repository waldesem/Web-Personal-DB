<script setup lang="ts">

import { profileStore } from '@/store/profile';

const storeProfile = profileStore();

const props = defineProps({
  profileId: String,
  imageUrl: String
});

</script>

<template>
  <div class="card" style="width: 16rem;">
    <img :src="props.imageUrl 
          ? props.imageUrl 
          : '/no-photo.png'" 
          style="width: 100%; height: auto;" 
          class="card-img-top" alt="...">
    <div class="card-body">
      <form @change="storeProfile.submitFile($event, 'image', props.profileId)" class="form">
        <input class="form-control form-control-sm" id="formImage" type="file">                  
      </form>
    </div>
  </div>
</template>