<script setup lang="ts">

import { profileStore } from '@/store/profile';

const storeProfile = profileStore();

</script>

<template>
  <div class="card" style="width: 16rem;">
    <img :src="storeProfile.urlImage 
          ? storeProfile.urlImage 
          : '/no-photo.png'" 
          style="width: 100%; height: auto;" 
          class="card-img-top" alt="...">
    <div class="card-body">
      <form @change="storeProfile.submitFile($event, 'image', storeProfile.profile.resume['id'])">
        <input class="form-control form-control-sm" id="formImage" type="file">                  
      </form>
    </div>
  </div>
</template>