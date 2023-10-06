<script setup lang="ts">


</script>

<template>
<form @submit.prevent="submitData" class="form form-check" role="form">
  <div class="mb-3 row required">
    <label class="col-form-label col-md-2" for="region">Регион</label>
    <div class="col-md-2">
      <select :disabled="storeLogin.userData.region_id !== '1'"
              @change="submitData" 
              class="form-select" id="region" name="region" 
              v-model="stat.region">
        <option :value="storeLogin.userData.region_id" selected>
          {{ storeClassify.classifyItems.regions[storeLogin.userData.region_id] }}</option>
        <option v-for="name, value in storeClassify.classifyItems.regions" 
                :key="value" :value="value">{{name}}</option>                
      </select>
    </div>
    <label class="col-form-label col-md-1" for="start">Период:</label>
    <div class="col-md-2">
      <input class="form-control" id="start" name="start" required type="date" 
          v-model="stat.start">
    </div>
    <div class="col-md-2">
      <input class="form-control" name="end" required type="date" 
          v-model=stat.end>
    </div>
    <div class="col-md-2">
      <button class="btn btn-primary btn-md" name="submit" type="submit">
          Принять</button>
    </div>
  </div>
</form>
</template>